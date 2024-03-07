import os
from dotenv import load_dotenv
from supabase import create_client
from azure.servicebus import ServiceBusClient
import json


load_dotenv()


supabase = create_client(
    os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
    )


def insert_user_data(username):
    response = supabase.table('user-profile').insert(
        {"username": username}
        ).execute()
    if hasattr(response, 'error') and response.error:
        print(f"Error updating user {username}: {response.error}")
    else:
        print(f"User {username} updated successfully.")


def process_service_bus_messages():
    service_bus_client = ServiceBusClient.from_connection_string(
        conn_str=os.environ.get("SERVICE_BUS_CONNECTION_STRING")
        )
    with service_bus_client:
        receiver = service_bus_client.get_queue_receiver(
            queue_name='userprofile-queue'
            )
        with receiver:
            for msg in receiver:
                try:
                    message_body_bytes = b''.join(b for b in msg.body)
                    message_body_str = message_body_bytes.decode('utf-8')
                    message_body = json.loads(message_body_str)
                    eventType = message_body['eventType']
                    username = message_body['username']
                    # Can add other event types to listen for
                    # e.g. loginmicroservice sends eventType
                    # = 'UserDeleted', then delete from
                    # this database using extra if statement
                    if eventType == "UserRegistered":
                        insert_user_data(username)
                        receiver.complete_message(msg)
                except Exception as e:
                    print(f"Error processing message: {e}")
                    receiver.dead_letter_message(msg)


if __name__ == '__main__':
    process_service_bus_messages()
