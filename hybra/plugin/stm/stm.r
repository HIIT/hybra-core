library(stm)

md <- data.frame( timestamp = timestamps )

processed <- textProcessor( documents, metadata = md )

out <- prepDocuments(processed$documents, processed$vocab, processed$meta)

stm <- stm( documents = out$documents, vocab = out$vocab, K = k,
  max.em.its = 75, init.type = "Spectral",  seed = 1, verbose = FALSE )

save( stm, paste( saveto, '/stm.rdata' ) )

print( plot( stm ) )
