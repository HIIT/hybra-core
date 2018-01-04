source('topics.r')
##source('stm.r')

args <- commandArgs(trailingOnly = TRUE)

dtm <- args[1]

if( ! grepl( '.rdata', dtm ) ) {
   dtm <- paste( dtm, 'dtm.rdata', sep='' )
}

load( dtm )

k <- as.integer( args[2] )

model <- create_model( dtm , k )

path <- paste( dtm , '/topic-', args[2], '.rdata' , sep = '' )
save( model , file = path )
