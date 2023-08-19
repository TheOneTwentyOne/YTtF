import json
import os
import yt_dlp
from checkPlaylistTitles import checkPlaylistTitles
from playlistUrlClean import playlistUrlClean

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
            ydl = yt_dlp.YoutubeDL({'quiet': True})
            info_dict = ydl.extract_info(url, download=False)
            videoTitle = str(info_dict['title'])
            videoTitle = videoTitle.strip().replace('/','').replace('\\','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','')
            # create empty text file
            print(videoTitle)
            outputFilePath = os.path.join(outputDir, videoTitle + ".txt")
            with open(outputFilePath, "w") as f:
                pass
            if url in descriptionDict:
                # use description data from dictionary if exists
                videoDescription = descriptionDict[url]
            else:
                # download description data from youtube-dl for new video
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    videoDescription = str(info_dict['description'].strip())
                    # store the description data in the dictionary
                    descriptionDict[url] = videoDescription
                # store the description data in the dictionary
                descriptionDict[url] = videoDescription
            # write description to text file
            with open(outputFilePath, "w", encoding="utf16", errors="replace") as f:
                f.write(videoDescription.replace("\uFFFD", ""))
        # write the descriptions to file
        with open(descriptionsFile, 'w') as f:
            json.dump(descriptionDict, f)
    os.remove(os.path.join(outputDir, "descriptions.json"))





"""
#------------------------------------
#HERE IS AN EXAMPLE OF USAGE
#------------------------------------

# Call the function with the desired playlist URL and output directory
playlistUrl = "https://youtube.com/playlist?list=PLLtfsNRMIOUd2uORg5V2TiP9Mk-73Kk4m"
outputDir = "C:\\Users\\aarav\\OneDrive\\Desktop\\TESTMUSIC\\"

# List of duplicates (format: [(normalized_title, [url_list])])
urls = playlistUrlClean(playlistUrl, outputDir, (checkPlaylistTitles(playlistUrl)))
downloadVideoDescriptions(urls, outputDir)
"""