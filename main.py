import random
from PIL import Image, ImageDraw
import json
from wordfreq import word_frequency
import tweepy
import time

#add the whole automated thing

#basically makes a list of RGB values that are kinda different enough to not have jus identical flags
def get_colors():
    #these colors are ones that are already absolutely anarchy flags
    bad_colors = [[0, 0, 0], [255, 255, 255], [255, 0, 0], [0, 153, 0], [140, 0, 148], [255, 102, 0], [254, 68, 255]]
    rgb = []
    i = 0
    #jus keep on addin until finiding a new RGB value is too hard
    while i != len(bad_colors):
        i = len(bad_colors)
        for p in range(10):
            listo = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            found = False
            for q in bad_colors:
                if (abs(listo[0] - q[0]) < 25) and (abs(listo[1] - q[1]) < 25) and (abs(listo[2] - q[2]) < 25):
                    found = True
            if found == False:
                rgb.append(listo)
                bad_colors.append(listo)
    #now we got our json
    with open('colors.json', 'w') as f:
        json.dump(rgb, f)

#the actual function called
def make_flag(words, colors):
    limit = 0
    while len(words) > 0 and len(colors) > 0 and limit < 3:
        color = colors[random.randint(0, len(colors)-1)]
        word = random.choice(words)
        anarcho = "the flag for anarcho-" + word + "."
        print(anarcho + ": " + str(color))
    print("all done!")

        #make a flag image
        flag = Image.new("RGB", (1875, 1250))
        draw = ImageDraw.Draw(flag)
        rect = draw.rectangle([0, 0, 1875, 1250],fill=(color[0], color[1], color[2]))
        tri = draw.polygon([0, 1250, 1875, 0, 1875, 1250], fill=(0, 0, 0))
        flag.save("flag.png")

        #set-up into the twitter bot
        keys = get_keys("../anarchy_keys.txt")
        auth = tweepy.OAuthHandler(keys[0], keys[1])
        auth.set_access_token(keys[2], keys[3])
        api = tweepy.API(auth)

        #and then, at last, we tweet.
        api.update_with_media("flag.png", status=anarcho)

        #so the actual looping works, remove from the lists and wait for a hot min (4 hours to be exact)
        words.remove(word)
        colors.remove(color)
        time.sleep(14400)



#just so i can upload this code publically lmao
def get_keys(filename):
    keys = []
    with open(filename) as f:
        for line in f:
            keys.append(line.rstrip())
    return keys

#take the random list of words i got online and assign it a popularity score
def filter_raw():
    with open("words_raw.json", "r") as f:
        words = json.load(f)
    freq = {}
    for i in words:
        freq[i] = word_frequency(i, 'en')
    with open('words_filtered.json', 'w') as f:
        json.dump(freq, f)

#get only the words people actual have kinda heard of
#think i used something in the range of 5e-8? i forgot tbh
def get_popular(freq):
    with open("words_filtered.json", "r") as f:
        words = json.load(f)
    popular = []
    #just so we don't accidentally get something that actually exists lmao
    bad_words = ["communism", "capitalism", "socialism", "feminism", "pacifism", "primitivism", "mutualism", "egoism", "leftism", "fascism"]
    for i in words.keys():
        if words[i] > freq and i not in bad_words:
            popular.append(i)
    print(len(popular))
    with open('words.json', 'w') as f:
        json.dump(popular, f)


#this is so i can just write main.py in the console (for now!).
def main():
    #get all the needed colors/words ready
    with open("words.json", "r") as f:
        words = json.load(f)

    with open("colors.json", "r") as f:
        colors = json.load(f)

    make_flag(words, colors)

if __name__ == "__main__":
    main()
