import data_loader

data = data_loader.load_facebook()

## set as bunch of methods instead?

print "Post together", len(data), "posts"
print "First post", min( map( lambda d: d['date'], data ) )
print "Last post", max( map( lambda d: d['date'], data ) )
print "Number of authors", len( set( map( lambda d: d['creator'], data ) ) )

d = []

for post in data:
    for comment in post['__comments']:
        d.append( comment )

print "Comments", len( d )
