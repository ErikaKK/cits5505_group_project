# CITS5505 Group Project

## What We Do（Purpose）
- Discover Your Spotify Listening Journey

- Transform your Spotify listening history into interactive visualizations and share your music journey with others. Our platform offers:

### Comprehensive Analytics Dashboard:
- 🎵 Top 5 Artists & Tracks - See who and what you've played the most
- ⏰ Daily Rhythm - Visualize your listening patterns throughout the day
- 📈 Monthly Trends - Track how your music habits evolve over time
- 📅 Custom Date Range - Focus on specific time periods for deeper insights

### Social Features:
- 🔄 Share Analytics - Send your listening data to other registered users
- 💬 Messaging System - Discuss music tastes through our built-in messenger
- 👥 Community - View and explore dashboards shared by other users

### Quick Search:
- 🔍 Instant Track Info - Look up any song details using its Spotify ID
- 🎯 No Registration Required - Access basic search features as a guest

### Privacy & Security:
- 🔒 Secure Sharing - Share your data only with chosen users
- 👤 User Authentication - Protected access to personal dashboard
- 📊 Data Control - Manage who sees your listening history

## Contributors
### Masters Group 64
| UWA ID              | Name | Github Username                           |
| ------------------- | ------ | -------------------------------------------- |
| 24071068       | Erica Kong | ErikaKK                  |
| 24422053      | Vincent Ma | iviiincent                |
| 24231774  | Nikhil Chadha | nikhilchadha28     |
| 24085253| Chenglin Hou  | 24085253|

## Tech Stack
- HTML
- CSS
- Tailwind
- JQuery
- Flask
- AJAX/Websockets
- SQLite interfaced to via the SQLAlchemy package

## Get Started

### Python Version

This project requires **Python 3.9.18**. Please ensure you're using this version to avoid compatibility issues.

### Clone the Repository

```bash
git clone git@github.com:iviiincent/cits5505_group_project.git yourProjectDirectory
```

### Navigate to the Project Directory

```bash
cd yourProjectDirectory
```

### Create a New Virtual Environment:

1. With venv:
    ```bash
    # create environment
    python3.9 -m venv venv
    
    # activate environment
    source venv/bin/activate    # macOS/Linux
    .\venv\Scripts\activate     # Windows
    ```
2. Or with conda:
    ```bash
    # create environment
    conda create -n yourEnvName python=3.9.18

    # activate environment
    conda activate yourEnvName
    ```

### Manage Dependencies:

- Install dependency:
  ```bash
  pip install -r requirements.txt
  ```
- Add new dependency:
  ```bash
  pip install <package-name>

  # commit in requirements.txt
  pip freeze > requirements.txt
  ```

### Start the APP

```bash
python3 run.py
```
### Create the database
```bash
flask db upgrade
```

- If you encounter database issues:
```bash
# Remove existing database
rm instance/app.db

# Reset migrations
flask db stamp base

# Reapply all migrations
flask db upgrade
```

### After modifying the models
```bash
flask db migrate
flask db upgrade
```

## Testing

### Unit Tests
#### Tests individual components of the application:
- Messages
- Security
- Homepage UI
- Visualisation
- Error handling

#### Run unit tests:
```bash
# Run all tests
python -m pytest tests/test_unit.py

# Run specific test class
python -m pytest tests/test_unit.py -k TestModels

# Run with coverage report
coverage run -m pytest tests/test_unit.py
coverage report
```
### Selenium Tests
#### Tests user interface and form interactions:
- Login flow
- Registration flow
- Form validation
- Login UI styling
- Upload page

#### Run tests:
```bash
# Start Flask server. Make sure the server running on http://127.0.0.1:5000
flask run  

# Run tests
pytest tests/test_selenium.py -v
```
## Explanations

- `app/` Contains the main application package.​
  - `__init__.py` Initializes the application creating a Flask app instance.
  - `models.py` Defines database models using SQLAlchemy.
  - `main/` Blueprint for main application routes and forms. [Main Routes Documentation](app/main/README.md)
  - `auth/` Blueprint for authentication-related routes and forms. [Authentication Documentation](app/auth/README.md)
  - `account/` Blueprint for account management routes and forms.[Account Management Documentation](app/account/README.md)
  - `messages/` Blueprint for messages routes and forms.[Messages System Documentation](app/messages/README.md)
  - `error/` Error handling for this app.
  - `templates/` This is where html templates i.e. index.html, layout.html are stored.
  - `static/` Contains static files i.e. CSS, Javascript, images.
- `run.py` Contains the actual python code that will import the app and start the development server.
- `config.py` Stores configurations for the app.
- `requirements.txt` This is where package dependencies are stored.
- `tests/` Contains tests for this app. Use `pytest` in `bash` to run all the tests.
- `migrations/` Migration historys.

## Visualisation
This feature allows user to use their Spotify music history data (.json extension file) to display 4 different personalised graphs. This makes user to understand their music listening behaviours.

### Features
- `Top 5 Artists Played graph`
   Displays top 5 artists played by user by taking sum of minutes played.
- `Top 5 Tracks Played graph`
   Displays top 5 Tracks Played by user by taking sum of minutes played.
- `Monthly Listening Time (in Hours)`
   Displays monthly time spend in listening music by user by taking sum of time of music played.
- `Average Minutes Played`
   Displays the average of minutes spend by user on listening to music each hour of any day.

### Technologies used
- `Python`: to open json file and help stucturing visual dashboard
- `Pandas`: to handle json file data and stucture that to table form
- `Matplotlib`: to create visualisation graphs.

## Project Workflow:
1. create an issue
2. assign yourself to an issue and **work on a new branch (not main branch)**
3. create a pull request when you solve the issue
4. another team member review this pull request
5. merge your work branch into main branch
6. add references to `README.md` if needed

- Creating issues
  - everyone can create issues
  - issue title need to be clear
  - add tags (frontend, backend, etc)

- Communication
  - can directly comment in issues or PRs because we all wfh
  - message on Teams group chat if you need
  - please respond within 2 days

## References

- [https://jinja.palletsprojects.com/en/stable/templates/](https://jinja.palletsprojects.com/en/stable/templates/)
- [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [https://fonts.google.com/icons](https://fonts.google.com/icons")
- [https://rapidapi.com/Glavier/api/spotify23](https://rapidapi.com/Glavier/api/spotify23)
- [https://swiperjs.com/get-started](https://swiperjs.com/get-started)
- [https://support.stats.fm/docs/import/spotify-import](https://support.stats.fm/docs/import/spotify-import)
