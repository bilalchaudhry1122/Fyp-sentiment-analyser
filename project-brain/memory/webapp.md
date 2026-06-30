# Web Application
- Framework: Flask
- Endpoints:
  - `/` (GET) -> `templates/index.html` dashboard home
  - `/analyze` (POST) -> run hybrid sentiment and mental health analysis pipeline
- Scripts: `src/app.py`, `src/routes/views.py`, `src/routes/analyze.py`
- Frontend UI: `templates/base.html`, `templates/index.html`, `templates/results.html`, `static/css/style.css`, `static/js/analyze.js`
