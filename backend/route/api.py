from fastapi import APIRouter
from typing import Optional, Dict, List
from pipeline.rerankingGen import finalCastPipeline, finalContentPipeline, generating
from utils.schema import PushRegenerateRequest, PushRequest, PushResponse, TrendResponse, TrendRequest   
from utils.state import backendState, initialize_backend_state
from pipeline.trendsPipeline import getTrends, refreshTrends
import time
import asyncio
# import csv
# from node import save

maxGenTime= 120
maxReGenTime= 30
maxTrendTime= 30

HARD_CODED_GENERAL_TREND = {
   "1": {"classification_type": "General", "trend_title": "16yo Msian Actress Qistina Raisah Buys Her First Car With Money She Earned Herself"}, 
   "2": {"classification_type": "General", "trend_title": "Disneys Moana 2 celebrates Pan Polynesian culture with fresh  storytelling and Grammy-winning music by Barlow and Bear"}, 
   "3": {"classification_type": "Series", "trend_title": "Everything you need to know about Sporting CP | Feature | News"}, 
   "4": {"classification_type": "General", "trend_title": "Wednesday TV: Lindsay Lohans Xmas Rom-Com"}, 
   "5": {"classification_type": "General", "trend_title": "Squid Game Season 2 Trailer: Lee Jung-Jae Commands Attention In The Korean  Thriller"}, 
   "6": {"classification_type": "General", "trend_title": "Morgan Freeman, 87, Makes Rare Appearance While Out in Los Angeles"}, 
   "7": {"classification_type": "General", "trend_title": "Thanksgiving Should Be in October"}, 
   "8": {"classification_type": "General", "trend_title": "The inaccessibility of Ticketmaster: The Oasis reunion and dynamic pricing"}, 
   "9": {"classification_type": "General", "trend_title": "Barbra Banda wins BBC Womens Footballer of the Year award"}, 
   "10": {"classification_type": "Series", "trend_title": "Doom at Your Service"}
}

HARD_CODED_REFRESH_TREND = {
   "1": {"classification_type": "Star", "trend_title": "16yo Msian Actress Qistina Raisah Buys Her First Car With Money She Earned Herself"}, 
   "2": {"classification_type": "General", "trend_title": "Disneys Moana 2 celebrates Pan Polynesian culture with fresh  storytelling and Grammy-winning music by Barlow and Bear"}, 
   "3": {"classification_type": "General", "trend_title": "Wednesday TV: Lindsay Lohans Xmas Rom-Com"}, 
   "4": {"classification_type": "General", "trend_title": "Squid Game Season 2 Is A Deeper, More Advanced Story Says Creator Hwang  Dong-hyuk"}, 
   "5": {"classification_type": "Series", "trend_title": "Lovely Runner, a time-travel drama"}, 
   "6": {"classification_type": "Star and Series", "trend_title": "Byeon Woo Seok and Kim Hye Yoon's romantic chemistry in Lovely Runner"}, 
   "7": {"classification_type": "Series", "trend_title": "The fantasy romance of Lovely Runner"}
}

HARD_CODED_GEN= {
   "1": {"english": {"title": "KIM Ha Neul's Shocking Scandal! 🚨", "body": "WOW! Detective Kim Tae-Heon is on the case! Can he clear KIM Ha Neul's name in Nothing Uncovered? Watch now on Viu! 📺 #KIMHaNeul #NothingUncovered"}, 
   "malay": {"title": "Skandal KIM Ha Neul! 🚨", "body": "WOW! Detektif Kim Tae-Heon menyiasat! Bolehkah dia membersihkan nama KIM Ha Neul dalam Nothing Uncovered? Tonton sekarang di Viu! 📺 #KIMHaNeul #TiadaYangTerketepi"}},

   "2": {"english": {"title": "KIM Ha Neul's Life Turns Upside Down!", "body": "OMG! Seo Jung-Won's perfect life is ruined! Can KIM Ha Neul's character find the truth behind the murder case? Watch Nothing Uncovered on Viu now! 📺 #KIMHaNeul #Thriller"}, 
   "malay": {"title": "Hidup KIM Ha Neul Berubah!", "body": "OMG! Kehidupan sempurna Seo Jung-Won hancur! Bolehkah watak KIM Ha Neul mencari kebenaran di sebalik kes pembunuhan? Tonton Nothing Uncovered di Viu sekarang! 📺 #KIMHaNeul #Thriller"}},

   "3": {"english": {"title": "Uncover the Truth with KIM Ha Neul! 🔍", "body": "Get ready for a wild ride! KIM Ha Neul stars as Seo Jung-Won in Nothing Uncovered. Don't miss out on the drama! Watch now on Viu! 📺 #KIMHaNeul #NothingUncovered"}, 
   "malay": {"title": "Bongkar Kebenaran dengan KIM Ha Neul! 🔍", "body": "Sedia untuk pengembaraan liar! KIM Ha Neul membintangi sebagai Seo Jung-Won dalam Nothing Uncovered. Jangan lepaskan drama! Tonton sekarang di Viu! 📺 #KIMHaNeul #TiadaYangTerketepi"}},

   "4": {"english": {"title": "KIM Ha Neul's Detective Skills Put to the Test! 🕵️‍♀️", "body": "Can KIM Ha Neul's character solve the murder case? Find out in Nothing Uncovered! Watch now on Viu! 📺 #KIMHaNeul #Mystery"}, 
   "malay": {"title": "Kemahiran Detektif KIM Ha Neul Diuji! 🕵️‍♀️", "body": "Bolehkah watak KIM Ha Neul menyelesaikan kes pembunuhan? Ketahui dalam Nothing Uncovered! Tonton sekarang di Viu! 📺 #KIMHaNeul #Misteri"}},

   "5": {"english": {"title": "Get Ready for KIM Ha Neul's Most Thrilling Role!", "body": "KIM Ha Neul stars as Seo Jung-Won in Nothing Uncovered. Don't miss out on the suspense! Watch now on Viu! 📺 #KIMHaNeul #Thriller"}, 
   "malay": {"title": "Sedia untuk Peranan Paling Menegangkan KIM Ha Neul!", "body": "KIM Ha Neul membintangi sebagai Seo Jung-Won dalam Nothing Uncovered. Jangan lepaskan suspens! Tonton sekarang di Viu! 📺 #KIMHaNeul #Thriller"}}
}

HARD_CODED_REGEN= {
   "1": {"english": {"title": "KIM Ha Neul's Shocking Scandal! 🚨", "body": "WOW! Detective Kim Tae-Heon is on the case! Can he clear KIM Ha Neul's name in Nothing Uncovered? Watch now on Viu! 📺 #KIMHaNeul #NothingUncovered"}, 
   "malay": {"title": "Skandal KIM Ha Neul! 🚨", "body": "WOW! Detektif Kim Tae-Heon menyiasat! Bolehkah dia membersihkan nama KIM Ha Neul dalam Nothing Uncovered? Tonton sekarang di Viu! 📺 #KIMHaNeul #TiadaYangTerketepi"}},

   "2": {"english": {"title": "KIM Ha Neul's Life Turns Upside Down!", "body": "OMG! Seo Jung-Won's perfect life is ruined! Can KIM Ha Neul's character find the truth behind the murder case? Watch Nothing Uncovered on Viu now! 📺 #KIMHaNeul #Thriller"}, 
   "malay": {"title": "Hidup KIM Ha Neul Berubah!", "body": "OMG! Kehidupan sempurna Seo Jung-Won hancur! Bolehkah watak KIM Ha Neul mencari kebenaran di sebalik kes pembunuhan? Tonton Nothing Uncovered di Viu sekarang! 📺 #KIMHaNeul #Thriller"}},

   "3": {"english": {"title": "Uncover the Truth with KIM Ha Neul! 🔍", "body": "Get ready for a wild ride! KIM Ha Neul stars as Seo Jung-Won in Nothing Uncovered. Don't miss out on the drama! Watch now on Viu! 📺 #KIMHaNeul #NothingUncovered"}, 
   "malay": {"title": "Bongkar Kebenaran dengan KIM Ha Neul! 🔍", "body": "Sedia untuk pengembaraan liar! KIM Ha Neul membintangi sebagai Seo Jung-Won dalam Nothing Uncovered. Jangan lepaskan drama! Tonton sekarang di Viu! 📺 #KIMHaNeul #TiadaYangTerketepi"}},

   "4": {"english": {"title": "KIM Ha Neul's Detective Skills Put to the Test! 🕵️‍♀️", "body": "Can KIM Ha Neul's character solve the murder case? Find out in Nothing Uncovered! Watch now on Viu! 📺 #KIMHaNeul #Mystery"}, 
   "malay": {"title": "Kemahiran Detektif KIM Ha Neul Diuji! 🕵️‍♀️", "body": "Bolehkah watak KIM Ha Neul menyelesaikan kes pembunuhan? Ketahui dalam Nothing Uncovered! Tonton sekarang di Viu! 📺 #KIMHaNeul #Misteri"}},

   "5": {"english": {"title": "Get Ready for KIM Ha Neul's Most Thrilling Role!", "body": "KIM Ha Neul stars as Seo Jung-Won in Nothing Uncovered. Don't miss out on the suspense! Watch now on Viu! 📺 #KIMHaNeul #Thriller"}, 
   "malay": {"title": "Sedia untuk Peranan Paling Menegangkan KIM Ha Neul!", "body": "KIM Ha Neul membintangi sebagai Seo Jung-Won dalam Nothing Uncovered. Jangan lepaskan suspens! Tonton sekarang di Viu! 📺 #KIMHaNeul #Thriller"}}
}

async def delay(seconds: int):
    await asyncio.sleep(seconds)

api_router = APIRouter()

@api_router.get("/scrapeTrends")
async def get_trend() -> Dict[int, TrendResponse]:
   start_time = time.time()
   try:
      # scrape trend function
      # return pushes
      return getTrends()
   except Exception as e:
      elapsed_time = time.time() - start_time
      print(e)
      await delay(max(maxTrendTime-elapsed_time,0))  # Delay before showing hardcoded results
      return HARD_CODED_GENERAL_TREND

@api_router.post("/refreshTrends")
async def post_trend(request: TrendRequest) -> Dict[int, TrendResponse]:
   start_time = time.time()
   try:
      # scrape trend function
      # return pushes
      print(f"Refreshing trends with cast_name: {request.cast_name} and series_name: {request.series_name}")
      return refreshTrends(request.cast_name, request.series_name)
   except Exception as e:
      elapsed_time = time.time() - start_time
      print(e)
      await delay(max(maxTrendTime-elapsed_time,0))  # Delay before showing hardcoded results
      return HARD_CODED_REFRESH_TREND

@api_router.post("/genPush")
async def post_gen_push(input_data: PushRequest) -> Dict[int, PushResponse]:
   start_time = time.time()
   try:
      initialize_backend_state()
      
      backendState["type_of_push_notification"] = input_data.push_type
      backendState["name_of_series"] = input_data.series_name
      backendState["name_of_cast"] = input_data.cast_name
      backendState["creativity"] = input_data.creativity
      backendState["demographics_of_target_receiver"] = f"{input_data.demographics[0]}-{input_data.demographics[1]} years old, fans of the cast and the show"
      backendState["include_emoji"] = input_data.isEmojis
      backendState["include_slangs"] = input_data.isSlangs
      backendState["additional_requirements"] = input_data.addRequirements
      backendState["supporting_documents"] = input_data.otherSupportingDocuments
      backendState["local_trend_in_malaysia"] = input_data.selected_trend
      
      print(backendState)
      
      if backendState["type_of_push_notification"] == "cast-driven":
         print("cast-driven")
         pushes = finalCastPipeline()
         print("HAVE PUSH HERE")
         print(pushes)
      else:
         print("content-driven")
         pushes = finalContentPipeline() 
      
      return pushes
   
   except Exception as e:
      elapsed_time = time.time() - start_time
      print(e)
      await delay(max(maxGenTime-elapsed_time,0))  # Delay before showing hardcoded results
      return HARD_CODED_GEN
   
@api_router.post("/regenPush")
async def post_regen_push(inputData: PushRegenerateRequest) -> Dict[int, PushResponse]:
   start_time = time.time()
   try:
      if inputData.basePush is not None:
         backendState["base_push_example"] = "Title:" + inputData.basePush.title + "\n" + "Body:" + inputData.basePush.body
      # backendState["base_push_example"] = "Title:" + inputData.basePush.title + "\n" + "Body:" + inputData.basePush.body
      backendState["additional_requirements"] = inputData.addRequirements

      input_variables = {
         "type_of_push_notification": backendState["type_of_push_notification"],
         "number_of_push_notifications": backendState["number_of_push_notifications"],
         "name_of_series": backendState["name_of_series"],
         "retrieved_wiki_of_series": backendState["retrieved_wiki_of_series"],
         "series_content": backendState["series_content"],
         "series_description": backendState["series_description"],
         "name_of_cast": backendState["name_of_cast"],
         "type_of_cast": backendState["type_of_cast"],
         "nickname_of_cast": backendState["nickname_of_cast"],
         "quote_of_cast": backendState["quote_of_cast"],
         "interesting_fact_of_cast": backendState["interesting_fact_of_cast"],
         "character_in_series_acted_by_cast": backendState["character_in_series_acted_by_cast"],
         "demographics_of_target_receiver": backendState["demographics_of_target_receiver"],
         "base_push_example": backendState["base_push_example"],
         "local_trend_in_malaysia": backendState["local_trend_in_malaysia"],
         "include_emoji": backendState["include_emoji"],
         "include_slangs": backendState["include_slangs"],
         "additional_requirements": backendState["additional_requirements"]
      }
      
      pushes =  generating(input_variables)
      backendState["pushes"] = pushes
      
      return pushes
   
   except Exception as e:
      elapsed_time = time.time() - start_time
      print(e)
      await delay(max(maxReGenTime-elapsed_time,0))  # Delay before showing hardcoded results
      return HARD_CODED_REGEN
   
# @api_router.get("/savedPush")
# async def get_saved_push() -> List[Dict[str, str]]:
#    try:
#       notifications = []
#       # Read the CSV file
#       with open("\utils\history.csv", mode='r', encoding='utf-8') as file:
#          reader = csv.DictReader(file)
#          for row in reader:
#             notifications.append(row)

#          return notifications
#    except Exception as e:
#       print(e)
#       raise e
   
# @api_router.post("/savePush")
# async def post_save_push(inputData: SaveRequest, push: Dict[int, PushResponse]) -> str:
#    try:
#       return "Push notifications liked!"
#    except Exception as e:
#       print(e)
#       raise e