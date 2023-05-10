import re, os, json, mutagen, time, yt_dlp
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
from moviepy.editor import VideoFileClip
from mutagen.mp3 import MP3
from mutagen.id3 import APIC
from mutagen.easyid3 import EasyID3

mainframe = tk.Tk()
mainframe.geometry("800x450")
mainframe.resizable(False, False)
mainframe.title("YTPMP3U")

# Assigns all of the values for the grid. 'i' is the width, 16, and 'j' is the height.
style = ttk.Style()
style.configure('CustomFrame.TFrame', background='black', relief='solid', borderwidth=1)
frames = {(i, j): ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame') for i in range(16) for j in range(9)}
for i, j in frames:
    frames[i, j].grid(row=j, column=i)


# Downloads all of the .mp4 and .mp3 files from the specified playlist
def downloadVideos(playlistUrl, outputDir):
    # Set the options for the yt-dlp downloader
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]',
        'outtmpl': outputDir + '%(title)s.%(ext)s',
        'yes_playlist': True
    }
    # Download the videos and audio files
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlistUrl])
    # Download the audio files
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outputDir + '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'extractaudio': True,
        'audioformat': 'mp3',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlistUrl])


# Fetches the URLs from the playlist
def getPlaylistVideoUrls(playlistUrl):
    with yt_dlp.YoutubeDL({'extract_flat': 'in_playlist'}) as ydl:
        result = ydl.extract_info(playlistUrl, download=False)
        urls = [item['url'] for item in result['entries']]
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
            with yt_dlp.YoutubeDL({'forcefilename': True, 'quiet': True}) as ydl:
                videoTitle = ydl.extract_info(url, download=False)['title']
            # create empty text file
            outputFilePath = os.path.join(outputDir, videoTitle + ".txt")
            with open(outputFilePath, "w", encoding= "Latin-1", errors="replace"):
                pass
            if url in descriptionDict:
                # use description data from dictionary if exists
                videoDescription = descriptionDict[url]
            else:
                # download description data from yt-dlp for new video
                with yt_dlp.YoutubeDL() as ydl:
                    videoDescription = ydl.extract_info(url, download=False)['description']
                # store the description data in the dictionary
                descriptionDict[url] = videoDescription
            # write description to text file
            with open(outputFilePath, "w", encoding= "Latin-1", errors="replace") as f:
                f.write(videoDescription.replace("\uFFFD", ""))
        # write the descriptions to file
        with open(descriptionsFile, 'w', encoding= "Latin-1", errors="replace") as f:
            json.dump(descriptionDict, f)
    os.remove(os.path.join(outputDir, "descriptions.json"))


def takeAlbumArt(outputDir):
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp4") or filename.endswith(".webm"):
            input_file = os.path.join(outputDir, filename)
            output_file = os.path.join(outputDir, os.path.splitext(filename)[0] + ".png")
            clip = VideoFileClip(input_file)
            clip.save_frame(output_file, t=1)
            clip.close()


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





"""

SECOND SECTION

"""





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