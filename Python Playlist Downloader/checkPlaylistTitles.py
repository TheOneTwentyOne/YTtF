import yt_dlp
from collections import defaultdict
from getPlaylistVideoUrls import getPlaylistVideoUrls

# Function to get the title names from a YouTube playlist
def checkPlaylistTitles(playlistUrl):
    videoUrls = getPlaylistVideoUrls(playlistUrl)
    titles_to_urls = defaultdict(list)
    duplicates = []

    with yt_dlp.YoutubeDL() as ydl:
        for url in videoUrls:
            info = ydl.extract_info(url, download=False)
            title = info.get('title')
            normalized_title = title.lower()  # Convert title to lowercase
            titles_to_urls[normalized_title].append(url)

    for normalized_title, url_list in titles_to_urls.items():
        if len(url_list) > 1:
            duplicates.append((normalized_title, url_list))

    return duplicates





"""
#------------------------------------
#HERE IS AN EXAMPLE OF USAGE
#------------------------------------


# Call the function with the desired playlist URL
playlistUrl = "https://youtube.com/playlist?list=PLLtfsNRMIOUd2uORg5V2TiP9Mk-73Kk4m"
duplicates = checkPlaylistTitles(playlistUrl)
for normalized_title, url_list in duplicates:
    print(f"Title: {normalized_title}")
    print("URLs:")
    for url in url_list:
        print(url)
    print("-" * 30)

print(duplicates)

"""