# Pilot Logbook Manager

A Django-based application for managing pilot logbook data, including robust import from JSON and export to ForeFlight-compatible CSV. Designed for extensibility and best practices.

---

## 🚀 Getting Started

### 1. **Clone the Repository**
```
git clone <your-repo-url>
cd Fleek
```

### 2. **Set Up Virtual Environment**
```
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. **Install Dependencies**
```
pip install -r requirements.txt
```

### 4. **Apply Migrations**
```
python manage.py migrate
```

---

## 📦 Usage

### **Import Data from JSON**
Import pilot logbook data from a JSON file (e.g., `Data/import - pilotlog_mcc.json`):
```
python manage.py import_data "Data/import - pilotlog_mcc.json"
```

### **Export Data to CSV**
Export all logbook data to a ForeFlight-compatible CSV file:
```
python manage.py export_data "export - logbook_template.csv"
```

---

## 🧪 Testing

### **Run Django Tests**
To run all tests (ensure you have test cases in `pilotlog/tests.py`):
```
python manage.py test pilotlog
```

---

## 🛠️ Project Structure
- `pilotlog/models.py` — Data models (Aircraft, Airport, Person, Flight)
- `pilotlog/services/importer.py` — Reusable JSON importer
- `pilotlog/services/exporter.py` — Reusable CSV exporter
- `pilotlog/management/commands/import_data.py` — CLI import command
- `pilotlog/management/commands/export_data.py` — CLI export command

---

## 🔄 Extending the App
- Add new fields to models in `pilotlog/models.py` as needed.
- Update `importer.py` and `exporter.py` to handle new fields or formats.
- Add new management commands for additional automation.

---

## 💡 Notes
- Ensure your JSON and CSV files match the expected schema for smooth import/export.
- All import/export logic is modular and reusable for future needs.

---

## 📧 Contact
For questions or improvements, please contact the project maintainer. 