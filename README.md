# Phonics Adventure

A playful phonics game for practicing letters, sounds, and beginning words. This repository contains both the original Python desktop app and a static web app.

## Web app

### Use it locally

The web app has no build step or package installation. Start a local web server from the project folder:

```bash
python3 -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000) in a browser. Use the **Learn** tab to move through the alphabet, listen to letter sounds, and hear example words. Use the **Quiz** tab to choose the matching word and earn stars.

The sound buttons use the browser's built-in Speech Synthesis API. If speech is unavailable in a browser, the rest of the app still works normally.

### Use it on GitHub Pages

Every push to `main` runs [.github/workflows/deploy-pages.yml](.github/workflows/deploy-pages.yml), which publishes the static files to GitHub Pages. The deployed site is:

<https://ankit210689.github.io/phonics_adventure/>

## Desktop app

### Install and run

The desktop version uses Python, Pygame for the window and graphics, and `pyttsx3` for text-to-speech. From the project folder, create an optional virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pygame pyttsx3
python3 main.py
```

On macOS or Linux, use `source venv/bin/activate`. On Windows PowerShell, activate the environment with `venv\Scripts\Activate.ps1` instead. Close the game window to exit.

## How the code works

### Shared learning data

[`data/letters.py`](data/letters.py) stores the alphabet as a list of dictionaries. Each letter includes its uppercase and lowercase forms, phonics label, spoken sound, example word, emoji, quiz choices, and correct answer. The desktop app imports this list directly. The web app contains the same data in [`app.js`](app.js) so it can run as a self-contained static site without a Python server.

### Desktop flow

[`main.py`](main.py) initializes Pygame, creates the game window, and maintains the current letter, mode, feedback, and star count. Each frame draws either the learning screen or quiz screen. Mouse clicks are checked against the button rectangles to navigate letters, play speech, select quiz answers, and award stars. `pyttsx3` speaks the current letter, sound, or word through the computer's installed voice.

### Web flow

[`index.html`](index.html) defines the page structure, including the learning panel, quiz panel, controls, progress display, and accessible labels. [`styles.css`](styles.css) provides the responsive layout and visual design for desktop and mobile screens. [`app.js`](app.js) manages the current letter, quiz question, score, tab switching, answer feedback, navigation, and browser speech. Button event listeners update the DOM whenever the learner changes letters or answers a question.

The web app is client-side only: all state lives in the browser while the page is open, and no account or server database is required.

## Project structure

```text
phonics_adventure/
├── main.py                         # Python/Pygame desktop app
├── index.html                      # Web app markup
├── styles.css                      # Web app styling
├── app.js                          # Web app behavior and data
├── data/letters.py                 # Desktop alphabet and quiz data
├── .github/workflows/deploy-pages.yml
│                                   # GitHub Pages deployment
└── requirements.txt                # Python dependency file
```

## Development checks

Check the browser JavaScript syntax and Python syntax before committing:

```bash
node --check app.js
python3 -m py_compile main.py data/letters.py
```
