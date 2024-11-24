from langchain_core.prompts import PromptTemplate
from langchain_together import ChatTogether
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from node import json_parser
from src import data

from dotenv import load_dotenv

load_dotenv(override=True)

# import os
# api_key = os.getenv("OPENAI_API_KEY")
# print("API Key Loaded:", api_key is not None)

llm = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=0)

scraped_data = ['M’sian Woman Celebrates Girl’s Birthday After Hearing She Had No One To Celebrate It With', 
         'M’sian Man Heads Straight To Water Park After Work, But Urgent Email Keeps Him Glued To Laptop', 
         'Kenderaan Terbakar, Anas Zahrin Beli Motosikal Buat Pasangan Suami Isteri, Netizen Sebak Doa Murah Rezeki.', 
         'Woman Blocks Car With Body To Let 2 SG-Registered Cars Cut Queue At JB Checkpoint', 
         'M’sian Woman Tells Couples To Use ChatGPT To Resolve Relationship Issues Instead Of Posting It Online', 
         'I’m A M’sian Website Designer Who Helps Transform Old Businesses While Preserving Their Wisdom And Spirit', 
         'M’sian Man Says You Shouldn’t Consider Marriage If Monthly Income Is Below RM15K', 
         'SG-Registered Car Driver Allegedly Swaps Car Plate Number To Pump RON95', 
         'Another UPNM Cadet Allegedly Burnt With Steam Iron, Investigations Underway', 
         '29yo M’sian Man Earns Nearly RM400K Monthly By Planting Various Vegetables', 
         'Bayar Lebih RM400,000\xa0Sales & Service Tax (SST), Aunty Ja Bangga Suka Dessert Makin Maju!', 
         'M’sians In KL Can Now Enjoy 50% Off Traffic Summonses From Nov 5 To 9', 
         'M’sian With RM1.7K Salary Tries To Buy RM163K Honda Civic, Leaves Car Dealer Speechless', 
         '“Masa Miskin Tak Termimpi Dapat Kereta” – Aliff Syukri Hadiahkan Toyota Vellfire Buat Bonda Rozita.', 
         '‘Not True’ — Starbucks M’sia Denies It’s Closing Over 100 Outlets Across Country']

def classifying(trend_titles):
    Query_prompt = PromptTemplate(
        input_variables=["title", "cast", "series", "description"],
        template=("""
            You are a classifier that determines the usefulness of a trend title for promoting TV shows and series in push notifications. 

            These are the information json of the series and corresponding cast:
            
            star: {cast}
            series: {series}
            series_description: {description}

            Classify the following title:

            Title: {title}

            Classify the title into one of the following categories: (Dont be harsh)

            - **None**: This is not an internet trend and cannot use to catch people eyeballs, DONT INCLUDE ANY INTERESTING NEWS THAT CAN CATCH PEOPLE ATTENTION TO THIS CATEGORY.
            - **Star**: The trend is related to a star and is useful for cast-driven push notifications.
            - **Series**: The trend relates to the series content description, such that would be useful to support the series content promotion.
            - **Star and Series**: The trend involves both a star and a series, making it useful for both types of push notifications.
            - **General**: The trend is related to a general topic (e.g. weather, festivals, hot trends slang or headlines) and is useful for any push notification, but not specifically tied to stars or series.

            Return the classification type and the trend title in JSON format as follows: 
            {{classification_type: trend_title}}
        """),
    )

    classifying_chain = Query_prompt | llm | JsonOutputParser()

    print("___Classifying___")
    
    cast = 'Kim Ha Nuel'
    series = 'Nothing Uncovered'
    description = "A korean series about a girl working hard to get into the kpop industry, bringing the best song to everyone!"

    results = {}
    print(trend_titles)
    for title in trend_titles:
        response = classifying_chain.invoke({"title": title, "cast": cast, "series": series, "description": description})
        results[title] = response
        print(response)
    return results

# print("THIS IS THE RESPONSE \n", results)
def testing():
    classifying(["ROSÉ & Bruno Mars’ New Song “APT.” Has Been Banned for South Korean Students, Here’s Why!"]) # For testing


# results = {'M’sian Woman Celebrates Girl’s Birthday After Hearing She Had No One To Celebrate It With': 'none', 
# 'M’sian Man Heads Straight To Water Park After Work, But Urgent Email Keeps Him Glued To Laptop': 'none',
# 'Kenderaan Terbakar, Anas Zahrin Beli Motosikal Buat Pasangan Suami Isteri, Netizen Sebak Doa Murah Rezeki.': 'star',
# 'Woman Blocks Car With Body To Let 2 SG-Registered Cars Cut Queue At JB Checkpoint': 'none',
# 'M’sian Woman Tells Couples To Use ChatGPT To Resolve Relationship Issues Instead Of Posting It Online': 'none', 
# 'I’m A M’sian Website Designer Who Helps Transform Old Businesses While Preserving Their Wisdom And Spirit': 'none',
# 'M’sian Man Says You Shouldn’t Consider Marriage If Monthly Income Is Below RM15K': 'none',
# 'SG-Registered Car Driver Allegedly Swaps Car Plate Number To Pump RON95': 'none',
# 'Another UPNM Cadet Allegedly Burnt With Steam Iron, Investigations Underway': 'none',
# '29yo M’sian Man Earns Nearly RM400K Monthly By Planting Various Vegetables': 'none',
# 'Bayar Lebih RM400,000\xa0Sales & Service Tax (SST), Aunty Ja Bangga Suka Dessert Makin Maju!': 'none',
# 'M’sians In KL Can Now Enjoy 50% Off Traffic Summonses From Nov 5 To 9': 'none',
# 'M’sian With RM1.7K Salary Tries To Buy RM163K Honda Civic, Leaves Car Dealer Speechless': 'none',
# '“Masa Miskin Tak Termimpi Dapat Kereta” – Aliff Syukri Hadiahkan Toyota Vellfire Buat Bonda Rozita.': 'star',
# '‘Not True’ — Starbucks M’sia Denies It’s Closing Over 100 Outlets Across Country': 'none'} 

def clean_text(text):
    return text.replace('"', '').replace("'", '').replace('‘', '').replace('’', '').replace('\n', ' ').replace('“', '').replace('”', '')

def classifying_test(trend_titles, cast="", series=""):
    # Define the prompt template with relevant placeholders
    query_prompt = PromptTemplate(
        input_variables=["titles", "cast", "series", "description"],
        template=("""
            You are a classifier that determines the usefulness of trend titles for promoting TV shows and series in push notifications.

            These are the information json of the series and corresponding cast:
            
            star: {cast}
            series: {series}
            series_description: {description}

            If star, series or series_description provided, classify strictly on the trend base on inforamtion given.      
            
            Classify the following titles:

            Titles: {titles}

            Classify each title into one of the following categories:

            - **None**: This is not an internet trend and cannot catch people's eyeballs, DONT INCLUDE ANY INTERESTING NEWS THAT CAN CATCH PEOPLE'S ATTENTION TO THIS CATEGORY.
            - **Star**: The trend is related to a star and is useful for cast-driven push notifications.
            - **Series**: The trend relates to the series content description, such that would be useful to support the series content promotion.
            - **Star and Series**: The trend involves both a star and a series, making it useful for both types of push notifications.
            - **General**: The trend is related to a general topic (e.g. weather, festivals, hot trends slang or headlines) and is useful for any push notification, but not specifically tied to stars or series.

            Return the classification type and the trend title in JSON format for each title as follows: 
            {{
            "1": {{"classification_type":classification_type, "trend_title":trend_title}},
            "2": {{"classification_type":classification_type, "trend_title":trend_title}},
            "3": {{"classification_type":classification_type, "trend_title":trend_title}},
            ...
            }}
        """),
    )

    # Create the classification chain
    classifying_chain = query_prompt | llm | StrOutputParser()

    print("___Classifying Trends___")

    # Series and cast information
    # cast = 'Kim Ha Nuel'
    # series = 'Nothing Uncovered'
    # description = "A Korean series"
    description = ""
    if series != "":
        description = data.getContentDrivenData(series, "Viu_datasets")['series_description']
    cleaned_trend_title = [clean_text(title) for title in trend_titles]
    numbered_titles = '\n'.join(f"{i + 1}. {title}" for i, title in enumerate(cleaned_trend_title))
    response = classifying_chain.invoke({"titles": numbered_titles, "cast": cast, "series": series, "description": description})
    print(response)
    response = json_parser.extract_json_from_string(response)
    print(f"Classification Results: {response}")
    return response