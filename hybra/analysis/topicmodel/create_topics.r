source('topics.r')
##source('stm.r')

args <- commandArgs(trailingOnly = TRUE)

dtm_path <- args[1]

if( ! grepl( '.rdata', dtm_path ) ) {
   dtm_path <- paste( dtm, 'dtm.rdata', sep='' )
}

load( dtm_path )

k <- as.integer( args[2] )

model <- create_model( dtm , k )

path <- paste( dtm_path , 'topic-', args[2], '.rdata' , sep = '' )

print( path )

save( model , file = path )
