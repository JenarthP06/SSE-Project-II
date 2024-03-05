from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from supabase import create_client
from azure.eventhub import EventHubConsumerClient

load_dotenv()

app = Flask(__name__)

#url = os.environ.get("SUPABASE_URL")
#key = os.environ.get("SUPABASE_KEY")

def create_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)

supabase = create_supabase_client()

#supabase = create_client(url, key)


@app.route('/')
def index():
    response = supabase.table('userprofile').select('*').execute()
    if hasattr(response, 'data'):
        data = response.data
    else:
        data = []

    displayed_data = [{'username': row['username'], 'favorite_films': row['favorite_films']} for row in data]

    return render_template('index.html', users=displayed_data)

#def add_favorite():
    data = request.get_json()

    user_id = data.get('id')
    username = data.get('username')
    film = data.get('Favourites')


    if user_id and username and film:
        # Assuming you have a 'favorites' table in Supabase
        supabase.table('userprofile').upsert([{"id": user_id, "username": username, "Favourites":film}], on_conflict=['id'])
        return jsonify({"message": "Favourite film added successfully"}), 201
    else:
        return jsonify({"error": "Missing id, username, or Favourites"}), 400
    
#def on_event(partition_context, event):
    # Process the received event from Azure Event Hub
    print("Received event from partition: {}".format(partition_context.partition_id))
    print("Data: {}".format(event.body_as_str()))

    # Extract relevant data from the event
    user_id = event.body_as_json().get('user_id')
    film_title = event.body_as_json().get('film_title')

    if user_id and film_title:
        # Store the data in Supabase
        supabase.table('favorites').upsert([{"user_id": user_id, "film_title": film_title}], on_conflict=['user_id'])

#consumer_client = EventHubConsumerClient.from_connection_string(
    conn_str="your-event-hub-connection-string",
    consumer_group="$Default",
    eventhub_name="your-event-hub-name",
#)

#with consumer_client:
    consumer_client.receive(
        on_event=on_event,
        starting_position="-1",  # Start from the latest available event
    )


if __name__ == '__main__':
    app.run(debug=True)
