from __future__ import division
import os 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import io


class analyzer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.dict = {}
        self.vs_analyzer = SentimentIntensityAnalyzer()
#for sentence in sentences:
#    vs = analyzer.polarity_scores(sentence)
#    print("{:-<65} {}".format(sentence, str(vs)))
    def read_file(self):
        with io.open(self.input_file, 'r') as fin:
            for line in fin:
                line = line.strip().split('    ')
                total = 0
                user_id = line[0]
                review = line[1]
                upvotes = line[2]
                if len(upvotes) > 1:
                    upvotes = upvotes.split('+')
                    if len(upvotes) > 1:
                        for ele in upvotes:
                            total += int(ele)
                elif len(upvotes) == 1:
                    total = int(upvotes)
                else:
                    total = 0
                rating = line[3]
                vs = self.vs_analyzer.polarity_scores(review)
                self.dict[user_id] = [len(review), float(rating), total, vs['compound']]

    def descriptive_stat(self):
        from numpy import array
        upvotes = []
        ratings = []
        sentiment = []
        review_len = []
       
        for ele in self.dict:
            upvotes.append(self.dict[ele][2])
            ratings.append(self.dict[ele][1])
            sentiment.append(self.dict[ele][3])
            review_len.append(self.dict[ele][0])
        with open('review_features.txt', 'w') as fp:
            for key in self.dict:
                fp.write('    '.join([key, str(self.dict[key][0]), str(self.dict[key][1]), str(self.dict[key][2]), str(self.dict[key][3])]))
                fp.write('\n')

        ## id, review length, ratings, upvotes, sentiment
        #upvotes_array = array(upvotes)
        #ratings_array = array(ratings)
        #sentiment_array = array(sentiment)
        #from scipy import stats
        #for arr in upvotes_array: #do not need the loop at this point, but looks prettier
        #print(stats.describe(upvotes_array))
        #print(stats.describe(ratings_array))
        #print(stats.describe(sentiment_array))
        #print(stats.describe(review_len))
    
    def user_info(self):
        from numpy import array
        total_reviews_list = list()
        average_upvotes_list = list()
        average_rating_list = list()

        with open('/Users/luhe/yelp_physician_rating/tutorial/tutorial/spiders/user_info.txt', 'r') as fin, open('complete_user_info.txt', 'w') as fout:
            for line in fin:
                multiply = 5
                total_reviews = 0
                total_ratings = 0
                average_rating = 0
        
                average_upvotes = 0
                line = line.strip().split('    ')
                user_id = line[0]
  
                if line[1] == '':
                    total_reviews = 0
                    average_rating = 0
                    average_upvotes = 0

                else:
                    rating_distribution = line[1].split('_')
                    for rating in rating_distribution:
                        total_reviews += int(rating)
                        total_ratings += multiply * int(rating)
                        multiply  = multiply - 1
                    average_rating = total_ratings / total_reviews
                    average_upvotes = int(line[2]) / total_reviews

                total_reviews_list.append(total_reviews)
                average_upvotes_list.append(average_upvotes)
                average_rating_list.append(average_rating)

                fout.write('    '.join([line[0], str(average_rating), str(total_reviews), str(average_upvotes)]))
                fout.write('\n')

            total_reviews_array = array(total_reviews_list)
            average_upvotes_array = array(average_upvotes_list)
            average_rating_array = array(average_rating_list)
            from scipy import stats
            #for arr in upvotes_array: #do not need the loop at this point, but looks prettier
            print(stats.describe(total_reviews_array))
            print(stats.describe(average_upvotes_array))
            print(stats.describe(average_rating_array))
                
                





        



def main():
    print('start')
    spider_analyzer = analyzer('/Users/luhe/yelp_physician_rating/tutorial/tutorial/spiders/crawled.txt')
    spider_analyzer.read_file()
    spider_analyzer.descriptive_stat()
    #spider_analyzer.user_info()


if __name__ == "__main__":
    main()