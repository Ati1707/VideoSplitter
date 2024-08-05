import os
import subprocess
import tkinter as tk
from tkinter import filedialog

import Downloader


def select_file():
    """Open a file dialog to select a video file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a video file",
                                           filetypes=[("Video files", "*.mp4;*.mkv;*.avi;*.mov")])
    return file_path


def get_user_choice():
    """Get the user's choice for splitting the video."""
    print("\nChoose an option:")
    print("1. Split by duration")
    print("2. Split by parts")
    choice = input("Enter 1 or 2: ").strip()
    return choice


def get_video_name(video_path):
    """Extract the base name and extension from the video path."""
    video_name_base = os.path.splitext(os.path.basename(video_path))[0]
    video_name_extension = os.path.splitext(video_path)[1].lstrip('.')
    return video_name_base, video_name_extension


def split_video_by_duration(video_path, duration):
    """Split the video by duration using ffmpeg."""
    video_name_base, video_name_extension = get_video_name(video_path)
    output_pattern = f"{video_name_base}_part_%03d.{video_name_extension}"

    command = [
        'ffmpeg', '-i', video_path, '-c', 'copy', '-map', '0',
        '-segment_time', duration, '-reset_timestamps', '1', '-f', 'segment', output_pattern
    ]
    subprocess.run(command)
    print(f"Video split into parts by duration {duration} successfully.")


def split_video_into_parts(video_path, parts):
    """Split the video into specified number of parts using ffmpeg and ffprobe."""
    command = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration = float(result.stdout.strip())

    part_duration = duration / parts
    duration_str = f"{int(part_duration // 3600):02}:{int((part_duration % 3600) // 60):02}:{int(part_duration % 60):02}"

    video_name_base, video_name_extension = get_video_name(video_path)
    output_pattern = f"{video_name_base}_part_%03d.{video_name_extension}"

    command = [
        'ffmpeg', '-i', video_path, '-c', 'copy', '-map', '0',
        '-segment_time', duration_str, '-reset_timestamps', '1', '-f', 'segment', output_pattern
    ]
    subprocess.run(command)
    print(f"Video split into {parts} parts successfully.")


def main():
    Downloader.check_download_ffmpeg()
    video_path = select_file()
    if not video_path:
        print("No file selected. Exiting.")
        return

    video_name_base, video_name_extension = get_video_name(video_path)
    choice = get_user_choice()

    if choice == '1':
        duration = input("Enter the duration to split (e.g., 00:10:00 for 10 minutes): ").strip()
        print(f"Splitting the video '{video_name_base}' by duration: {duration}")
        split_video_by_duration(video_path, duration)
    elif choice == '2':
        parts = int(input("Enter the number of parts to split the video into: ").strip())
        print(f"Splitting the video '{video_name_base}' into {parts} parts.")
        split_video_into_parts(video_path, parts)
    else:
        print("Invalid choice. Exiting.")
        return


if __name__ == "__main__":
    main()
