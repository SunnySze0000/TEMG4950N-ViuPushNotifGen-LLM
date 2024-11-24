import json
from dotenv import load_dotenv
load_dotenv(override=True)

from src import data
from node import loader, splitter, embedder, retriever, slanger, json_parser
from langchain_core.output_parsers import StrOutputParser
from langchain_together import ChatTogether
from utils import prompts, questions
from utils.state import backendState
from pipeline import rerankingRAG
import pprint

def generating(input_var):
    #llm = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=backendState['creativity'])
    llm = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=0.8)

    chain = prompts.final_prompt | llm | StrOutputParser()
    push = chain.invoke(input_var)
    print(push)
    push = json_parser.extract_json_from_string(push)
    
    #print('Before Slanging: ')
    #print(push)

    print('After Slanging: ')
    if input_var.get('include_slangs', False):
        push = slanger.rephrase(push)
        print(push)
        push = json_parser.extract_json_from_string(push)
    
    print(type(push))

    return push

def finalCastPipeline(push_number=5, datasets="Viu_datasets"):
    
    cast = backendState["name_of_cast"]
    
    print("___Start Handling Data___")
    cast_driven_data = data.getCastDrivenData(cast, backendState['name_of_series'], datasets)

    if cast_driven_data == None:
        print("Sorry but I don't have related information \n")
        print("---TERMINATED---")
        return

    print("___Start Loading___")
    series_wiki = loader.webLoading(cast_driven_data["series_wiki_url"])
    cast_wiki = loader.wikiLoading(cast)
    
    print("___Start Splitting___")
    splitted_wiki = splitter.splitting([series_wiki, cast_wiki])
    
    print("___Start Embedding___")
    vectorstore = embedder.embedding(splitted_wiki, cast, backendState['name_of_series'])

    print("___Start Retrieval___")
    answers = []
    question_list = questions.cast_driven_questions(cast_driven_data["series_name"], cast_driven_data["target_cast"])
    for question in question_list:
        inputs = {"question": question, "vectorstore": vectorstore, "retry_count": 0}
        for output in rerankingRAG.retrieval_RAG_pipeline.stream(inputs):
            for key, value in output.items():
                pprint.pprint(f"Finished running: {key}:")
        try:
            answers.append(value["generation"])
        except KeyError:
            print("Sorry but I don't have related information \n")
            print("---END OF PROCESS: EXCEED TIME LIMIT---")
    if len(answers) == 1:
        for _ in range(4):
            answers.append(None)
            
    retrieved_wiki_of_series = retriever.wiki_retrieving(vectorstore, cast, cast_driven_data["series_name"])
    
    # backendState = {
    #     "number_of_push_notifications": push_number,
    #     "name_of_series": cast_driven_data["series_name"],
    #     "retrieved_wiki_of_series": retrieved_wiki_of_series,
    #     "series_content": answers[0], 
    #     "series_description": cast_driven_data["series_description"],
    #     "name_of_cast": cast_driven_data["target_cast"],
    #     "type_of_cast": cast_driven_data["target_cast_type"],
    #     "nickname_of_cast": answers[1],
    #     "quote_of_cast": answers[2],
    #     "interesting_fact_of_cast": answers[3],
    #     "character_in_series_acted_by_cast": answers[4],
    # }

    # change backendstate
    backendState['number_of_push_notifications'] = push_number
    backendState['name_of_series'] = cast_driven_data["series_name"]
    backendState['retrieved_wiki_of_series'] = retrieved_wiki_of_series
    backendState['series_content'] = answers[0]
    backendState['series_description'] = cast_driven_data["series_description"]
    backendState['name_of_cast'] = cast_driven_data["target_cast"]
    backendState['type_of_cast'] = cast_driven_data["target_cast_type"]
    backendState['nickname_of_cast'] = answers[1]
    backendState['quote_of_cast'] = answers[2]
    backendState['interesting_fact_of_cast'] = answers[3]
    backendState['character_in_series_acted_by_cast'] = answers[4]
    
    input_variables = {
        "type_of_push_notification": backendState['type_of_push_notification'],
        "number_of_push_notifications": backendState['number_of_push_notifications'],
        "name_of_series": backendState['name_of_series'],
        "retrieved_wiki_of_series": backendState['retrieved_wiki_of_series'],
        "series_content": backendState['series_content'],
        "series_description": backendState['series_description'],
        "name_of_cast": backendState['name_of_cast'],
        "type_of_cast": backendState['type_of_cast'],
        "nickname_of_cast": backendState['nickname_of_cast'],
        "quote_of_cast": backendState['quote_of_cast'],
        "interesting_fact_of_cast": backendState['interesting_fact_of_cast'],
        "character_in_series_acted_by_cast": backendState['character_in_series_acted_by_cast'],
        "demographics_of_target_receiver": backendState['demographics_of_target_receiver'],
        "base_push_example": backendState['base_push_example'],
        "local_trend_in_malaysia": backendState['local_trend_in_malaysia'],
        "include_emoji": backendState['include_emoji'],
        "include_slangs": backendState['include_slangs'],
        "additional_requirements": backendState['additional_requirements'],
    }
    
    print("___Start Generation___")
    pushes = generating(input_variables)
    backendState['pushes'] = pushes
    print(backendState)
    print(pushes)
    print("___End of Main Pipeline___")
    return pushes

def finalContentPipeline(push_number=5, datasets="Viu_datasets"):
    
    content = backendState["name_of_series"]
    
    print("___Start Handling Data___")
    content_driven_data = data.getContentDrivenData(content, datasets)

    if content_driven_data == None:
        print("Sorry but I don't have related information \n")
        print("---TERMINATED---")
        return

    print("___Start Loading___")
    series_wiki = loader.webLoading(content_driven_data["series_wiki_url"])
    content_wiki = loader.wikiLoading(content)
    
    print("___Start Splitting___")
    splitted_wiki = splitter.splitting([series_wiki, content_wiki])
    
    print("___Start Embedding___")
    vectorstore = embedder.embedding(splitted_wiki, content, backendState['name_of_series'])

    print("___Start Retrieval___")
    answers = []
    question_list = questions.content_driven_questions(content_driven_data["series_name"])
    for question in question_list:
        inputs = {"question": question, "vectorstore": vectorstore, "retry_count": 0}
        for output in rerankingRAG.retrieval_RAG_pipeline.stream(inputs):
            for key, value in output.items():
                pprint.pprint(f"Finished running: {key}:")
        try:
            answers.append(value["generation"])
        except KeyError:
            print("Sorry but I don't have related information \n")
            print("---END OF PROCESS: EXCEED TIME LIMIT---")
    if len(answers) == 1:
        for _ in range(4):
            answers.append(None)
            
    retrieved_wiki_of_series = retriever.wiki_content_retrieving(vectorstore, content_driven_data["series_name"])
    
    backendState['number_of_push_notifications'] = push_number
    backendState['name_of_series'] = content_driven_data["series_name"]
    backendState['retrieved_wiki_of_series'] = retrieved_wiki_of_series
    backendState['series_content'] = answers[0]
    backendState['series_description'] = content_driven_data["series_description"]
    
    input_variables = {
        "type_of_push_notification": backendState['type_of_push_notification'],
        "number_of_push_notifications": backendState['number_of_push_notifications'],
        "name_of_series": backendState['name_of_series'],
        "retrieved_wiki_of_series": backendState['retrieved_wiki_of_series'],
        "series_content": backendState['series_content'],
        "series_description": backendState['series_description'],
        "name_of_cast": backendState['name_of_cast'],
        "type_of_cast": backendState['type_of_cast'],
        "nickname_of_cast": backendState['nickname_of_cast'],
        "quote_of_cast": backendState['quote_of_cast'],
        "interesting_fact_of_cast": backendState['interesting_fact_of_cast'],
        "character_in_series_acted_by_cast": backendState['character_in_series_acted_by_cast'],
        "demographics_of_target_receiver": backendState['demographics_of_target_receiver'],
        "base_push_example": backendState['base_push_example'],
        "local_trend_in_malaysia": backendState['local_trend_in_malaysia'],
        "include_emoji": backendState['include_emoji'],
        "include_slangs": backendState['include_slangs'],
        "additional_requirements": backendState['additional_requirements'],
    }
    
    print("___Start Generation___")
    backendState['pushes'] = generating(input_variables)
    print("___End of Pipeline___")
    return backendState['pushes']

def simplifiedCastPipe(cast, push_number=1, datasets="Viu_datasets"):

    print("___Start Handling Data___")
    cast_driven_data = data.getCastDrivenData(cast, 'Lovely Runner', datasets)

    if cast_driven_data == None:
        print("Sorry but I don't have related information \n")
        print("---TERMINATED---")
        return

    print("___Start Loading___")
    series_wiki = loader.webLoading(cast_driven_data["series_wiki_url"])
    cast_wiki = loader.wikiLoading(cast)
    
    print("___Start Splitting___")
    splitted_wiki = splitter.splitting([series_wiki, cast_wiki])
    
    print("___Start Embedding___")
    vectorstore = embedder.embedding(splitted_wiki, cast)

    print("___Start Retrieval___")
    answers = []
    question_list = questions.cast_driven_questions(cast_driven_data["series_name"], cast_driven_data["target_cast"])
    for question in question_list:
        inputs = {"question": question, "vectorstore": vectorstore, "retry_count": 0}
        for output in rerankingRAG.retrieval_RAG_pipeline.stream(inputs):
            for key, value in output.items():
                pprint.pprint(f"Finished running: {key}:")
        try:
            answers.append(value["generation"])
        except KeyError:
            print("Sorry but I don't have related information \n")
            print("---END OF PROCESS: EXCEED TIME LIMIT---")
    if len(answers) == 1:
        for _ in range(4):
            answers.append(None)
            
    retrieved_wiki_of_series = retriever.wiki_retrieving(vectorstore, cast, cast_driven_data["series_name"])
    
    input_variables = {
        "type_of_push_notification": "cast-driven",
        "number_of_push_notifications": push_number,
        "name_of_series": cast_driven_data["series_name"],
        "retrieved_wiki_of_series": retrieved_wiki_of_series,
        "series_content": answers[0], 
        "series_description": cast_driven_data["series_description"],
        "name_of_cast": cast_driven_data["target_cast"],
        "type_of_cast": cast_driven_data["target_cast_type"],
        "nickname_of_cast": answers[1],
        "quote_of_cast": answers[2],
        "interesting_fact_of_cast": answers[3],
        "character_in_series_acted_by_cast": answers[4],
        "demographics_of_target_receiver": "50-65 years old, fans of cast",
        "base_push_example": None,
        "local_trend_in_malaysia": None, #"Hot weather alert", #"KIM Hye Yoon will be in Viu scream date on 24th February 2024", #"Kim Hye Yoon, star of Lovely Runner, won the Outstanding Asia Star Award." #"Viu is organizing an event inviting Kim Ha Nuel, Lin Tin Wai, and Rong Lam to Malaysia on June10, tickets are all sold out and people are very hyped to it.",
        "include_emoji": True,
        "include_slangs": True,
        "additional_requirements": None,
    }
    
    print("___Start Generation___")
    push = generating(input_variables)
    
    print("___Decision of Regeneration___")
    while True:
        user_input = input("Do you want to regenerate the push notification? (yes/no): ")
        if user_input == "yes":
            base_push_num = input("Base push example? (leave blank if none): ")
            if base_push_num != "":
                input_variables["base_push_example"] = "Title" + push[base_push_num]['english']['title'] + "\n" + "Body" + push[base_push_num]['english']['body']
            req = input("Additional requirements? (leave blank if none): ")
            if req != "":
                input_variables["additional_requirements"] = req

            print("___Start Regeneration___")
            push = generating(input_variables)
        else:
            print("___End of Regeneration___")
            break
    
    print("___End of Pipeline___")

def simplifiedContentPipe(content, push_number, datasets="Viu_datasets"):
    print("___Start Handling Data___")
    content_driven_data = data.getContentDrivenData(content, datasets)

    print("___Start Loading___")
    series_wiki = loader.webLoading(content_driven_data["series_wiki_url"]) #empty link
    content_wiki = loader.wikiLoading(content)
    
    print("___Start Splitting___")
    splitted_wiki = splitter.splitting([series_wiki, content_wiki])
    
    print("___Start Embedding___")
    vectorstore = embedder.embedding(splitted_wiki, content)

    print("___Start Retrieval___")
    answers = []
    question_list = questions.content_driven_questions(content_driven_data["series_name"])
    for question in question_list:
        inputs = {"question": question, "vectorstore": vectorstore, "retry_count": 0}
        for output in rerankingRAG.retrieval_RAG_pipeline.stream(inputs):
            for key, value in output.items():
                pprint.pprint(f"Finished running: {key}:")
        try:
            answers.append(value["generation"])
        except KeyError:
            print("Sorry but I don't have related information \n")
            print("---END OF PROCESS: EXCEED TIME LIMIT---")
    if len(answers) == 1:
        for _ in range(4):
            answers.append(None)
            
    retrieved_wiki_of_series = retriever.wiki_content_retrieving(vectorstore, content_driven_data["series_name"])
    
    input_variables = {
        "type_of_push_notification": "content-driven",
        "number_of_push_notifications": push_number,
        "name_of_series": content_driven_data["series_name"],
        "retrieved_wiki_of_series": retrieved_wiki_of_series,
        "series_content": answers[0], 
        "series_description": content_driven_data["series_description"],
        "name_of_cast": None,
        "type_of_cast": None,
        "nickname_of_cast": None,
        "quote_of_cast": None,
        "interesting_fact_of_cast": None,
        "character_in_series_acted_by_cast": None,
        "demographics_of_target_receiver": "20-30 years old, fans of cast",
        "base_push_example": None,
        "local_trend_in_malaysia": None, #"Viu is organizing an event inviting Kim Ha Nuel, Lin Tin Wai, and Rong Lam to Malaysia on June10, tickets are all sold out and people are very hyped to it.",
        "include_emoji": True,
        "include_slangs": False,
        "additional_requirements": None,
    }
    
    print("___Start Generation___")
    push = generating(input_variables)
    
    print("___Decision of Regeneration___")
    while True:
        user_input = input("Do you want to regenerate the push notification? (yes/no): ")
        if user_input == "yes":
            base_push_num = input("Base push example? (leave blank if none): ")
            if base_push_num != "":
                input_variables["base_push_example"] = "Title" + push[base_push_num]['english']['title'] + "\n" + "Body" + push[base_push_num]['english']['body']
            req = input("Additional requirements? (leave blank if none): ")
            if req != "":
                input_variables["additional_requirements"] = req

            print("___Start Regeneration___")
            push = generating(input_variables)
        else:
            print("___End of Regeneration___")
            break
    
    print("___End of Pipeline___")