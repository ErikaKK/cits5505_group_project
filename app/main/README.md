# Main Routes

This module handles the main landing page of the application.

## Key Features

| Feature      | Description                                               |
| ------------ | --------------------------------------------------------- |
| Landing Page | Serves the main entry point of the application            |
| Auth Status  | Displays different content based on authentication status |

## Routes

| Route | Method | Description                     | Authentication Required |
| ----- | ------ | ------------------------------- | --------------------- |
| /     | GET    | Display the application homepage | No                    |

## Template Variables

| Variable | Type    | Description                           |
| -------- | ------- | ------------------------------------- |
| title    | string  | Page title set to "Home"              |
| login    | boolean | Current user's authentication status  |


