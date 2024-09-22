import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
youtube = build(serviceName="youtube", version="v3", developerKey=os.environ["YOUTUBE_API_KEY"])

def get_channel_id(channel_url: str) -> str:
    """
    Retrieves and returns the channel ID from a the specified YouTube channel URL.
    """
    channel_username = channel_url.split("/")[3]
    response = youtube.channels().list(part="snippet", forHandle=channel_username).execute()
    channel_id = response["items"][0]["id"]

    return channel_id

def get_uploads_playlist_id(channel_id: str) -> str:
    """
    Retrieves the playlist ID for recently uploaded videos from the specified YouTube channel.
    """
    response = youtube.channels().list(part="contentDetails", id=channel_id).execute()
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    return uploads_playlist_id

def get_playlist_items(playlist_id: str) -> list[str]:
    """
    Retrieves and returns the titles of videos from a specified YouTube playlist.
    """
    response = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=50).execute()
    videos_list = []
    for x in response["items"]:
        temp = x["snippet"]["title"]
        videos_list.append(temp)
        
    return videos_list

def iterate_channel_sections(channel_id: str) -> list[str]:
    """
    Retrieves and returns a list of playlist IDs from the specified YouTube channel"s homepage.
    """
    response = youtube.channelSections().list(part="contentDetails", channelId=channel_id).execute()
    playlist_id_list = []
    for x in response["items"]:
        try:
            playlist_id_list.extend(x["contentDetails"]["playlists"])
        except:
            continue
        
    return playlist_id_list

def summarize_playlist_contents(playlist_id: str) -> str:
    """
    Summarizes the contents of a playlist using Gemini AI.
    """
    video_titles = get_playlist_items(playlist_id)
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config={"temperature": 0})

    response = model.generate_content(
        f"Here is the uploads playlist from a YouTube channel: '{video_titles}'\n"
        f"Summerize the contents of this channel concisely.\n"
        )
    playlist_summary = response._result.candidates[0].content.parts[0].text
    
    return playlist_summary

def summarize_channel_contents(channel_url):
    """
    Summarizes the contents of a channel using Gemini AI.
    """
    channel_id = get_channel_id(channel_url)
    uploads_playlist_id = get_uploads_playlist_id(channel_id)
    channel_summary = summarize_playlist_contents(uploads_playlist_id) 
    
    return channel_summary
