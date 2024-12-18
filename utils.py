import aiohttp
import os
from tqdm.asyncio import tqdm
from dotenv import load_dotenv
import instaloader

# Load environment variables
load_dotenv()

FLIC_TOKEN = os.getenv("FLIC_TOKEN")
HEADERS = {
    "Flic-Token": FLIC_TOKEN,
    "Content-Type": "application/json",
}

async def get_upload_url():
    url = "https://api.socialverseapp.com/posts/generate-upload-url"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                if "url" in data and "hash" in data:
                    return data["url"], data["hash"]
                else:
                    print(f"Unexpected response format: {data}")
                    return None, None
            else:
                print(f"Failed to get upload URL: {response.status}")
                return None, None

async def upload_video(upload_url, file_path):
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as file:
            total_size = os.path.getsize(file_path)
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Uploading") as pbar:
                chunk_size = 1024 * 1024
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    async with session.put(upload_url, data=chunk) as response:
                        if response.status != 200:
                            print(f"Failed to upload {file_path}: {response.status}")
                            return False
                    pbar.update(len(chunk))
            print(f"Uploaded: {file_path}")
            return True

async def create_post(video_title, video_hash, category_id=1):
    url = "https://api.socialverseapp.com/posts"
    body = {
        "title": video_title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=HEADERS, json=body) as response:
            if response.status == 200:
                print(f"Post created: {video_title}")
            else:
                print(f"Failed to create post: {response.status}")

async def download_video(video_url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status == 200:
                total_size = int(response.headers.get('content-length', 0))
                with open(save_path, "wb") as file:
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                        async for data in response.content.iter_chunked(1024):
                            file.write(data)
                            pbar.update(len(data))
                print(f"Downloaded: {save_path}")
            else:
                print(f"Failed to download {video_url}: {response.status}")

async def get_video_url_from_page(page_url):
    return await get_instagram_video_url(page_url)

async def get_instagram_video_url(page_url):
    try:
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, page_url.split("/")[-2])
        video_url = post.video_url
        return video_url
    except Exception as e:
        print(f"Error extracting video URL: {e}")
        return None