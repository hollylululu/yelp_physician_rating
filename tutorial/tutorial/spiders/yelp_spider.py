import scrapy
import os


class QuotesSpider(scrapy.Spider):
    name = "yelp"

    def __init__(self):
        path = os.getcwd() + '/book_keeping/'
        #os.mkdir(path, 0755)
        print "Path is created"
        self.link_file = path + 'links.txt'

    def start_requests(self):
        #read in a url-list file 
        root_file = os.getcwd() + '/book_keeping/root_links.txt'
        fronts = [line.rstrip('\n') for line in open(root_file)]
        for url in fronts:
            yield scrapy.Request(url=url, callback=self.get_all_pages)
        pages = [line.rstrip('\n') for line in open(self.link_file)]
        for page in pages:
            yield scrapy.Request(url=page, callback=self.parse)

    def parse(self, response):
        reviews = response.css('div#wrap.lang-en>div.biz-country-us>div.main-content-wrap>div#super-container>div.container>div.clearfix>div.column>div>div.feed>div.review-list>ul>li')
        with open('content.txt', 'a') as fout:
            for review in reviews[1: len(reviews)]:
                content = review.css('div.review>div.review-wrapper>div.review-content>p::text').extract()
                content = '.'.join(content).encode('utf-8')
                upvotes = review.css('div.review>div.review-wrapper>div.review-footer>div.rateReview>ul.voting-buttons>li.vote-item>a.ybtn>span.count::text').extract()
                upvotes = ' '.join(upvotes).encode('utf-8')
                user = review.css('div.review>div.review-sidebar>div.review-sidebar-content>div.ypassport>div.media-story>ul>li.user-name>a::attr(href)').extract()[0].encode('utf-8')
                star = review.css('div.review>div.review-wrapper>div.review-content>div.biz-rating>div>div::attr(title)').extract()[0].encode('utf-8')
                fout.write('\t'.join([user, content, upvotes, star]))
                fout.write('\n')

    def get_all_pages(self, response):
        pages = response.css('div#wrap.lang-en>div.biz-country-us>div.main-content-wrap>div#super-container>div.container>div.clearfix>div.column>div>div.feed>div.review-pager>div.pagination-block>div.arrange>div.pagination-links>div.arrange')
            #print next_page
        with open(self.link_file, 'a') as fout:
            for page in pages:
                next_page = page.css('div.arrange_unit>a::attr(href)').extract()
                for ele in next_page[0:len(next_page)-1]:
                    fout.write(ele.encode('utf-8'))
                    fout.write('\n')

    def get_user_info(self, response):
        rating_list = list()
        upvotes_list = list()
        user_info = dict()
        total_upvotes = 0
        # num_friends = 0
        # num_photo = 0

        with open('user_info.txt', 'a') as fout:
            # Get user ID - use as the key
            user_id = response.xpath('//div[@class="photo-slideshow_image"]//a/@href').extract_first().split('=')[1]
            user_info[user_id] = []
            fout.write(user_id + '    ')

            # Get rating distribution
            rating = response.xpath('//*[@class="ysection"]/table//tr')
            nest = rating.xpath('.//td/table//tr')
            rating_list = nest.xpath('td[@class="histogram_count"]/text()').extract()
            user_info[user_id].append(rating_list)
            print rating_list

            fout.write('_'.join(rating_list))
            fout.write('    ')

            # Get number of upvotes
            upvotes = response.xpath('//*[@class="user-details-overview_sidebar"]//div[@class="ysection"][2]/ul')
            upvotes_list = upvotes.xpath('./li/strong[1]/text()').extract()
            for ele in upvotes_list:
                total_upvotes += int(ele)

            user_info[user_id].append(total_upvotes)

            fout.write(str(total_upvotes))
            fout.write('\n')