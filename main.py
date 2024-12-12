import asyncio
import os
import hashlib
from utils import get_upload_url, upload_video, create_post, download_video, get_video_url_from_page
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

VIDEO_DIR = "./videos"

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".mp4"):
            asyncio.run(process_video(event.src_path))

async def process_video(file_path):
    try:
        # Get upload URL and hash
        upload_url, video_hash = await get_upload_url()
        if not upload_url or not video_hash:
            return

        # Upload video
        uploaded = await upload_video(upload_url, file_path)
        if not uploaded:
            return

        # Create a post
        video_title = os.path.basename(file_path).split(".")[0]
        await create_post(video_title, video_hash)

        # Delete local file
        os.remove(file_path)
        print(f"Deleted local file: {file_path}")
    except Exception as e:
        print(f"Error processing video {file_path}: {e}")

async def monitor_directory():
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, VIDEO_DIR, recursive=False)
    observer.start()
    print("Monitoring directory for new videos...")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def list_videos(directory):
    print("================================================================")
    print("Current videos in directory:")
    for file_name in os.listdir(directory):
        if file_name.endswith(".mp4"):
            print(f" - {file_name}")
    print("================================================================")

async def upload_existing_videos(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(".mp4"):
            file_path = os.path.join(directory, file_name)
            await process_video(file_path)

async def main():
    try:
        choice = input("Choose an option:\n1. Upload from URL\n2. Start monitoring directory\nEnter 1 or 2: ")
        if choice == '1':
            # Take page URL from the user
            page_url = input("Enter the Instagram page URL: ")
            video_url = await get_video_url_from_page(page_url)
            if not video_url:
                print("Failed to extract video URL from the page")
                return
            
            # Generate a valid file name
            file_name = hashlib.md5(video_url.encode()).hexdigest() + ".mp4"
            save_path = os.path.join(VIDEO_DIR, file_name)
            
            await download_video(video_url, save_path)

            # Upload the downloaded video
            await process_video(save_path)

            # List videos in the directory
            list_videos(VIDEO_DIR)

            # Start monitoring directory
            await monitor_directory()
            
        elif choice == '2':
            # Check and upload existing videos in the directory
            await upload_existing_videos(VIDEO_DIR)

            # Start monitoring directory
            await monitor_directory()
        else:
            print("Invalid choice. Please enter 1 or 2.")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
    asyncio.run(main())