from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_together import ChatTogether

llm = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=0.4)

def ageRephrase(push, age):

    prompt = PromptTemplate(
    input_variables=["pushes", "age_of_target_audience"],
    template = """You are an assistant that naturally enhances push notification text by incorporating styles and symbols to match the age of target audience.
        Below is a set of push notifications in JSON format. Your task is to enhance both version to the desginated age group according to the guidelines below.
        while keeping the English versions and JSON structure intact.

    Audience-Specific Guidelines:

    TEENS (10-21):
    Tone: Ultra-casual, excited, FOMO-driven
    Language: "OMG!", "fr fr", "ngl", "slay", "LOL"...
    Symbols: (∩>o<∩)♡, (≧∇≦), (¬‿¬), !!!, ???, ...
    Content: Social moments, friendship drama, relatable scenes
    Hooks: Trends, viral moments, cast's social media, Pop culture references, binge appeal
    Example: "fr fr, Song Kang spilling tea on TikTok rn!!! 🫢 Catch his behind-the-scenes!!! (≧∇≦)"
    BM Style: Heavy Manglish, trending slang

    ADULTS (age 22-34):
    Tone: Smart casual, sophisticated humor
    Language: Professional with subtle wit
    Content: Character depth, plot complexity, quality
    Hooks: Critical acclaim, unique storylines, cast achievements, social issues
    Example: "Award-winning performance alert! Critics call it 'unmissable'"
    BM Style: Standard BM with urban flair

    MATURE ADULTS (age 35-49):
    Tone: Refined, quality-focused
    Language: Professional, clear, respectful
    Content: Production value, artistic merit, family themes
    Hooks: Director credentials, awards, family viewing
    Example: "From acclaimed director Lee Jae-wook: A masterpiece of storytelling"
    BM Style: Proper BM, occasional formal terms

    SENIOR ADULTS (age 50+):
    Tone: Traditional, respectful, clear
    Language: Straightforward, no slang
    Symbols: 😊🤗🤭👍🏻🙏🏻🌹💐🏵🥀🪷
    Content: Cultural values, historical accuracy
    Hooks: Classic elements, familiar actors, family bonds
    Example: "Revisit the golden age🪷🪷 of drama with veteran star [Name]😊😊"
    BM Style: Classical BM, traditional expressions
    
    Key Engagement Elements:
    Teens: Social proof, FOMO, trending elements
    Adults: Quality markers, intelligent content, social relevance
    Mature Adults: Family value, critical acclaim
    Senior Adults: Traditional appeal, cultural significance
    
    Here is the push notifications in JSON: {pushes}
        
        age of the target audience: {age_of_target_audience}

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

    return chain.invoke({"pushes": push, "age_of_target_audience": age})