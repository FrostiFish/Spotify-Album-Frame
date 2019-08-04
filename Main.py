import spotipy
import spotipy.util as util
import urllib.request
import os
import shutil
import time
import sched
from subprocess import check_output

path = os.getcwd()

schedule = sched.scheduler(time.time, time.sleep)

fehUpdated = False
userPlayingTrack = False
lastUserPlayingTrack = False

def get_pid(name):
    return int(check_output(["pidof", name]))

def launchFEH(fehpath):
    os.system("feh -x -F -D10 " + fehpath + " &")

def killFEH():
    os.system("kill -9 " + get_pid("feh"))

def checkFEHUpdate():
    global userPlayingTrack
    global lastUserPlayingTrack

    if userPlayingTrack != lastUserPlayingTrack:
        fehUpdated = False
    schedule.enter(1, 2, checkFEHUpdate)

def updateFEH():
    global fehUpdated

    if userPlayingTrack and not fehUpdated:
        killFEH()
        print("Killed FEH")
        launchFEH(path + "/currentplayback.jpg/")
        print("Launched FEH")

        fehUpdated = True

    elif not userPlayingTrack and not fehUpdated:
        killFEH()
        print("Killed FEH")
        launchFEH(path + "/topTracks/")
        print("Launched FEH")

        fehUpdated = True

    schedule.enter(1, 3, updateFEH)

# Spotify authorization variables
username = 'jorg.eikens'
scope = 'user-read-currently-playing user-read-playback-state user-top-read'
client_id = 'c9db738e9e0847ea8c7bc6acf166f29d'
client_secret = '09dccb48fc624b04af58d16a48ae8d6d'
redirect_uri = 'http://localhost/'

limit = 10
lastCurrentPlaybackID = None
lastTopTracks = [None] * limit

dirName = "./topTracks/"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:
    print("Directory " , dirName ,  " already exists")


def updateImages():
    token = util.prompt_for_user_token(username, scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)
    if token:
        sp = spotipy.Spotify(auth = token)
        results = sp.current_playback()
        global lastCurrentPlaybackID
        global lastTopTracks

        if results:
            print("User is playing a track")
            userPlayingTrack = True

            if results['currently_playing_type'] == 'track' and results['item']['id'] != lastCurrentPlaybackID and results['item']['is_local'] == False:
                url640 = results['item']['album']['images'][0]['url']
                lastCurrentPlaybackID = results['item']['id']

                imageCurrentPlayback = open("./currentplayback.jpg", 'wb')
                imageCurrentPlayback.write(urllib.request.urlopen(url640).read())
                imageCurrentPlayback.close()

                print("User changed track")
                print(path + "/currentplayback.jpg updated")

        if results == None:
            print("User is not playing any track")
            userPlayingTrack = False

            results = sp.current_user_top_tracks(limit = limit, offset = 0, time_range='short_term')

            topTracksChanged = False

            for index in range(limit):
                if results['items'][index]['id'] != lastTopTracks[index]:
                    topTracksChanged = True

            if topTracksChanged:
                for index in range(limit):
                    url640 = results['items'][index]['album']['images'][0]['url']
                    lastTopTracks[index] = results['items'][index]['id']

                    imageTopTracks = open("./topTracks/" + str(index) + ".jpg", 'wb')
                    imageTopTracks.write(urllib.request.urlopen(url640).read())
                    imageTopTracks.close()

                    print(path + "/topTracks/" + str(index) + ".jpg updated")

    else:
        print("Can't get token for ", username)
        return None

    schedule.enter(1, 1, updateImages)

def main():
    schedule.absenter(0, 1, updateImages)
    schedule.enterabs(0, 2, launchFEH, kwargs = {'fehpath' : (path + "/currentplayback.jpg/")})
    schedule.enterabs(0, 3, checkFEHUpdate)
    schedule.enterabs(0, 4, updateFEH)
    schedule.run()

if __name__ == '__main__':
    main()
