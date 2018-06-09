#Depedent variable: upvotes of a review
#Independent variables (review features): length of a review, rating of a review, sentiment polarity of a review
#Dependent variables (user features): total reviews, total upvotes, average upvotes, average rating
###############################################################################################################################

#Read in and plot review features: id, length, rating, upvotes, sentiment polarity

review_feature <- read.table('/Users/luhe/yelp_physician_rating/tutorial/tutorial/spiders/analyzer/stat.txt')
colnames(review_feature) <- c("id", "length", "rating", "upvote", "sentiment")
summary(review_feature)
hist(review_feature$length,
     main = "Histogram for reviews' sentiment polarity",
     xlab = "Sentiment polarity",
     border = "blue",
     col = "grey")

plot(review_feature$sentiment, review_feature$upvote,
     xlab = "Sentiment polarity",
     ylab = "Number of upvotes",
     col  = "blue",
     cex  = 0.6)

abline(lm(review_feature$length ~ review_feature$sentiment))

#Read in and plot user features: id, total number of upvotes, average rating, total number of reviews, average number of upvotes
info <- read.table('/Users/luhe/yelp_physician_rating/tutorial/tutorial/spiders/user_info.txt', fill=T)
colnames(info) <- c("id", "rating_distribution", "Total_upvotes")
summary(info)
hist(info$Total_upvotes,
     main = "Histogram for reviews' sentiment polarity",
     xlab = "Sentiment polarity",
     border = "blue",
     col = "grey")


user_metadata <- read.table('/Users/luhe/yelp_physician_rating/tutorial/tutorial/spiders/analyzer/complete_user_info.txt', fill=T)
colnames(user_metadata) <- c("id", "average_rating", "total_reviews", "average_upvotes")


#Merge review features and user features 
complete_user_matadata <- merge(user_metadata, info, by="id")
summary(complete_user_matadata$average_upvotes)
hist(complete_user_matadata$average_upvotes,
     main = "Histogram for users' average upvotes",
     xlab = "Average number of upvotes received",
     border = "green",
     col = "grey",
     xlim=c(0,30))
complete_data <- merge(complete_user_matadata, review_feature, by="id")

#Delete a column: rating distribution -> no longer needed
#Replacing all missing data with 0
complete_data$rating_distribution <- NULL
complete_data$Total_upvotes[is.na((complete_data$Total_upvotes))] <- 0
complete_data$Total_upvotes[is.na((complete_data$Total_upvotes))] <- 0


#Build models
m0 <- lm(complete_data$upvote ~ 1) # to obtain Total SS
m1 <- lm(upvote ~ length + sentiment, data = complete_data) # Model 1
m2 <- lm(upvote ~ length + sentiment + rating, data = complete_data) # Model 2
m3 <- lm(upvote ~ length + sentiment + rating + total_reviews, data = complete_data) # Model 3
m4 <- lm(upvote ~ length + sentiment + rating + total_reviews + Total_upvotes, data = complete_data) # Model 4
m5 <- lm(upvote ~ length + sentiment + rating + total_reviews + Total_upvotes + average_upvotes, data = complete_data) # Model 5
m6 <- lm(upvote ~ length + sentiment + rating + total_reviews + Total_upvotes + average_upvotes + average_rating, data = complete_data) # Model 6

anova(m0)
anova(m1, m2, m3, m4, m5, m6)
summary(m1)


#check correlations
cor(complete_data$average_rating, complete_data$total_reviews)
cor(complete_data[2:9])
