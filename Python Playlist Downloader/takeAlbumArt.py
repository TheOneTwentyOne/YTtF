import os
from moviepy.editor import VideoFileClip

# Gets the album art from the .mp4 file
def takeAlbumArt(outputDir):
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp4") or filename.endswith(".webm"):
            input_file = os.path.join(outputDir, filename)
            output_file = os.path.join(outputDir, os.path.splitext(filename)[0] + ".png")
            clip = VideoFileClip(input_file)
            clip.save_frame(output_file, t=1)
            clip.close()