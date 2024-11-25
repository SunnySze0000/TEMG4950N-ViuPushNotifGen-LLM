from scrapy.crawler import CrawlerProcess
from utils.Scrapy_scraper.weirdkaya.spiders.holiday_spider import Holiday_Spider
from utils.Scrapy_scraper.weirdkaya.spiders.Trend_spider import Trend_Spider
# from twisted.internet import defer

def run_all_spiders():
    # Store all items from both spiders
    results = {
        'holidays': {},
        'trends': {}
    }

    
    # Define item pipeline
    class ItemCollectorPipeline:
        def process_item(self, item, spider):
            if spider.name == 'holiday':
                results['holidays'].update(item)
            elif spider.name == 'trend':
                results['trends'].update(item)
                # if 'title' in item:
                #     results['trends'].append(item['title'])
                # else:
                #     results['trends'].extend(item)
            return item
    
    # Configure and run spiders
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',
        'ITEM_PIPELINES': {ItemCollectorPipeline: 300},
        # Add other settings as needed
    })
    
    # Add spiders to process
    process.crawl(Holiday_Spider)
    process.crawl(Trend_Spider)
    
    # Run all spiders and wait until finished
    process.start()
    
    return results

# def run_all_spiders():
#     # results = {
#     #     'holidays': {},
#     #     'trends': []
#     # }
#     all_items = []
    
#     class ItemCollectorPipeline:
#         def process_item(self, item, spider):
#             all_items.append(item)
#             return item
    
#     process = CrawlerProcess({
#         'USER_AGENT': 'Mozilla/5.0',
#         'ITEM_PIPELINES': {ItemCollectorPipeline: 300},
#     })

#     @defer.inlineCallbacks
#     def crawl_sequentially():
#         # First spider
#         print("Starting Holiday Spider...")
#         yield process.crawl(Holiday_Spider)
#         print("Holiday Spider finished!")
        
#         # Second spider
#         print("Starting Trend Spider...")
#         yield process.crawl(Trend_Spider)
#         print("Trend Spider finished!")
        
#         # Stop the reactor when both spiders are done
#         process.stop()

#     # Run spiders sequentially
#     process.start(stop_after_crawl=False)
#     crawl_sequentially()
    
#     return all_items