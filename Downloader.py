import os
import subprocess
import urllib.request
import zipfile
import shutil
import re
import time


def is_ffmpeg_installed():
    """Check if FFmpeg is installed by trying to run `ffmpeg -version`."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_local_ffmpeg_version():
    result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, text=True, check=True)
    version_line = result.stdout.splitlines()[0]
    match = re.search(r'ffmpeg version (\d+\.\d+\.\d+)', version_line)
    return match.group(1)


def get_latest_ffmpeg_version():
    url = 'https://www.gyan.dev/ffmpeg/builds/release-version'
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def delete_existing_ffmpeg():
    for exe in ['ffmpeg.exe', 'ffprobe.exe']:
        if os.path.exists(exe):
            os.remove(exe)


def is_ffmpeg_update_available():
    local_version = get_local_ffmpeg_version().replace('.', '')
    latest_version = get_latest_ffmpeg_version().replace('.', '')

    if int(latest_version) > int(local_version):
        print("Update available!")
        delete_existing_ffmpeg()
        download_ffmpeg()


def download_ffmpeg():
    """Download the FFmpeg executable for Windows."""
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    output_path = 'ffmpeg-release-essentials.zip'
    print("Downloading FFmpeg...")
    urllib.request.urlretrieve(url, output_path)
    print("Download complete.")
    extract_ffmpeg(output_path)


def extract_ffmpeg(zip_path, extract_to='ffmpeg'):
    """Extract the downloaded FFmpeg zip file."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")
    time.sleep(2)
    os.remove(zip_path)
    move_ffmpeg_binaries()


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
        if os.path.exists('ffmpeg.exe'):
            print("Checking if newer version is available...")
            is_ffmpeg_update_available()
    else:
        print("FFmpeg is not installed.")
        download_ffmpeg()
        print("FFmpeg installation complete. FFmpeg binaries have been moved to the main directory.")
