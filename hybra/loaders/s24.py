import os
import json
import datetime
import cStringIO

from lxml import etree

path = '/appl/kielipankki/Suomi24/'

files = filter( lambda x: x.endswith('VRT2') or x.endswith('VRT'), os.listdir( path ) )

has_already = filter( lambda x: x.endswith('VRT2.json') or x.endswith('VRT.json'), os.listdir( '.' ) )
has_already = map( lambda x: x.replace('.json', ''), has_already)

files = set(files) - set(has_already)

keywords = raw_input('Define keywords, separated by commas ')

outdir = keywords.replace(' ', '')

if not os.path.exists( outdir ):
    os.makedirs( outdir )

keywords = keywords.split(',')

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

    for d in etree.iterparse( open('temp.xml') , tag = 'text', recover = True ):
        d = d[1]

        text = ''
        text_lemma = ''

        for p in d.findall('paragraph'):

            for s in p.findall('sentence'):

                for line in s.text.split('\n'):

                    line = line.split('\t')

                    if len( line ) > 3:

                        text += line[0] + ' '
                        text_lemma += line[2] + ' '


        flag = False

        for kw in keywords:
            if kw in text or kw in text_lemma:
                flag = True

        if flag:

            o = {}
            o['text_content'] = d.get('title') + ' ' + text
            o['text_content_lemma'] = text_lemma
            o['source'] = 'Suomi24'
            o['source_detail'] =  d.get('discussionarea') + '/' + d.get('subsections')
            o['url'] = d.get('urlmsg')

            dt = d.get('date').split('.') + d.get('time').split(':')
            dt = map( int, dt )

            o['timestamp'] = str( datetime.datetime( dt[2], dt[1], dt[0], dt[3], dt[4]) )

            o['creator'] = d.get('anonnick')
            o['id'] = d.get('tid') + '-' + d.get('cid')

            out.append( o )

    json.dump( out, open( outdir + '/' + f + '.json', 'w' ) )
    print 'Done', f

 except Exception, e:
       print 'Failed', f
       print e
