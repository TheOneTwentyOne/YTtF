import os

# Replaces "#" with "." for any of the files in the directory.
def replaceHashtagSymbol(outputDir):
    for filename in os.listdir(outputDir):
        if "#" in filename:
            newFilename = filename.replace("#", ".")
            os.rename(os.path.join(outputDir, filename), os.path.join(outputDir, newFilename))