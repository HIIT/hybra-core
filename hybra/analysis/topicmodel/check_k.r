source('topics.r')

library("argparser")

p <- arg_parser("Find the best fit of a topic model thing")

p <- add_argument(p, "--plot", help="create a plot", flag=TRUE)
p <- add_argument(p, "--method", help="choose method in use", default = "logll")
p <- add_argument(p, "--dtm", help="dtm used" )
p <- add_argument(p, "folder", help="folders to analyse")

args <- parse_args( p )

value_method <- check_fitness_ll; ## default to logll

if( args$method == 'perplexity' ) {

  library('topicmodels')

  ## there should be additional parameter for dtm
  load( '/Users/mnelimar/OneDrive - Aalto-yliopisto/projects/2016-topicmodelkritiikki/dtm_perdocument.rdata' )
  value_method <- function( x ) { perplexity( x, dtm3 ); } ## make similar to logkelihood

}

##for( path in commandArgs(trailingOnly=TRUE) ) {

  df = data.frame( k = integer(), value =integer() )

  path <- args$folder;

  for( f in list.files( path, pattern = 'topic*') ){
        print( f )
  	load( paste(path, f, sep = '') )
  	k <- model@k
    value <- value_method( model )
  	row = c(k, value)
  	df[ nrow(df)+1,] <- row
  }

  print("Examinging")
  print( path )

  print("Best fit k" )
  print( df$k[ which.max( df$value ) ] )

  print("Best fit value")
  print( df$value[ which.max( df$value ) ] )
  print("") ## Empty line

  if( args$plot ) {

    library('ggplot2')

    g <- ggplot( df , aes(k , value ) ) +
    geom_line() +
    xlab('k') + ylab('measure') +
    theme_minimal() +
    xlim(2,250) ## TODO: make args

    ggsave( file = 'plot.pdf' , g)

  }

##}
