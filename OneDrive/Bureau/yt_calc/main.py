from flask import Flask, render_template, request, redirect, url_for, session
from calculate import calculate_playlist_duration
from googleapiclient.discovery import build
import re
def format_duration(duration):
    days, remainder = divmod(duration, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_duration = ""
    if days > 0:
        formatted_duration += f"{days} days, "
    if hours > 0:
        formatted_duration += f"{hours} hours, "
    if minutes > 0:
        formatted_duration += f"{minutes} minutes, "
    if seconds > 0 or not formatted_duration:
        formatted_duration += f"{seconds} seconds"

    return formatted_duration

def extract_youtube_playlist_id(link):
    playlist_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'playlist\?list=([^&=%\?]+)'
    )

    match = re.match(playlist_regex, link)
    if match:
        id =  match.group(5)
        hours, minutes, seconds = calculate_playlist_duration(id)
        total_seconds = hours * 3600 + minutes * 60 + seconds
        duration = format_duration(total_seconds)
        return duration  # Return the extracted duration as the result
    else:
        return "Invalid YouTube playlist link."

app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"  # Replace with a secret key for session

@app.route('/', methods=['POST', 'GET'])
def show_page():
    duration = None  # Initialize the duration to None

    if request.method == "POST":
        youtube_link = request.form.get("url")
        duration = extract_youtube_playlist_id(youtube_link)
        session['duration'] = duration  # Store the duration in the session

    return render_template('calculator.html', duration=duration)

if __name__ == '__main__':
    app.run(debug=True)