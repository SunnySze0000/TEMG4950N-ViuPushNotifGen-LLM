from dotenv import load_dotenv

load_dotenv(override=True)

# cast = 'KIM Ha Neul'
# viu_datasets = "Viu_datasets"

# # from pipeline.pipeline import castDrivenPipeline
# # castDrivenPipeline(cast, push_number = 5)

# from pipeline import genPush
# genPush.testingPipeline(cast, push_number = 5)

# # from pipeline.pipeline import contentDrivenPipeline
# # contentDrivenPipeline('Nothing Uncovered', push_number = 5)

# from pipeline import genPush
# genPush.testingContentPipeline('Nothing Uncovered', push_number = 5)

#Test for spider
from pipeline.getScrapedHolidayItem import run_holiday_spider
from pipeline.getSrapedTrendItem import run_weirdkaya_trend_spider
from pipeline.getScrapedItem import run_spiders
from pipeline.getAllScrapedItem import run_all_spiders
from pipeline.getScrapedWarningItem import run_weather_warning_spider
from node.Holiday_classifier import check_holiday_status
if __name__ == "__main__":
    # scraped_data1 = run_holiday_spider()
    # scraped_data2 = run_weirdkaya_trend_spider()
    # print("main scraped data1: ", scraped_data1)
    # scraped_data1, scraped_data2 = run_spiders()
    # print("main scraped data2: ", scraped_data2)

    scraped_data = run_all_spiders()
    # print(scraped_data)
    holiday_dict = scraped_data['holidays']
    trend_title = scraped_data['trends']['trend']
    Today_holiday, Upcoming_holiday, Error_holiday = check_holiday_status(holiday_dict)
    print(Today_holiday, Upcoming_holiday, Error_holiday)
    # print("main scraped data:")
    # print("hodidays: ")
    # print(holiday_dict)
    # print("trend: ")
    # print(trend_title)

    # run_weather_warning_spider()

#rerankingGen.simplifiedContentPipe('Nothing Uncovered', push_number = 1)

# from node import save
# # Example JSON data
# json_data = {
#     "english": {
#         "title": "KIM Ha Neul's Life Turned Upside Down! 🤯",
#         "body": "The queen of romantic comedies is now a murder suspect? 🤔 Don't believe it! Watch Nothing Uncovered to uncover the truth behind the scandal! 💥 #KimHaNeul #NothingUncovered"
#     },
#     "malay": {
#         "title": "Kehidupan KIM Ha Neul Terbalik! 🤯",
#         "body": "Ratu komedi romantik kini menjadi suspek pembunuhan? 🚔️ Jangan percayya! Tonton Nothing Uncovered untuk mengungkapkan kebenaran di sebalik skandal! 💥 #KimHaNeul #NothingUncovered"
#     }
# }

# inp = {
#     "type_of_push_notification": "cast-driven",
#     "number_of_push_notifications": 1,
#     "name_of_series": "Loving Storm",
#     "retrieved_wiki_of_series": None,
#     "series_content": "Reyna confessed to Lee Tin Wai, however being brutally rejected inin the storm, leaving herself alone standing in the heavy rain and thunder.",
#     "series_description": "Young couple Reyna and Lin navigate the highs and lows of their tumultuous relationship, filled with love, laughter, and heartbreak. After a painful breakup, they must confront their feelings and challenges to find their way back to each other once more.",
#     "name_of_cast": "Tam Qin",
#     "type_of_cast": "Main Cast",
#     "nickname_of_cast": None,
#     "quote_of_cast": None,
#     "interesting_fact_of_cast": None,
#     "character_in_series_acted_by_cast": "Reyna",
#     "demographics_of_target_receiver": "fan of Tam Qin",
#     "base_push_example": None,
#     "local_trend_in_malaysia": "Typhoon number 8 is announced at nine am this morning, students have one day of extra holiday",
#     "include_emoji": True,
#     "include_slangs": True,
#     "additional_requirements": None,
# }

# # Save the JSON data to CSV
# save.save_to_csv(json_data, 'utils\history.csv')
# save.update_examples(inp, json_data)

from pipeline import getGoogleTrend
import time
#from node import classifier
trends = getGoogleTrend.get_coutry_daily_trending('malaysia').iloc[:,0].tolist()
snippet_list = []
search_list = []
for trend in trends:
    search = getGoogleTrend.get_trend_search(trend)
    snippet_list.append(search[0]['snippet'])
    search_list.append(search[0])
    time.sleep(1)

print(type(snippet_list))
