from mutagen.flac import FLAC
import os, re

# Renames files with the artist name and removes illegal characters
def renameFlacFiles(outputDir):
    # Regular expression for illegal characters
    illegalCharsRegex = r'[\\/:*?"<>|]'
    # Loop through all FLAC files in the directory
    flacFiles = [file for file in os.listdir(outputDir) if file.endswith('.flac')]
    for file in flacFiles:
        try:
            audio = FLAC(os.path.join(outputDir, file))
            # Extract and sanitize first artist name
            artist = re.sub(illegalCharsRegex, '', audio.get('artist', ['Unknown'])[0].split(',')[0])
            oldFilename = os.path.join(outputDir, file)
            newFilename = os.path.join(outputDir, f"{artist} - {file}")
            os.rename(oldFilename, newFilename)
            print(f"Renamed {oldFilename} to {newFilename}")
        except:
            print(f"Failed to rename {file}")
