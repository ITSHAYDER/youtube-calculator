import re
from datetime import timedelta
from googleapiclient.discovery import build

YOUTUBE_API = "youtube_api_key"

def calculate_playlist_duration(playlist_id):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API)

    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    total_seconds = 0

    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute()

        vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(vid_ids)
        )

        vid_response = vid_request.execute()

        for item in vid_response['items']:
            duration = item['contentDetails']['duration']

            hours = int(hours_pattern.search(duration).group(1)) if hours_pattern.search(duration) else 0
            minutes = int(minutes_pattern.search(duration).group(1)) if minutes_pattern.search(duration) else 0
            seconds = int(seconds_pattern.search(duration).group(1)) if seconds_pattern.search(duration) else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_seconds += video_seconds

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            break

    total_seconds = int(total_seconds)

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return hours, minutes, seconds




