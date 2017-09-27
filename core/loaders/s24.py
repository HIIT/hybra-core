import os
import json
import datetime
import cStringIO

from lxml import etree

path = '/Volumes/Suomi24/'

for f in filter( lambda x: x.endswith('VRT2') or x.endswith('VRT'), os.listdir( path ) ):

    data = open( path + f ).read()
    print 'Doing', f
    out = []

    ## fix to stringio and save some writing to hd

    temp = cStringIO.StringIO()
    temp.write("""<?xml version="1.0" encoding="UTF-8" ?>
    <root>"""
    + data +
    "</root>")

    for d in etree.iterparse( temp , tag = 'text', recover = True ):
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



        if 'rasis' in text or 'rasis' in text_lemma:

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

    json.dump( out, open( f + '.json', 'w' ) )
    print 'Done', f
