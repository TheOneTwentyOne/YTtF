import os
from PIL import Image
from mutagen.flac import FLAC, Picture

# Adds artwork to .flac files and deletes the image files
def addArtworkToFlacFiles(outputDir):
    for filename in os.listdir(outputDir):
        if filename.endswith(".flac"):
            flacFile = os.path.join(outputDir, filename)
            imageFile = os.path.join(outputDir, os.path.splitext(filename)[0] + ".png")
            # Adds artwork to .flac file
            try:
                audio = FLAC(flacFile)
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
                print("Added artwork to", flacFile)
            except Exception as e:
                print(f"Could not add artwork to {flacFile}. Error: {str(e)}")
            # Deletes the .png file
            if imageFile.lower().endswith('.png'):
                os.remove(imageFile)