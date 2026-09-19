# Phonics Adventure

A playful phonics game for practicing letters, sounds, and beginning words.

## Web version

The static web app lives in `index.html`, `styles.css`, and `app.js`. Run it locally with:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. The browser's speech synthesis API powers the sound buttons.

Every push to `main` deploys the web version to GitHub Pages through `.github/workflows/deploy-pages.yml`.

## Python version

Install the dependencies and run the original desktop game:

```bash
pip install -r requirements.txt
python3 main.py
```
