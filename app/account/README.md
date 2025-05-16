# Account Management and Spotify Data visualisation

- This module handles user account management, Spotify data upload, visualisation, and data sharing functionality.
- path: `/account`

## Key Features

| Feature                | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| Profile Management    | Update username, email, and personal information             |
| Password Management   | Secure password change functionality                         |
| Data Upload          | Upload and merge Spotify listening history JSON files        |
| Data visualisation   | Interactive dashboard showing listening patterns              |
| Data Sharing         | Share selected date ranges of listening data with other users |
| Conflict Resolution  | Smart handling of overlapping or conflicting data uploads     |

## Routes

| Route                    | Method | Description                                           |
| ----------------------- | ------ | ----------------------------------------------------- |
| /profile                | GET    | View profile information                              |
| /profile                | POST   | Update profile information                            |
| /change_password        | GET    | Display password change form                          |
| /change_password        | POST   | Process password change                               |
| /user-info              | GET    | Get current user information                          |
| /upload                 | GET    | Display upload page                                   |
| /upload-file            | POST   | Process JSON file upload                              |
| /replace-data           | POST   | Replace existing Spotify data                         |
| /share-data             | POST   | Share Spotify data with another user                  |
| /dashboard              | GET    | Display visualisation dashboard                       |
| /visualise/date-range   | GET    | Get available date range for visualisation            |
| /visualise/dashboard    | POST   | Generate visualisation for selected date range        |

## Data visualisation Features

- Top 5 Artists Chart
- Top 5 Tracks Chart
- Monthly Listening Time Distribution
- Average Daily Listening Patterns
- Custom Date Range Selection
- Interactive Dashboard

## Data Upload Features

- Smart Data Merging
- Conflict Detection
- Timestamp Overlap Handling
- Data Validation
- Progress Feedback

## Security Features

- Login Required Protection
- CSRF Protection
- Password Hashing
- Email Verification
- Data Access Control

## Error Handling

- Duplicate Username/Email Detection
- Invalid Date Range Handling
- File Format Validation
- Database Transaction Management
- Detailed Error Messages

## API Response Formats

### Success Response
```json
{
    "success": true,
    "message": "Operation successful",
    "details": {
        "new_entries_added": 100
    }
}
