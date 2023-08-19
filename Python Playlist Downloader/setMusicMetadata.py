import os
from mutagen.flac import FLAC

# Extracts metadata from .txt files and sets it as metadata tags for the corresponding .flac files in the output directory.
def setMusicMetadata(outputDir):
    # Loop through all .flac files in the directory
    for file in os.listdir(outputDir):
        if file.endswith('.flac'):
            # Extract title and artist metadata from the .txt file
            with open(os.path.join(outputDir, file[:-5] + '.txt'), 'r', encoding='utf16') as f:
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
            audio = FLAC(os.path.join(outputDir, file))
            audio['title'] = title
            audio['artist'] = artist_str
            audio.save()
            # Delete the .txt file after setting the metadata
            os.remove(os.path.join(outputDir, file[:-5] + '.txt'))
