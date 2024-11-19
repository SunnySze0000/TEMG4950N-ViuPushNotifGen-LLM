import csv
import os
from utils import example

def save_to_csv(data, filename):
    # header = ['English', 'Eng_Title', 'Eng_Body', 'Malay', 'Malay_Title', 'Malay_Body']

    # file_exists = os.path.exists(filename)
    #print(file_exists)

    try:
        with open(filename, mode='a', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # if not file_exists:
            #     writer.writerow(header)

            english_data = data['english']
            malay_data = data['malay']

            row = [
                'English',                     # Language
                english_data['title'],         # English Title
                english_data['body'],          # English Body
                'Malay',                       # Language
                malay_data['title'],           # Malay Title
                malay_data['body']             # Malay Body
            ]

            writer.writerow(row)  # Write the data row
            print(f'Successfully saved data to {filename}')
    except Exception as e:
        print(f'Error: {e}')


def update_examples(variables, data):

    filename = 'utils\example.py'

    del variables['retrieved_wiki_of_series'] # wiki not stored
    variables['english_title'] = data['english']['title']
    variables['english_body'] = data['english']['body']
    variables['malay_title'] = data['malay']['title']
    variables['malay_body'] = data['malay']['body']
    example.examples.append(variables)

    with open(filename, mode='w', encoding='utf-8') as file:
        file.write('examples = ' + repr(example.examples))  # Write the updated examples list

    print("Example list updated")