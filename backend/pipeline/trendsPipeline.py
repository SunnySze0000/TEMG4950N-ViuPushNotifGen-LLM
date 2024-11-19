from pipeline.getAllScrapedItem import run_all_spiders
from node.Holiday_classifier import check_holiday_status
from pipeline import getGoogleTrend
from node import classifier
import time
import json

def filtering(data):

    filtered_data = {key: value for key, value in data.items() if 'None' not in value.keys()}
    return filtered_data


def getTrends(websearch_kw = "Viu Malaysia"):
    scraped_data = run_all_spiders()
    holiday_dict = scraped_data['holidays']
    trend_title = scraped_data['trends']['trend'] # IN LIST
    Today_holiday, Upcoming_holiday, Error_holiday = check_holiday_status(holiday_dict)

    # cast google search
    searches = getGoogleTrend.get_trend_search(websearch_kw)
    snippets = []
    for search in searches:
        snippets.append(search['snippet'])
    print(snippets)

    # general google trend search
    titles = getGoogleTrend.get_trending_titles()

    source1 = filtering(classifier.classifying_test(trend_title))
    source2 = filtering(classifier.classifying_test(titles))
    source3 = filtering(classifier.classifying_test(snippets))

    combined_results = concatenate_classifications(source1, source2, source3)

    for holiday in Today_holiday:
        date = holiday['date']
        holiday_name = holiday['holiday_name']
        holiday_entry = create_holiday_entry(date, holiday_name)
        combined_results[str(len(combined_results) + 1)] = holiday_entry

    for holiday in Upcoming_holiday:
        date = holiday['date']
        holiday_name = holiday['holiday_name']
        holiday_entry = create_holiday_entry(date, holiday_name)
        combined_results[str(len(combined_results) + 1)] = holiday_entry

    print('-------------------1')
    print(source1)
    print('-------------------2')
    print(source2)
    print('-------------------3')
    print(source3)

    print('-------------------Combined')
    combined_json = json.dumps(combined_results, indent=2, ensure_ascii=False)
    print(combined_json)

    return combined_json


def concatenate_classifications(*classifications):
    combined = {}
    current_index = 1

    for classification in classifications:
        for key, value in classification.items():
            combined[str(current_index)] = value
            current_index += 1

    return combined

def create_holiday_entry(holiday):
    date, holiday_name = holiday
    return {
        "classification_type": "General",
        "trend_title": f"{date} - {holiday_name}"
    }

# c1 = {
#     "1": {"classification_type": "star", "trend_title": "Kim Ha Nuel"},
#     "2": {"classification_type": "series", "trend_title": "Nothing Uncovered"},
#     "3": {"classification_type": "none", "trend_title": "A Korean series"}
# }

# c2 = {
#     "1": {"classification_type": "none", "trend_title": "Kim Ha Nuel"},
#     "2": {"classification_type": "star", "trend_title": "Nothing Uncovered"},
#     "3": {"classification_type": "none", "trend_title": "A Korean series"}
# }
# combined_results = concatenate_classifications(c1, c2)