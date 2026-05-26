![image_URL](https://github.com/Studentdavid614/Janvid-Karteikartenprojekt-OP1-/blob/main/Bild.png?raw=true)

# OP1-Karteikarten
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Dieses Projekt zeigt den Aufbau einer webbasiertern Applikation konstruiert mit NiceGUI, fokussiert auf sauberer Architektur, Daten validierung und dem intergrieren von Datenbanken
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Die Applikation beschäftigt sich hauptsächlich mit folgenden Dingen:

- den gesamten Prozess von der Anforderungsanalyse bis zur Implementierung abzudecken
- fortgeschrittene Python-Konzepte in einer webbasierten Anwendung anzuwenden
- Datenvalidierung, eine geschichtete Architektur und den Einsatz eines ORMs zu demonstrieren
- sauberen, wartbaren und gut getesteten Code zu erstellen
- Teamarbeit sowie professionelle Dokumentation zu unterstützen

📝 Anwenungsanforderungen des Projekts:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Viele Schülerinnen und Schüler haben Probleme mit grossen Mengen an Unterrichtsstoff auswendig zu lernen. Dazu greien die meisten zu einer LernAPP. Grundsätzlich eine gute IDee jedoch besitzen viele LernApps nich über die gewünschten Funktionen oder sind Kostenpflichtig. Beides nicht optimal für einen Schüler/inn.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Szenario
Die Applikations gibt uns die Möglichkeit für:
- Das erstellen mit einem ppersonellem LogIn
- Das Eintragen von neuem Lernstoff in From von Karteikarten
- Das Einteilen von dem eigefügten Lernstoff in verschiedene Klassen bzw. Fächer
- Aus den erstellten karteikarten eine Liste erstellen
- Die erstellten Listen teilen mit anseren Benutzern
- Das Lernen von den eingetragenen Karteikarten (Lernmodi)
- Das Prüfen von den gelerneten Karteikarten (Prüfungsmodi)
   - Analyse der geprüften Karteikarten, Anzahlt richtig / falsch
- Das Bearbeiten von den einegetragenen Karteikarten (Bearbeitungsmodi)
- Das Löschen von den eingetragenen Karteikarten (Löschmodi)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📖 User Stories
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. LogIn
Als Benutzer richte ich mir ein eigens Konto ein mit einer Email und einem geschützten Password. Danach kann ich mich damit immer wieder ein und aus loggen.
- Inputs: Email und Passwort
- Outputs: None
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2. View Menü
Als Benutzer dieser Applikation will ich als erstes das Hauptmenü sehen mit den darin enthaltenen Hauptfunktionen.
- (Löschen, Bearbeiten, Hinzufügen, Lernen, Prüfen)
- Inputs: None
- Output: ((main functions))
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
3. Hinzufügen von Karteikarten
Als Benutzer will ich meinen Lernstoff in Fomr von karteikarten hinzufügen.
- Input: Karteikarten ((Fach ID))
- Output: Updated Karteikartenliste ((txt.file))
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
4. Karten Listen erstellen
Nachdem ich als Benutzer meine Karten erstellt habe um diese zu lernen oder zu prüfen, habe ich die Möglichkeit diese als Liste zu speichern um sie später wieder gezielt zu lernen ohne dass ich alle Karten zusammen lernen muss. ZUdem kann ich diese Liste dann mit anderen Benutzern teilen oder selbst die Listen von anderen Benutzern lernen.
- Inputs: ((Listen.ID))
- Outputs: Updaten Listen
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
5. View Menü to choose a mainfunction
Als Benutzer will ich nach dem hinzufügen meiner Karteikarten eine Liste sehen mit allen möglichen Hauptfunktionen.
- Inputs: ((main function)) choosen
- outputs: View ((main functions))
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
6. View Results
Als Benutzer will ich sehen wie meine Leistungen waren in den gewählten ((mainfunctions)) wie ((lernen oder prüfen))
- Inputs: none
- Outputs: results
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
7. Karteikarten zurücksetzen
Als Benutzer will ich meine veralteten Karteikarten welche ich in den Modi (lernen und Prüfung) nicht mehr brauche, bearbeiten oder sogar löschen.
- Inputs: ((main function löschen, bearbeiten))
- Output: Updated Karteikartenliste ((txt.file))
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
8. View Menü/ neue Karteikarten hinzufügen
ALs Benutzer willich nachdem meine alten Karteikarten gelöscht bzw. bearbeitet wurden neue Karteikarten hinzufügen.
- Input: ((main function hinzufügen))
- output: ((main function)) Updated Karteikartenliste ((txt.file))
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🧩 Use Cases
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
![image_URL](https://github.com/Studentdavid614/David---Jana-OP1-Karteikartensystem/blob/main/BILD%20USE%20CASES.png?raw=true)

Main cases:
- View Mainfunctions
  - Karteikarte Hinzufügen
  - Fächer spezifische Listen aus den Karteikarten erstellen
  - Listen mit andern Usern teilen
  - Karteikarte Bearbeiten
  - Karteikarte Lernen
  - Karteikarte Prüfen
  - Karteikarte Löschen
Schauspieler:
- User
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Wireframes / Mockups
![image_URL]()
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🏛️ Architecture
Layers
- UI: NiceGUI 
- Application logic: controllers and services
- Persistence: 

Design Decisions
- MVC structure (Model–View–Controller)
- Clear separation of concerns
- Business logic independent of UI

Design Patterns Used

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🗄️ Database and ORM
![image_URL](https://github.com/Studentdavid614/David---Jana-OP1-Karteikartensystem/blob/main/BILD%20ORM.png?raw=true)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
⚙️ Implementation
Technology
Python 3.x
NiceGUI
SQLModel / SQLAlchemy
ReportLab
pytest
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📚 Libraries Used
nicegui – UI framework
sqlmodel – ORM
sqlalchemy – database toolkit
reportlab – PDF generation
python-dotenv – configuration
pytest – testing
pytest-cov – coverage
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
👥 Team & Contributions

- David:   Nice GUI-Frontend, Routing, PDF-Export, Statistik Dashboard
- Jana: 	 Datenmodellierung, Service-Layer, Authentifizierung, Test-Framework
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
