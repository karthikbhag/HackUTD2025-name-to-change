# classify_posts.py

import joblib
import re
import json
from datetime import datetime
import ssl
import certifi
from atproto import Client
from geopy.geocoders import Nominatim
from pymongo import MongoClient
from dotenv import load_dotenv
import os
context = ssl.create_default_context(cafile=certifi.where())
load_dotenv()

USERNAME = os.getenv('BLUESKY_USERNAME')
PASSWORD = os.getenv('BLUESKY_PASSWORD')
MONGODB_URI = os.getenv('MONGODB_URI')
def preprocess_text(text):
    if not text:
        return ""
    text = str(text).lower()
    return re.sub(r'[^a-zA-Z\s]', '', text)

def load_names(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return {line.strip().lower() for line in file if line.strip()}

def extract_location(text, filename='Final_List.txt'):
    cities = load_names(filename)
    found = [city for city in cities if re.search(r'\b' + re.escape(city) + r'\b', text.lower())]
    return found

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="city_coordinates_extractor", ssl_context=context)
    location = geolocator.geocode(city_name, timeout=30)
    if location:
        return location.latitude, location.longitude
    return None

def fetch_disaster_related_posts(username, password, search_terms=None, days_back=3):
    if search_terms is None:
        search_terms = ["disaster", "emergency", "earthquake", "hurricane", "flood", "wildfire", "tornado", "tsunami"]

    try:
        client = Client()
        client.login(username, password)

        feed_uris = [
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejsyozb6iq',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejwgffwqky',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejxlobe474',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejy45orees',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejqjms3noe'
        ]

        posts = []
        for uri in feed_uris:
            feed = client.app.bsky.feed.get_feed({'feed': uri, 'limit': 25})
            for post in feed.feed:
                text = post.post.record.text.lower()
                if any(term in text for term in search_terms):
                    posts.append({
                        'text': post.post.record.text,
                        'created_at': post.post.record.created_at,
                        'author': post.post.author.handle,
                        'uri': post.post.uri
                    })
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

def save_to_mongodb(client, data):
    try:
        db = client['bluesky_db']
        collection = db['Classified_Data']

        inserted_count = 0
        for item in data['predictions']:
            # Check if the report already exists using the 'report' or 'uri' field
            if not collection.find_one({'report': item['report'], 'date': item['date']}):  # or use 'uri' if available
                collection.insert_one(item)
                inserted_count += 1

        print(f"Saved {inserted_count} new documents to MongoDB.")
    except Exception as e:
        print(f"MongoDB error: {e}")

def main():
    # Load model, vectorizer, and label encoder
    try:
        clf = joblib.load('model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        label_encoder = joblib.load('label_encoder.pkl')
    except Exception as e:
        print("Model files not found. Run `train_model.py` first.")
        return

    def predict_disaster(text):
        processed = preprocess_text(text)
        vectorized = vectorizer.transform([processed])
        prediction = clf.predict(vectorized)[0]
        disaster_type = label_encoder.inverse_transform([prediction])[0]
        is_disaster = "Not a disaster" if disaster_type.lower() == 'none' else "Disaster"
        return is_disaster, disaster_type

    username = USERNAME
    password = PASSWORD
    posts = fetch_disaster_related_posts(username, password, days_back=3)

    results = {'predictions': []}
    for post in posts:
        is_disaster, disaster_type = predict_disaster(post['text'])
        found_cities = extract_location(post['text'])
        locations = []

        if found_cities:
            coords = get_coordinates(found_cities[0].title())
            if coords:
                locations.append({'city': found_cities[0].title(), 'latitude': coords[0], 'longitude': coords[1]})

        results['predictions'].append({
            'name': disaster_type,
            'location': locations[0]['city'] if locations else '',
            'latitude': locations[0]['latitude'] if locations else '',
            'longitude': locations[0]['longitude'] if locations else '',
            'report': post['text'],
            'disaster_level': is_disaster,
            'date': post['created_at']
        })
    try:
        mongo_client = MongoClient(MONGODB_URI)
        save_to_mongodb(mongo_client, results)
    except Exception as e:
        print("MongoDB connection error.")


if __name__ == "__main__":
    main()

def lambda_handler(event=None, context=None):
    main()
    return {
        "statusCode": 200,
        "body": json.dumps("Classification completed.")
    }