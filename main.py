"""
██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗
██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗
██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║
██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║
╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
"""
import os
import math
import time
import youtube_dl
import yt_dlp
import datetime
import threading


import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *

from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, TIT2, TPE1, TALB, TDRC
from mutagen.flac import FLAC

from PIL import Image

"""
 ██████╗ ██████╗ ███╗   ███╗███╗   ███╗██╗   ██╗███╗   ██╗ █████╗ ██╗         
██╔════╝██╔═══██╗████╗ ████║████╗ ████║██║   ██║████╗  ██║██╔══██╗██║         
██║     ██║   ██║██╔████╔██║██╔████╔██║██║   ██║██╔██╗ ██║███████║██║         
██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║         
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║███████╗    
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    

███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗    
██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝    
█████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗    
██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║    
██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║    
╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝    
"""


class communal_methods:
    def advanced_clean(input_string):
        return (
            input_string.replace("⧸", "")
            .replace("／", "")
            .replace("∕", "")
            .replace("⧵", "")
            .replace("∖", "")
            .replace("＼", "")
            .replace("꞉", "")
            .replace("∶", "")
            .replace("⁚", "")
            .replace("：", "")
            .replace("ː", "")
            .replace("＊", "")
            .replace("⁎", "")
            .replace("∗", "")
            .replace("？", "")
            .replace("＂", "")
            .replace("“", "")
            .replace("”", "")
            .replace("‘", "")
            .replace("’", "")
            .replace("„", "")
            .replace("‟", "")
            .replace("❝", "")
            .replace("❞", "")
            .replace("＞", "")
            .replace("﹥", "")
            .replace("›", "")
            .replace("＜", "")
            .replace("﹤", "")
            .replace("｜", "")
            .replace("│", "")
            .replace("|", "")
            .replace("_", "")
            .replace("", "")
            .replace("/", "")
            .replace("\\", "")
            .replace(":", "")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
            .replace("|", "")
            .replace("?", "")
        )

    def basic_clean(input_string):
        return (
            input_string.replace("\\", "")
            .replace("/", "")
            .replace(":", "")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
            .replace("|", "")
        )

    def crop_image(subdirectory, cleaned_title, thumbnail_path):
        # Load the downloaded .webp thumbnail image
        thumbnail = Image.open(thumbnail_path)

        # Calculate cropping dimensions to create a square centered image
        width, height = thumbnail.size
        crop_size = min(width, height)

        # Crop the image
        cropped_thumbnail = thumbnail.crop(
            (
                ((width - crop_size) // 2),
                ((height - crop_size) // 2),
                ((width + crop_size) // 2),
                ((height + crop_size) // 2),
            )
        )

        # Save the cropped thumbnail back as .webp format
        cropped_thumbnail.save(thumbnail_path, format="WebP")

        # Convert WebP to PNG
        webp_image = Image.open(thumbnail_path)
        thumbnail_path = f"{subdirectory}/{cleaned_title}.png"
        webp_image.save(thumbnail_path, "PNG")
        os.remove(f"{subdirectory}/{cleaned_title}.webp")

    def set_variables(info, subdirectory):
        # clean all files
        files = os.listdir(subdirectory)
        for file in files:
            new_file_name = communal_methods.advanced_clean(str(file))
            old_file_path = f"{subdirectory}/{file}"
            new_file_path = f"{subdirectory}/{new_file_name}"
            os.rename(old_file_path, new_file_path)

        # Calculate variables
        cleaned_title = communal_methods.advanced_clean(str(info["title"]))
        channel_name = info.get("channel", None)
        time_variable = int((time.time() % 10) * 100000)
        description = info["description"].split("\n")
        if description[0].startswith("Provided to YouTube by "):
            title, *artists = [a.strip() for a in description[2].strip().split(" · ")]
            title = title.strip()
            artist = communal_methods.basic_clean(str(artists[0]))
            artist_metadata = ",(&) ".join(artists)
            album = description[4].strip()
            if (description[8].strip()).startswith("Released on: "):
                raw_date = description[8].strip()
                raw_date = raw_date.replace("Released on: ", "")
                date = datetime.datetime.strptime(raw_date, "%Y-%m-%d")
                return (
                    cleaned_title,
                    channel_name,
                    time_variable,
                    description,
                    title,
                    artist,
                    artist_metadata,
                    album,
                    date,
                )
            else:
                return (
                    cleaned_title,
                    channel_name,
                    time_variable,
                    description,
                    title,
                    artist,
                    artist_metadata,
                    album,
                    None,
                )
        else:
            return (
                cleaned_title,
                channel_name,
                time_variable,
                description,
                None,
                None,
                None,
                None,
                None,
            )


"""
    ███╗   ███╗██████╗ ██████╗     ███████╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
    ████╗ ████║██╔══██╗╚════██╗    ██╔════╝██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
    ██╔████╔██║██████╔╝ █████╔╝    ███████╗█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║
    ██║╚██╔╝██║██╔═══╝  ╚═══██╗    ╚════██║██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║
██╗ ██║ ╚═╝ ██║██║     ██████╔╝    ███████║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝ ╚═╝     ╚═╝╚═╝     ╚═════╝     ╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""


def mp3Process(url, subdirectory, main_directory, checkbox_states):
    global song_denominator
    image_bool, rename_bool, metadata_bool, threaded_bool = checkbox_states

    ydl_opts = {
        "outtmpl": f"{subdirectory}/%(title)s.%(ext)s",
        "format": "bestaudio/best",  # Download best audio quality
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",  # You can adjust the audio quality here (e.g., 128, 192, 256, 320)
            }
        ],
        "writethumbnail": image_bool,
        "writeinfojson": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Download the video, thumbnail, and description
        info = ydl.extract_info(url, download=True)
        (
            cleaned_title,
            channel_name,
            time_variable,
            description,
            title,
            artist,
            artist_metadata,
            album,
            date,
        ) = communal_methods.set_variables(info, subdirectory)

        primary_mp3_path = f"{subdirectory}/{cleaned_title}.mp3"
        audio = MP3(primary_mp3_path, ID3=ID3)

        if image_bool:
            thumbnail_path = f"{subdirectory}/{cleaned_title}.webp"
            communal_methods.crop_image(subdirectory, cleaned_title, thumbnail_path)
            thumbnail_path = f"{subdirectory}/{cleaned_title}.png"
            # Attach image to the .mp3 file
            with open(thumbnail_path, "rb") as image_file:
                artwork = image_file.read()
                audio_tags = audio.tags
                if not audio_tags:
                    audio_tags = ID3()
                    audio.tags = audio_tags
                audio_tags.add(
                    APIC(
                        encoding=3,  # utf-8
                        mime="image/png",
                        type=3,  # Cover (front) image
                        desc="Cover",
                        data=artwork,
                    )
                )
                audio.save(primary_mp3_path)
            os.remove(thumbnail_path)

        if metadata_bool:
            audio["TIT2"] = TIT2(encoding=3, text=title)
            audio["TPE1"] = TPE1(encoding=3, text=artist_metadata)
            audio["TALB"] = TALB(encoding=3, text=album)
            if date is not None:
                formatted_date = date.strftime("%Y")
                audio["TDRC"] = TDRC(encoding=3, text=formatted_date)
            audio.save(primary_mp3_path)
            os.remove(f"{subdirectory}/{cleaned_title}.info.json")
        else:
            audio["TPE1"] = TPE1(encoding=3, text=(str(channel_name).strip()))
            audio.save(primary_mp3_path)
            os.remove(f"{subdirectory}/{cleaned_title}.info.json")

        if rename_bool:
            if metadata_bool == False:
                artist = channel_name
            secondary_mp3_path = f"{main_directory}/{artist} - {cleaned_title}.mp3"
            tertiary_mp3_path = (
                f"{main_directory}/{artist} - {cleaned_title} - ({time_variable}).mp3"
            )
            try:
                os.rename(primary_mp3_path, secondary_mp3_path)
            except Exception as e:
                os.rename(primary_mp3_path, tertiary_mp3_path)

        else:
            secondary_mp3_path = f"{main_directory}/{cleaned_title}.mp3"
            tertiary_mp3_path = (
                f"{main_directory}/{cleaned_title} - ({time_variable}).mp3"
            )
            try:
                os.rename(primary_mp3_path, secondary_mp3_path)
            except Exception as e:
                os.rename(primary_mp3_path, tertiary_mp3_path)

    song_denominator += 1


def filterPlaylistMp3(
    urls, main_directory, number_of_threads, checkbox_states, playlist_name
):
    if number_of_threads <= 0:
        number_of_threads = 1

    # Calculate the number of elements in each sublist
    sublist_size = len(urls) // number_of_threads
    remainder = len(urls) % number_of_threads

    # Create empty sublists
    sublists = [[] for _ in range(number_of_threads)]

    # Split the input list into sublists
    start_index = 0
    for i in range(number_of_threads):
        sublist_end = start_index + sublist_size + (1 if i < remainder else 0)
        sublists[i] = urls[start_index:sublist_end]
        start_index = sublist_end

    threads = []
    for sublist in sublists:
        subdirectory = (
            main_directory
            + "/"
            + communal_methods.basic_clean(str(playlist_name))
            + str(sublists.index(sublist))
        )
        os.makedirs(subdirectory, exist_ok=True)
        thread = threading.Thread(
            target=startDownloadMp3,
            args=(sublist, subdirectory, main_directory, checkbox_states),
        )
        threads.append(thread)
        thread.start()
    # Wait for all threads to finish
    for thread in threads:
        thread.join()


def startDownloadMp3(urls, subdirectory, main_directory, checkbox_states):
    for url in urls:
        mp3Process(url, subdirectory, main_directory, checkbox_states)
    if not os.listdir(subdirectory):
        os.chmod(subdirectory, 0o777)
        os.rmdir(subdirectory)


"""
    ███████╗██╗      █████╗  ██████╗    ███████╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
    ██╔════╝██║     ██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
    █████╗  ██║     ███████║██║         ███████╗█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══╝  ██║     ██╔══██║██║         ╚════██║██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║
██╗ ██║     ███████╗██║  ██║╚██████╗    ███████║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝ ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""


def flacProcess(url, subdirectory, main_directory, checkbox_states):
    global song_denominator
    image_bool, rename_bool, metadata_bool, threaded_bool = checkbox_states

    ydl_opts = {
        "outtmpl": f"{subdirectory}/%(title)s.%(ext)s",
        "format": "bestaudio/best",  # Download best audio quality
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "flac",
                "preferredquality": "9",  # You can adjust the audio quality here (e.g., 1-9)
            }
        ],
        "writethumbnail": image_bool,
        "writeinfojson": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Download the video, thumbnail, and description
        info = ydl.extract_info(url, download=True)
        (
            cleaned_title,
            channel_name,
            time_variable,
            description,
            title,
            artist,
            artist_metadata,
            album,
            date,
        ) = communal_methods.set_variables(info, subdirectory)

        primary_flac_path = f"{subdirectory}/{cleaned_title}.flac"
        audio = FLAC(primary_flac_path)

        if image_bool:
            thumbnail_path = f"{subdirectory}/{cleaned_title}.webp"
            communal_methods.crop_image(subdirectory, cleaned_title, thumbnail_path)
            thumbnail_path = f"{subdirectory}/{cleaned_title}.png"
            # Attach image to the .mp3 file
            with open(thumbnail_path, "rb") as imageFile:
                artwork = imageFile.read()
                audio.clear_pictures()
                audio.add_picture(artwork)
            audio.save(primary_flac_path)
            os.remove(thumbnail_path)

        if metadata_bool:
            audio["title"] = title
            audio["artist"] = artist_metadata
            audio["album"] = album
            if date != None:
                audio["date"] = date
            audio.save(primary_flac_path)
            os.remove(f"{subdirectory}/{cleaned_title}.info.json")
        else:
            audio["artist"] = channel_name
            audio.save(primary_flac_path)
            os.remove(f"{subdirectory}/{cleaned_title}.info.json")

        if rename_bool:
            if metadata_bool == False:
                artist = channel_name
            secondary_flac_path = f"{main_directory}/{artist} - {cleaned_title}.flac"
            tertiary_flac_path = (
                f"{main_directory}/{artist} - {cleaned_title} - ({time_variable}).flac"
            )
            try:
                os.rename(primary_flac_path, secondary_flac_path)
            except Exception as e:
                os.rename(primary_flac_path, tertiary_flac_path)

        else:
            secondary_flac_path = f"{main_directory}/{cleaned_title}.flac"
            tertiary_flac_path = (
                f"{main_directory}/{cleaned_title} - ({time_variable}).flac"
            )
            try:
                os.rename(primary_flac_path, secondary_flac_path)
            except Exception as e:
                os.rename(primary_flac_path, tertiary_flac_path)

    song_denominator += 1


def filterPlaylistFlac(
    urls, directory_path, number_of_threads, checkbox_states, playlistTitle
):
    if number_of_threads <= 0:
        number_of_threads = 1

    # Calculate the number of elements in each sublist
    sublist_size = len(urls) // number_of_threads
    remainder = len(urls) % number_of_threads

    # Create empty sublists
    sublists = [[] for _ in range(number_of_threads)]

    # Split the input list into sublists
    start_index = 0
    for i in range(number_of_threads):
        sublist_end = start_index + sublist_size + (1 if i < remainder else 0)
        sublists[i] = urls[start_index:sublist_end]
        start_index = sublist_end

    threads = []
    for sublist in sublists:
        subdir = (
            directory_path
            + "/"
            + communal_methods.basic_clean(str(playlistTitle))
            + str(sublists.index(sublist))
        )
        os.makedirs(subdir, exist_ok=True)
        thread = threading.Thread(
            target=startDownloadFlac,
            args=(sublist, subdir, directory_path, checkbox_states),
        )
        threads.append(thread)
        thread.start()
    # Wait for all threads to finish
    for thread in threads:
        thread.join()


def startDownloadFlac(urls, subdirectory, main_directory, checkbox_states):
    for url in urls:
        flacProcess(url, subdirectory, main_directory, checkbox_states)
    if not os.listdir(subdirectory):
        os.chmod(subdirectory, 0o777)
        os.rmdir(subdirectory)


"""
███╗   ███╗ █████╗ ██╗███╗   ██╗    ██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗
████╗ ████║██╔══██╗██║████╗  ██║    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
██╔████╔██║███████║██║██╔██╗ ██║    ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║
██║╚██╔╝██║██╔══██║██║██║╚██╗██║    ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
██║ ╚═╝ ██║██║  ██║██║██║ ╚████║    ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
"""

urls = []
song_numerator = 100
song_denominator = 0


def extract_URLs(playlist_url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "force_generic_extractor": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(playlist_url, download=False)
            if "entries" in info_dict:
                playlist_name = info_dict.get("title", "Untitled Playlist")
                urls = [
                    entry["url"] for entry in info_dict["entries"] if "url" in entry
                ]

                # Filter out duplicates by converting the list to a set and back to a list
                unique_urls = list(set(urls))

                link_urls = [
                    "https://www.youtube.com/watch?v=" + str(url) for url in unique_urls
                ]
                return link_urls, playlist_name
        except youtube_dl.DownloadError:
            return None


# Event handler for checkbox changes
def get_checkbox_states():
    global checkbox_states
    checkbox_states = [
        checkbox1_var.get(),
        checkbox2_var.get(),
        checkbox3_var.get(),
        checkbox4_var.get(),
    ]


# Function to open file explorer to select directory
def get_directory():
    selected_directory = askdirectory()
    directoryBox.delete(0, tkinter.END)  # Clear previous entry
    directoryBox.insert(tkinter.END, selected_directory)


# Function to start download process in a separate thread
def activate_program():
    global url_type_option
    global urls
    global selected_file_option
    global checkbox_states
    global song_numerator

    playlist_or_video_url = urlBox.get()
    url_type = url_type_option.get()
    directory_path = directoryBox.get()
    file_type = selected_file_option.get()
    checkbox_states = checkbox_states
    number_of_threads = int(thread_box.get())

    if url_type == "Playlist":
        urls, playlistTitle = extract_URLs(playlist_or_video_url)
    else:
        urls.append(playlist_or_video_url)
        playlistTitle = "singleFile"

    if int(number_of_threads) > len(urls):
        number_of_threads = len(urls)

    if checkbox_states[3] is False:
        number_of_threads = 1

    song_numerator = len(urls)

    # Create a separate thread to execute the download process
    if file_type == ".mp3":
        download_thread = threading.Thread(
            target=filterPlaylistMp3,
            args=(
                urls,
                directory_path,
                number_of_threads,
                checkbox_states,
                playlistTitle,
            ),
        )
        download_thread.start()

        # Update progress bar directly from the download thread
        progressbar = threading.Thread(target=update_progress_bar)
        progressbar.start()
    elif file_type == ".flac":
        download_thread = threading.Thread(
            target=filterPlaylistFlac,
            args=(
                urls,
                directory_path,
                number_of_threads,
                checkbox_states,
                playlistTitle,
            ),
        )
        download_thread.start()

        # Update progress bar directly from the download thread
        progressbar = threading.Thread(target=update_progress_bar)
        progressbar.start()

    # Update the GUI to handle events
    main_window.after(100, update_gui)


def update_gui():
    main_window.update_idletasks()


def show_disclaimer():
    disclaimer_text = """\
Petrichor Systems - Disclaimer and License Notice

By using Petrichor Systems software "YouTube to File Downloader (YTtF)", you agree to the following terms:

1. No Liability: The Software is provided "as is" and without any warranty, either express or implied. Petrichor Systems, its author, and contributors will not be held liable for any damages, including but not limited to direct, indirect, special, incidental, or consequential damages arising out of the use or inability to use the Software.

2. No Responsibility for Data Loss: Petrichor Systems, its author, and contributors are not responsible for any data loss that may occur as a result of using the Software. It is the user's responsibility to regularly backup their data.

3. All Rights Reserved: The Software is protected by copyright and other intellectual property laws. All rights are reserved by Petrichor Systems. You may not distribute, modify, or reproduce the Software in any form without the express written permission of Petrichor Systems.

4. No Support: Petrichor Systems, its author, and contributors are under no obligation to provide support, maintenance, or updates for the Software.

5. Governing Law: This agreement shall be governed by and construed in accordance with the laws of the United States of America.

By using the Software, you acknowledge that you have read, understood, and agreed to be bound by the terms and conditions of this disclaimer and license notice.

PetrichorDawn
Email: ab123456now@gmail.com
Petrichor Systems
"""
    tkinter.messagebox.showinfo("Disclaimer", disclaimer_text)


# Main application window
main_window = Tk()
main_window.geometry("960x540")
main_window.resizable(False, False)
main_window.title("YTtF")
main_window.configure(bg="#D3D3D3")  # Set background color to light gray

# Global variables
checkbox_states = [True, True, True, True]

# Colors
gunmetal = "#292D38"
charcoal = "#373f51"
platinum = "#D8DBE2"
orange_web = "#FAA916"

# Styles
title_label_style = Style()
title_label_style.configure(
    "title_label_style.TLabel",
    background=charcoal,
    foreground=platinum,
    font=("Segoe UI", 30, "bold"),
)

label_style = Style()
label_style.configure(
    "label_style.TLabel",
    background=charcoal,
    foreground=platinum,
    font=("Segoe UI", 10, "bold"),
)

checkbox_style = Style()
checkbox_style.configure(
    "checkbox_style.TCheckbutton", background=gunmetal, foreground=platinum
)

background_tile = Style()
background_tile.configure("background_tile.TFrame", background="#373f51")

# Assigns all of the values for the grid. 'i' is the width, 16, and 'j' is the height, 9.
frames = {
    (i, j): Frame(
        main_window, height=540 / 9, width=960 / 16, style="background_tile.TFrame"
    )
    for i in range(16)
    for j in range(9)
}
for i, j in frames:
    frames[i, j].grid(row=j, column=i)


# Widgets and UI elements
verticalSeparator = Separator(
    main_window, orient="vertical", style="separator.TSeparator"
)
verticalSeparator.grid(row=2, column=7, columnspan=2, rowspan=6, sticky="ns")
horizontalSeparator = Separator(
    main_window, orient="horizontal", style="separator.TSeparator"
)
horizontalSeparator.grid(row=1, column=1, columnspan=14, rowspan=2, sticky="ew")

disclaimer_button = tkinter.Button(
    main_window,
    text="Show Disclaimer",
    command=show_disclaimer,
    font=("Segoe UI", 10),
    activebackground=gunmetal,
    activeforeground=platinum,
    bg=charcoal,
    fg=platinum,
)
disclaimer_button.grid(row=8, column=7, rowspan=3, columnspan=2, sticky="ew")


titleLabel = Label(
    main_window,
    text="YouTube to File Downloader (YTtF)",
    style="title_label_style.TLabel",
)
titleLabel.grid(row=0, column=2, columnspan=12, rowspan=2)

urlLabel = Label(main_window, text="Playlist URL:", style="label_style.TLabel")
urlLabel.grid(row=2, column=0, columnspan=3)
urlBox = tkinter.Entry(main_window, width=40, background=gunmetal, foreground=platinum)
urlBox.grid(row=2, column=2, columnspan=6)

url_type_option = tkinter.StringVar(value="Playlist")
url_type_options = ["Playlist", "Single"]
for index, file_option in enumerate(url_type_options):
    url_radio_button = tkinter.Radiobutton(
        main_window,
        text=file_option,
        variable=url_type_option,
        value=file_option,
        bg=charcoal,
        fg=platinum,
        activebackground=gunmetal,
        activeforeground=platinum,
        indicatoron=0,
        selectcolor=gunmetal,
    )
    url_radio_button.grid(row=2, column=index + 4, rowspan=2)


directoryLabel = Label(
    main_window, text="Output directory:", style="label_style.TLabel"
)
directoryLabel.grid(row=3, column=0, columnspan=3, rowspan=2)
directoryButton = tkinter.Button(
    main_window,
    text="Select via Explorer",
    command=get_directory,
    font=("Segoe UI", 10),
    activebackground=gunmetal,
    activeforeground=platinum,
    bg=charcoal,
    fg=platinum,
)
directoryButton.grid(row=4, column=2, columnspan=6)
directoryBox = tkinter.Entry(
    main_window, width=40, background=gunmetal, foreground=platinum
)
directoryBox.grid(row=3, column=2, columnspan=6, rowspan=2)

file_selection_label = Label(
    main_window,
    text="Select a file type:\n     (Click one)",
    style="label_style.TLabel",
)
file_selection_label.grid(row=5, column=0, columnspan=3)

selected_file_option = tkinter.StringVar(value=".mp3")
file_type_options = [".mp3", ".flac"]
for index, file_option in enumerate(file_type_options):
    file_radio_button = tkinter.Radiobutton(
        main_window,
        text=file_option,
        variable=selected_file_option,
        value=file_option,
        bg=charcoal,
        fg=platinum,
        activebackground=gunmetal,
        activeforeground=platinum,
        indicatoron=0,
        selectcolor=gunmetal,
    )
    file_radio_button.grid(row=5, column=index + 4)

checkbox_values = [BooleanVar() for _ in range(4)]
checkbox_frame = tkinter.Frame(
    main_window, background=gunmetal, borderwidth=3, relief="sunken"
)
checkbox_frame.grid(row=6, column=2, columnspan=6, rowspan=2, sticky="n")

checkbox_label = Label(main_window, text="File Options:", style="label_style.TLabel")
checkbox_label.grid(row=6, column=0, columnspan=3, rowspan=1)

checkbox1_var = tkinter.BooleanVar(value=True)
checkbox1 = Checkbutton(
    checkbox_frame,
    text="Image",
    variable=checkbox1_var,
    command=get_checkbox_states,
    style="checkbox_style.TCheckbutton",
)
checkbox1.grid(row=0, column=0, padx=5, pady=5, sticky="w")

checkbox2_var = tkinter.BooleanVar(value=True)
checkbox2 = Checkbutton(
    checkbox_frame,
    text="Rename",
    variable=checkbox2_var,
    command=get_checkbox_states,
    style="checkbox_style.TCheckbutton",
)
checkbox2.grid(row=0, column=1, padx=5, pady=5, sticky="w")

checkbox3_var = tkinter.BooleanVar(value=True)
checkbox3 = Checkbutton(
    checkbox_frame,
    text="Metadata",
    variable=checkbox3_var,
    command=get_checkbox_states,
    style="checkbox_style.TCheckbutton",
)
checkbox3.grid(row=1, column=0, padx=5, pady=5, sticky="w")

checkbox4_var = tkinter.BooleanVar(value=True)
checkbox4 = Checkbutton(
    checkbox_frame,
    text="Multi-threaded",
    variable=checkbox4_var,
    command=get_checkbox_states,
    style="checkbox_style.TCheckbutton",
)
checkbox4.grid(row=1, column=1, padx=5, pady=5, sticky="w")

thread_label = Label(
    main_window,
    text="# of Threads\n (ENTER 10\n IF YOU DO NOT KNOW\n WHAT A THREAD IS.)",
    style="label_style.TLabel",
)
thread_label.grid(row=7, column=0, columnspan=3, rowspan=2)
thread_box = tkinter.Spinbox(
    main_window,
    background=gunmetal,
    foreground=platinum,
    buttonbackground=gunmetal,
    from_=1,
    to=128,
)
thread_box.grid(row=7, column=2, columnspan=6, rowspan=2)

# Start button event handler
start_button = tkinter.Button(
    main_window,
    text="Activate Program",
    command=activate_program,
    font=("Segoe UI", 10),
    activebackground=gunmetal,
    activeforeground=platinum,
    bg=charcoal,
    fg=platinum,
)
start_button.grid(row=7, column=10, columnspan=4, rowspan=2)

# Create a text widget with dynamic text
error_box = tkinter.Text(
    main_window,
    wrap=tkinter.NONE,
    font=("Segoe UI", 10),
    state=tkinter.DISABLED,
    height=13,
    width=40,
    background=gunmetal,
    foreground=platinum,
)
error_box.grid(row=2, column=9, columnspan=6, rowspan=5, sticky="ew")

progress_box = tkinter.Frame(
    main_window,
    width=400,
    height=25,
    relief="sunken",
    borderwidth=2,
    background=gunmetal,
)
progress_box.grid(row=6, column=9, columnspan=6, rowspan=2)


frame_dimensions = {"width": 15 / 2, "height": 20, "borderwidth": 1}
MAX_PROGRESS_BARS = 40
progress_boxes = []
for column in range(MAX_PROGRESS_BARS):
    frame = tkinter.Frame(progress_box, **frame_dimensions, background=gunmetal)
    frame.grid(row=0, column=column)
    progress_boxes.append(frame)

miniframe_progress_boxes = []
miniframe_dimensions = {"width": 12 / 2, "height": 18, "borderwidth": 1}
for frame in progress_boxes[:MAX_PROGRESS_BARS]:
    miniframe = tkinter.Frame(
        progress_box, **miniframe_dimensions, background=platinum, relief="raised"
    )
    miniframe.grid(row=0, column=int(progress_boxes.index(frame)))
    miniframe_progress_boxes.append(miniframe)


def update_progress_bar():
    global song_denominator
    while song_denominator < song_numerator:
        percent_finished = song_denominator / song_numerator
        number_of_twenty = math.floor(MAX_PROGRESS_BARS * percent_finished)
        for i in range(number_of_twenty):
            miniframe_progress_boxes[i].configure(background="#00ff64")
        time.sleep(0.5)

    # Update progress bar after completion
    percent_finished = song_denominator / song_numerator
    number_of_twenty = math.floor(MAX_PROGRESS_BARS * percent_finished)
    for i in range(number_of_twenty):
        miniframe_progress_boxes[i].configure(background="#00ff64")


def on_closing():
    main_window.destroy()


main_window.protocol("WM_DELETE_WINDOW", on_closing)


# Run the application
if __name__ == "__main__":
    main_window.mainloop()
