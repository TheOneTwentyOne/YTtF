import re, os, sys, json, mutagen, subprocess, time
import tkinter as tk
from tkinter import font, filedialog, ttk
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, error
from mutagen.easyid3 import EasyID3

mainframe = tk.Tk()
mainframe.geometry("800x450")
mainframe.resizable(False, False)
mainframe.title("YTPMP3U")
oneXone = ttk.Frame(mainframe, height=50, width=50, style='CustomFrame.TFrame');oneXone.grid(row=0, column=0)
style = ttk.Style()
style.configure('CustomFrame.TFrame', background='black', relief='solid', borderwidth=1)

oneXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame');oneXone.grid(row=0, column=0)
oneXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame');oneXtwo.grid(row=1, column=0)
oneXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame');oneXthree.grid(row=2, column=0)
oneXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame');oneXfour.grid(row=3, column=0)
oneXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame');oneXfive.grid(row=4, column=0)
oneXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame');oneXsix.grid(row=5, column=0)
oneXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame');oneXseven.grid(row=6, column=0)
oneXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); oneXeight.grid(row=7, column=0)
oneXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); oneXnine.grid(row=8, column=0)

twoXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXone.grid(row=0, column=1)
twoXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXtwo.grid(row=1, column=1)
twoXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXthree.grid(row=2, column=1)
twoXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXfour.grid(row=3, column=1)
twoXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXfive.grid(row=4, column=1)
twoXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXsix.grid(row=5, column=1)
twoXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXseven.grid(row=6, column=1)
twoXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXeight.grid(row=7, column=1)
twoXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twoXnine.grid(row=8, column=1)

threeXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXone.grid(row=0, column=2)
threeXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXtwo.grid(row=1, column=2)
threeXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXthree.grid(row=2, column=2)
threeXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXfour.grid(row=3, column=2)
threeXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXfive.grid(row=4, column=2)
threeXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXsix.grid(row=5, column=2)
threeXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXseven.grid(row=6, column=2)
threeXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXeight.grid(row=7, column=2)
threeXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); threeXnine.grid(row=8, column=2)

fourXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXone.grid(row=0, column=3)
fourXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXtwo.grid(row=1, column=3)
fourXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXthree.grid(row=2, column=3)
fourXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXfour.grid(row=3, column=3)
fourXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXfive.grid(row=4, column=3)
fourXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXsix.grid(row=5, column=3)
fourXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXseven.grid(row=6, column=3)
fourXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXeight.grid(row=7, column=3)
fourXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourXnine.grid(row=8, column=3)

fiveXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXone.grid(row=0, column=4)
fiveXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXtwo.grid(row=1, column=4)
fiveXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXthree.grid(row=2, column=4)
fiveXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXfour.grid(row=3, column=4)
fiveXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXfive.grid(row=4, column=4)
fiveXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXsix.grid(row=5, column=4)
fiveXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXseven.grid(row=6, column=4)
fiveXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXeight.grid(row=7, column=4)
fiveXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fiveXnine.grid(row=8, column=4)

sixXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXone.grid(row=0, column=5)
sixXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXtwo.grid(row=1, column=5)
sixXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXthree.grid(row=2, column=5)
sixXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXfour.grid(row=3, column=5)
sixXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXfive.grid(row=4, column=5)
sixXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXsix.grid(row=5, column=5)
sixXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXseven.grid(row=6, column=5)
sixXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXeight.grid(row=7, column=5)
sixXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixXnine.grid(row=8, column=5)

sevenXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXone.grid(row=0, column=6)
sevenXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXtwo.grid(row=1, column=6)
sevenXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXthree.grid(row=2, column=6)
sevenXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXfour.grid(row=3, column=6)
sevenXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXfive.grid(row=4, column=6)
sevenXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXsix.grid(row=5, column=6)
sevenXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXseven.grid(row=6, column=6)
sevenXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXeight.grid(row=7, column=6)
sevenXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sevenXnine.grid(row=8, column=6)

eightXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXone.grid(row=0, column=7)
eightXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXtwo.grid(row=1, column=7)
eightXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXthree.grid(row=2, column=7)
eightXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXfour.grid(row=3, column=7)
eightXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXfive.grid(row=4, column=7)
eightXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXsix.grid(row=5, column=7)
eightXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXseven.grid(row=6, column=7)
eightXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXeight.grid(row=7, column=7)
eightXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); eightXnine.grid(row=8, column=7)

nineXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXone.grid(row=0, column=8)
nineXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXtwo.grid(row=1, column=8)
nineXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXthree.grid(row=2, column=8)
nineXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXfour.grid(row=3, column=8)
nineXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXfive.grid(row=4, column=8)
nineXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXsix.grid(row=5, column=8)
nineXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXseven.grid(row=6, column=8)
nineXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXeight.grid(row=7, column=8)
nineXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); nineXnine.grid(row=8, column=8)

tenXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXone.grid(row=0, column=9)
tenXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXtwo.grid(row=1, column=9)
tenXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXthree.grid(row=2, column=9)
tenXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXfour.grid(row=3, column=9)
tenXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXfive.grid(row=4, column=9)
tenXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXsix.grid(row=5, column=9)
tenXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXseven.grid(row=6, column=9)
tenXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXeight.grid(row=7, column=9)
tenXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); tenXnine.grid(row=8, column=9)

elevenXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXone.grid(row=0, column=10)
elevenXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXtwo.grid(row=1, column=10)
elevenXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXthree.grid(row=2, column=10)
elevenXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXfour.grid(row=3, column=10)
elevenXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXfive.grid(row=4, column=10)
elevenXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXsix.grid(row=5, column=10)
elevenXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXseven.grid(row=6, column=10)
elevenXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXeight.grid(row=7, column=10)
elevenXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); elevenXnine.grid(row=8, column=10)

twelveXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXone.grid(row=0, column=11)
twelveXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXtwo.grid(row=1, column=11)
twelveXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXthree.grid(row=2, column=11)
twelveXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXfour.grid(row=3, column=11)
twelveXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXfive.grid(row=4, column=11)
twelveXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXsix.grid(row=5, column=11)
twelveXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXseven.grid(row=6, column=11)
twelveXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXeight.grid(row=7, column=11)
twelveXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); twelveXnine.grid(row=8, column=11)

thirteenXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXone.grid(row=0, column=12)
thirteenXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXtwo.grid(row=1, column=12)
thirteenXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXthree.grid(row=2, column=12)
thirteenXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXfour.grid(row=3, column=12)
thirteenXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXfive.grid(row=4, column=12)
thirteenXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXsix.grid(row=5, column=12)
thirteenXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXseven.grid(row=6, column=12)
thirteenXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXeight.grid(row=7, column=12)
thirteenXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); thirteenXnine.grid(row=8, column=12)

fourteenXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXone.grid(row=0, column=13)
fourteenXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXtwo.grid(row=1, column=13)
fourteenXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXthree.grid(row=2, column=13)
fourteenXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXfour.grid(row=3, column=13)
fourteenXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXfive.grid(row=4, column=13)
fourteenXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXsix.grid(row=5, column=13)
fourteenXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXseven.grid(row=6, column=13)
fourteenXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXeight.grid(row=7, column=13)
fourteenXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fourteenXnine.grid(row=8, column=13)

fifteenXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXone.grid(row=0, column=14)
fifteenXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXtwo.grid(row=1, column=14)
fifteenXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXthree.grid(row=2, column=14)
fifteenXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXfour.grid(row=3, column=14)
fifteenXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXfive.grid(row=4, column=14)
fifteenXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXsix.grid(row=5, column=14)
fifteenXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXseven.grid(row=6, column=14)
fifteenXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXeight.grid(row=7, column=14)
fifteenXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); fifteenXnine.grid(row=8, column=14)

sixteenXone = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXone.grid(row=0, column=15)
sixteenXtwo = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXtwo.grid(row=1, column=15)
sixteenXthree = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXthree.grid(row=2, column=15)
sixteenXfour = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXfour.grid(row=3, column=15)
sixteenXfive = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXfive.grid(row=4, column=15)
sixteenXsix = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXsix.grid(row=5, column=15)
sixteenXseven = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXseven.grid(row=6, column=15)
sixteenXeight = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXeight.grid(row=7, column=15)
sixteenXnine = ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame'); sixteenXnine.grid(row=8, column=15)

# Downloads all of the .mp4 and .mp3 files from the specified playlist
def downloadVideos(playlistUrl, outputDir):
    # Downloads the .mp4 and .mp3 files
    subprocess.call(["yt-dlp", "-f", "bestvideo[height<=500][ext=mp4]+bestaudio[ext=m4a]/best[height<=500][ext=mp4]/bestvideo[height<=500][ext=webm]+bestaudio[ext=webm]/best[height<=500][ext=webm]", "-o", outputDir + "%(title)s.%(ext)s", "--yes-playlist", playlistUrl])
    subprocess.call(["yt-dlp", "--extract-audio", "--audio-format", "mp3", "-P", outputDir, "-o", "%(title)s.%(ext)s", playlistUrl])


# Fetches the URLs from the playlist
def getPlaylistVideoUrls(playlistUrl):
    process = subprocess.Popen(["yt-dlp", "-j", "--flat-playlist", playlistUrl], stdout=subprocess.PIPE)
    output, error = process.communicate()
    urls = [json.loads(line)["url"] for line in output.splitlines()]
    return urls



# Downloads all of the descriptions from the videos.
def downloadVideoDescriptions(videoUrls, outputDir):
    print("downloadVideoDescriptions")
    descriptionDict = {}
    descriptionsFile = os.path.join(outputDir, 'descriptions.json')
    if os.path.exists(descriptionsFile):
        # read description data from file if exists
        with open(descriptionsFile, 'r') as f:
            descriptionDict = json.load(f)
    else:
        # download descriptions from youtube-dl for new videos
        for url in videoUrls:
            # get the video title
            process = subprocess.Popen(["yt-dlp", "--get-filename", "--output", "%(title)s", url], stdout=subprocess.PIPE)
            videoTitle, _ = process.communicate()
            videoTitle = videoTitle.decode("ISO-8859-1").strip()
            # create empty text file
            outputFilePath = os.path.join(outputDir, videoTitle + ".txt")
            with open(outputFilePath, "w") as f:
                pass
            if url in descriptionDict:
                # use description data from dictionary if exists
                videoDescription = descriptionDict[url]
            else:
                # download description data from youtube-dl for new video
                process = subprocess.Popen(["yt-dlp", "--get-description", url], stdout=subprocess.PIPE)
                videoDescription, _ = process.communicate()
                videoDescription = videoDescription.decode("ISO-8859-1")
                # store the description data in the dictionary
                descriptionDict[url] = videoDescription
            # write description to text file
            with open(outputFilePath, "w", encoding="ISO-8859-1") as f:
                f.write(videoDescription)
        # write the descriptions to file
        with open(descriptionsFile, 'w') as f:
            json.dump(descriptionDict, f)
    os.remove(os.path.join(outputDir, "descriptions.json"))


# take a snapshot of each video at the 1-second mark using ffmpeg
def takeAlbumArt(outputDir):
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp4") or filename.endswith(".webm"):
            input_file = os.path.join(outputDir, filename)
            output_file = os.path.join(outputDir, os.path.splitext(filename)[0] + ".png")
            subprocess.call(["ffmpeg", "-i", input_file, "-ss", "00:00:01", "-vframes", "1", "-q:v", "2", "-vf", "scale=500:-2,fps=1/15,format=rgba", output_file])


# Delete the MP4 file
def deleteMp4File(outputDir):
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp4"):
            mp4File = os.path.join(outputDir, filename)
            # Delete the mp4 file
            os.remove(mp4File)


# Adds artwork to mp3 files and delete the image files
def addArtworkToMp3Files(outputDir):
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp3"):
            mp3File = os.path.join(outputDir, filename)
            imageFile = os.path.join(outputDir, os.path.splitext(filename)[0] + ".png")
            # Adds artwork to mp3 file
            try:
                audio = mutagen.File(mp3File)
                with open(imageFile, "rb") as f:
                    artwork = f.read()
                # Specifies the MIME type of the album cover as "image/png"
                mime_type = 'image/png'
                if imageFile.lower().endswith('.jpg') or imageFile.lower().endswith('.jpeg'):
                    # Uses PIL to convert JPEG to PNG format
                    img = Image.open(imageFile).convert('RGBA')
                    pngFile = os.path.splitext(imageFile)[0] + '.png'
                    img.save(pngFile, 'PNG')
                    with open(pngFile, "rb") as f:
                        artwork = f.read()
                    mime_type = 'image/png'
                    # Deletes the .jpg or .jpeg file
                    os.remove(imageFile)
                audio.tags.add(APIC(mime=mime_type, type=3, desc=u'Cover', data=artwork))
                audio.save()
                print("Added artwork to", mp3File)
            except Exception as e:
                print(f"Could not add artwork to {mp3File}. Error: {str(e)}")
            # Deletes the .png file
            if imageFile.lower().endswith('.png'):
                os.remove(imageFile)


# Replaces "#" with "." for any of the files in the directory.
def replaceHashtagSymbol(outputDir):
    for filename in os.listdir(outputDir):
        if "#" in filename:
            newFilename = filename.replace("#", ".")
            os.rename(os.path.join(outputDir, filename), os.path.join(outputDir, newFilename))


# Deletes all illegal characters from the .txt and .mp3 files in the output folder.
def deleteIllegalChars(outputDir):
    illegalChars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for filename in os.listdir(outputDir):
        if filename.endswith('.mp3') or filename.endswith('.txt'):
            newFilename = filename.translate({ord(char): None for char in illegalChars})
            newFilename = newFilename.replace('⧸', '').replace('／', '').replace('∕', '')
            newFilename = newFilename.replace('⧵', '').replace('∖', '').replace('＼', '')
            newFilename = newFilename.replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '')
            newFilename = newFilename.replace('＊', '').replace('⁎', '').replace('∗', '')
            newFilename = newFilename.replace('？', '')
            newFilename = newFilename.replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '')
            newFilename = newFilename.replace('＞', '').replace('﹥', '').replace('›', '')
            newFilename = newFilename.replace('＜', '').replace('﹤', '')
            newFilename = newFilename.replace('｜', '').replace('│', '').replace('|', '')
            newFilename = newFilename.replace('', '')
            if newFilename != filename:
                os.rename(os.path.join(outputDir, filename), os.path.join(outputDir, newFilename))


# Extracts metadata from .txt files and sets it as ID3 tags for the corresponding mp3 files in the output directory.
def setMusicMetadata(outputDir):
    # Loop through all mp3 files in the directory
    for file in os.listdir(outputDir):
        if file.endswith('.mp3'):
            # Extract title and artist metadata from the .txt file
            with open(os.path.join(outputDir, file[:-4] + '.txt'), 'r', encoding='ISO-8859-1') as f:
                # Skip first two lines and extract the third line
                f.readline()
                f.readline()
                metadata = f.readline().strip().split(' · ')
                # Set title metadata as the first element before the first " · " symbol
                title = metadata[0].strip()
                # Set artist metadata as the rest of the elements after the first " · " symbol
                artists = metadata[1:]
                artists = [a.strip() for a in artists]
                artists_set = set(artists)
                # Get the order of appearance of the artists and remove duplicates
                artist_order = []
                for artist in artists:
                    if artist not in artist_order:
                        artist_order.append(artist)
                artists = [a for a in artist_order if a in artists_set]
                artist_str = ', '.join(artists)
            # Set the artist and title metadata for the mp3 file
            audio = EasyID3(os.path.join(outputDir, file))
            audio['title'] = title
            audio['artist'] = artist_str
            audio.save()
            # Delete the .txt file after setting the metadata
            os.remove(os.path.join(outputDir, file[:-4] + '.txt'))
            print(f"Failed to rename {file}")


# Renames files with the artist name and removes illegal characters
def renameMp3Files(outputDir):
    # Regular expression for illegal characters
    illegalCharsRegex = r'[\\/:*?"<>|]'
    # Loop through all mp3 files in the directory
    mp3Files = [file for file in os.listdir(outputDir) if file.endswith('.mp3')]
    for file in mp3Files:
        try:
            audio = MP3(os.path.join(outputDir, file))
            # Extract and sanitize first artist name
            artist = re.sub(illegalCharsRegex, '', audio['TPE1'].text[0].split(',')[0])
            oldFilename = os.path.join(outputDir, file)
            newFilename = os.path.join(outputDir, f"{artist} - {file}")
            os.rename(oldFilename, newFilename)
            print(f"Renamed {oldFilename} to {newFilename}")
        except:
            print(f"Failed to rename {file}")






























































def show_popup():
    # Create the popup window
    popup_window = tk.Toplevel()
    popup_window.title("Finished")
    # Add a label to the popup window with the message
    message_label = tk.Label(popup_window, text="Finished Successfully!")
    message_label.pack(padx=20, pady=10)
    # Set the size and position of the popup window
    popup_window.geometry("200x100+500+300")
    # Run the popup window
    popup_window.mainloop()

def update_progress(value):
    current_value = progress_bar["value"]
    if current_value < value * 10:
        progress_bar["value"] = current_value + 1
        mainframe.after(10, update_progress, value)

# Function to start downloading playlist
def start_download():
    directory_path = directoryBox.get()
    directory_path = directory_path + '/'
    url_link = urlBox.get()
    update_progress(1)
    downloadVideos(url_link, directory_path)
    update_progress(2)
    urlLists = getPlaylistVideoUrls(url_link)
    update_progress(3)
    downloadVideoDescriptions(urlLists, directory_path)
    update_progress(4)
    takeAlbumArt(directory_path)
    update_progress(5)
    deleteMp4File(directory_path)
    update_progress(6)
    addArtworkToMp3Files(directory_path)
    replaceHashtagSymbol(directory_path)
    update_progress(7)
    deleteIllegalChars(directory_path)
    update_progress(8)
    setMusicMetadata(directory_path)
    update_progress(9)
    renameMp3Files(directory_path)
    update_progress(10)
    time.sleep(1)
    show_popup()
    time.sleep(1)
    update_progress(0)
    

# Function to open file explorer to select directory
def select_directory():
    directory = filedialog.askdirectory()
    directoryBox.insert(0, directory) 

titleLabel = tk.Label(mainframe, text="YouTube Playlist to .mp3 Utility (YTPMP3U)", font=("MS Sans Serif", 22, 'bold'))
titleLabel.grid(row=0, column=2, columnspan=12, rowspan=2)

style = ttk.Style()
style.configure("Horizontal.TSeparator", background="green")
horizontalSeparator = ttk.Separator(mainframe, orient='horizontal', style="Horizontal.TSeparator")
horizontalSeparator.grid(row=1, column=1, columnspan=14, rowspan=2, sticky='ew')


style = ttk.Style()
style.configure("Vertical.TSeparator", background="green")
verticalSeparator = ttk.Separator(mainframe, orient='vertical', style="Vertical.TSeparator")
verticalSeparator.grid(row=2, column=7, columnspan=2, rowspan=6, sticky='ns')


urlLabel = ttk.Label(mainframe, text="Playlist URL:", font=("MS Sans Serif", 11))
urlLabel.grid(row=3, column=0, columnspan=3)
urlBox = ttk.Entry(mainframe, width=40)
urlBox.grid(row=3, column=2, columnspan=6)

directoryLabel = ttk.Label(mainframe, text="Output directory:", font=("MS Sans Serif", 11))
directoryLabel.grid(row=5, column=0, columnspan=3)
directoryButton = ttk.Button(mainframe, text="Select through Explorer", command=select_directory)
directoryButton.grid(row=6, column=2, columnspan=6)
directoryBox = ttk.Entry(mainframe, width=37)
directoryBox.grid(row=5, column=2, columnspan=6)

start_button = ttk.Button(mainframe, text="Activate Program", command=start_download)
start_button.grid(row=5, column=10, columnspan=4)

# Create the progress bar
progress_bar = ttk.Progressbar(mainframe, orient="horizontal", length=250, mode="determinate")
progress_bar.grid(row=4, column=9, columnspan=6)

mainframe.mainloop()
