import psycopg2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from psycopg2 import sql
from datetime import datetime
from pytz import utc
from config import YOUTUBE_API_KEY, DB_CONFIG, CHANNEL_ID, MAX_VIDEOS_PER_CHANNEL, MAX_COMMENTS_PER_VIDEO

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

def get_channel_videos(channel_id):
    videos = []
    try:
        search_response = youtube.search().list(
            channelId=channel_id,
            type='video',
            part='id,snippet',
            maxResults=MAX_VIDEOS_PER_CHANNEL
        ).execute()

        while search_response:
            for search_result in search_response.get('items', []):
                if search_result['id']['kind'] == 'youtube#video':
                    videos.append(search_result['id']['videoId'])
            
            if 'nextPageToken' in search_response and len(videos) < MAX_VIDEOS_PER_CHANNEL:
                search_response = youtube.search().list(
                    channelId=channel_id,
                    type='video',
                    part='id,snippet',
                    maxResults=MAX_VIDEOS_PER_CHANNEL - len(videos),
                    pageToken=search_response['nextPageToken']
                ).execute()
            else:
                break

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
    return videos

def get_video_comments(video_id):
    comments = []
    try:
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=MAX_COMMENTS_PER_VIDEO
        ).execute()

        while results:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'video_id': video_id,
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })

            if 'nextPageToken' in results and len(comments) < MAX_COMMENTS_PER_VIDEO:
                results = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=MAX_COMMENTS_PER_VIDEO - len(comments),
                    pageToken=results['nextPageToken']
                ).execute()
            else:
                break

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')

    return comments

def bulk_insert_comments(comments):
    insert_query = sql.SQL("""
        INSERT INTO youtube_comments (video_id, author, comment_text, like_count, published_at)
        VALUES (%s, %s, %s, %s, %s)
    """)
    
    data = [(
        comment['video_id'],
        comment['author'],
        comment['text'],
        comment['likes'],
        datetime.strptime(comment['published_at'], "%Y-%m-%dT%H:%M:%SZ").astimezone(utc)
    ) for comment in comments]
    
    cur.executemany(insert_query, data)
    conn.commit()

def main():
    videos = get_channel_videos(CHANNEL_ID)
    
    total_comments = 0
    for video_id in videos:
        comments = get_video_comments(video_id)
        bulk_insert_comments(comments)
        total_comments += len(comments)
        print(f"Inserted {len(comments)} comments for video {video_id}")

    print(f"Total inserted comments: {total_comments}")

if __name__ == "__main__":
    main()

cur.close()
conn.close()