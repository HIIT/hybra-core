## takes
## * data, vector of strings as parameter
## * lang, language name as parameter
## * docnames, names of each document

library(tm)
library(slam)

a <- Corpus( VectorSource( data ) )
stop <- stopwords( lang )

## bunch of cleanup and transformations
a <- tm_map(a, removeNumbers, mc.cores=1 )
a <- tm_map(a, stripWhitespace, mc.cores=1 )
a <- tm_map(a, removePunctuation, mc.cores=1 )
a <- tm_map(a, content_transformer(tolower), mc.cores=1 )
a <- tm_map( a, stemDocument, language = lang, mc.cores = 1)
a <- tm_map(a, removeWords, stop )


## compute word frequencies
dtm <-DocumentTermMatrix(a)

dtm$dimnames$Docs <- docnames

## throw away columns with 0 indicators
dtm <- dtm[ row_sums( dtm ) > 0, ]
