import json
import re
from langchain_together import ChatTogether
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def extract_json_from_string(input_string):
    # Regular expression to find JSON-like content
    json_pattern = re.compile(r'\{.*\}', re.DOTALL)
    match = json_pattern.search(input_string)
    #print(match.group(0))
    
    if match:
        json_str = match.group(0)
        # Replace single quotes with double quotes
        json_str = re.sub(r"(?<=\{)\'|\'(?=\})|(?<=: )\'|\'(?=,)|(?<=, )\'|\'(?=:)|(?<=\{)\'|\'(?=\})", '"', json_str)
        
        # Check if the number of opening and closing braces are equal
        open_brace_count = json_str.count('{')
        close_brace_count = json_str.count('}')
        
        if open_brace_count > close_brace_count:
            # Calculate how many '}' are needed
            missing_braces = open_brace_count - close_brace_count
            json_str += '}' * missing_braces
        json_str = json_str.replace('\n', '').replace('\r', '')
        print("JSON STRING")
        print(json_str)
        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError as e:
            parsed_json = reParsing(json_str)

        return parsed_json
    
def reParsing(input_string):
    
    llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", temperature=0)

    QUERY_PROMPT = PromptTemplate(
        input_variables=["input"],
        template="""You are an expert in correcting strings to the requested JSON format.
        This is the requested JSON format:
        {{
        "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
        "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
        ...
        }}
        Do not include any \n or \r in the JSON string.
        Do not ouput any other things except the JSON string.
        Make sure the format is surely correct. Correct the following string to the requested JSON format:
        Original question: {input}""",
    )

    reParsing_chain = QUERY_PROMPT | llm | StrOutputParser()

    print("---REPARSING---")

    parsed_result = reParsing_chain.invoke(input_string)
    return extract_json_from_string(parsed_result) 