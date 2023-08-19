from checkPlaylistTitles import checkPlaylistTitles
from downloadProcess import downloadProcess
from individualSongDownload import individualSongDownload




def filterPlaylist(url_link, directory_path, progress_var):
    
    duplicates = checkPlaylistTitles(url_link)
    downloadProcess(url_link, directory_path, progress_var, duplicates)


    individualSongDownload(url_link, directory_path)

