import os

# Deletes all illegal characters from the .txt and .mp3 files in the output folder.
def deleteIllegalChars(outputDir):
    illegalChars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for filename in os.listdir(outputDir):
        if filename.endswith('.flac') or filename.endswith('.txt'):
            newFilename = filename.translate({ord(char): None for char in illegalChars})
            newFilename = newFilename.replace('⧸', '').replace('／', '').replace('∕', '')
            newFilename = newFilename.replace('⧵', '').replace('∖', '').replace('＼', '')
            newFilename = newFilename.replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '')
            newFilename = newFilename.replace('＊', '').replace('⁎', '').replace('∗', '')
            newFilename = newFilename.replace('？', '')
            newFilename = newFilename.replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '')
            newFilename = newFilename.replace('＞', '').replace('﹥', '').replace('›', '')
            newFilename = newFilename.replace('＜', '').replace('﹤', '')
            newFilename = newFilename.replace('｜', '').replace('│', '').replace('|', '')
            newFilename = newFilename.replace('_','')
            newFilename = newFilename.replace('', '')
            if newFilename != filename:
                os.rename(os.path.join(outputDir, filename), os.path.join(outputDir, newFilename))