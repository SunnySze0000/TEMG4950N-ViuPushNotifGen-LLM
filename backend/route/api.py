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

HARD_CODED_GENERAL_TREND ={
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
   "7": {"classification_type": "Star and Series", "trend_title": "Byeon Woo-seok’s ‘Sudden Shower’ earns him a historic win at the 2024 MAMA Awards"}
}

HARD_CODED_GEN= {
   "1": {"english": {"title": "OMG, Get Ready to Fall for BYEON Woo Seok in Lovely Runner!", "body": "fr fr, BYEON Woo Seok is back!!! 💘 Don't miss him as Ryu Sun-jae in Lovely Runner, a fantasy romance that will sweep you off your feet! ❤️ Watch now and experience the magic! ✨(≧∇≦)"}, 
   "malay": {"title": "Bersedia Jatuh Cinta dengan BYEON Woo Seok di Lovely Runner!", "body": "fr fr, Idola K-drama kembali!!! 💘 Jangan lepaskan BYEON Woo Seok sebagai Ryu Sun-jae di Lovely Runner, sebuah drama fantasi romantis yang akan membuat korang terpikat! ❤️ Tonton sekarang dan rasai keajaiban! ✨(≧∇≦)"}},

   "2": {"english": {"title": "BYEON Woo Seok's Time-Traveling Romance in Lovely Runner is EVERYTHING!!!", "body": "What if you could travel back in time to save your crush? ⏰ BYEON Woo Seok's character Ryu Sun-jae will make your heart skip a beat in Lovely Runner! ❤️ Watch now and get ready for a love story that transcends time! 🔥(¬‿¬)"}, 
   "malay": {"title": "Romans Cinta BYEON Woo Seok yang Mengembara Masa di Lovely Runner adalah SEMUA!!!", "body": "Bagaimana jika korang dapat mengembara masa ke belakang untuk menyelamatkan crush korang? ⏰ Watak Ryu Sun-jae BYEON Woo Seok akan membuat hati korang berdegup kencang di Lovely Runner! ❤️ Tonton sekarang dan bersedia untuk cerita cinta yang mengatasi masa! 🔥(¬‿¬)"}},

   "3": {"english": {"title": "BYEON Woo Seok SLAYS as Ryu Sun-jae in Lovely Runner!", "body": "Critics are raving about BYEON Woo Seok's portrayal of Ryu Sun-jae in Lovely Runner! 🎉 Don't miss this fantasy romance that will leave you breathless! ❤️ Watch now and experience the magic of BYEON Woo Seok's acting! ✨(∩>o<∩)♡"}, 
   "malay": {"title": "BYEON Woo Seok MEMUKAU sebagai Ryu Sun-jae di Lovely Runner!", "body": "Pengkritik memujiimachinery lakonan BYEON Woo Seok sebagai Ryu Sun-jae di Lovely Runner! 🎉 Jangan lepaskan drama fantasi romantis ini yang akan membuat korang terpegun! ❤️ Tonton sekarang dan rasai keajaiban lakonan BYEON Woo Seok! ✨(∩>o<∩)♡"}},

   "4": {"english": {"title": "The Ultimate BYEON Woo Seok Fan Experience in Lovely Runner is HERE!!!", "body": "Get ready to swoon over BYEON Woo Seok's charms in Lovely Runner! 😍 As Ryu Sun-jae, he'll make your heart skip a beat. Watch now and experience the ultimate fan service! ❤️(≧∇≦)"}, 
   "malay": {"title": "Pengalaman Peminat BYEON Woo Seok yang Terbaik di Lovely Runner adalah DI SINI!!!", "body": "Bersedia untuk jatuh cinta dengan keperibadian BYEON Woo Seok di Lovely Runner! 😍 Sebagai Ryu Sun-jae, dia akan membuat hati korang berdegup kencang. Tonton sekarang dan rasai pengalaman peminat yang terbaik! ❤️(≧∇≦)"}},

   "5": {"english": {"title": "Love Knows No Bounds in Lovely Runner, Starring BYEON Woo Seok!!!", "body": "A romance that transcends time and space? ⏰ BYEON Woo Seok's Lovely Runner is a must-watch! ❤️ Don't miss this fantasy romance that will capture your heart! ✨(¬‿¬)"}, 
   "malay": {"title": "Cinta Tidak Mengenal Batas di Lovely Runner, Dibintangi BYEON Woo Seok!!!", "body": "Romans yang mengatasi masa dan ruang? ⏰ Lovely Runner BYEON Woo Seok adalah wajib tonton! ❤️ Jangan lepaskan drama fantasi romantis ini yang akan membuat hati korang terpikat! ✨(¬‿¬)"}}
}

HARD_CODED_REGEN= {
   "1": {"english": {"title": "OMG, Byeon Woo Seok's Time-Traveling Romance!", "body": "fr fr, get ready to fall in love with Ryu Sun-Jae!!! (∩>o<∩)♡ In Lovely Runner, Byeon Woo Seok stars as a top star who travels back in time to relive his past. Will he find love in the past? Watch now and find out!!! 📺"}, 
   "malay": {"title": "OMG, Romansa Masa Lalu Byeon Woo Seok!", "body": "fr fr, kitorang nak jatuh cinta dengan Ryu Sun-Jae!!! (∩>o<∩)♡ Di Lovely Runner, Byeon Woo Seok membintangi sebagai bintang teratas yang kembali ke masa lalu. Adakah dia akan menemui cinta di masa lalu? Tonton sekarang dan cari tahu!!! 📺"}},

   "2": {"english": {"title": "LOL, Love Knows No Bounds! Byeon Woo Seok in Lovely Runner", "body": "ngl, imagine meeting your idol in the past!!! 😍 Byeon Woo Seok's Ryu Sun-Jae gets a second chance at love in Lovely Runner. Don't miss this romantic fantasy drama!!! ❤️ Watch now on Viu! (≧∇≦)"}, 
   "malay": {"title": "LOL, Cinta Tak Terbatas! Byeon Woo Seok di Lovely Runner", "body": "ngl, bayangkan korang bertemu idola di masa lalu!!! 😍 Byeon Woo Seok sebagai Ryu Sun-Jae mendapat kesempatan kedua untuk cinta di Lovely Runner. Jangan lepaskan drama romantis fantasi ini!!! ❤️ Tonton sekarang di Viu! (≧∇≦)"}},

   "3": {"english": {"title": "OMG, Byeon Woo Seok's Heartfelt Performance in Lovely Runner!", "body": "fr fr, get ready to be swept away by Byeon Woo Seok's charms!!! 😊 In Lovely Runner, he plays Ryu Sun-Jae, a top star who travels back in time to relive his past. Watch now and experience the emotional rollercoaster!!! 🎢 (∩>o<∩)♡"}, 
   "malay": {"title": "OMG, Prestasi Byeon Woo Seok yang Mengharukan di Lovely Runner!", "body": "fr fr, kitorang nak dibuai oleh karisma Byeon Woo Seok!!! 😊 Di Lovely Runner, dia berperan sebagai Ryu Sun-Jae, bintang teratas yang kembali ke masa lalu. Tonton sekarang dan alami rollercoaster emosi!!! 🎢 (∩>o<∩)♡"}},

   "4": {"english": {"title": "Time-Traveling Love Story! Byeon Woo Seok in Lovely Runner", "body": "what if you could go back in time and change your past??? ⏰ Byeon Woo Seok's Ryu Sun-Jae gets a second chance at love in Lovely Runner. Don't miss this romantic fantasy drama!!! ❤️ Watch now on Viu! (¬‿¬)"}, 
   "malay": {"title": "Kisah Cinta Masa Lalu! Byeon Woo Seok di Lovely Runner", "body": "bagaimana jika korang dapat kembali ke masa lalu dan mengubah masa lalu??? ⏰ Byeon Woo Seok sebagai Ryu Sun-Jae mendapat kesempatan kedua untuk cinta di Lovely Runner. Jangan lepaskan drama romantis fantasi ini!!! ❤️ Tonton sekarang di Viu! (¬‿¬)"}},

   "5": {"english": {"title": "OMG, Byeon Woo Seok's Ryu Sun-Jae: A Love Story that Transcends Time!", "body": "fr fr, imagine falling in love with someone from the past!!! 😍 Byeon Woo Seok's Ryu Sun-Jae travels back in time to relive his past and finds love in Lovely Runner. Watch now and experience the magic!!! ✨ (∩>o<∩)♡"}, 
   "malay": {"title": "Ryu Sun-Jae Byeon Woo Seok: Kisah Cinta yang Melintasi Masa!", "body": "fr fr, bayangkan kitorang jatuh cinta dengan seseorang dari masa lalu!!! 😍 Byeon Woo Seok sebagai Ryu Sun-Jae kembali ke masa lalu dan menemui cinta di Lovely Runner. Tonton sekarang dan alami keajaiban!!! ✨ (∩>o<∩)♡"}}
}

HARD_CODED_REFINE = {
   "1": {"english": {"title": "Wooseok's Time-Warping Romance! ⏰", "body": "Get ready to fall in love with Byeon Woo-seok's charming performance in Lovely Runner! 💕 Will he change his fate through time travel? Find out now! #LovelyRunner #ByeonWooSeok #KdramaAddict"}, "malay": {"title": 'Romansa Wooseok Melalui Masa! ⏰', "body": 'Siap-siap jatuh cinta dengan persembahan Byeon Woo-seok yang memikat di Lovely Runner! 💕 Nak tahu adakah dia akan mengubah takdirnya melalui perjalanan masa? Cari tahu sekarang lah! #LovelyRunner #ByeonWooSeok #KDramaAddict'}},
   "2": {"english": {"title": "Byeon Woo-seok's Time-Traveling Secrets! 🕰️", "body": "Uncover the mysteries of Lovely Runner with Byeon Woo-seok's character, Ryu Sun-jae! 🔍 Will he uncover the truth about his past? Watch now! #LovelyRunner #ByeonWooSeok #KdramaMystery"}, "malay": {"title": 'Rahsia Perjalanan Masa Byeon Woo-seok! 🕰️', "body": 'Bongkarlah misteri Lovely Runner bersama watak Byeon Woo-seok, Ryu Sun-jae! 🔍 Nak tahu adakah dia akan mengungkapkan kebenaran tentang masa lalunya? Tonton sekarang lah! #LovelyRunner #ByeonWooSeok #KDramaMystery'}},
   "3": {"english": {"title": "Wooseok's Leap Through Time! ⏱️", "body": 'Join Byeon Woo-seok on a thrilling adventure through time in Lovely Runner! 🕰️ Will he be able to change his fate? Find out now! #LovelyRunner #ByeonWooSeok #KdramaAddict'}, "malay": {"title": 'Lompatan Wooseok Melalui Masa! ⏱️', "body": 'Jom bergabung dengan Byeon Woo-seok dalam pengembaraan yang menegangkan melalui masa di Lovely Runner! 🕰️ Nak tahu adakah dia akan mengubah takdirnya? Cari tahu sekarang lah! #LovelyRunner #ByeonWooSeok #KDramaAddict'}},
   "4": {"english": {"title": "Time-Traveling Love: Wooseok's Story! ❤️", "body": "Get ready to swoon over Byeon Woo-seok's romantic performance in Lovely Runner! 💘 Will he find love through time travel? Watch now! #LovelyRunner #ByeonWooSeok #KdramaRomance"}, "malay": {"title": 'Cinta Melalui Masa: Kisah Wooseok! ❤️', "body": 'Siap-siap jatuh cinta dengan persembahan romantis Byeon Woo-seok di Lovely Runner! 💘 Nak tahu adakah dia akan mencari cinta melalui perjalanan masa? Tonton sekarang lah! #LovelyRunner #ByeonWooSeok #KDramaRomance'}},
   "5": {"english": {"title": "Byeon Woo-seok's Timeless Performance! 🕰️", "body": "Experience the magic of Lovely Runner with Byeon Woo-seok's outstanding performance! 🌟 Will he change the course of his life through time travel? Find out now! #LovelyRunner #ByeonWooSeok #KdramaMasterpiece"}, "malay": {"title": 'Persembahan Abadi Byeon Woo-seok! 🕰️', "body": 'Alami keajaiban Lovely Runner dengan persembahan luar biasa Byeon Woo-seok! 🌟 Nak tahu adakah dia akan mengubah hala tuju hidupnya melalui perjalanan masa? Cari tahu sekarang lah! #LovelyRunner #ByeonWooSeok #KDramaMasterpiece'}}
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
      if inputData.basePush is None:
         return HARD_CODED_REGEN
      else:
         return HARD_CODED_REFINE
   
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