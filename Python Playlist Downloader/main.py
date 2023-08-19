# This section imports all of the required packages
import threading
import tkinter as tk
from tkinter import filedialog, ttk
from filterPlaylist import filterPlaylist





def start_download():
    directory_path = directoryBox.get()
    directory_path = directory_path + '/'
    url_link = urlBox.get()

    # Create a progress variable to update the progress bar
    progress_var = tk.DoubleVar()
    progress_bar.configure(variable=progress_var)
    progress_var.set(0)

    # Create a separate thread to execute the download process
    download_thread = threading.Thread(target=filterPlaylist, args=(url_link, directory_path, progress_var))
    download_thread.start()

# Function to open file explorer to select directory
def select_directory():
    directory = filedialog.askdirectory()
    directoryBox.insert(0, directory) 

def update_progress(value):
    current_value = progress_bar["value"]
    if current_value < value * 10:
        progress_bar["value"] = current_value + 1
        mainframe.after(10, update_progress, value)





# This sets up the main window used in Tkinter.
mainframe = tk.Tk()
mainframe.geometry("800x450")
mainframe.resizable(False, False)
mainframe.title("YTPFLACU")

# Assigns all of the values for the grid. 'i' is the width, 16, and 'j' is the height, 9.
style = ttk.Style()
style.configure('CustomFrame.TFrame', background='black', relief='solid', borderwidth=1)
frames = {(i, j): ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame') for i in range(16) for j in range(9)}
for i, j in frames:
    frames[i, j].grid(row=j, column=i)

# These are the widgets and buttons and other UI elements
titleLabel = tk.Label(mainframe, text="YouTube Playlist to .flac Utility (YTPFLACU)", font=("MS Sans Serif", 22, 'bold'))
titleLabel.grid(row=0, column=2, columnspan=12, rowspan=2)

style = ttk.Style()
style.configure("Horizontal.TSeparator", background="green")
horizontalSeparator = ttk.Separator(mainframe, orient='horizontal', style="Horizontal.TSeparator")
horizontalSeparator.grid(row=1, column=1, columnspan=14, rowspan=2, sticky='ew')


style = ttk.Style()
style.configure("Vertical.TSeparator", background="green")
verticalSeparator = ttk.Separator(mainframe, orient='vertical', style="Vertical.TSeparator")
verticalSeparator.grid(row=2, column=7, columnspan=2, rowspan=6, sticky='ns')


urlLabel = ttk.Label(mainframe, text="Playlist URL:", font=("MS Sans Serif", 11))
urlLabel.grid(row=3, column=0, columnspan=3)
urlBox = ttk.Entry(mainframe, width=40)
urlBox.grid(row=3, column=2, columnspan=6)

directoryLabel = ttk.Label(mainframe, text="Output directory:", font=("MS Sans Serif", 11))
directoryLabel.grid(row=5, column=0, columnspan=3)
directoryButton = ttk.Button(mainframe, text="Select through Explorer", command=select_directory)
directoryButton.grid(row=6, column=2, columnspan=6)
directoryBox = ttk.Entry(mainframe, width=37)
directoryBox.grid(row=5, column=2, columnspan=6)

start_button = ttk.Button(mainframe, text="Activate Program", command=start_download)
start_button.grid(row=5, column=10, columnspan=4)

# Create the progress bar
progress_bar = ttk.Progressbar(mainframe, orient="horizontal", length=250, mode="determinate")
progress_bar.grid(row=4, column=9, columnspan=6)





if __name__ == '__main__':
    mainframe.mainloop()