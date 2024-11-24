from dotenv import load_dotenv
load_dotenv(override=True)

from utils import slang
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_together import ChatTogether

llm = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=0.4)

def prepare_context(slang_data, shortform_data):
    slang_context = "\n".join(
        [f"{entry['word']}: {entry['meaning']} ({entry['explaination']}) Example: {entry['example']}" for entry in slang_data]
    )

    shortform_context = "\n".join(
        [f"{entry['short-form word']}: {entry['normal word']} ({entry['meaning']})" for entry in shortform_data]
    )

    return slang_context, shortform_context

def rephrase(push):
    slangs, shortforms = prepare_context(slang.slang_list, slang.shortform_list)

    prompt = PromptTemplate(
    input_variables=["pushes", "slangs", "shortforms"],
    template = """You are an assistant that naturally enhances text by incorporating conversational Malaysian slang and short forms.
        Below is a set of push notifications in JSON format and a list of slang/shortforms. Your task is to enhance only the Malay versions to sound 
        more casual and relatable, while keeping the English versions and JSON structure intact.
        
        Guidelines for slang usage:
        1. Use slang and short forms sparingly - only where they sound natural in casual conversation
        2. Maintain the message's clarity and professionalism
        3. Keep formal words when they are more appropriate
        4. Preserve all emojis and hashtags exactly as they appear
        5. Consider the context and tone of each message
        
        The modifications should make the text feel more authentic and relatable, like how a local Malaysian would casually communicate.
    
        Here is the push notifications in JSON: {pushes}
        
        Available slang terms: {slangs}
        Available short forms: {shortforms}

        Use escape characters for quotes if there is in the JSON strings.
        The output format have to be JSON as follows! The number is the push number:
        {{
        "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
        "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
        "3": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
        ...
        }}
        Return only valid JSON without any additional text or explanations infront or after.
        Do not include anything else other than the JSON, or the output will be invalid.
        """
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"pushes": push,  "slangs": slangs, "shortforms": shortforms})