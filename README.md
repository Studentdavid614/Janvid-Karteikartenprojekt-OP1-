![image_URL](https://github.com/Studentdavid614/Janvid-Karteikartenprojekt-OP1-/blob/main/Bild.png?raw=true)
(Bild Startseite)

# OP1-Karteikarten
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Dieses Projekt zeigt den Aufbau einer webbasierten Applikation konstruiert mit NiceGUI, fokussiert auf sauberer Architektur, Daten validierung und dem intergrieren von Datenbanken
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Die Applikation beschäftigt sich hauptsächlich mit folgenden Dingen:

- den gesamten Prozess von der Anforderungsanalyse bis zur Implementierung abzudecken
- fortgeschrittene Python-Konzepte in einer webbasierten Anwendung anzuwenden
- Datenvalidierung, eine geschichtete Architektur und den Einsatz eines ORMs zu demonstrieren
- sauberen, wartbaren und gut getesteten und wartbaren Code zu erstellen
- Teamarbeit sowie professionelle Dokumentation zu unterstützen

📝 Anwenungsanforderungen des Projekts:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Viele Schülerinnen und Schüler haben Probleme mit grossen Mengen an Unterrichtsstoff auswendig zu lernen. Dazu greifen die meisten zu einer LernAPP. Grundsätzlich eine gute Idee jedoch besitzen viele Lern-Apps nicht über die gewünschten Funktionen oder sind Kostenpflichtig. Beides nicht optimal für einen Schüler/inn.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Szenario
Die Applikations gibt uns die Möglichkeit für:
- Das erstellen eines personellem LogIn
- Das Eintragen von neuem Lernstoff in Form von Karteikarten
- Das Einteilen von dem eigefügten Lernstoff in verschiedene Klassen bzw. Fächer
- Aus den erstellten karteikarten eine Liste erstellen
- Die erstellten Listen teilen mit anderen Benutzern
- Das Lernen von den eingetragenen Karteikarten (Lernmodi)
- Das Prüfen von den gelerneten Karteikarten (Prüfungsmodi)
   - Analyse der geprüften Karteikarten, Anzahlt richtig / falsch
- Das Bearbeiten von den einegetragenen Karteikarten (Bearbeitungsmodi)
- Das Löschen von den eingetragenen Karteikarten (Löschmodi)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📖 User Stories
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. LogIn:
Als Benutzer richte ich mir ein eigens Konto ein mit einer Email und einem geschützten Passwort. Danach kann ich mich damit immer wieder ein und aus loggen.
- Inputs: Email und Passwort
- Outputs: None
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2. View Menü:
Als Benutzer dieser Applikation will ich als erstes das Hauptmenü sehen mit den darin enthaltenen Hauptfunktionen.
- (Löschen, Bearbeiten, Hinzufügen, Lernen, Prüfen)
- Inputs: None
- Output: main functions
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
3. Hinzufügen von Karteikarten:
Als Benutzer will ich meinen Lernstoff in Fomr von karteikarten hinzufügen.
- Input: Karteikarten 
- Output: Updated Karteikartenliste 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
4. Kartenlisten erstellen:
Nachdem ich als Benutzer meine Karten erstellt habe um diese zu lernen oder zu prüfen, habe ich die Möglichkeit diese als Liste zu speichern um sie später wieder gezielt zu lernen ohne dass ich alle Karten zusammen lernen muss. ZUdem kann ich diese Liste dann mit anderen Benutzern teilen oder selbst die Listen von anderen Benutzern lernen.
- Inputs: list.ID
- Outputs: updated lists
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
5. Menü sehen um Hauptfunktion zu wählen:
Als Benutzer will ich nach dem hinzufügen meiner Karteikarten eine Liste sehen mit allen möglichen Hauptfunktionen.
- Inputs: none
- outputs: view mainfunctions
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
6. Resultate ansehen:
Als Benutzer will ich sehen wie meine Leistungen waren in den gewählten Hauptfunktionen wie lernen oder prüfen
- Inputs: none
- Outputs: results
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
7. Karteikarten zurücksetzen:
Als Benutzer will ich meine veralteten Karteikarten welche ich in den Modi (lernen und Prüfung) nicht mehr brauche, bearbeiten oder sogar löschen.
- Inputs: mainfunction löschen, bearbeiten
- Output: Updated Karteikartenliste txt.file
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
8. Neue Karteikarten hinzufügen:
Als Benutzer will ich nachdem meine alten Karteikarten gelöscht bzw. bearbeitet wurden neue Karteikarten hinzufügen.
- Input: mainfunction hinzufügen
- output: updated Karteikartenliste 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🧩 Use Cases
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
![image_URL](https://github.com/Studentdavid614/David---Jana-OP1-Karteikartensystem/blob/main/BILD%20USE%20CASES.png?raw=true)

(Bild Use Cases)
Main cases:
- View Mainfunctions
  - Karteikarte Hinzufügen
  - Fächer spezifische Listen aus den Karteikarten erstellen
  - Listen mit andern Usern teilen
  - Karteikarten Bearbeiten
  - Karteikarten Lernen
  - Karteikarten Prüfen
  - Karteikarten Löschen
Schauspieler:
- User
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Wireframes / Mockups

![image_URL](https://github.com/Studentdavid614/Janvid-Karteikartenprojekt-OP1-/blob/main/Bild%20(2).png?raw=true)
(Bild Konto erstellen)
![image_URL](https://github.com/Studentdavid614/Janvid-Karteikartenprojekt-OP1-/blob/main/Bild%20(1).png?raw=true)
(Bild Lernmodi)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Tech Stack
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```text
Frontend
- NiceGUI

Backend
- Python
- FastAPI

Database
- SQLite
- SQLModel
- SQLAlchemy

Authentication & Security
- JWT Authentication
- BCrypt Password Hashing

Testing
- Pytest

Deployment & DevOps
- Docker
- Docker Compose
```
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Architektur
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Die Applikation folgt einer Layered Architecture mit klarer Trennung von Verantwortlichkeiten:
```text
Presentation Layer (NiceGUI Pages)
    ↓
Application Layer (main.py)
    ↓
Business Logic Layer (services.py)
    ↓
Data Access Layer (models.py, db.py, auth.py)
    ↓
Database Layer (SQLite via SQLModel)
```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Projektstruktur
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
```text
app/
├── main.py              # NiceGUI Routes und UI Pages
├── models.py            # SQLModel Datenmodelle
├── db.py                # Datenbank-Initialisierung
├── auth.py              # Authentifizierung & Sicherheit
├── services.py          # Business Logic
├── pdf_export.py        # PDF-Generierung
├── import_cards.py      # CSV/JSON Import
└── seed_data.py         # Test-Datengenerator

tests/
├── test_models.py       # Model Unit Tests
└── test_services.py     # Service Integration Tests

requirements.txt         # Python Dependencies
README.md                # User Guide
DEVELOPMENT.md           # Entwickler-Dokumentation
.env.example             # Umgebungsvariablen Template
Dockerfile               # Container Image Definition
docker-compose.yml       # Multi-Container Setup
setup.py                 # Setup Automation Script
```
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Beispiel für eine Teststruktur
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
```python
def test_something(isolated_services):
    """Test description."""
    
    svc = isolated_services

    # Setup
    result = svc.my_function()

    # Assert
    assert result is not None
    assert result.value == expected_value
```
```bash
pytest tests/
```
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Datenbank-Modelle
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
User
Speichert Benutzerinformationen mit gehashtem Passwort.

- id: Primary Key
- username: Eindeutig, Index für schnelle Lookups
- email: Eindeutig für Registrierung
- password_hash: BCrypt Hash, niemals Klartext speichern!
- created_at: Audit-Trail

```text
User
├── 1:N CardSets
├── 1:N SetPermissions
└── 1:N LearningHistory

CardSet
├── N:1 User
├── 1:N Cards
└── 1:N SetPermissions

Card
├── N:1 CardSet
└── 1:N LearningHistory
```

```text
SQLite + SQLModel
```
----------------------------------------------------------------------------------------------
🗄️ORM
![image_URL](https://github.com/Studentdavid614/David---Jana-OP1-Karteikartensystem/blob/main/BILD%20ORM.png?raw=true)
(Bild ORM)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
👥 Team & Contributions

- David:   Nice GUI-Frontend, Routing, PDF-Export, Statistik-Dashboard
- Jana: 	 Datenmodellierung, Service-Layer, Authentifizierung, Test-Framework
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
