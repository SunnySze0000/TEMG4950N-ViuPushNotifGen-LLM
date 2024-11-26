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


final_prompt = FewShotPromptTemplate(
    examples = examples,
    example_prompt = example_prompt,
    suffix = """
    You're a social media expert working for Viu who's amazing at writing viral push notifications! 
    Create {number_of_push_notifications} super engaging {type_of_push_notification} push notifications for "{name_of_series}" on Viu.
    
    Think like a social media influencer - make it irresistible! We want people's thumbs to stop scrolling 🛑
    
    Key requirements:
    - Write in both English and Bahasa Melayu
    - Hook readers with cast info, juicy content, trending topics, quotes, or viral moments
    - Make it impossible NOT to click! (But keep it real)
    - Front-load the good stuff - cast name and series title in first 100 characters
    - Include title + body + call-to-action + hashtags
    - Feel free to make it longer if you've got more tea to spill ☕
    
    Here's your content goldmine (use what sparks joy):
    - Series name: {name_of_series}
    - Wiki intel: {retrieved_wiki_of_series}
    - Content deets: {series_content}
    - Series lowdown: {series_description}
    - Star power: {name_of_cast}
    - Cast type: {type_of_cast}
    - Nickname: {nickname_of_cast}
    - Quotable moments: {quote_of_cast}
    - Fun facts: {interesting_fact_of_cast}
    - Character: {character_in_series_acted_by_cast}
    
    Target audience age: {demographics_of_target_receiver}
    Base inspiration: {base_push_example}
    What's trending: {local_trend_in_malaysia}
    Extra spice needed: {additional_requirements}
    
    Pro tips:
    - If it's cast-driven, spotlight {name_of_cast}
    - For younger audiences: Keep it fresh and energetic
    - For die-hard fans: Deep dive into cast details and behind-the-scenes
    - If there's a base example, take it to the next level and generate new pushes base on the Base inspiration, narrow down the variation in each push.
    - If there's extra spice required, make sure every push fit the additional requirements
    - If there's a Malaysian trend, work that magic in in all {number_of_push_notifications} pushes
    - Slang it up in Bahasa Maleyu only if {include_slangs} is True
    - Throw in emojis only if {include_emoji} is True
    
    Audience-Specific Guidelines:

    TEENS (13-17):
    Tone: Ultra-casual, excited, FOMO-driven
    Language: "OMG!", "fr fr", "ngl", "slay", ...
    Symbols: (∩˃o˂∩)♡, (≧∇≦), (¬‿¬), !!!, ???, ...
    Content: Social moments, friendship drama, relatable scenes
    Hooks: Trends, viral moments, cast's social media
    Example: "Song Kang spilling tea on TikTok rn!!! 🫢 Catch his behind-the-scenes"
    BM Style: Heavy Manglish, trending slang

    YOUNG ADULTS (age 18-24):
    Tone: Trendy but mature, witty, relatable
    Language: Mix of professional and internet slang
    Content: Romance, life challenges, plot twists
    Hooks: Pop culture references, social issues, binge appeal
    Example: "That plot twist got us shook! 😱 New episode drops in 1 hour!"
    BM Style: Modern Malaysian expressions

    ADULTS (age 25-34):
    Tone: Smart casual, sophisticated humor
    Language: Professional with subtle wit
    Content: Character depth, plot complexity, quality
    Hooks: Critical acclaim, unique storylines, cast achievements
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
    Emojis: 😊🤗🤭👍🏻🙏🏻🌹💐🏵🥀🪷
    Content: Cultural values, historical accuracy
    Hooks: Classic elements, familiar actors, family bonds
    Example: "Revisit the golden age🪷🪷 of drama with veteran star [Name]😊😊"
    BM Style: Classical BM, traditional expressions
    
    Key Engagement Elements:
    Teens: Social proof, FOMO, trending elements
    Young Adults: Binge-worthy aspects, social relevance
    Adults: Quality markers, intelligent content
    Mature Adults: Family value, critical acclaim
    Senior Adults: Traditional appeal, cultural significance

    Serve it up in this JSON format (numbers = push notification order):
    {{
    "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
    "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
    ...
    }}

    JSON only - no extra text or comments!""",
    
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


# final_prompt = FewShotPromptTemplate(
#     examples = examples,
#     example_prompt = example_prompt,
#     suffix = """
#     Hey! Write {number_of_push_notifications} catchy {type_of_push_notification} push notifications for "{name_of_series}" on Viu!
    
#     First, identify the age group from {demographics_of_target_receiver} and use these guidelines:

#     Teen (13-17):
#     - Use trendy internet slang and abbreviations (iykyk, ngl, fr fr)
#     - Heavy emoji usage if {include_emoji} is True
#     - Reference trending TikTok sounds/memes
#     - Focus on relatable school/teen life situations
#     - Use "we" to create FOMO
#     - Emphasis on friendship and social aspects
#     - Use short-form content references (TikTok, Reels)
    
#     Young Adult (18-24):
#     - Mix of internet slang and proper language
#     - Moderate emoji usage if {include_emoji} is True
#     - Reference pop culture and current events
#     - Focus on romance, career, university life angles
#     - Appeal to independence and self-discovery
#     - Highlight binge-worthy aspects
#     - Reference social media trends
    
#     Adult (25-34):
#     - More sophisticated but still casual language
#     - Minimal emoji usage if {include_emoji} is True
#     - Reference nostalgia and life milestones
#     - Focus on plot complexity and production quality
#     - Appeal to escape from daily routine
#     - Highlight award nominations/critical acclaim
#     - Include work-life balance angles
    
#     Mature Adult (35-49):
#     - Professional yet approachable tone
#     - Very selective emoji usage if {include_emoji} is True
#     - Reference classic shows/movies from 90s-2000s
#     - Focus on storytelling and acting quality
#     - Appeal to family viewing experience
#     - Highlight director/producer credentials
#     - Include family-friendly content markers

#     Senior Adult (50-64):
#     - Clear, straightforward language
#     - Minimal to no emoji usage if {include_emoji} is True
#     - Reference classic entertainment from 70s-90s
#     - Focus on historical accuracy and authenticity
#     - Appeal to wisdom and life experience
#     - Highlight educational value
#     - Mention familiar actors from their era
#     - Include family bonding aspects

#     Elderly (65+):
#     - Simple, respectful language
#     - No emoji usage unless specifically requested
#     - Reference golden age of cinema/TV
#     - Focus on traditional storytelling
#     - Appeal to multigenerational viewing
#     - Highlight comfort and familiarity
#     - Use larger font-friendly characters
#     - Emphasize cultural preservation
#     - Include nostalgia elements from 50s-70s
#     - Mention health/wellness angles if relevant

#     Age-specific hooks:
#     Teens: FOMO, social status, friendship drama, viral trends
#     Young Adults: Romance, life challenges, career goals, social issues
#     Adults: Plot twists, character development, social commentary
#     Mature Adults: Production value, artistic merit, family themes
#     Senior Adults: Life wisdom, cultural values, historical connections
#     Elderly: Traditional values, family bonds, cultural heritage

#     Language Complexity Guide:
#     Teens: Simple + trendy slang
#     Young Adults: Casual + modern references
#     Adults: Balanced + professional
#     Mature Adults: Refined + thoughtful
#     Senior Adults: Clear + traditional
#     Elderly: Simple + respectful

#     Cultural Reference Guide:
#     Teens: TikTok, Instagram, current pop stars
#     Young Adults: Netflix shows, social media trends
#     Adults: 2000s-2010s pop culture, current events
#     Mature Adults: 90s-2000s references
#     Senior Adults: 70s-90s entertainment
#     Elderly: Classic cinema, traditional media

#     Malaysian Cultural Elements by Age:
#     Teens: Local TikTok trends, young Malaysian artists
#     Young Adults: Local influencers, modern Malaysian music
#     Adults: Malaysian pop culture, local celebrities
#     Mature Adults: Classic Malaysian shows/movies
#     Senior Adults: Traditional Malaysian media
#     Elderly: Classic P. Ramlee era, traditional arts

#     Think like you're texting your bestie about the most OMG moments! Keep it casual and fun!
    
#     What you gotta do:
#     - Write in English + Bahasa Melayu
#     - Drop some attention-grabbing hooks (cast stuff, drama tea, trending topics, whatever's hot!)
#     - Make it super clickable but don't try too hard
#     - Put the good stuff first (cast + series name in first 50 chars)
#     - Keep it short and sweet, but spill more tea if you got it
#     - The pushes need to be in 80 characters or less

#     Device Consideration:
#     Teens/Young Adults: Optimize for mobile view
#     Adults/Mature Adults: Mixed device optimization
#     Senior Adults/Elderly: Consider larger text compatibility
    
#     Quick rules:
#     - Talking about {name_of_cast}? Make sure to mention them!
#     - Young audience? Keep it fun and casual! ("gotta", "WOW", "OMG" etc.), Use multiple question marks and exclamation marks at a once (eg. !!!, ???, ..., etc.) to show excitement
#     - Fan crowd? Spill some behind-the-scenes tea!
#     - Got a Malaysian trend? Drop it in naturally!
#     - Slang it up in BM if {include_slangs} is True
#     - Chuck in some emojis if {include_emoji} is True (but don't overdo it!)
#     - If "base_push_example" is provided, must improve and regenerate all the pushes based on the "base_push_example"!
#     - If "local_trend_in_malaysia" is provided, the trend must be incoporated into the pushes with any method!
#     - If "additional_requirements" are given, make sure you follow them and apply on all pushes!

#     Use what you want from this info:
#     - Show name: {name_of_series}
#     - Wiki stuff: {retrieved_wiki_of_series}
#     - What's it about: {series_content}
#     - Show details: {series_description}
#     - Star: {name_of_cast}
#     - Cast type: {type_of_cast}
#     - Nickname: {nickname_of_cast}
#     - Cool quotes: {quote_of_cast}
#     - Fun facts: {interesting_fact_of_cast}
#     - Their character: {character_in_series_acted_by_cast}

#     Tips!!!:
#     - Use first person or third person
#     - Use the actor's perspective to speak to audiences if cast-driven, use in 1 or 2 push
#     - Act as a friend sharing exciting news
#     - Simplified the structure to be more like casual messaging
#     - Formal marketing language
#     - Reduce the complexity, simpler writing
#     - Remove formal writing cues
#     - Use multiple question marks and exclamation marks at a once (eg. !!!, ???, ..., etc.) to show excitement
#     - Use casual tone ("gotta", "WOW", "OMG" etc.) but not go too far
#     - Mention "Viu"!!!
    
#     Who we're talking to: {demographics_of_target_receiver}
#     Example to level up: {base_push_example}
#     What's trending: {local_trend_in_malaysia}
#     Extra stuff needed: {additional_requirements}

#     Stick to this JSON format (no other text!):
#     {{
#     "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     ...
#     }}""",
    
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
#     Generate {number_of_push_notifications} {type_of_push_notification} push notifications for "{name_of_series}" on Viu.
#     Target audience: {demographics_of_target_receiver}

#     Content Details:
#     - Series: {name_of_series}
#     - Cast: {name_of_cast}
#     - Character: {character_in_series_acted_by_cast}
#     - Description: {series_description}
#     - Wiki stuff: {retrieved_wiki_of_series}
#     - What's it about: {series_content}
#     - Nickname: {nickname_of_cast}
#     - Cool quotes: {quote_of_cast}
#     - Fun facts: {interesting_fact_of_cast}

#     Audience-Specific Guidelines:

#     TEENS (13-17):
#     Tone: Ultra-casual, excited, FOMO-driven
#     Language: "OMG!", "fr fr", "ngl", "slay", ...
#     Symbols: (∩˃o˂∩)♡, (≧∇≦), (¬‿¬), !!!, ???, ...
#     Content: Social moments, friendship drama, relatable scenes
#     Hooks: Trends, viral moments, cast's social media
#     Example: "Song Kang spilling tea on TikTok rn!!! 🫢 Catch his behind-the-scenes"
#     BM Style: Heavy Manglish, trending slang

#     YOUNG ADULTS (18-24):
#     Tone: Trendy but mature, witty, relatable
#     Language: Mix of professional and internet slang
#     Content: Romance, life challenges, plot twists
#     Hooks: Pop culture references, social issues, binge appeal
#     Example: "That plot twist got us shook! 😱 New episode drops in 1 hour!"
#     BM Style: Modern Malaysian expressions

#     ADULTS (25-34):
#     Tone: Smart casual, sophisticated humor
#     Language: Professional with subtle wit
#     Content: Character depth, plot complexity, quality
#     Hooks: Critical acclaim, unique storylines, cast achievements
#     Example: "Award-winning performance alert! Critics call it 'unmissable'"
#     BM Style: Standard BM with urban flair

#     MATURE ADULTS (35-49):
#     Tone: Refined, quality-focused
#     Language: Professional, clear, respectful
#     Content: Production value, artistic merit, family themes
#     Hooks: Director credentials, awards, family viewing
#     Example: "From acclaimed director Lee Jae-wook: A masterpiece of storytelling"
#     BM Style: Proper BM, occasional formal terms

#     SENIOR ADULTS (50+):
#     Tone: Traditional, respectful, clear
#     Language: Straightforward, no slang
#     Content: Cultural values, historical accuracy
#     Hooks: Classic elements, familiar actors, family bonds
#     Example: "Revisit the golden age of drama with veteran star [Name]"
#     BM Style: Classical BM, traditional expressions

#     Technical Requirements:
#     - Character limit: 80
#     - Include emojis: {include_emoji}
#     - Include Malaysian slang: {include_slangs}
#     - Must incorporate: {local_trend_in_malaysia}
#     - Base example to improve: {base_push_example}
#     - Additional requirements: {additional_requirements}
#     - Mention "Viu" naturally in context
#     - Not include any website links

#     Key Engagement Elements:
#     Teens: Social proof, FOMO, trending elements
#     Young Adults: Binge-worthy aspects, social relevance
#     Adults: Quality markers, intelligent content
#     Mature Adults: Family value, critical acclaim
#     Senior Adults: Traditional appeal, cultural significance

#     Stick to this JSON format (no other text!):
#     {{
#     "1": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     "2": {{"english": {{"title": "title", "body": "body"}}, "malay": {{"title": "title", "body": "body"}}}},
#     ...
#     }}""",
    
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