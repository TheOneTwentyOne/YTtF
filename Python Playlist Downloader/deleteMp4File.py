import os

# Delete the MP4 file
def deleteMp4File(outputDir):
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp4"):
            mp4File = os.path.join(outputDir, filename)
            # Delete the mp4 file
            os.remove(mp4File)
