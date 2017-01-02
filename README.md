# Fantasy

Sets up draft spreadsheets and automates scoreboards

Built for use in FRC Team 687's Fantasy FIRST System. See game rules [here](https://docs.google.com/document/d/1XDRi5UZszs_nBqM6RU9CGxQQGKnNz4FOEwigU6gbvTY/edit?usp=sharing)

### Dependencies
- Python 3.4+
- requests
- gsheets

### Setup
1. Generate a Google Developer project
2. Create a service account with edit access. Place json file in home directory and point to it in `settings.py`
3. Gather participant names and place them in `src/comp/participants.csv` or in another csv document arranged in the same manner. If using another csv document, point to it in `settings.py`
4. Put admin names and emails in `src/comp/admins.csv`. Admins are people who will receive edit access to draft and scoreboards. It is highly recommended to place these into a google drive folder and share the folder will all the participants.
