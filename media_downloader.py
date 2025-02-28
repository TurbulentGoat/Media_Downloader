import os
import subprocess
import urllib.parse

# Determine the folder where this script is located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_yt_dlp_installed():
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: yt-dlp is not installed. Please install it using 'pip install yt-dlp'.")
        return False
    return True

def is_playlist(url):
    # Simple heuristic: if the URL contains the "list=" parameter, it's likely a playlist.
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    return "list" in query_params

def download_audio(url):
    # For music downloads (e.g., YouTube Music)
    output_dir = os.path.join(BASE_DIR, "Music")
    os.makedirs(output_dir, exist_ok=True)
    
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--yes-playlist" if is_playlist(url) else "--no-playlist",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    try:
        print(f"Downloading audio from: {url}")
        subprocess.run(command, check=True)
        print(f"Audio download complete! Files saved in '{output_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to download audio.\n{e}")

def download_video(url):
    # Video with audio
    output_dir = os.path.join(BASE_DIR, "Videos")
    os.makedirs(output_dir, exist_ok=True)
    
    command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "--yes-playlist" if is_playlist(url) else "--no-playlist",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    try:
        print(f"Downloading video (with audio) from: {url}")
        subprocess.run(command, check=True)
        print(f"Video download complete! Files saved in '{output_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to download video.\n{e}")

def download_video_no_audio(url):
    # Video only, no audio
    output_dir = os.path.join(BASE_DIR, "Videos", "video_only")
    os.makedirs(output_dir, exist_ok=True)
    
    command = [
        "yt-dlp",
        "-f", "bestvideo",
        "--yes-playlist" if is_playlist(url) else "--no-playlist",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    try:
        print(f"Downloading video (no audio) from: {url}")
        subprocess.run(command, check=True)
        print(f"Video (no audio) download complete! Files saved in '{output_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to download video (no audio).\n{e}")

def download_audio_from_video(url):
    # Audio only extracted from a video (different folder from music)
    output_dir = os.path.join(BASE_DIR, "Videos", "audio_from_video")
    os.makedirs(output_dir, exist_ok=True)
    
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--yes-playlist" if is_playlist(url) else "--no-playlist",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    try:
        print(f"Downloading audio (extracted from video) from: {url}")
        subprocess.run(command, check=True)
        print(f"Audio extraction complete! Files saved in '{output_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to extract audio from video.\n{e}")

def main():
    if not ensure_yt_dlp_installed():
        return

    print("Select download type:")
    print("1. Video")
    print("2. Music")
    download_type = input("Enter your choice (1 or 2): ").strip()
    if download_type not in ("1", "2"):
        print("Invalid choice. Exiting.")
        return

    url = input("Enter the link: ").strip()
    if not url:
        print("Error: No URL provided.")
        return

    if download_type == "2":
        download_audio(url)
    else:
        print("For video downloads, choose an option:")
        print("1. Video with audio")
        print("2. Video only (no audio)")
        print("3. Audio only (extracted from video)")
        option = input("Enter your choice (1, 2, or 3): ").strip()

        if option == "1":
            download_video(url)
        elif option == "2":
            download_video_no_audio(url)
        elif option == "3":
            download_audio_from_video(url)
        else:
            print("Invalid option. Exiting.")

if __name__ == "__main__":
    main()
