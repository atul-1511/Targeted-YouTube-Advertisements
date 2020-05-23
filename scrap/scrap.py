# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:29:21 2019

@author: visanand
"""
#importing important libraries
import pandas as pd
from apiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from apiclient.errors import HttpError
import requests, sys, time, os, argparse


#developer key for youtube API
DEVELOPER_KEY = 'AIzaSyBr5s02qg_sbnDZkOAKnWfD4ipDOlBqpw8'

#giving instructions to youtube to fetch the data from the youtube api
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

#reading the video ids containg the list of video ids only. cahan
video_index=pd.read_csv(r"C:\Users\visanand\Desktop\ML\Scrap\video_ids.csv")

#creating an empty dataframe containing the features to be extracted
df = pd.DataFrame(columns=['ids','title','channelTitle','tags','viewCount','likeCount','dislikeCount','commentCount','description','thumbnails' ,'transcript','categoryId'])

# Any characters to exclude, generally these are things that become problematic in CSV files
unsafe_characters = ['\n', '"']

#preparing features- which removes the unwanted character from the text passed
def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'{feature}'

#tages are processed 
def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature(" | ".join(tags_list))

#this loop runs video_id number of time. change the range based on requiorememt
for index, rows in video_index[50:60].iterrows():
   # try:
        ids = video_index.iloc[index,0]
        print( index, ids)
        
        #ids='K4wEI5zhHB0'
        #extracting the stats and results data from youtube api.
        results = youtube.videos().list(id=ids, part='snippet').execute()
        stats = youtube.videos().list(id=ids, part='statistics').execute()
        
        if(results['items']!=[]):
            for result in results.get('items', []):
                
                #getting the features from the api extracted data
                video_id= prepare_feature(result['id'])
                
                title= prepare_feature(result['snippet']['title'])
                
                description=prepare_feature(result['snippet']['description'])
                
                channelTitle=prepare_feature(result['snippet']['channelTitle'])
                
                category_id=prepare_feature(result['snippet']['categoryId'])
                
                #checking for error in the tags. some of the videos dont have the tags
                try:
                    
                    tags = get_tags(result['snippet'].get("tags", ["[none]"]))

                except:
                    tags=''
                    
                thumbnails=prepare_feature(result['snippet']['thumbnails']['default']['url'])
                
                viewCount=stats['items'][0]['statistics']['viewCount']
                
                likeCount=stats['items'][0]['statistics']['likeCount']
                
                dislikeCount=stats['items'][0]['statistics']['dislikeCount']
                
                commentCount=stats['items'][0]['statistics']['commentCount']
                
                #getting the annotations from the api
                try:
                    annotations=YouTubeTranscriptApi.get_transcript(rows[0],languages=['en'])
                    
                    trans=""
                    
                    for i in annotations:
                        
                        trans+=i['text']+" "
                except:
                    trans=""
                    
                #combining all the extracted data from the api to a dataframme    
                df.loc[index]=[video_id,title,channelTitle,tags,viewCount,likeCount,dislikeCount,commentCount,description,thumbnails,trans,category_id]
                
      #  except:
                df.loc[index]=[video_id,title,channelTitle,tags,viewCount,likeCount,dislikeCount,commentCount,description,thumbnails,trans,category_id,]
        else:
            #if the video is not availaible then make the whole row related to the dataframe blank
            df.loc[index]=[ids,"","","","","","","","","","",""]
     

df.to_csv("youtube_data.csv")
    
print('--------"DONE"----------')