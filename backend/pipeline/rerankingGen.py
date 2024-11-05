from dotenv import load_dotenv
load_dotenv(override=True)

from src import data
from node import loader, splitter, embedder, retriever
from langchain_core.output_parsers import JsonOutputParser
from langchain_together import ChatTogether
from utils import prompts, questions
from pipeline import retrieveRAG, rerankingRAG
import pprint

llm = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=0.4)

def generating(input_var):

    chain = prompts.final_prompt | llm | JsonOutputParser()
    push = chain.invoke(input_var)
    
    print(push)
    return push

def castPipeline(cast, push_number, datasets = "Viu_datasets"):

    print("___Start Handling Data___")
    cast_driven_data = data.getCastDrivenData(cast, datasets)

    print("___Start Loading___")
    series_wiki = loader.webLoading(cast_driven_data["series_wiki_url"]) #empty link
    cast_wiki = loader.wikiLoading(cast)
    
    print("___Start Splitting___")
    splitted_wiki = splitter.splitting([series_wiki, cast_wiki])
    
    print("___Start Embedding___")
    vectorstore = embedder.embedding(splitted_wiki, cast)

    print("___Start Retrieval___")
    answers = []
    question_list = questions.cast_driven_questions(cast_driven_data["series_name"], cast_driven_data["target_cast"])
    for question in question_list:
        #inputs = {"question": question, "vectorstore": vectorstore}
        try:
            answers = answers + retriever.reranker_retrieving(question, vectorstore)
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
        "demographics_of_target_receiver": "20-30 years old, fans of cast",
        "base_push_example": None,
        "local_trend_in_malaysia": "Viu is organizing an event inviting Kim Ha Nuel, Lin Tin Wai, and Rong Lam to Malaysia on June10, tickets are all sold out and people are very hyped to it.",
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
            base_push_num = input("Base push example? (Input 1 - 5, leave blank if none): ")
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


def simplifiedCastPipe(cast, push_number, datasets = "Viu_datasets"):

    print("___Start Handling Data___")
    cast_driven_data = data.getCastDrivenData(cast, datasets)

    print("___Start Loading___")
    series_wiki = loader.webLoading(cast_driven_data["series_wiki_url"]) #empty link
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
        "demographics_of_target_receiver": "20-30 years old, fans of cast",
        "base_push_example": None,
        "local_trend_in_malaysia": "Viu is organizing an event inviting Kim Ha Nuel, Lin Tin Wai, and Rong Lam to Malaysia on June10, tickets are all sold out and people are very hyped to it.",
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
