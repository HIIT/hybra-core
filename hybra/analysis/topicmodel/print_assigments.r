source('topics.r')

library('topicmodels')

print( commandArgs(trailingOnly=TRUE) )

for( path in commandArgs(trailingOnly=TRUE) ) {

  print( paste( path , 'best.rdata', sep ='' )  )

  ## load( paste( path , 'best.rdata', sep ='' ) )
  load( path )
  ls()
  write.csv( topics( model, 1 ), file = paste( path , 'topic_assigments.csv', sep ='' ) )

}
