read.csv("/home/mark/eclipse-workspace/HeritageScrape/results/totalTweets.csv")->data
t<-as.vector(data$Text)

require(tm)


t <- Corpus(VectorSource(t))
t <- tm_map(t, tolower) 
t <- tm_map(t, removePunctuation)
t <- tm_map(t, removeNumbers)
t <- tm_map(t, removeWords, stopwords('en'))
t.dtm <- TermDocumentMatrix(t, control = list(minWordLength = 3)) 

data$Text<-t
print(data$Text)

write.csv(data, "/home/mark/eclipse-workspace/HeritageScrape/modified/modified_totalTweets.csv")
