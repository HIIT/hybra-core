import os
import pickle
import datetime
import cStringIO
import re

from lxml import etree

path = '/appl/kielipankki/Suomi24/2017H2/'

files = filter( lambda x: x.endswith('vrt'), os.listdir( path ) )
files = filter( lambda x: x.startswith('comments'), files )

has_already = filter( lambda x: x.endswith('vrt.json'), os.listdir( '.' ) )
has_already = map( lambda x: x.replace('.json', ''), has_already)

files = set(files) - set(has_already)

import sys
keywords = sys.argv[1]

outdir = keywords.replace(' ', '')

if not os.path.exists( outdir ):
    os.makedirs( outdir )

keywords = keywords.split(',')

total = 0

for f in files:

 try:

    data = open( path + f ).read()
    print 'Doing', f
    out = []

    ## fix to stringio and save some writing to hd

    temp = open('temp.xml', 'w')
    temp.write("""<?xml version="1.0" encoding="UTF-8" ?>
    <root>"""
    + data +
    "</root>")

    for d in etree.iterparse( open('temp.xml') , tag = 'text' , recover = True ):

        total += 1
        d = d[1]

        text = ''
        text_lemma = ''

        for p in d.findall('paragraph'):

            for s in p.findall('sentence'):

                for line in s.text.split('\n'):

                    line = line.split('\t')

                    if len( line ) > 2:

                        text += line[0] + ' '
                        text_lemma += line[1] + ' '


        flag = False

        #for kw in keywords:
        #    if kw in text or kw in text_lemma:
        #        flag = True

        flag = re.search( '[^\s]*rasism[^\s]*|[^\s]*rasist[^\s]*' , text, re.I ) or  re.search( '[^\s]*rasism[^\s]*|[^\s]*rasist[^\s]*' , text_lemma, re.I )

        if flag:

            o = {}
            o['text_content'] = text
            o['text_content_lemma'] = text_lemma
            o['source'] = 'Suomi24'
            o['source_detail'] =  d.get('topics')
            o['url'] = 'https://keskustelu.suomi24.fi/t/' +  d.get('thread') + '#comment-' + d.get('comment')

            dt = d.get('date').split('-') + d.get('time').split(':')
            dt = map( int, dt )

            o['timestamp'] = datetime.datetime( dt[0], dt[1], dt[2], dt[3], dt[4])

            o['creator'] = d.get('nick')
            o['id'] = d.get('thread') + '-' + d.get('comment')

            out.append( o )

    pickle.dump( out, open( outdir + '/' + f + '.pickle', 'w' ) )
    print 'Done', f

 except Exception, e:
       print 'Failed', f
       print e


print 'Total number of messages', total
