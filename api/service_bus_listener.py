import os
from dotenv import load_dotenv
from supabase import create_client
from azure.servicebus import ServiceBusClient
import json

load_dotenv()

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def insert_user_data(username):
    response = supabase.table('user-profile').insert({"username": username}).execute()
    if response.error:
        print(f"Error updating user {username}: {response.error}")
    else:
        print(f"User {username} updated successfully.")

def process_service_bus_messages():
    service_bus_client = ServiceBusClient.from_connection_string(conn_str=os.environ.get("SERVICE_BUS_CONNECTION_STRING"))
    with service_bus_client:
        receiver = service_bus_client.get_subscription_receiver(
            topic_name='user-events',
            subscription_name='user-profile-updates'
        )
        with receiver:
            for msg in receiver:
                try:
                    message_body = json.loads(msg.body.decode('utf-8'))
                    username = message_body['username']

                    insert_user_data(username)
                    receiver.complete_message(msg)
                except Exception as e:
                    print(f"Error processing message: {e}")
                    receiver.dead_letter_message(msg)

if __name__ == '__main__':
    print("Starting to listen for Service Bus messages...")
    process_service_bus_messages()
