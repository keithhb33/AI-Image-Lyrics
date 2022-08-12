import subprocess
import sys

modules_list = ["wave", "flask", "lyricsgenius"]

for module in modules_list:
    subprocess.call([sys.executable, "-m", "pip", "install", module])


from cgitb import text
import requests
import sys
import os
import string

import wave
import contextlib
import lyricsgenius as lg
from lyricsgenius import Genius

import os.path
import json
import random
from numpy import *
from os import path

import speech_recognition as sr 
import os 

import json
from flask import request
from flask import Flask, render_template, redirect
import jyserver.Flask as jsf


print("MAKE SURE YOU'RE IN THE .py FILES' DIRECTORY")





app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "/home/keith/VSCode/AIMusicVideos/static/outputs"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]

def allowed_image(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
        



counter = 0
exported_img = []
exported_lyric = []

def image(prompt):
    global counter
    counter +=1
    
    url = "https://backend.craiyon.com/generate"
    
    s = requests.Session()
    payload = {
        "prompt": prompt   
    }
    
    res = s.post(url, json=payload)
    return res.content

def audio_duration():
    fname = 'song_files/song.wav'
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration



def convert_jpg(prompt):
    global name
    global lyric
    
    try:
        image_urls = str(image(prompt))
        image_urls = image_urls.replace('\\\\n', '')

        print("IMAGE URLS: " + image_urls)

        end_index = int(image_urls.index('],"version') - 1)
        
        image_urls = image_urls[14:end_index]
        image_list = image_urls.split('","')
            
        chosen_image = image_list[random.randint(0,8)]

        exported_img.append(chosen_image)
        exported_lyric.append(prompt)
        
        lyric = exported_lyric
        name = exported_img
        

        print("Writing...\n")
    except:
        pass
    #send filename to javascript
    #upload_image(file_name)
            
            
            

def separate_prompts(transcript, transcript_list, word_group):
    for j in range(len(transcript)):
        transcript_list.append(transcript[j])
        if '\\' in transcript_list and 'n' in transcript_list: 
            word_group = ' '.join([str(elem) for elem in transcript_list])
            word_group = word_group.replace('[', '')
            word_group = word_group.replace('\ n', '')
            word_group = str(word_group)
            word_group = word_group.split(" ")
            final_word = ""
            remove_indices = []
            transcript_list = []
            
            
            for n in range(len(word_group)):
                if word_group[n] == '':
                    word_group[n] = ' '
                
                if word_group[n] == ' ' and (n % 2 == 0):
                    remove_indices.append(n)
            
            for m in range(len(remove_indices)):
                remove_index = remove_indices[m]
                word_group.pop(remove_index)
                #subtract the values of all values in remove_indices
                for b in range(len(remove_indices)):
                    remove_indices[b] -= 1
            word_group.pop(0)
            
            if "\\" in word_group:
                word_group.remove('\\')
    
            while word_group[-1] == '"':
                word_group.pop()

            try:
                while (word_group[0] == " " or word_group[0] == "'" or word_group[0] == "," or word_group[0] == '"'):
                    word_group.pop(0)
            except:
                pass

            for i in range(len(word_group)):
                final_word += word_group[i]

            if "Lyrics" in final_word:
                index_split = int(final_word.find("Lyrics"))
                index_split += 6
                final_word = final_word[index_split:]
                


            if "[" in final_word or "]" in final_word or final_word == "" or final_word == " " or final_word == '",':
                pass
            else:
                print(final_word)
                convert_jpg(final_word)
            final_word = ""

        if j == len(transcript) - 1:
            with open('song_files/song.txt', 'r') as f:
                for line in f:
                    pass
                last_line = line
            
            #Take into account last line of text in song.txt file
            for l in range(len(last_line)):
                try:
                    if isinstance(int(last_line[l]), int):
                        num_index = l
                        for k in range(num_index):
                            final_word += last_line[k]
                        print(final_word)
                        convert_jpg(final_word)
                        break
                except:
                    pass

def create_images(artist_name, song_title):

    artist_name = string.capwords(artist_name)
    song_title = string.capwords(song_title)

    text_path = "song_files/song.txt"

    genius_api_key = "RUC-To73cg9fE2zHFayzD9_20QgQRp-K1NidWIt0e0PM89gtnbOtfNVda1o4Sx-7"
    genius = lg.Genius(genius_api_key)
    artist = genius.search_artist(artist_name, max_songs=0, sort="title")

    song = artist.song(song_title)
    final_lyrics = song.lyrics

    with open(text_path, 'w') as f:
        f.write(str(final_lyrics))
    
    with open(text_path) as f:
        lines = f.readlines()
    transcript = str(lines)

    transcript_list = []
    word_group = ""

    separate_prompts(transcript, transcript_list, word_group)
    #delete files after they have been sent to server

name = []
lyric = ""

@app.route('/')
def index():
    global name
    global lyric
    
    return render_template('index.html', name=name, lyric=lyric)

#base64 code is displayed but needs to be refreshed to show up on scree -- need to update page without having to refresh

@app.route('/backend', methods=['POST'])
def test():
    global name
    output = request.get_json()
    result = json.loads(output) #converts the json output to a python dictionary
    
    print("Artist: " + str(result["artistValue"]))
    print("Song: " + str(result["songValue"]))
    
    artist_value = str(result["artistValue"])
    song_value = str(result["songValue"])
    
    create_images(artist_value, song_value)
    return "success"

@app.route('/restart', methods=['POST'])
def restarting():
    os.execl(sys.executable, *([sys.executable]+sys.argv))

if __name__ == "__main__":
    app.run(debug=True)








#IN CONVERT_JPG METHOD, INSTEAD OF OUTPUTTING TO OUTPUT DIRECTORY, OUTPUT TO SCREEN
#ABOVE OUTPUTTED IMAGE, CHANGE EACH LABEL TO MATCH THE PICTURE'S TRANSCRIPT
#START WITH PLACING EACH OF THE IMAGES ON THE SCREEN FIRST
