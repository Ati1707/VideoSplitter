import os
import subprocess
import urllib.request
import zipfile
import shutil

def is_ffmpeg_installed():
    """Check if FFmpeg is installed by trying to run `ffmpeg -version`."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_ffmpeg():
    """Download the FFmpeg executable for Windows."""
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    output_path = 'ffmpeg-release-essentials.zip'
    print("Downloading FFmpeg...")
    urllib.request.urlretrieve(url, output_path)
    print("Download complete.")
    return output_path

def extract_ffmpeg(zip_path, extract_to='ffmpeg'):
    """Extract the downloaded FFmpeg zip file."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")
    os.remove(zip_path)

def move_ffmpeg_binaries(extract_to='ffmpeg'):
    """Move ffmpeg.exe and ffprobe.exe to the main directory."""
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            if file in ['ffmpeg.exe', 'ffprobe.exe']:
                shutil.move(os.path.join(root, file), file)
                print(f"Moved {file} to main directory.")
    shutil.rmtree(extract_to)

def check_download_ffmpeg():
    if is_ffmpeg_installed():
        print("FFmpeg is already installed.")
    else:
        print("FFmpeg is not installed.")
        zip_path = download_ffmpeg()
        extract_ffmpeg(zip_path)
        move_ffmpeg_binaries()
        print("FFmpeg installation complete. FFmpeg binaries have been moved to the main directory.")
