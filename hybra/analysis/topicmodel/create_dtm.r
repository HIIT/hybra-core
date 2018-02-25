library("argparser")

p <- arg_parser("Find the best fit of a topic model thing")

p <- add_argument(p, "folder", help="Folder where files of which DTM is created")
p <- add_argument(p, "--upper", help="Which percentage from the upper frequency of keywords is removed", default = 0.001)
p <- add_argument(p, "--lower", help="Which percentage from the lower frequency of keywords is removed", default = 0.1)
p <- add_argument(p, "--clear", help="Remove all existing .rdata-files", flag=TRUE, default=TRUE)
p <- add_argument(p, "--stopwords", help="Files of stopwords to be removed. Separate files with :", default = 'stop_generic.txt' )

args <- parse_args( p )

source('topics.r')

for( path in args$folder ) {

   print( paste( "Working on" , path ) )

   if( args$clear ) {
     unlink( paste( path , '*.rdata*', sep = '' ) ) ## remove all existing rdata in the folder
   }

   stopwords <- strsplit( args$stopwords, ':' )[[1]]

   print( stopwords )

   dtm <- create_dtm( path, args$upper, args$lower, stopwords )
   save( dtm , file = paste( path, 'dtm.rdata' , sep = '' ) )

}
