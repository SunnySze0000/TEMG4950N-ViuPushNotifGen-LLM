from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from utils.example import examples

example_prompt = PromptTemplate.from_template(
    """
    Given:
    type_of_push_notification={type_of_push_notification},
    number_of_push_notifications={number_of_push_notifications},
    name_of_series={name_of_series},
    series_content={series_content},
    series_description={series_description},
    name_of_cast={name_of_cast},
    type_of_cast={type_of_cast},
    nickname_of_cast={nickname_of_cast},
    quote_of_cast={quote_of_cast},
    interesting_fact_of_cast={interesting_fact_of_cast},
    character_in_series_acted_by_cast={character_in_series_acted_by_cast},
    demographics_of_target_receiver={demographics_of_target_receiver},
    base_push_example={base_push_example},
    local_trend_in_malaysia={local_trend_in_malaysia},
    include_emoji={include_emoji},
    include_slangs={include_slangs},
    additional_requirements={additional_requirements},
    
    The following juicy push notification for {name_of_series} is generated as below:
    english_title={english_title},
    english_body={english_body},
    malay_title={malay_title},
    malay_body={malay_body}
    """
)

# final_prompt = FewShotPromptTemplate(
#     examples = examples,
#     example_prompt = example_prompt,
#     suffix = """
#     Generate {number_of_push_notifications} {type_of_push_notification} push notifications for the Viu TV show "{name_of_series}".
#     Exaggerate and be a clickbait in the push!
    
#     Each push notification should be generated in both English and Bahasa Melayu.
#     Exaggerate and be a clickbait in the push!
    
#     The push notifications need to be very juicy and tempting to attract users to click.
#     Exaggerate and be a clickbait in the push!
    
#     Use a hook at the front, which can be the cast, content, trend, news, cast quote, series content, or memes—anything you think would be attractive.
#     Exaggerate and be a clickbait in the push!
    
#     Be creative and make the push notification as juicy as you can, and it can be longer.
#     Exaggerate and be a clickbait in the push!
    
#     Write the most important and attractive content in the first 100 characters of the body, ensuring the cast name and series name appear within these characters.
#     Exaggerate and be a clickbait in the push!
    
#     Each push notification must contain a title and a body. 
#     Exaggerate and be a clickbait in the push!
    
#     Add a call to action. Include hashtags at the end.
#     Exaggerate and be a clickbait in the push!
    
#     Be very juicy and not boring, and be creative.
#     Exaggerate and be a clickbait in the push!
    
#     The push must contain the more content of the show, it is fine to have the push being long.
#     Exaggerate and be a clickbait in the push!
    
#     If there are any extra requirements by the user, you must fulfill them while keeping the push interesting.
#     All input data may be None; use those that are not None and choose which ones to use by yourself.
#     Aim to generate the best clickbait {type_of_push_notification} notification.
    
#     If "Type of Push Notification" is cast-driven, "name_of_cast" must be included in the push.
#     If "Demographics of the target receiver of the push", please adjust the push according to the target receiver demographics, which is 
#         be more energetic for younger receivers,
#         be more cast-focus and use more information of the cast when the target receivers are fan on the cast
#     If "Base Push Example" is provided, improve and regenerate a push based on the "Base Push Example".
#     If "Local trend in Malaysia" is provided, the trend must be incoporated into the push with any method.
#     If "Include Slangs" is True, please incorporate local slangs in the Bahasa Melayu version.
#     If and only if "Include Emoji" is True, please se emojis.
    
#     The followings are additional requirements that must be fulfiled when generating the push notification.
#     {additional_requirements}

#     The following information will be input into the prompt, choose wisely which to incoporate in the push, use more as you can:
#     - Number of push notifications: {number_of_push_notifications}
#     - Name of the series: {name_of_series}
#     - Retrieved wiki of the series: {retrieved_wiki_of_series}
#     - Series content: {series_content}
#     - Series description: {series_description}
#     - Name of the cast: {name_of_cast}
#     - Type of cast={type_of_cast},
#     - Nickname of the cast: {nickname_of_cast}
#     - Quote of the cast: {quote_of_cast}
#     - Interesting fact of the cast: {interesting_fact_of_cast}
#     - Character in the series acted by the cast: {character_in_series_acted_by_cast}
    
#     - Demographics of the target receiver of the push: {demographics_of_target_receiver}

#     - Base Push Example: {base_push_example}
#     - Local trend in Malaysia: {local_trend_in_malaysia}
#     - Include Emoji: {include_emoji}
#     - Include Slangs: {include_slangs}
#     - Additional requirements from the user: {additional_requirements}

#     TThe output format have to be JSON as follows! The number is the push number:
#     {{
#     "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     "3": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     ...
#     }}
#     Never include anything else other than the JSON, 
#     Never include descriptions or commments in the output, infront JSON or after JSON, 
#     else the output will be invalid.""",
#    
#     input_variables=[
#         "type_of_push_notification",
#         "number_of_push_notifications",
#         "name_of_series",
#         "retrieved_wiki_of_series",
#         "series_content",
#         "series_description",
#         "name_of_cast",
#         "nickname_of_cast",
#         "quote_of_cast",
#         "interesting_fact_of_cast",
#         "character_in_series_acted_by_cast",
#         "demographics_of_target_receiver",
#         "base_push_example",
#         "local_trend_in_malaysia",
#         "include_emoji",
#         "include_slangs",
#         "additional_requirements",
#     ],
# )


# final_prompt = FewShotPromptTemplate(
#     examples = examples,
#     example_prompt = example_prompt,
#     suffix = """
#     You're a social media expert working for Viu who's amazing at writing viral push notifications! 
#     Create {number_of_push_notifications} super engaging {type_of_push_notification} push notifications for "{name_of_series}" on Viu.
    
#     Think like a social media influencer - make it irresistible! We want people's thumbs to stop scrolling 🛑
    
#     Key requirements:
#     - Write in both English and Bahasa Melayu
#     - Hook readers with cast info, juicy content, trending topics, quotes, or viral moments
#     - Make it impossible NOT to click! (But keep it real)
#     - Front-load the good stuff - cast name and series title in first 100 characters
#     - Include title + body + call-to-action + hashtags
#     - Feel free to make it longer if you've got more tea to spill ☕
    
#     Pro tips:
#     - If it's cast-driven, spotlight {name_of_cast}
#     - For younger audiences: Keep it fresh and energetic
#     - For die-hard fans: Deep dive into cast details and behind-the-scenes
#     - If there's a base example, take it to the next level
#     - If there's a Malaysian trend, work that magic in
#     - Slang it up in BM if {include_slangs} is True
#     - Throw in emojis if {include_emoji} is True

#     Here's your content goldmine (use what sparks joy):
#     - Series name: {name_of_series}
#     - Wiki intel: {retrieved_wiki_of_series}
#     - Content deets: {series_content}
#     - Series lowdown: {series_description}
#     - Star power: {name_of_cast}
#     - Cast type: {type_of_cast}
#     - Nickname: {nickname_of_cast}
#     - Quotable moments: {quote_of_cast}
#     - Fun facts: {interesting_fact_of_cast}
#     - Character: {character_in_series_acted_by_cast}
    
#     Target audience: {demographics_of_target_receiver}
#     Base inspiration: {base_push_example}
#     What's trending: {local_trend_in_malaysia}
#     Extra spice needed: {additional_requirements}

#     Serve it up in this JSON format (numbers = push notification order):
#     {{
#     "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     ...
#     }}

#     JSON only - no extra text or comments!""",
    
#     input_variables=[
#         "type_of_push_notification",
#         "number_of_push_notifications",
#         "name_of_series",
#         "retrieved_wiki_of_series",
#         "series_content",
#         "series_description",
#         "name_of_cast",
#         "nickname_of_cast",
#         "quote_of_cast",
#         "interesting_fact_of_cast",
#         "character_in_series_acted_by_cast",
#         "demographics_of_target_receiver",
#         "base_push_example",
#         "local_trend_in_malaysia",
#         "include_emoji",
#         "include_slangs",
#         "additional_requirements",
#     ],
# )


final_prompt = FewShotPromptTemplate(
    examples = examples,
    example_prompt = example_prompt,
    suffix = """
    Yo! Write {number_of_push_notifications} catchy {type_of_push_notification} push notifications for "{name_of_series}" on Viu!
    
    Think like you're texting your bestie about the most OMG moments! Keep it casual and fun!
    
    What you gotta do:
    - Write in English + Bahasa Melayu
    - Drop some attention-grabbing hooks (cast stuff, drama tea, trending topics, whatever's hot!)
    - Make it super clickable but don't try too hard
    - Put the good stuff first (cast + series name in first 50 chars)
    - Keep it short and sweet, but spill more tea if you got it
    - Add hashtags at the end (just 2-3 is enough!)
    - The pushes need to be in 100 characters or less
    
    Quick rules:
    - Talking about {name_of_cast}? Make sure to mention them!
    - Young audience? Keep it fun and casual! ("gotta", "WOW", "OMG" etc.), Use multiple question marks and exclamation marks at a once (eg. !!!, ???, ..., etc.) to show excitement
    - Fan crowd? Spill some behind-the-scenes tea!
    - Got a Malaysian trend? Drop it in naturally!
    - Slang it up in BM if {include_slangs} is True
    - Chuck in some emojis if {include_emoji} is True (but don't overdo it!)
    - If "base_push_example" is provided, must improve and regenerate all the pushes based on the "base_push_example"!
    - If "local_trend_in_malaysia" is provided, the trend must be incoporated into the pushes with any method!
    - If "additional_requirements" are given, make sure you follow them and apply on all pushes!

    Use what you want from this info:
    - Show name: {name_of_series}
    - Wiki stuff: {retrieved_wiki_of_series}
    - What's it about: {series_content}
    - Show details: {series_description}
    - Star: {name_of_cast}
    - Cast type: {type_of_cast}
    - Nickname: {nickname_of_cast}
    - Cool quotes: {quote_of_cast}
    - Fun facts: {interesting_fact_of_cast}
    - Their character: {character_in_series_acted_by_cast}

    Tips!!!:
    - Use first person or third person
    - Use the actor's perspective to speak to audiences if cast-driven, use in 1 or 2 push
    - Act as a friend sharing exciting news
    - Simplified the structure to be more like casual messaging
    - Formal marketing language
    - Reduce the complexity, simpler writing
    - Remove formal writing cues
    - Use multiple question marks and exclamation marks at a once (eg. !!!, ???, ..., etc.) to show excitement
    - Use casual tone ("gotta", "WOW", "OMG" etc.) but not go too far
    - Mention "Viu"!!!
    
    Who we're talking to: {demographics_of_target_receiver}
    Example to level up: {base_push_example}
    What's trending: {local_trend_in_malaysia}
    Extra stuff needed: {additional_requirements}

    Stick to this JSON format (no other text!):
    {{
    "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
    "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
    ...
    }}""",
    
    input_variables=[
        "type_of_push_notification",
        "number_of_push_notifications",
        "name_of_series",
        "retrieved_wiki_of_series",
        "series_content",
        "series_description",
        "name_of_cast",
        "nickname_of_cast",
        "quote_of_cast",
        "interesting_fact_of_cast",
        "character_in_series_acted_by_cast",
        "demographics_of_target_receiver",
        "base_push_example",
        "local_trend_in_malaysia",
        "include_emoji",
        "include_slangs",
        "additional_requirements",
    ],
)