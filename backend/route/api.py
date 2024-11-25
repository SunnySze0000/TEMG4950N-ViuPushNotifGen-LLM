from fastapi import APIRouter
from typing import Optional, Dict, List
from pipeline.rerankingGen import finalCastPipeline, finalContentPipeline, generating
from utils.schema import PushRegenerateRequest, PushRequest, PushResponse, TrendResponse, TrendRequest
from utils.state import backendState, initialize_backend_state
from pipeline.trendsPipeline import getTrends, refreshTrends
# import csv
# from node import save

api_router = APIRouter()

@api_router.get("/scrapeTrends")
async def get_trend() -> Dict[int, TrendResponse]:
   try:
      # scrape trend function
      # return pushes
      return getTrends()
   except Exception as e:
      print(e)
      raise e

@api_router.post("/refreshTrends")
async def post_trend(request: TrendRequest) -> Dict[int, TrendResponse]:
   try:
      # scrape trend function
      # return pushes
      print(f"Refreshing trends with cast_name: {request.cast_name} and series_name: {request.series_name}")
      return refreshTrends(request.cast_name, request.series_name)
   except Exception as e:
      print(e)
      raise e

@api_router.post("/genPush")
async def post_gen_push(input_data: PushRequest) -> Dict[int, PushResponse]:
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
      print(e)
      raise e
   
@api_router.post("/regenPush")
async def post_regen_push(inputData: PushRegenerateRequest) -> Dict[int, PushResponse]:
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
      print(e)
      raise e
   
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