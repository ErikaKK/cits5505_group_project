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

