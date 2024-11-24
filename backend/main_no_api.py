from dotenv import load_dotenv

load_dotenv(override=True)

cast = 'KIM Hye Yoon'
#cast = 'KIM Ha Neul'
viu_datasets = "Viu_datasets"

# #Test for spider
from pipeline.getScrapedHolidayItem import run_holiday_spider
from pipeline.getSrapedTrendItem import run_weirdkaya_trend_spider
from pipeline.getScrapedItem import run_spiders
from pipeline.getAllScrapedItem import run_all_spiders
from pipeline.getScrapedWarningItem import run_weather_warning_spider
from node.Holiday_classifier import check_holiday_status
from pipeline import getGoogleTrend
from pipeline import rerankingGen
from node import classifier
import time
# if __name__ == "__main__":
#     # scraped_data1 = run_holiday_spider()
#     # scraped_data2 = run_weirdkaya_trend_spider()
#     # print("main scraped data1: ", scraped_data1)
#     # scraped_data1, scraped_data2 = run_spiders()
#     # print("main scraped data2: ", scraped_data2)

#     scraped_data = run_all_spiders()
#     # print(scraped_data)
#     holiday_dict = scraped_data['holidays'] # IN DICT
#     trend_title = scraped_data['trends']['trend'] # IN LIST
#     Today_holiday, Upcoming_holiday, Error_holiday = check_holiday_status(holiday_dict)
#     print(Today_holiday, Upcoming_holiday, Error_holiday)
#     # print("main scraped data:")
#     # print("hodidays: ")
#     print(holiday_dict)
#     print("trend: ")
#     print(trend_title)

    #run_weather_warning_spider()

############################################################################################################
# from pipeline import getGoogleTrend
# from pipeline import rerankingGen
# from node import classifier
# import time

# Test generate push
#rerankingGen.simplifiedCastPipe(cast, push_number = 5)

## Test for cast search trend
# searches = getGoogleTrend.get_trend_search('KIM Ha Neul')
# snippets = []
# for search in searches:
#     snippets.append(search['snippet'])
# print(snippets)
# result = classifier.classifying_test(snippets)

# Test for general google trend search
from pipeline import trendsPipeline
titles = getGoogleTrend.get_trending_titles()
print(titles)

# print("-----------------Old Classifying-------------------")
# results = trendsPipeline.filtering(classifier.classifying_legacy(titles))
# print("-----------------New Classifying-------------------")
results = trendsPipeline.filtering(classifier.classifying_test(titles))
print("----------------------After filtering-------------------")
print(results)

# filtered_data = {key: value for key, value in results.items() if 'None' not in value.keys()}
# print(filtered_data)

# from pipeline import trendsPipeline
# trendsPipeline.getTrends(cast, "Lovely Runner")
# trendsPipeline.getTrends()

# trends = getGoogleTrend.get_trending_titles()

# def clean_text(text):
#     return text.replace('"', '').replace("'", '').replace('‘', '').replace('’', '').replace('\n', ' ')

# cleaned_trend_title = [clean_text(title) for title in trends]

# print(trends)
# print("-------------------")
# print(cleaned_trend_title)