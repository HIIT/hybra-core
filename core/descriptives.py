import data_loader

def describe( data ):
    if len(data) == 0:
        print "Dataset empty."
        return

    print "Post together", len(data), "posts"
    print "First post", min( map( lambda d: d['date'], data ) )
    print "Last post", max( map( lambda d: d['date'], data ) )
    print "Number of authors", len( set( map( lambda d: d['creator'], data ) ) )

if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print function_name
            f =  getattr( data_loader, function_name )
            data = f()
            describe( data )
