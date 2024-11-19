import os
import pandas as pd
import random

def excelToPandas(datasets):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    datasets_path = os.path.join(script_dir, datasets)
    
    content_meta_df = pd.read_excel(datasets_path + '/content_metadata.xlsx',
                                usecols=["EXTERNAL_SERIES_ID", "GROUP_SERIES_NAME", "MAIN_CASTS", "SUPPORTING_CASTS", "CAMEO_CASTS", "HOST", "VO_TALENT", "WIKI_EN_URL"],
                                engine='openpyxl')

    content_des_df = pd.read_excel(datasets_path + '/content_description_multilang_mapping.xlsx',
                               usecols=["EXTERNAL_SERIES_ID", "AREA_NME", "LANG_NME", "SRI_DES", "EPS_NO", "EPS_SYP", "EPS_DES"],
                               engine='openpyxl')
    
    return content_meta_df, content_des_df

def getSeriesEpisodeMatch(serie_database, episode_database, language):
    
    serie_extrernal_id = set(serie_database["EXTERNAL_SERIES_ID"])
    episode_extrernal_id = set(episode_database["EXTERNAL_SERIES_ID"])

    common_id = serie_extrernal_id.intersection(episode_extrernal_id)  
    
    #print(list(common_id))
    
    return list(common_id)  

def getMalayData(datasets):
    
    content_meta_df, content_des_df = excelToPandas(datasets)
    
    #Get the row from meta
    meta = content_meta_df
    
    #Get the row from description by area
    dess = content_des_df[(content_des_df['AREA_NME'] == 'Malaysia')]
    
    common_id = getSeriesEpisodeMatch(meta, dess, "Malaysia")
    
    filtered_meta = meta[meta['EXTERNAL_SERIES_ID'].isin(common_id)]
    
    filtered_meta.to_json('malay_meta.json', orient='records', lines=True)

    return filtered_meta

def getCastDrivenData(cast, series_name, datasets):
    content_meta_df, content_des_df = excelToPandas(datasets)
    #Get the row from meta by cast
    meta = content_meta_df[
        (content_meta_df['MAIN_CASTS'].str.contains(cast)) |
        (content_meta_df['SUPPORTING_CASTS'].str.contains(cast)) |
        (content_meta_df['CAMEO_CASTS'].str.contains(cast)) |
        (content_meta_df['HOST'].str.contains(cast)) |
        (content_meta_df['VO_TALENT'].str.contains(cast))
    ]
    print(meta)
    #Get the row from description by area
    dess = content_des_df[(content_des_df['AREA_NME'] == 'Malaysia')]
    common_id = getSeriesEpisodeMatch(meta, dess, "Malaysia")
    #selected series & episodes
    filtered_meta = meta[meta['EXTERNAL_SERIES_ID'].isin(common_id) & (meta['GROUP_SERIES_NAME'] == series_name)]
    #print(filtered_meta)
    selected_series_id = filtered_meta.iloc[0]['EXTERNAL_SERIES_ID']
    series = meta[meta["EXTERNAL_SERIES_ID"] == selected_series_id]
    episodes = dess[dess['EXTERNAL_SERIES_ID'] == selected_series_id]
    #print(series)
    #choose a random episode
    random_episode_idx = random.randint(0, len(episodes) - 1)

    #Group the data, ASSUME promote episode 1 in this case
    data = {
        "target_cast": cast,
        "target_cast_type": next((col for col in series.columns if series[col].str.contains(cast).any()), None),
        "series_idx": series.iloc[0]['EXTERNAL_SERIES_ID'],
        "series_name": series.iloc[0]['GROUP_SERIES_NAME'],
        "series_description": episodes.iloc[random_episode_idx]["SRI_DES"],
        "series_wiki_url": series.iloc[0]['WIKI_EN_URL'],
        "episode_idx": episodes.iloc[random_episode_idx]["EPS_NO"],
        "episode_name": episodes.iloc[random_episode_idx]["EPS_SYP"],
        "episode_description": episodes.iloc[random_episode_idx]["EPS_DES"],
    }
    
    print(data)
    
    return data


def getContentDrivenData(content, datasets):
        
        content_meta_df, content_des_df = excelToPandas(datasets)
        
        #Get the row from meta by cast
        meta = content_meta_df[(content_meta_df['GROUP_SERIES_NAME'] == content)]
        
        #Get the row from description by area
        dess = content_des_df[(content_des_df['AREA_NME'] == 'Malaysia')]
        
        common_id = getSeriesEpisodeMatch(meta, dess, "Malaysia")

        series = meta[(meta["EXTERNAL_SERIES_ID"] == common_id[0])]
        episodes = dess[(dess["EXTERNAL_SERIES_ID"] == common_id[0])]

        # Create Dataframe of episode descriptions
        df = pd.DataFrame(episodes, columns=["EPS_NO", "EPS_SYP", "EPS_DES"])
        df['EPISODES_DES'] = df.agg(lambda x: f"Episode: {x['EPS_NO']}; Episode Synopsis: {x['EPS_SYP']}; Episode Description: {x['EPS_DES']}", axis=1)

        data = {
            "target_content": content,
            "series_idx": series.iloc[0]['EXTERNAL_SERIES_ID'],
            "series_name": series.iloc[0]['GROUP_SERIES_NAME'],
            "series_description": episodes.iloc[0]["SRI_DES"],
            "series_wiki_url": series.iloc[0]['WIKI_EN_URL'],
            "episodes_description": " | ".join(df['EPISODES_DES'].tolist()),
        }

        print(data)

        return data
        


#getContentDrivenData("Anggun Mikayla", "Viu_datasets")