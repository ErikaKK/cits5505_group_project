# Message System 

path: `/messages`

## Key Features

| Feature             | Description                                               |
| ------------------- | --------------------------------------------------------- |
| Start Conversation  | Search by user's email and create a new conversation      |
| Send Message        | Send a text message and a .json file (optional)           |
| Inbox/Sent/All View | Filter messages by receiver/sender role                   |
| Table Rendering     | JSON file (if attached) is shown as a readable HTML table |

## Routes

| Route               | Method | Description                                  |
| ------------------- | ------ | -------------------------------------------- |
| /messages           | GET    | Load the message page                        |
| /messages/send      | POST   | Send a new message (text and/or JSON)        |
| /messages/find_user | POST   | Find a user by email to start a conversation |

## (For Developers) Utility

`messages/utils.py` enable developers to send messages programmatically without HTTP requests in other module.


```python
from app.messages.utils import send_message_internal

send_message_internal(
    sender_id=current_user.id,         # User ID of sender
    receiver_email="target@example.com", # Email address of receiver
    message="Analysis complete! Please check the attached summary.",
    shared_data=None  # Optional, however, it must be read directly from spotify api
)
```

**Must read it before calling it**

- If the receiver email does not exist, a `ValueError` will be raised.
- Shared_data must be a **JSON-serializable object** if provided, and no validator is provided.
  - Please check it after calling it to validate your correct usage.
