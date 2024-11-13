from fastapi import APIRouter
from typing import Optional, Dict, List
from pipeline.rerankingGen import finalCastPipeline, finalContentPipeline, generating
from utils.schema import PushRegenerateRequest, PushRequest, PushResponse
from utils.state import backendState

api_router = APIRouter()

@api_router.get("/scrapeTrends")
async def get_trend() -> dict:
   try:
      # scrape trend function
      # return pushes
      return {}
   except Exception as e:
      print(e)
      raise e

@api_router.post("/scrapeTrends")
async def post_trend(cast_name: Optional[str], series_name: Optional[str]) -> dict:
   try:
      # scrape trend function
      # return pushes
      return {}
   except Exception as e:
      print(e)
      raise e

@api_router.post("/genPush")
async def post_gen_push(input_data: PushRequest) -> Dict[int, PushResponse]:
   try:
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
      backendState["base_push_example"] = "Title:" + inputData.basePush.english.title + "\n" + "Body:" + inputData.basePush.english.body
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