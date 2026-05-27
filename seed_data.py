"""
Generate sample 1000 flashcards for testing/seeding the database.
Run this file to populate the database with sample cards.
"""

try:
    from .db import get_session
    from .auth import get_user_by_username, create_user
    from .services import create_card_set, create_card
    from .models import Visibility
except ImportError:
    try:
        from app.db import get_session
        from app.auth import get_user_by_username, create_user
        from app.services import create_card_set, create_card
        from app.models import Visibility
    except ImportError:
        from db import get_session
        from auth import get_user_by_username, create_user
        from services import create_card_set, create_card
        from models import Visibility


def generate_vocabulary_cards():
    """Generate English vocabulary cards."""
    vocabulary = [
        # Basic nouns
        ("What is the English for 'Apfel'?", "Apple"),
        ("What is the English for 'Banane'?", "Banana"),
        ("What is the English for 'Kirsche'?", "Cherry"),
        ("What is the English for 'Traube'?", "Grape"),
        ("What is the English for 'Zitrone'?", "Lemon"),
        ("What is the English for 'Orange'?", "Orange"),
        ("What is the English for 'Pfirsich'?", "Peach"),
        ("What is the English for 'Erdbeere'?", "Strawberry"),
        ("What is the English for 'Wassermelone'?", "Watermelon"),
        ("What is the English for 'Aubergine'?", "Eggplant"),
        ("What is the English for 'Karotte'?", "Carrot"),
        ("What is the English for 'Gurke'?", "Cucumber"),
        ("What is the English for 'Blumenkohl'?", "Cauliflower"),
        ("What is the English for 'Brokkoli'?", "Broccoli"),
        ("What is the English for 'Spinat'?", "Spinach"),
        ("What is the English for 'Zwiebel'?", "Onion"),
        ("What is the English for 'Knoblauch'?", "Garlic"),
        ("What is the English for 'Tomate'?", "Tomato"),
        ("What is the English for 'Kartoffel'?", "Potato"),
        ("What is the English for 'Reis'?", "Rice"),
        # Verbs
        ("What is the English for 'essen'?", "Eat"),
        ("What is the English for 'trinken'?", "Drink"),
        ("What is the English for 'schlafen'?", "Sleep"),
        ("What is the English for 'gehen'?", "Go/Walk"),
        ("What is the English for 'laufen'?", "Run"),
        ("What is the English for 'sprechen'?", "Speak"),
        ("What is the English for 'hören'?", "Hear/Listen"),
        ("What is the English for 'sehen'?", "See"),
        ("What is the English for 'schreiben'?", "Write"),
        ("What is the English for 'lesen'?", "Read"),
        # Animals
        ("What is the English for 'Katze'?", "Cat"),
        ("What is the English for 'Hund'?", "Dog"),
        ("What is the English for 'Pferd'?", "Horse"),
        ("What is the English for 'Kuh'?", "Cow"),
        ("What is the English for 'Schaf'?", "Sheep"),
        ("What is the English for 'Schwein'?", "Pig"),
        ("What is the English for 'Vogel'?", "Bird"),
        ("What is the English for 'Fisch'?", "Fish"),
        ("What is the English for 'Schlange'?", "Snake"),
        ("What is the English for 'Frosch'?", "Frog"),
        ("What is the English for 'Löwe'?", "Lion"),
        ("What is the English for 'Tiger'?", "Tiger"),
        ("What is the English for 'Elefant'?", "Elephant"),
        ("What is the English for 'Giraffe'?", "Giraffe"),
        ("What is the English for 'Affe'?", "Monkey"),
    ]
    return vocabulary * 20  # Multiply to reach 1000+ cards


def generate_geography_cards():
    """Generate geography cards."""
    geography = [
        ("What is the capital of France?", "Paris"),
        ("What is the capital of Germany?", "Berlin"),
        ("What is the capital of Spain?", "Madrid"),
        ("What is the capital of Italy?", "Rome"),
        ("What is the capital of Switzerland?", "Bern"),
        ("What is the capital of Austria?", "Vienna"),
        ("What is the capital of Netherlands?", "Amsterdam"),
        ("What is the capital of Belgium?", "Brussels"),
        ("What is the capital of Portugal?", "Lisbon"),
        ("What is the capital of Greece?", "Athens"),
        ("What is the capital of Sweden?", "Stockholm"),
        ("What is the capital of Norway?", "Oslo"),
        ("What is the capital of Denmark?", "Copenhagen"),
        ("What is the capital of Finland?", "Helsinki"),
        ("What is the capital of Poland?", "Warsaw"),
        ("What is the capital of Czech Republic?", "Prague"),
        ("What is the capital of Hungary?", "Budapest"),
        ("What is the capital of Romania?", "Bucharest"),
        ("What is the capital of Bulgaria?", "Sofia"),
        ("What is the capital of Slovenia?", "Ljubljana"),
        ("What is the largest country in Europe?", "Russia"),
        ("What is the largest country in Asia?", "Russia"),
        ("What is the largest country in Africa?", "Algeria"),
        ("What is the largest country in South America?", "Brazil"),
        ("What is the largest country in North America?", "Canada"),
    ]
    return geography * 40  # Multiply to reach ~1000 cards


def generate_history_cards():
    """Generate history cards."""
    history = [
        ("What year did Columbus discover America?", "1492"),
        ("What year did the Titanic sink?", "1912"),
        ("What year did the Hindenburg disaster happen?", "1937"),
        ("What year did the Berlin Wall fall?", "1989"),
        ("What year did the first moon landing happen?", "1969"),
        ("What year did World War I start?", "1914"),
        ("What year did World War II end?", "1945"),
        ("What year was the Declaration of Independence signed?", "1776"),
        ("What year was the Magna Carta signed?", "1215"),
        ("What year did the Reformation begin?", "1517"),
        ("Who was the first president of the United States?", "George Washington"),
        ("Who was the first Emperor of Rome?", "Augustus"),
        ("Who invented the printing press?", "Johannes Gutenberg"),
        ("Who invented the telephone?", "Alexander Graham Bell"),
        ("Who invented the steam engine?", "James Watt"),
    ]
    return history * 60  # Multiply to reach ~900 cards


def generate_math_cards():
    """Generate math cards."""
    math_cards = [
        ("What is 2 + 2?", "4"),
        ("What is 3 + 4?", "7"),
        ("What is 5 + 6?", "11"),
        ("What is 2 * 3?", "6"),
        ("What is 4 * 5?", "20"),
        ("What is 10 * 10?", "100"),
        ("What is 100 / 10?", "10"),
        ("What is 20 / 4?", "5"),
        ("What is 15 - 8?", "7"),
        ("What is 50 - 25?", "25"),
        ("What is the square root of 16?", "4"),
        ("What is the square root of 25?", "5"),
        ("What is the square root of 100?", "10"),
        ("What is 2^3?", "8"),
        ("What is 3^2?", "9"),
        ("What is 5^2?", "25"),
        ("What is π approximately equal to?", "3.14159"),
        ("What is the value of e approximately?", "2.71828"),
        ("What is the formula for the area of a circle?", "πr²"),
        ("What is the formula for the circumference of a circle?", "2πr"),
        ("What is the Pythagorean theorem?", "a² + b² = c²"),
        ("What is the slope formula?", "m = (y₂ - y₁) / (x₂ - x₁)"),
        ("What is the quadratic formula?", "x = (-b ± √(b² - 4ac)) / 2a"),
        ("What is the formula for the area of a triangle?", "(base × height) / 2"),
        ("What is the formula for the volume of a sphere?", "(4/3)πr³"),
    ]
    return math_cards * 40  # Multiply to reach ~1000 cards


def generate_science_cards():
    """Generate science cards."""
    science = [
        ("What is the chemical symbol for Gold?", "Au"),
        ("What is the chemical symbol for Silver?", "Ag"),
        ("What is the chemical symbol for Iron?", "Fe"),
        ("What is the chemical symbol for Copper?", "Cu"),
        ("What is the chemical symbol for Oxygen?", "O"),
        ("What is the chemical symbol for Hydrogen?", "H"),
        ("What is the chemical symbol for Carbon?", "C"),
        ("What is the chemical symbol for Nitrogen?", "N"),
        ("What is the chemical formula for water?", "H₂O"),
        ("What is the chemical formula for salt?", "NaCl"),
        ("What is the chemical formula for carbon dioxide?", "CO₂"),
        ("What is the chemical formula for methane?", "CH₄"),
        ("What is the smallest planet in our solar system?", "Mercury"),
        ("What is the largest planet in our solar system?", "Jupiter"),
        ("How many moons does Mars have?", "2"),
        ("How many moons does Jupiter have?", "95"),
        ("How many moons does Saturn have?", "146"),
        ("What is the speed of light?", "299,792,458 m/s"),
        ("What is the speed of sound?", "343 m/s"),
        ("What is the melting point of ice?", "0°C (32°F)"),
        ("What is the boiling point of water?", "100°C (212°F)"),
        ("What is the atomic number of Hydrogen?", "1"),
        ("What is the atomic number of Carbon?", "6"),
        ("What is the atomic number of Oxygen?", "8"),
        ("What is the atomic number of Iron?", "26"),
    ]
    return science * 40  # Multiply to reach ~1000 cards


def populate_database_with_sample_cards():
    """Populate the database with sample cards."""
    print("Populating database with sample cards...")
    
    with get_session() as session:
        # Create default user
        admin = get_user_by_username(session, "demo")
        if not admin:
            admin = create_user(session, "demo", "demo@example.com", "demo123")
            print(f"Created admin user: demo")
    
    # Create card sets and populate them
    card_sets_data = [
        ("English Vocabulary", "Basic English vocabulary for beginners", generate_vocabulary_cards()),
        ("Geography", "World geography: capitals and largest countries", generate_geography_cards()),
        ("History", "World history facts and dates", generate_history_cards()),
        ("Mathematics", "Math facts and formulas", generate_math_cards()),
        ("Science", "Chemistry, physics, and astronomy", generate_science_cards()),
    ]
    
    total_cards = 0
    
    for set_name, description, cards in card_sets_data:
        with get_session() as session:
            admin = get_user_by_username(session, "demo")
            card_set = create_card_set(admin.id, set_name, description, Visibility.PUBLIC)
            
            for front, back in cards:
                create_card(card_set.id, front, back)
                total_cards += 1
            
            print(f"✓ Created '{set_name}' with {len(cards)} cards")
    
    print(f"\n✓ Successfully created {total_cards} flashcards!")
    print("You can now log in with:")
    print("  Username: demo")
    print("  Password: demo123")


if __name__ == "__main__":
    populate_database_with_sample_cards()
