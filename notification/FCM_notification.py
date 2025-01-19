import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def send_push_notification(token, title, body):
    """
    Sends a push notification to a specific device.
    
    Args:
        token (str): The FCM device token.
        title (str): The title of the notification.
        body (str): The body of the notification.
    """
    try:
        # Create a message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        
        # Send the message
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Example usage
if __name__ == "__main__":
    device_token = "your_device_fcm_token_here"  # Replace with the FCM token of the target device
    notification_title = "Hello"
    notification_body = "This is a test notification!"
    send_push_notification(device_token, notification_title, notification_body)
