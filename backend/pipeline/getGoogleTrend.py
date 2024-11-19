from dotenv import load_dotenv
load_dotenv(override=True)

# from pytrends.request import TrendReq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from trendspy import Trends

# def get_coutry_daily_trending(country='malaysia'):

#     pytrends = TrendReq(hl='en-US', tz=480)
#     data = pytrends.trending_searches(pn=country)
#     return data

def get_trending_titles():
    tr = Trends()
    trends = tr.trending_now(geo='MY')
    titles = []
    for i in range (len(trends)):
        news = tr.trending_now_news_by_ids(
            trends[i].news_tokens,  # News tokens from trending topic
            max_news=1  # Number of articles to retrieve
        )
        titles.append(news[0].title)
    # print("-------------------")
    # print(trends[0])
    # print("-------------------")
    return titles


def get_trending_keywords():
    tr = Trends()
    trends = tr.trending_now(geo='MY')
    t = [tk.keyword for tk in trends]
    return t


def get_trend_search(trend):

    wrapper = DuckDuckGoSearchAPIWrapper(region="my-en", time="d", max_results=2) # my-en = Malaysia English my-ms = Malaysia Malay
    search = DuckDuckGoSearchResults(api_wrapper=wrapper, output_format="list")

    result = search.invoke(trend)

    return result

def get_website(url):

    loader = WebBaseLoader(url)
    docs = loader.load()

    return docs[0]