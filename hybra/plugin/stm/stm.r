library(stm)
library(lubridate)

md <- data.frame( timestamp = ymd_hms( timestamps ), source = sources, author = authors, text = texts )

processed <- textProcessor( documents, metadata = md, stem = FALSE, striphtml = TRUE, language = NA, customstopwords = stopwords )

## todo: set upper and lower thresholds
out <- prepDocuments(processed$documents, processed$vocab, processed$meta, lower.thresh= 20, verbose = FALSE )

## upper.thresh = 100

stm <- stm( documents = out$documents, vocab = out$vocab, K = k, data = out$meta,
  max.em.its = 75, init.type = "Spectral",  seed = 1, verbose = FALSE )

save( stm, out, file = paste( saveto, '/stm.rdata', sep = '' ) )

print( plot( stm, "summary" ) )
