# Video Bot

This project is a video bot that downloads videos from Instagram and uploads them to a server. It also monitors a directory for new videos and uploads them automatically.

## Features

- Download videos from Instagram using a page URL.
- Upload downloaded videos to a server.
- Monitor a directory for new videos and upload them automatically.
- Display progress bars for downloading and uploading videos.

## Requirements

- Python 3.7+
- `aiohttp`
- `tqdm`
- `python-dotenv`
- `instaloader`
- `watchdog`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Kaushik-Shahare/video-bot.git
    cd video-bot
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install aiohttp tqdm python-dotenv beautifulsoup4 instaloader watchdog
    ```

4. Create a `.env` file in the root directory and add your environment variables:

    ```env
    FLIC_TOKEN=your_flic_token_here
    ```

## Usage

1. Run the script:

    ```sh
    python main.py
    ```

2. Follow the prompts to enter the Instagram page URL.

3. The script will download the video, upload it to the server, and monitor the `videos` directory for new videos.

## Directory Structure

```plaintext
video-bot/ 
├── .env 
├── .gitignore 
├── README.md 
├── main.py 
├── utils.py 
└── videos/
```

## Notes

- Ensure that the `videos` directory exists in the root directory. The script will create it if it does not exist.
- The script will automatically upload any existing videos in the `videos` directory at startup.
- The script uses the `watchdog` library to monitor the `videos` directory for new videos and upload them automatically.
