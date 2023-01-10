from flask import Flask, render_template, request
import requests
import cs50

db = cs50.SQL("sqlite:///summary.db")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the url from the form
        url = request.form['url']
        api_url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer"

        # Set up the payload and headers for the API request
        payload = {
            "url": url,
            "text": "",
            "sentnum": 5
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "227964e341msh0ab40beaf225cb8p1ba9d5jsn613e11f2e03c",
            "X-RapidAPI-Host": "textanalysis-text-summarization.p.rapidapi.com"
        }

        # Make the API request
        response = requests.request("POST", api_url, json=payload, headers=headers)

        # Extract the summary sentences from the API response
        summary_sentences = response.json()['sentences']

        summary_output = ' '.join(summary_sentences)

        # Create requests table
        db.execute("CREATE TABLE IF NOT EXISTS requests (search_id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, summary TEXT)")

        # Insert request into requests table
        db.execute("INSERT INTO requests (url, summary_output) VALUES (?, ?)", url, summary_output)

        # Render the summary page with the summary sentences
        return render_template('index.html', summary_sentences=summary_sentences)
    else:
        # Render the home page
        return render_template('index.html')
       
