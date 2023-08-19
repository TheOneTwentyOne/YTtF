import yt_dlp

# Fetches the URLs from the playlist
def getPlaylistVideoUrls(playlistUrl):
    with yt_dlp.YoutubeDL({'extract_flat': 'in_playlist'}) as ydl:
        result = ydl.extract_info(playlistUrl, download=False)
        urls = [item['url'] for item in result['entries']]
        return urls



"""
url = "https://youtube.com/playlist?list=PLLtfsNRMIOUd2uORg5V2TiP9Mk-73Kk4m"

print(getPlaylistVideoUrls(url))"""