import json
import re
import time

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
        parsed_json = json.loads(json_str)
        
        
        
        return parsed_json