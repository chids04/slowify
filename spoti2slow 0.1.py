import requests
import spotipy
import urllib.request
import re
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
import os
import urllib.parse as urlparse
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


#get spotify playlist url
#get song name + artist name in a dict
#search up for song name + artist name + slowed and reverb on youtube
#add video id of first result of each song to a list
#add ids of the videos to a youtube playlist
#add option to download playlist using youtube-dl (not done yet)


class Slowed_Reverb_Playlist:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tracks = []
        self.vidID = []

    def spotiSongList(self, url):
        auth_manager = SpotifyClientCredentials(client_id = self.client_id, client_secret = self.client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        results = sp.playlist_tracks(url)
        
        for item in results["items"]:
            trackName = item["track"]["name"] + " - " + item["track"]["artists"][0]["name"] + " - " + "Slowed and Reverbed"
            self.tracks.append(trackName)
        
        
        results = sp.playlist_tracks(url)
        trackLen = results["total"]

        iterAmount = trackLen // 100

        print(iterAmount)

        if trackLen > 100:
            offset = 0
            for i in range(0, iterAmount):
                offset = offset + 100
                results = sp.playlist_tracks(url, offset = offset)
                for item in results["items"]:
                    trackName = item["track"]["name"] + " - " + item["track"]["artists"][0]["name"] + " - " + "Slowed and Reverbed"
                    self.tracks.append(trackName)
        else:
            pass
            
        


    def genVideoID(self):
        for song in self.tracks:
            results = YoutubeSearch(song, max_results = 10).to_dict()
            reqs = ["Slowed", "slowed", "reverb", 'Reverb', "reverbed", "Reverbed"]

            for v in results:
                if any(x in v['title'] for x in reqs):
                    self.vidID.append(v['id'])
                    break

        print(self.vidID)

    def addToPlaylist(self,playlist):
        scopes = ["https://www.googleapis.com/auth/youtube"] #make sure app on google dev console has this scope in oauth

        
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json" #make sure client secret json oauth from app from credentials dashboard in google dev console is in same dir as this py file

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
        parsed = urlparse.urlparse(playlist)
        id = urlparse.parse_qs(parsed.query)["list"][0]

        for item in self.vidID:
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                "snippet": {
                    "playlistId": id, #an actual playlistid
                    "position": 0,
                    "resourceId": {
                    "kind": "youtube#video",
                    "videoId": item #an actual videoid
                    }
                }
                }
            )
            response = request.execute()

            print(f"\n{response}")

        


client_id = "client id" #client id from google dev console
client_secret = "client secret" #client secret from google dev console

s = Slowed_Reverb_Playlist(client_id, client_secret)
s.spotiSongList("https://open.spotify.com/playlist/4jdbUv9lhpKFrKnpg8taYV?si=efe5b1d9db7e4970")
s.genVideoID()
s.addToPlaylist("https://www.youtube.com/playlist?list=PLCzh8USRFJndSgrbXN32xJqrzF2HVETNb")

