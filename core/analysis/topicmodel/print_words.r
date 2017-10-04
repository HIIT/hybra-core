source('topics.r')

library('topicmodels')

print( commandArgs(trailingOnly=TRUE) )

for( path in commandArgs(trailingOnly=TRUE) ) {

  print( paste( path , 'best.rdata', sep ='' )  )

  load( paste( path , 'best.rdata', sep ='' ) )
  ls()
  write.csv( t( terms( model, 15 ) ), file = paste( path , 'best_terms.csv', sep ='' ) )

}
