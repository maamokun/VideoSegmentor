import os
from pytube import YouTube

# Directory paths
url_file = 'vids.txt'
output_dir = 'input'

def download_video(url, output_dir):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        stream.download(output_path=output_dir)
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def download_videos_from_file(url_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(url_file, 'r') as file:
        urls = file.readlines()
    
    for url in urls:
        url = url.strip()
        if url:
            download_video(url, output_dir)

# Run the download process
download_videos_from_file(url_file, output_dir)

print("All downloads complete! UwU 🎉")
