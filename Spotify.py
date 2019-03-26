import argparse
import pprint
import sys
import os
import subprocess
import json
import spotipy
import spotipy.util as util
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

client_id= "c3bbdacb4cbd494bb06a9f1a0f8000e3"
client_secret= "8ddbddaf415b437a91367a53132c870f"
redirect_uri='https://www.google.com/'
username='Marcos Fabricio'
playlist = '6vl3AzV6Eh7jd23nzKCM47'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
scope = 'user-library-read playlist-read-private'

# try:
#     token = util.prompt_for_user_token(username, scope,client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
#     sp=spotipy.Spotify(auth= token)

# except:
#     print('Token is not accesible for ' + username)

#client_credentials_manager = SpotifyClientCredentials()

def get_playlist_content(username, playlist_id, sp):
    offset = 0
    songs = []
    while True:
        content = sp.user_playlist_tracks(username, playlist_id, fields=None,
        limit=10000, offset=offset, market=None)
        print(content)
        songs += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break
    with open('{}-{}'.format(username, playlist_id), 'w') as outfile:
        json.dump(songs, outfile)

def get_playlist_audio_features(username, playlist_id, sp):
    offset = 0
    songs = []
    items = []
    ids = []
    
    while True:
        content = sp.user_playlist_tracks(username, playlist_id, fields=None, limit=100, offset=offset, market=None)
        songs += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break
    for i in songs:
        ids.append(i['track']['id'])
        index = 0
        audio_features = []
    while index < len(ids):
        audio_features += sp.audio_features(ids[index:index + 50])
        index += 50

    features_list = []
    
    for features in audio_features:
        features_list.append([features['energy'], features['liveness'],
        features['tempo'], features['speechiness'],
        features['acousticness'], features['instrumentalness'],
        features['time_signature'], features['danceability'],
        features['key'], features['duration_ms'],
        features['loudness'], features['valence'],
        features['mode'], features['type'],
        features['uri']])
        df = pd.DataFrame(features_list, columns=['energy', 'liveness',
        'tempo', 'speechiness',
        'acousticness', 'instrumentalness',
        'time_signature', 'danceability',
        'key', 'duration_ms', 'loudness',
        'valence', 'mode', 'type', 'uri'])
        df.to_csv('{}-{}.csv'.format(username, playlist_id), index=False)

def get_user_playlist(username, sp):
    playlists = sp.user_playlists(username)
    
    for playlist in playlists['items']:
        print("Name: {}, Number of songs: {}, Playlist ID: {} ".
        format(playlist['name'].encode('utf8'),
        playlist['tracks']['total'],
        playlist['id']))
