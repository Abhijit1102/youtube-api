
from flask import Flask, render_template, redirect, url_for, request
from googleapiclient.discovery import build
import logging

# // extract the channels 
api_key ="AIzaSyAMZMPK66pQ39jJDv7oXOFTDpkboOzWUFg"

channel_id =["UCphU2bAGmw304CFAzy0Enuw"]
# channel_ids = ','.join(channel_ids)
youtube = build('youtube','v3',developerKey = api_key)

application = Flask(__name__)
app = application

@app.route('/')
def home():
    try:
       return render_template('home.html')
    except Exception as e:
        logging.error(f"e")


@app.route('/result', methods=['GET'])

try:
        
    def result():
        def get_video_ids(youtube, playlist_id):
            video_ids = []
            next_page_token = None
            while True:
                request = youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                for item in response["items"]:
                    video_ids.append(item["contentDetails"]["videoId"])
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            return video_ids


        def getchannelStats(youtube, channel_id):
            requests = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=','.join(channel_id))
            response = requests.execute()
            final = list()
            for i in range(len(response['items'])):
                playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                urls = [f'https://www.youtube.com/watch?v={video_id}' for video_id in get_video_ids(youtube, playlist_id)[:5]]
                data = dict(channel_name=response['items'][i]['snippet']['title'],
                            playlist_id=playlist_id,
                            urls=urls)
                final.append(data)
            return final
            
        def get_video_details(youtube, video_ids):
            all_video_stats = []
            requests = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids[:5])
            )
            response = requests.execute()

            for video in response['items']:
                video_stats = dict(
                    Title=video['snippet']['title'],
                    Published_date=video['snippet']['publishedAt'],
                    views=video['statistics']['viewCount'],
                )
                all_video_stats.append(video_stats)

            return all_video_stats

    # Get the channel data for the specified channel ID
        channel_data = getchannelStats(youtube, channel_id)

        # Get the video IDs for the first playlist of the first channel
        playlist_id = channel_data[0]['playlist_id']
        video_ids = get_video_ids(youtube, playlist_id)[:5]

        # Get the thumbnail URLs for the specified video IDs
        thumbnail_urls = []
        for video_id in video_ids:
            request = youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()

            # Check if the response has any items
            if len(response["items"]) > 0:
                # Extract the thumbnail URL from the response
                thumbnail_url = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
                # Append the thumbnail URL to the list
                thumbnail_urls.append(thumbnail_url)
            else:
                print(f"No items found in response for video ID {video_id}.")

        # Get the video details for the specified video IDs
        video_details = get_video_details(youtube, video_ids)

        # Combine all the fetched data into a list of dictionaries
        data = []
        for i in range(len(video_details)):
            video_data = {
                'Title': video_details[i]['Title'],
                'urls': channel_data[0]['urls'][i],
                'Published_date': video_details[i]['Published_date'],
                'views': video_details[i]['views'],
                'thumbnail_url': thumbnail_urls[i]
            }
            data.append(video_data)

        return render_template('result.html', data=data)
except Exception as e:
    logging.error(f"e")


@app.route('/submit', methods=['POST'])

try:       
    def submit():
        if request.form['submit_button'] == 'Click Here':
            return redirect(url_for('result'))
except Exception as e :
    logging.error(f"e")

if __name__ == '__main__':
    
    app.run(debug=True)
