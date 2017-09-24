
def extract_links( posts ):

    from urlparse import urlparse

    links = map( lambda x: x['links'], posts )
    links = filter( lambda x: len(x) > 0, links )
    ret = []
    for link in links: ## todo: use iter tools
        for l in link:
            l = urlparse( l )
            ret.append( l.netloc + l.path )
    return ret

def extract_domains( links ):

    import tldextract

    def fix( link ):
        link = tldextract.extract( link )
        return '.'.join( link[-2:] )

    return map( fix , links )
