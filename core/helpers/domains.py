from urlparse import urlparse

def extract_domains( links ):

    import tldextract

    def fix( link ):
        link = tldextract.extract( link )
        return '.'.join( link[-2:] )

    return map( fix , links )
