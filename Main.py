import spotipy
import spotipy.util as util
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import  BytesIO

# Spotify authorization variables
username = 'jorg.eikens'
scope = 'user-read-currently-playing user-read-playback-state user-top-read'
client_id = 'c9db738e9e0847ea8c7bc6acf166f29d'
client_secret = '09dccb48fc624b04af58d16a48ae8d6d'
redirect_uri = 'http://localhost/'

def showPIL(pilImage):
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')

    imgWidth, imgHeight = pilImage.size

    ratio = min(w/imgWidth, h/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)

    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()

def getImage():
    token = util.prompt_for_user_token(username, scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)
    if token:
        sp = spotipy.Spotify(auth = token)
        results = sp.current_playback()

        if results:

            if results['currently_playing_type'] == 'track' and results['item']['is_local'] == False:
                url640 = results['item']['album']['images'][0]['url']
                response = requests.get(url640)
                img = Image.open(BytesIO(response.content))
                print(url640)

        if results == None:
            print("Not playing any track")

    else:
        print("Can't get token for ", username)
        return None

def main():
    getImage()

if __name__ == '__main__':
    main()
