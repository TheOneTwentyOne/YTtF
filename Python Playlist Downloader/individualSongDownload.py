import json
import os
import re
import yt_dlp
from mutagen.flac import FLAC, Picture
from checkPlaylistTitles import checkPlaylistTitles
from replaceHashtagSymbol import replaceHashtagSymbol
from takeAlbumArt import takeAlbumArt
from deleteIllegalChars import deleteIllegalChars
from deleteMp4File import deleteMp4File



def fetch_video_title(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', 'UnknownTitle')



def individualSongDownload(url_link, directory_path):
    urlLists = checkPlaylistTitles(url_link)
    dirPath = directory_path + "duplicates/"
    for normalized_title, url_list in urlLists:
        for url in url_list:
            # Download the audio and video files
            ydl_opts_audio = {
                'format': 'bestaudio/best',
                'outtmpl': dirPath + '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                    'preferredquality': '0',
                }],
                'extractaudio': True,
                'audioformat': 'flac',
            }

            ydl_opts_video = {
                'format': 'best[ext=mp4]',
                'outtmpl': dirPath + '%(title)s.%(ext)s',
                'yes_playlist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                ydl_audio.download([url])

            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl_video:
                ydl_video.download([url])



            # Download and store the video description
            descriptionsFile = os.path.join(dirPath, 'descriptions.json')
            descriptionDict = {}

            if os.path.exists(descriptionsFile):
                with open(descriptionsFile, 'r') as f:
                    descriptionDict = json.load(f)

            ydl = yt_dlp.YoutubeDL({'quiet': True})
            info_dict = ydl.extract_info(url, download=False)
            videoTitle = str(info_dict['title'])
            videoTitle = videoTitle.strip().replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

            outputFilePath = os.path.join(dirPath, videoTitle + ".txt")

            if url in descriptionDict:
                videoDescription = descriptionDict[url]
            else:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    videoDescription = str(info_dict['description'].strip())
                    descriptionDict[url] = videoDescription

            with open(outputFilePath, "w", encoding="utf16", errors="replace") as f:
                f.write(videoDescription.replace("\uFFFD", ""))

            with open(descriptionsFile, 'w') as f:
                json.dump(descriptionDict, f)

            os.remove(os.path.join(dirPath, "descriptions.json"))



            takeAlbumArt(dirPath)    
            deleteMp4File(dirPath)


            filename = dirPath + normalized_title
            filenameFlac = filename+".flac"
            print("-"*30)
            print(filename)
            print("-"*30)
            for files in os.listdir(dirPath):
                if filenameFlac.lower() == files.lower():
                    print("-"*30)
                    print(files)
                    print("-"*30)
                    print(filename)
                    print("-"*30)
                    filenameFlac = files  # Set the actual case of the filename
            # Adds artwork to .flac files and deletes the image files
            imageFile = filename + ".png"
            print("-"*30)
            print(imageFile)
            print("-"*30)
            # Adds artwork to .flac file
            try:
                audio = FLAC(filenameFlac)
                with open(imageFile, "rb") as f:
                    artwork = f.read()
                # Creates a Picture object with MIME type "image/png"
                pic = Picture()
                pic.type = 3  # Cover (front) image
                pic.mime = 'image/png'
                pic.desc = "Cover"
                pic.data = artwork
                audio.clear_pictures()  # Remove existing pictures
                audio.add_picture(pic)
                audio.save()
                print("Added artwork to", filename)
            except Exception as e:
                print(f"Could not add artwork to {filename}. Error: {str(e)}")
            # Deletes the .png file
            if imageFile.lower().endswith('.png'):
                os.remove(imageFile)

            replaceHashtagSymbol(dirPath)
            deleteIllegalChars(dirPath)


            # Extract title and artist metadata from the .txt file
            print("-"*30)
            print((filename + ".txt"))
            print("-"*30)

            with open((filename + ".txt"), 'r', encoding='utf16') as f:
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
            # Set the artist and title metadata for the .flac file
            audio = FLAC(filename + ".flac")
            audio['title'] = title
            audio['artist'] = artist_str
            audio.save()
            # Delete the .txt file after setting the metadata
            os.remove(filename + ".txt")


            illegalCharsRegex = r'[\\/:*?"<>|]'
            try:
                audio = FLAC(filenameFlac)
                # Extract and sanitize first artist name
                artist = re.sub(illegalCharsRegex, '', audio.get('artist', ['Unknown'])[0].split(',')[0])
                oldFilename = filenameFlac
                title = fetch_video_title(url)
                newFilename = os.path.join(dirPath, f"{artist} - {title}" + ".flac")
                os.rename(oldFilename, newFilename)
                print(f"Renamed {oldFilename} to {newFilename}")
            except:
                print(f"Failed to rename {filename}")
