import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL to scrape and make a request to the page
url = os.environ.get("TARGET_URL", "https://www.author-summit.com/agenda")
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract all the events from the page
    events = []

    for event in soup.find_all("a", class_="schedule-event w-inline-block"):
        time = event.find("div", class_="schedule-event-time").get_text(strip=True)
        title = event.find("h6").get_text(strip=True)
        description = event.find("p", class_="schedule-event-description").get_text(
            strip=True
        )
        speaker = event.find("div", class_="schedule-speaker-name")
        speaker_name = speaker.get_text(strip=True) if speaker else "No speaker listed"
        events.append(
            {
                "time": time,
                "title": title,
                "description": description,
                "speaker": speaker_name,
            }
        )

    # Convert events to a pandas DataFrame
    df = pd.DataFrame(events)

    # Display and save the dataframe
    pd.set_option("display.max_colwidth", None)
    df[["time", "title"]].to_csv("events.csv", index=False)
    print(df[["time", "title"]].to_string(index=False))
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
