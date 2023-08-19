import yt_dlp
from checkPlaylistTitles import checkPlaylistTitles


def playlistUrlClean(playlistUrl, outputDir, duplicates):

    full_video_urls = []
    
    # Set the options for the yt-dlp downloader
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]',
        'outtmpl': outputDir + '%(title)s.%(ext)s',
        'yes_playlist': True
    }

    # Download the videos and collect video URLs
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlistUrl, download=False)
        if 'entries' in result:
            for entry in result['entries']:
                full_video_urls.append(entry['webpage_url'])  # Use 'webpage_url' instead of 'url'
    
    # Remove duplicate video URLs based on the provided list of duplicates
    filtered_full_video_urls = []
    for url in full_video_urls:
        should_skip = any(duplicate_url in url for _, duplicate_url_list in duplicates for duplicate_url in duplicate_url_list)
        if not should_skip:
            filtered_full_video_urls.append(url)

    return filtered_full_video_urls






"""
#------------------------------------
#HERE IS AN EXAMPLE OF USAGE
#------------------------------------

# Call the function with the desired playlist URL and output directory
playlistUrl = "https://youtube.com/playlist?list=PLLtfsNRMIOUd2uORg5V2TiP9Mk-73Kk4m"
outputDir = "C:\\Users\\aarav\\OneDrive\\Desktop\\TESTMUSIC\\"

# List of duplicates (format: [(normalized_title, [url_list])])
duplicates = checkPlaylistTitles(playlistUrl)

print(playlistUrlClean(playlistUrl, outputDir, duplicates))
"""