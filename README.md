# CITS5505 Group Project

## Tech stack
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
### Creating the database


### After modifying the models

```bash
flask db migrate
flask db upgrade
```

## Explanations

- `app/` Contains the main application package.​
  - `auth/` Blueprint for authentication-related routes and forms.​
  - `main/` Blueprint for main application routes and forms
  - `error/` Error handling for this app
  - `static/` Contains static files i.e. CSS, Javascript, images
  - `__init__.py` Initializes your application creating a Flask app instance.
  - `models.py` Defines database models using SQLAlchemy.
  - `templates/` This is where you store your html templates i.e. index.html, layout.html
- `run.py` Contains the actual python code that will import the app and start the development server.
- `config.py` Stores configurations for your app.
- `tests/` Contains tests for this app. Use `pytest` in `bash` to run all the tests.
- `requirements.txt` this is where you store your package dependencies, you can use pip

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