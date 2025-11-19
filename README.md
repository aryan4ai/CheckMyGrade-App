# CheckMyGrade (Lab 1 starter in my Masters course in San Jose State {subject: DATA200, i.e. Python})

Console-based Python app for managing students, courses, professors, and grades using CSV persistence.

## Files
- `main.py` – run the app (simple console)
- `models.py` – dataclasses for core entities
- `security.py` – reversible password "encryption" demo (XOR + Base64)
- `storage.py` – CSV helpers
- `services.py` – CRUD, search, sort, stats, reports

## Data files (CSV)
- `data/students.csv`
- `data/course.csv`
- `data/professors.csv`
- `data/login.csv`

> Note: The lab requires **CSV**, not Excel, and **four** CSVs: students, course, professors, login.

## How to run
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python main.py
```

No third-party packages are required.
