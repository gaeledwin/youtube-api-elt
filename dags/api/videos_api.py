import requests
from datetime import date
import os
import json
from dotenv import load_dotenv
from airflow.decorators import task
from airflow.models import Variable

api_key = Variable.get('API_KEY')
max_results = 50
channel_handle = Variable.get('CHANNEL_HANDLE')

@task
def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        item = data.get('items', [])
        playlist_id = item[0]['contentDetails']['relatedPlaylists']['uploads']
        return playlist_id
    except requests.exceptions.RequestException as e:
        raise e

@task
def get_videos_ids(playlist_id):
    videos_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={api_key}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}" 
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                videos_ids.append(video_id)
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        return videos_ids
    except requests.exceptions.RequestException as e:
        raise e

@task
def extract_data_videos(videos_ids):
    videos_data = []
    try:
        for i in range(0, len(videos_ids), max_results):
            batch = videos_ids[i:i + max_results]
            ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={ids_str}&key={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
                
                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('commentCount', None)
                }
                
                videos_data.append(video_data)
        return videos_data
    except requests.exceptions.RequestException as e:
        raise e
  
@task  
def save_to_json(extracted_data):
    file_path = f'./data/youtube_data_{date.today()}.json'
    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)
        