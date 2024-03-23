import scrapy
import requests 

class SentimentSpider(scrapy.Spider):
    name = 'sentiment_spider'

    def start_requests(self):
        urls = getattr(self, 'urls', None)
        if urls:
            urls = urls.split(',')  
        else:
            urls = [] 

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_data = {
            'url': response.url,
            'title': response.css('title::text').get(),
            'h1': response.css('h1::text').getall(),
            'h2': response.css('h2::text').getall(),
            'h3': response.css('h3::text').getall(),
            'text': ' '.join(response.xpath("//body//text()").getall()).strip()
        }

        #sentiment analysis part- working on actual API call)
        sentiment_result = self.analyze_sentiment(page_data['text'])

        page_data_with_sentiment = {**page_data, 'sentiment': sentiment_result}

        yield page_data_with_sentiment

    def analyze_sentiment(self, text):
        """
        Placeholder for sentiment analysis function.
        This function should make a request to a sentiment analysis API
        and return the analysis result.
        """

        api_url = ''
        payload = {'text': text}
        headers = {'Authorization': 'Bearer YOUR_API_KEY'}

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                analysis_result = response.json()
                return analysis_result.get('sentiment', 'Unknown')
            else:
                return 'Error: API request failed'
        except Exception as e:
            return f'Error: {e}'

