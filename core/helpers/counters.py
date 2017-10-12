import collections

def counts_author( data, verbose ):

    authors = map( lambda d: d['creator'], data )

    author_counts = collections.Counter(authors)

    if verbose:

        print_counts( author_counts, 'author' )

    return author_counts

def counts_domain( data, verbose ):

    import urls

    domains = urls.domains( map( lambda d: d['url'], data ) )

    domain_counts = collections.Counter(domains)

    if verbose:

        print_counts( domain_counts,  'domain' )

    return domain_counts

def print_counts( counts, count_type ):

    total_count = len( counts.keys() )

    print count_type.title() + 's found in data:', total_count

    print 'Entry counts by ' + count_type + ':'

    for key, value in counts.most_common(total_count):
        print '-', key, value
