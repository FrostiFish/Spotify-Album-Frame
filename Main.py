import spotipy
import spotipy.util as util
import urllib.request
import os

# Spotify authorization variables
username = 'jorg.eikens'
scope = 'user-read-currently-playing user-read-playback-state user-top-read'
client_id = 'c9db738e9e0847ea8c7bc6acf166f29d'
client_secret = '09dccb48fc624b04af58d16a48ae8d6d'
redirect_uri = 'http://localhost/'

# Create target Directory if don't exist
dirName = "./currentPlayback/"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:
    print("Directory " , dirName ,  " already exists")

dirName = "./topTracks/"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:
    print("Directory " , dirName ,  " already exists")

def getImage():
    token = util.prompt_for_user_token(username, scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)
    if token:
        sp = spotipy.Spotify(auth = token)
        results = sp.current_playback()

        if results:

            if results['currently_playing_type'] == 'track' and results['item']['is_local'] == False:
                url640 = results['item']['album']['images'][0]['url']

                imageCurrentPlayback = open("./currentPlayback/currentplayback.jpg", 'wb')
                imageCurrentPlayback.write(urllib.request.urlopen(url640).read())
                imageCurrentPlayback.close()
                print("Image saved")

        if results == None:
            print("Not playing any track")

            limit = 10

            results = sp.current_user_top_tracks(limit = limit, offset = 0, time_range='short_term')

            for index in range(limit):

                print(results)

                url640 = results['items'][index]['album']['images'][0]['url']

                imageTopTracks = open("./topTracks/" + str(index) + ".jpg", 'wb')
                imageTopTracks.write(urllib.request.urlopen(url640).read())
                imageTopTracks.close()

                print("Top Track " + str(index) + " image saved")

    else:
        print("Can't get token for ", username)
        return None

def main():
    getImage()

if __name__ == '__main__':
    main()
