import sqlite3
import random
import json

def seed_db():
    conn = sqlite3.connect('ymmo.db')
    cursor = conn.cursor()
    
    # DROP and CREATE for V2
    cursor.execute("DROP TABLE IF EXISTS properties")
    cursor.execute('''
        CREATE TABLE properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT,
            prix INTEGER NOT NULL,
            surface INTEGER NOT NULL,
            chambres INTEGER DEFAULT 0,
            ville TEXT NOT NULL,
            status TEXT DEFAULT 'disponible',
            dpe TEXT DEFAULT 'A',
            equipements TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    villes = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse', 'Aix-en-Provence']
    types = ['Appartement T2', 'Maison de ville', 'Studio', 'Villa avec piscine', 'Duplex', 'Penthouse', 'Attique']
    dpes = ['A', 'B', 'B', 'C', 'C', 'D'] # Biens premium, donc plutôt A/B/C
    lux_equips = [
        ['Piscine à débordement', 'Domotique'], 
        ['Vue panoramique', 'Gardien 24/7', 'Ascenseur privé'], 
        ['Cuisine marbre', 'Cave à vin', 'Home cinéma'],
        ['Rooftop', 'Jacuzzi'],
        ['Parquet de Versailles', 'Moulures', 'Double orientation', 'Cheminée']
    ]
    
    properties = []
    for i in range(50):
        ville = random.choice(villes)
        typ = random.choice(types)
        titre = f"{typ} d'Exception à {ville}"
        surface = random.randint(40, 350)
        
        base_prix_m2 = {'Paris': 15000, 'Lyon': 7000, 'Bordeaux': 6500, 'Toulouse': 5800, 'Marseille': 5500, 'Aix-en-Provence': 8000}
        prix_m2 = base_prix_m2[ville] + random.randint(1000, 4000) # Luxe
        prix = surface * prix_m2
        
        chambres = surface // 40
        dpe = random.choice(dpes)
        equip = json.dumps(random.choice(lux_equips))
        
        desc = "Une propriété rarissime offrant des prestations de très haut standing. Matériaux nobles, luminosité exceptionnelle et cadre de vie idyllique. Cette résidence a été conçue par un architecte de renom et offre un art de vivre unique au cœur d'un environnement privilégié."
        
        properties.append((titre, desc, prix, surface, chambres, ville, dpe, equip))
        
    cursor.executemany('''
        INSERT INTO properties (titre, description, prix, surface, chambres, ville, dpe, equipements)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', properties)
    
    conn.commit()
    conn.close()
    print(f"✅ BDD SQLite V2 initialisée avec les nouvelles features premium (DPE, Equipements) !")

if __name__ == '__main__':
    seed_db()
