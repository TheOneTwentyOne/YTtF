from downloadVideoDescriptions import downloadVideoDescriptions
from downloadVideos import downloadVideos
from playlistUrlClean import playlistUrlClean
from takeAlbumArt import takeAlbumArt
from deleteMp4File import deleteMp4File
from addArtworkToFlacFiles import addArtworkToFlacFiles
from replaceHashtagSymbol import replaceHashtagSymbol
from deleteIllegalChars import deleteIllegalChars
from setMusicMetadata import setMusicMetadata
from renameFlacFiles import renameFlacFiles




def downloadProcess(url, directory_path, progress_var, duplicates):

    downloadVideos(url, directory_path, duplicates)
    progress_var.set(10)

    urlLists = playlistUrlClean(url, directory_path, duplicates)
    progress_var.set(20)
    
    downloadVideoDescriptions(urlLists, directory_path)
    progress_var.set(30)



    takeAlbumArt(directory_path)
    progress_var.set(40)

    deleteMp4File(directory_path)
    progress_var.set(50)

    addArtworkToFlacFiles(directory_path)
    progress_var.set(60)

    replaceHashtagSymbol(directory_path)
    progress_var.set(70)

    deleteIllegalChars(directory_path)
    progress_var.set(80)

    setMusicMetadata(directory_path)
    progress_var.set(90)

    renameFlacFiles(directory_path)
    progress_var.set(100)
