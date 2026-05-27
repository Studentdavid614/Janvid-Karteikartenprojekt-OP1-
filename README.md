# Karteikarten - Learning Card Application

Eine moderne NiceGUI-Applikation zum Erstellen, Lernen und Verwalten von Karteikarten mit User-Management, Sharing-Funktionalität und Statistiken.

## Features

- **User-Management**: Registrierung und Login mit Passwort-Hashing
- **Karteikartensets**: Erstelle, bearbeite und organisiere Karteikarten in Sets
- **Sharing & Permissions**: Teile Sets mit anderen Benutzern mit Bearbeitungsberechtigung
- **Public/Private Sets**: Sets können öffentlich oder privat sein
- **Lernmodus**: Interaktiver Lernmodus mit Kartenumdrehen
- **Statistiken**: Umfassende Lernstatistiken und Fortschrittsanzeige
- **PDF-Export**: Exportiere Karteikartensets als PDF zum Ausdrucken
- **Modern Design**: Yellow-Theme mit responsivem NiceGUI-Layout

## Technologien

- **Frontend**: NiceGUI
- **Backend**: Python, FastAPI (via NiceGUI)
- **Datenbank**: SQLite mit SQLModel/SQLAlchemy
- **Security**: bcrypt für Passwort-Hashing, python-jose für JWT
- **PDF**: ReportLab für PDF-Generierung
- **Testing**: pytest

## Schnellstart

### 1. Virtuelles Environment erstellen

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# oder macOS/Linux
source venv/bin/activate
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Datenbank mit Beispieldaten füllen (optional)

```bash
# Demo-Benutzer erstellen und ~1000 Beispielkarten importieren
python -m app.seed_data
```

Dies erstellt einen Demo-Benutzer:
- **Username**: demo
- **Passwort**: demo123

Und 5 öffentliche Karteikartensets mit jeweils ~200 Karten:
- English Vocabulary
- Geography
- History
- Mathematics
- Science

### 4. Applikation starten

```bash
python -m app.main
```

Die App läuft dann unter `http://localhost:8080`

## Verwendung

### Registrierung & Login

1. Besuche die App unter `http://localhost:8080/login`
2. Klicke auf "Registrieren" um einen neuen Account zu erstellen
3. Gib Benutzername, E-Mail und Passwort ein
4. Nach erfolgreicher Registrierung wirst du automatisch angemeldet

### Karteikartensets erstellen

1. Klicke auf "Neues Set erstellen" auf der Hauptseite
2. Gib einen Namen und optionale Beschreibung ein
3. Wähle, ob das Set privat oder öffentlich sein soll
4. Klicke "Erstellen"

### Karten hinzufügen

1. Öffne ein Set durch Klick auf "Bearbeiten"
2. Fülle "Frage" und "Antwort" ein
3. Klick "Hinzufügen" um die Karte hinzuzufügen
4. Wiederhole für alle Karten

### Lernen

1. Klicke "Lernen" auf einem Set
2. Lese die Frage
3. Klick "Antwort zeigen" um die Antwort zu sehen
4. Markiere "Richtig" oder "Falsch"
5. Die App zeigt automatisch die nächste Karte

### Sets teilen

1. Öffne ein Set (muss dein eigenes sein)
2. Klicke "Teilen"
3. Wähle die Sichtbarkeit (Privat/Öffentlich)
4. Gib Benutzernamen ein um Berechtigungen zu vergeben
5. Wähle zwischen "Ansehen" oder "Bearbeiten"
6. Klick "Hinzufügen"

### Statistiken ansehen

1. Klick "Statistik" im Header
2. Sieh deine Gesamtstatistiken (Beantwortet, Richtig, Falsch, Genauigkeit)
3. Sieh Fortschritt pro Set (Beherrschte Karten, Genauigkeit)

### PDF exportieren

1. Auf der Hauptseite oder in öffentlichen Sets
2. Klick das PDF-Button neben einem Set
3. Das PDF wird automatisch heruntergeladen

## Kartendaten importieren

### CSV-Format

Erstelle eine CSV-Datei mit den Spalten `front,back`:

```csv
front,back
Was ist die Hauptstadt von Frankreich?,Paris
Was ist 2+2?,4
```

### JSON-Format

Erstelle eine JSON-Datei mit folgendem Format:

```json
[
  {
    "front": "Was ist die Hauptstadt von Frankreich?",
    "back": "Paris"
  },
  {
    "front": "Was ist 2+2?",
    "back": "4"
  }
]
```

### Daten importieren

In Python:

```python
from app.import_cards import import_from_csv, import_from_json

# Aus CSV
result = import_from_csv('cards.csv', 'username', 'Set Name', 'Beschreibung')

# Aus JSON
result = import_from_json('cards.json', 'username', 'Set Name')

print(f"Importiert: {result['imported']} Karten")
print(f"Fehler: {len(result['errors'])}")
```

## Datenbank

Die App verwendet SQLite unter `karteikarten.db`. Um die Datenbank zurückzusetzen, lösche einfach diese Datei und starte die App neu.

## Tests

```bash
# Alle Tests ausführen
pytest

# Mit Coverage
pytest --cov=app tests/
```

## Struktur

```
app/
  ├── main.py              # NiceGUI Applikation und alle Pages
  ├── db.py                # Datenbankverbindung
  ├── models.py            # SQLModel Datenmodelle
  ├── auth.py              # Authentifizierung und Passwort-Hashing
  ├── services.py          # Business Logic (CardSets, Cards, Permissions, Stats)
  ├── pdf_export.py        # PDF-Generierung
  ├── import_cards.py      # CSV/JSON Import Utilities
  └── seed_data.py         # Beispieldaten Generator
tests/
  ├── test_models.py       # Model Tests
  └── test_services.py     # Service Tests
requirements.txt           # Python Dependencies
README.md                  # Dieser File
```

## Datenbankmodelle

### User
- id: Eindeutige User-ID
- username: Eindeutiger Benutzername
- email: Eindeutige E-Mail
- password_hash: Gehashtes Passwort
- created_at: Erstellungsdatum

### CardSet
- id: Eindeutige Set-ID
- name: Name des Sets
- description: Beschreibung
- creator_id: Ersteller (User-ID)
- visibility: PRIVATE oder PUBLIC
- created_at, updated_at: Zeitstempel

### Card
- id: Eindeutige Karten-ID
- card_set_id: Set-ID (Fremdschlüssel)
- front: Frage/Vorderseite
- back: Antwort/Rückseite
- correct_count, incorrect_count: Statistiken

### SetPermission
- card_set_id: Set-ID (Fremdschlüssel)
- user_id: User-ID (Fremdschlüssel)
- permission_level: VIEW oder EDIT
- granted_at: Wann die Berechtigung gewährt wurde

### LearningHistory
- id: Eindeutige Eintrags-ID
- user_id: User-ID (Fremdschlüssel)
- card_id: Karten-ID (Fremdschlüssel)
- is_correct: Ob die Antwort richtig war
- answered_at: Wann beantwortet

## Theme-Anpassung

Das Yellow-Theme ist in `main.py` in den Konstanten definiert:

```python
PRIMARY_COLOR = "#FFB800"        # Hauptgelb
SECONDARY_COLOR = "#FF9500"      # Orange
DARK_BG = "#1a1a1a"              # Dunkler Hintergrund
LIGHT_TEXT = "#ffffff"           # Heller Text
CARD_BG = "#2d2d2d"              # Kartenhintergrund
```

Um ein anderes Theme zu verwenden, ändere einfach diese Hex-Codes.

## Lizenz

Dieses Projekt wurde als Teil von "OP1 - Projektorientiertes Programmieren" an der FHNW erstellt.

## Support

Bei Fragen oder Issues, kontaktiere den Kursleiter oder erstelle ein Issue im Repository.

