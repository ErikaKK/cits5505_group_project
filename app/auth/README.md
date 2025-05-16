# Authentication Routes

- This module handles user authentication, including login, registration, and logout functionality.
- path: `/auth`

## Key Features

| Feature             | Description                                                     |
| ------------------ | --------------------------------------------------------------- |
| User Registration  | Create new account with username, email, and password           |
| User Login        | Authenticate with email and password, with remember-me option    |
| User Logout       | Secure session termination                                       |
| Duplicate Check   | Prevent duplicate usernames and emails during registration       |
| Flash Messages    | Provide feedback for authentication actions                      |
| Session Management| Handle user sessions and authentication state                    |

## Routes

| Route      | Method | Description                                           | Authentication Required |
| ---------- | ------ | ----------------------------------------------------- | --------------------- |
| /login     | GET    | Display login form                                    | No                    |
| /login     | POST   | Process login attempt                                 | No                    |
| /logout    | GET    | Log out current user                                  | Yes                   |
| /register  | GET    | Display registration form                             | No                    |
| /register  | POST   | Process new user registration                         | No                    |

## Security Features

- Password hashing
- CSRF protection
- Session management
- Remember-me functionality
- Duplicate account prevention
- Authentication state checking

## Form Validation

### Registration Form
- Username validation
- Email format validation
- Password strength requirements
- Password confirmation matching

### Login Form
- Email format validation
- Password validation
- Remember-me option

## Flash Messages

### Success Messages
- "Your account has been created! You can now log in."

### Error Messages
- "Invalid username or password"
- "Username or email already exists. Please choose a different one."

## Dependencies

- Flask-Login for authentication management
- SQLAlchemy for database operations
- WTForms for form handling
- Werkzeug for password hashing

