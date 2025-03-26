#Lab 08
from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

NASA_API_KEY = "DEMO_KEY"  # Replace with your actual API key
APOD_URL = "https://api.nasa.gov/planetary/apod"


def get_apod(date=None):
    """Fetch the APOD from NASA API for a given date (or today's date)."""
    params = {"api_key": NASA_API_KEY}
    if date:
        params["date"] = date

    response = requests.get(APOD_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.route('/')
def home():
    """Landing page that shows the APOD for today."""
    apod_data = get_apod()
    return render_template("index.html", apod=apod_data)


@app.route('/history', methods=['GET', 'POST'])
def history():
    """History page where users can input a date to fetch past APODs."""
    apod_data = None
    error_message = None
    today_date = datetime.today().strftime('%Y-%m-%d')  # Get today's date

    if request.method == 'POST':
        date = request.form.get('date')
        try:
            datetime.strptime(date, "%Y-%m-%d")  # Validate format
            apod_data = get_apod(date)
        except Exception:
            error_message = "Invalid date or API error. Try again."
    
    return render_template('history.html', apod=apod_data, error=error_message, today_date=today_date)


if __name__ == '__main__':
    app.run(debug=True)
# HTML Templates

templates = {
    "index.html": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NASA APOD - Home</title>
    </head>
    <body>
        <h1>Astronomy Picture of the Day</h1>
        <p>Date: {{ apod.date }}</p>
        <img src="{{ apod.url }}" alt="APOD">
        <p>{{ apod.explanation }}</p>
        {% if apod.copyright %}
            <p>Copyright: {{ apod.copyright }}</p>
        {% endif %}
        <br>
        <a href="/history">View APOD History</a>
    </body>
    </html>
    """,
    "history.html": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NASA APOD - History</title>
    </head>
    <body>
        <h1>Search for a Past APOD</h1>
        <form method="post">
            <label for="date">Select a date:</label>
            <input type="date" id="date" name="date" min="1995-06-16" max="{{ "now"|date("Y-m-d") }}" required>
            <button type="submit">Get APOD</button>
        </form>
        {% if apod %}
            <p>Date: {{ apod.date }}</p>
            <img src="{{ apod.url }}" alt="APOD">
            <p>{{ apod.explanation }}</p>
            {% if apod.copyright %}
                <p>Copyright: {{ apod.copyright }}</p>
            {% endif %}
        {% elif error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
}

# Save templates to files
import os
os.makedirs("templates", exist_ok=True)
for filename, content in templates.items():
    with open(f"templates/{filename}", "w") as f:
        f.write(content)
