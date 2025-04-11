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
### Clone the Repository
```bash
git clone git@github.com:ErikaKK/groupProject.git
```
### Navigate to the Project Directory
```bash
cd yourProjectDirectory
```

### Create a New Virtual Environment:
```bash
python3 -m venv venv
```
- Ensure not to commit the virtual environment directory to the version control system 
- Add `.gitignore` in your virtual environment directory:
```bash
cd venv/
touch .gitignore
```
- Or add `venv/` to `.gitignore`
```bash
echo "venv/" >> .gitignore
```
### Activate the Virtual Environment:
- On macOS/Linux:

```bash

source venv/bin/activate
```
- On Windows:

```bash

.\venv\Scripts\activate
```

### Start the APP
```bash
python3 run.py
```
### Install Project Dependencies:
```bash
pip install -r requirements.txt
```
### After Adding New Project Dependencies:
```bash
pip freeze > requirements.txt

```
### After modifying the models 
```bash
flask db migrate
flask db upgrade
```
## Explanation
- `app/` Contains the main application package.​

- `auth/` Blueprint for authentication-related routes and forms.​

- `main/` Blueprint for main application routes and forms
- `run.py` contains the actual python code that will import the app and start the development server.
- `config.py` stores configurations for your app.
- `__init__.py` initializes your application creating a Flask app instance.
- `views.py` this is where routes are defined.
- `models.py` Defines database models using SQLAlchemy.
- `static/` contains static files i.e. CSS, Javascript, images
- `templates/` this is where you store your html templates i.e. index.html, layout.html
- `requirements.txt` this is where you store your package dependancies, you can use pip

## Project Workflow:
1. create an issue
2. assign yourself to an issue and **work on a new branch (not main branch)**
3. create a pull request when you solve the issue
4. another team member review this pull request
5. merge your work branch into main branch

- Creating issues
  - everyone can create issues
  - issue title need to be clear
  - add tags (frontend, backend, etc)

- Communication
  - can directly comment in issues or PRs because we all wfh
  - please respond within 2 days
