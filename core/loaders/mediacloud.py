def load( file = '' ):

    import dateparser

    ## TODO: implement here hybra-core like caching and API management

    for e in json.load( open( file ) ):

        try:

            d = {}

            d['text_content'] = e['full_text_bow']
            d['timestamp'] = dateparser.parse( e['publish_date'] )
            d['source'] = e['media_name']
            d['source_detail'] = e['publish_date']

            yield data

        except:
            pass ## potentially breaks everything
