# 📅 PLAN D'ACTION DÉTAILLÉ - Projet Ymmo
## Roadmap semaine par semaine

---

## 🎯 SEMAINE 1: PLANIFICATION & SPÉCIFICATIONS

### Objectif
Avoir l'architecture complète documentée et l'environnement de développement prêt.

### Jour 1: Réunion & Spécifications (4h)

**Personne 1 (Frontend/Backend):**
- [ ] Créer un Google Doc partagé pour les spécifications
- [ ] Lister toutes les pages/écrans du site:
  - [ ] Page d'accueil
  - [ ] Listing des biens (filtres)
  - [ ] Détail d'un bien
  - [ ] Formulaire d'ajout/édition
  - [ ] Dashboard utilisateur
  - [ ] Login/Register
  - [ ] Dashboard analytique
- [ ] Pour chaque page: sketcher les wireframes (crayon + papier OU Figma gratuit)
- [ ] Lister les endpoints API nécessaires (GET /properties, POST /properties, etc.)

**Personne 2 (Infrastructure):**
- [ ] Dessiner l'architecture réseau (siège + 12 agences)
- [ ] Planifier le plan d'adressage IP (subnet par agence)
- [ ] Lister les configurations Windows Server nécessaires
- [ ] Planifier les VMs pour la démo (1 serveur, 2 agences min, 1 routeur)

**Collectif (15 min)**
- [ ] Réunion: partager les sketches
- [ ] Valider l'approche générale
- [ ] Diviser les tâches clairement

---

### Jour 2: Base de Données & Structure (3h)

**Personne 1:**
- [ ] Créer le schéma MongoDB détaillé:
  ```javascript
  // Exemple pour Users:
  {
    _id: ObjectId,
    email: String, // unique
    password_hash: String,
    nom: String,
    prenom: String,
    role: String // "agent", "client", "admin"
  }
  ```
- [ ] Dessiner le MCD (Modèle Conceptuel de Données)
- [ ] Valider auprès de P2 qu'il n'y a pas de redondance

**Personne 2:**
- [ ] Créer le schéma d'architecture réseau (draw.io ou Lucidchart)
- [ ] Plan d'adressage détaillé:
  - [ ] Siège: 192.168.1.0/24
  - [ ] Agence 1: 10.1.0.0/24
  - [ ] Agence 2: 10.2.0.0/24
  - [ ] etc.
- [ ] Liste de matériel (serveurs, routeurs, pare-feu)

---

### Jour 3: Setup Environnement (4h)

**Personne 1:**
```bash
# Backend
mkdir ymmo-project
cd ymmo-project
git init
git remote add origin <votre-repo-github>

# Python virtualenv
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Dépendances basiques
cat > requirements.txt << EOF
Flask==2.3.2
Flask-CORS==4.0.0
pymongo==4.4.0
python-dotenv==1.0.0
bcrypt==4.0.1
PyJWT==2.8.0
pandas==2.0.3
numpy==1.24.3
EOF

pip install -r requirements.txt

# Tester MongoDB
python -c "import pymongo; print('✓ PyMongo OK')"
python -c "from flask import Flask; print('✓ Flask OK')"
```

- [ ] Créer `.env`:
```
MONGO_URI=mongodb://localhost:27017/ymmo
SECRET_KEY=votre_clé_secrète_forte_ici
DEBUG=True
FLASK_APP=app.py
```

- [ ] Créer structure de dossiers:
```
backend/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── properties.py
│   ├── users.py
│   └── listings.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── property.py
│   └── listing.py
├── utils/
│   ├── __init__.py
│   └── validators.py
└── tests/
    └── __init__.py
```

**Personne 2:**
- [ ] Installer VirtualBox ou Hyper-V
- [ ] Télécharger ISO Windows Server 2022
- [ ] Préparer les images VM
- [ ] Installer GNS3 ou Cisco Packet Tracer (simulateur réseau)

**Collectif:**
- [ ] Push sur GitHub avec un README initial
- [ ] Vérifier que tout le monde peut faire un git clone

---

### Jour 4: Documentation Initiale (3h)

**Personne 1:**
- [ ] Créer `docs/SPECIFICATIONS.md`:
```markdown
# Spécifications Fonctionnelles - Ymmo

## 1. Authentification
- Registration: email + mot de passe
- Login: email + mot de passe → JWT token
- Logout: invalider le token
- Rôles: agent, client, admin

## 2. Gestion des Biens
### Cas d'usage: Ajouter un bien
- Utilisateur (agent) remplit formulaire
- Champs: titre, description, prix, surface, localisation (lat/long), images
- Validation: tous les champs obligatoires
- Résultat: bien créé en BD, visible sur le listing

[... détailler tous les cas d'usage ...]
```

**Personne 2:**
- [ ] Créer `docs/ARCHITECTURE_INFRA.md`:
```markdown
# Architecture Infrastructure - Ymmo

## Topologie Réseau
- 1 Siège (Aix-en-Provence)
- 12 Agences connectées via VPN/IPSec

## Plan d'Adressage
- Siège: 192.168.1.0/24
- Agence 1: 10.1.0.0/24
[...]

## Sécurité
- Pare-feu: bloquer par défaut, autoriser les services nécessaires
- VPN: IPSec site-to-site
- Authentification: Active Directory

[... détailler ...]
```

**Collectif:**
- [ ] Réunion finale de validation (30 min)
- [ ] Tous les documents commitées sur GitHub

---

## ✅ SEMAINE 1 - CHECKLIST

- [ ] Spécifications complètes (docs/SPECIFICATIONS.md)
- [ ] Schéma base de données (MCD)
- [ ] Architecture réseau dessinée
- [ ] Environnement dev configuré (Python + venv + deps)
- [ ] Repository GitHub créé et partagé
- [ ] README avec instructions de setup
- [ ] Première branche 'develop' créée
- [ ] Planning des sprints suivants validé

---

## 🚀 SEMAINE 2: CORE BACKEND & PAGES STATIQUES

### Objectif
Avoir une API minimal fonctionnelle et les pages HTML de base.

---

### Jour 1: Setup Flask Initial (4h)

**Personne 1:**

Créer `backend/app.py`:
```python
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
CORS(app)

# Routes placeholder
@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

- [ ] Tester: `python app.py` → `curl http://localhost:5000/api/health`

Créer `backend/config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ymmo')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', False)
    JWT_SECRET = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

**Personne 2:**
- [ ] Créer la première VM Windows Server
- [ ] Configurer IP: 192.168.1.10
- [ ] Joindre un domaine (ou créer une forêt)
- [ ] Documenter les étapes

---

### Jour 2: Modèles & Base de Données (4h)

**Personne 1:**

Créer `backend/models/user.py`:
```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client['ymmo']

class User:
    @staticmethod
    def create(email, password_hash, nom, prenom, role='client'):
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'nom': nom,
            'prenom': prenom,
            'role': role,
            'created_at': datetime.now()
        }
        result = db.users.insert_one(user_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_email(email):
        return db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        from bson import ObjectId
        return db.users.find_one({'_id': ObjectId(user_id)})
```

Faire pareil pour Property et Listing.

- [ ] Tester la connexion MongoDB
- [ ] Créer quelques documents de test manuellement

**Personne 2:**
- [ ] Commencer la config Active Directory
- [ ] Créer des unités organisationnelles (OU)
- [ ] Ajouter des comptes de test

---

### Jour 3: Routes API de Base (4h)

**Personne 1:**

Créer `backend/routes/auth.py`:
```python
from flask import Blueprint, request, jsonify
from models.user import User
import bcrypt
import jwt
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom')
    
    # Validation
    if not email or not password:
        return {'error': 'Email et password requis'}, 400
    
    # Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Créer user
    user_id = User.create(email, hashed, nom, data.get('prenom'))
    
    return {'user_id': str(user_id)}, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.find_by_email(email)
    if not user or not bcrypt.checkpw(password.encode(), user['password_hash']):
        return {'error': 'Invalid credentials'}, 401
    
    token = jwt.encode(
        {'user_id': str(user['_id']), 'email': email},
        os.getenv('SECRET_KEY'),
        algorithm='HS256'
    )
    
    return {'token': token}, 200
```

Faire pareil pour les propriétés:

Créer `backend/routes/properties.py`:
```python
from flask import Blueprint, request, jsonify
from models.property import Property
from bson import ObjectId

properties_bp = Blueprint('properties', __name__, url_prefix='/api/properties')

@properties_bp.route('', methods=['GET'])
def list_properties():
    # Filtres optionnels
    prix_min = request.args.get('prix_min', type=int)
    prix_max = request.args.get('prix_max', type=int)
    
    query = {}
    if prix_min:
        query['prix'] = {'$gte': prix_min}
    if prix_max:
        if 'prix' in query:
            query['prix']['$lte'] = prix_max
        else:
            query['prix'] = {'$lte': prix_max}
    
    properties = list(Property.find(query))
    return {'properties': properties}, 200

@properties_bp.route('', methods=['POST'])
def create_property():
    data = request.json
    prop_id = Property.create(data)
    return {'property_id': str(prop_id)}, 201

@properties_bp.route('/<property_id>', methods=['GET'])
def get_property(property_id):
    prop = Property.find_by_id(ObjectId(property_id))
    if not prop:
        return {'error': 'Not found'}, 404
    return {'property': prop}, 200
```

Enregistrer les routes dans app.py:
```python
from routes.auth import auth_bp
from routes.properties import properties_bp

app.register_blueprint(auth_bp)
app.register_blueprint(properties_bp)
```

- [ ] Tester avec Postman/Insomnia:
  - POST /api/auth/register
  - POST /api/auth/login
  - GET /api/properties
  - POST /api/properties

**Personne 2:**
- [ ] Configurer les stratégies de groupe (GPO)
- [ ] Tester les droits d'accès
- [ ] Documenter les configurations

---

### Jour 4: Frontend HTML/CSS (4h)

**Personne 1 (Frontend):**

Créer `frontend/index.html`:
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ymmo - Plateforme Immobilière</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="logo">Ymmo</div>
            <ul class="nav-links">
                <li><a href="index.html">Accueil</a></li>
                <li><a href="pages/listing.html">Annonces</a></li>
                <li><a href="pages/login.html">Connexion</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="hero">
            <h1>Trouve ton bien immobilier idéal</h1>
            <p>Plateforme décentralisée avec analyste IA</p>
            <a href="pages/listing.html" class="btn btn-primary">Voir les annonces</a>
        </section>

        <section class="featured-properties">
            <h2>Biens en vedette</h2>
            <div id="properties-container" class="properties-grid">
                <!-- Injecté par JavaScript -->
            </div>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 Ymmo. Tous droits réservés.</p>
    </footer>

    <script src="js/api.js"></script>
    <script src="js/main.js"></script>
</body>
</html>
```

Créer `frontend/css/style.css`:
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #2563eb;
    --secondary: #64748b;
    --success: #16a34a;
    --danger: #dc2626;
    --light: #f8fafc;
    --dark: #1e293b;
    --radius: 8px;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: var(--dark);
    background: white;
}

header {
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
}

.navbar {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: var(--dark);
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--primary);
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.hero {
    text-align: center;
    padding: 3rem 0;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.1rem;
    color: var(--secondary);
    margin-bottom: 2rem;
}

.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius);
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: #1d4ed8;
}

.properties-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.property-card {
    border: 1px solid #e2e8f0;
    border-radius: var(--radius);
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
}

.property-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.property-image {
    width: 100%;
    height: 200px;
    background: var(--light);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--secondary);
}

.property-content {
    padding: 1.5rem;
}

.property-title {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.property-price {
    color: var(--primary);
    font-weight: bold;
    font-size: 1.25rem;
    margin-bottom: 1rem;
}

.property-details {
    color: var(--secondary);
    font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }

    .nav-links {
        gap: 1rem;
    }

    .properties-grid {
        grid-template-columns: 1fr;
    }
}
```

Créer `frontend/js/api.js`:
```javascript
const API_URL = 'http://localhost:5000/api';

class ApiClient {
    async get(endpoint) {
        const response = await fetch(`${API_URL}${endpoint}`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return await response.json();
    }

    async post(endpoint, data) {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return await response.json();
    }

    async getProperties(filters = {}) {
        const query = new URLSearchParams(filters);
        return this.get(`/properties?${query}`);
    }

    async getProperty(id) {
        return this.get(`/properties/${id}`);
    }

    async createProperty(data) {
        return this.post('/properties', data);
    }
}

const api = new ApiClient();
```

Créer `frontend/js/main.js`:
```javascript
async function loadProperties() {
    try {
        const data = await api.getProperties();
        const container = document.getElementById('properties-container');
        
        if (!data.properties || data.properties.length === 0) {
            container.innerHTML = '<p>Aucun bien disponible.</p>';
            return;
        }

        container.innerHTML = data.properties.map(prop => `
            <div class="property-card">
                <div class="property-image">Image</div>
                <div class="property-content">
                    <h3 class="property-title">${prop.titre}</h3>
                    <p class="property-price">${prop.prix.toLocaleString('fr-FR')} €</p>
                    <p class="property-details">
                        ${prop.surface} m² • ${prop.chambres} chambre(s)
                    </p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('properties-container').innerHTML = 
            '<p>Erreur lors du chargement des propriétés.</p>';
    }
}

// Charger les propriétés à l'init
document.addEventListener('DOMContentLoaded', loadProperties);
```

- [ ] Ouvrir `frontend/index.html` dans le navigateur
- [ ] Vérifier que le CSS s'applique
- [ ] Tester l'appel API (console des dev tools)

---

### ✅ SEMAINE 2 - CHECKLIST

**Backend:**
- [ ] Flask configuré et routé
- [ ] Connexion MongoDB stable
- [ ] Routes AUTH (register/login) fonctionnelles
- [ ] Routes PROPERTIES (GET/POST) fonctionnelles
- [ ] Tests avec Postman réussis
- [ ] JWT tokens générés correctement

**Frontend:**
- [ ] Pages HTML de base créées
- [ ] CSS responsive appliqué
- [ ] API client JavaScript configuré
- [ ] Listing des biens affichage dynamiquement
- [ ] Pas d'erreurs console

**Infrastructure:**
- [ ] Première VM Windows Server configurée
- [ ] Active Directory en place
- [ ] Documentation en cours

---

## 🎯 SEMAINES 3-4: COMPLÉTUDE

### Plan général

**Semaine 3:**
- Ajouter les pages manquantes (détail, formulaire, dashboard)
- Authentification complète (logout, vérification token)
- Upload images pour les propriétés
- Responsive design finalisé

**Semaine 4:**
- Module analyse de données
- Dashboard analytique
- Tests complets
- Optimisation performance

---

## 🏗️ SEMAINES 5-6: INFRASTRUCTURE

### Plan général

**Semaine 5:**
- Configuration Windows Server avancée
- Architecture VPN/IPSec
- Plan d'adressage IP finalisé

**Semaine 6:**
- Déploiement des VMs
- Tests de sécurité
- Documentation infrastructure complète

---

## 📚 SEMAINES 7-8: FINALISATION

**Semaine 7:**
- Tests exhaustifs
- Correction bugs
- Documentation complète
- Guide déploiement

**Semaine 8:**
- Préparation présentation orale
- Démonstration live
- Répétition

---

## 📝 NOTES IMPORTANTES

### Communication d'équipe
- **Standup quotidien**: 10 min le matin (status + blockers)
- **Code review**: Chaque PR doit être reviewée par l'autre personne
- **Documentation**: Écrire pendant qu'on code, pas à la fin

### Git workflow
```bash
# Pour une nouvelle feature
git checkout -b feature/auth-login
# ... faire des commits
git commit -m "feat: add login endpoint"
git push origin feature/auth-login
# Créer une PR sur GitHub
# Attendre review + merge

# Avant de commencer une nouvelle tâche
git checkout develop
git pull origin develop
git checkout -b feature/next-feature
```

### Testing
- **Backend**: `pytest` pour les routes API
- **Frontend**: Tests manuels + vérification sur navigateurs (Chrome, Firefox, Safari)
- **Infrastructure**: Tests de connectivity VPN, ping entre sites

### Documentation pendant le dev
```python
# Bon exemple - commentaires clairs
def create_property(data):
    """
    Crée une nouvelle propriété en base de données.
    
    Args:
        data: Dict contenant {titre, prix, surface, localisation, ...}
    
    Returns:
        ObjectId: ID de la propriété créée
        
    Raises:
        ValueError: Si les champs obligatoires manquent
    """
    # Validation des champs
    ...
```

---

## 🚨 RISQUES COMMUNS & SOLUTIONS

| Risque | Impact | Solution |
|--------|--------|----------|
| Retard sur spécifications | Rework tardif | Valider specs avant le code |
| Mauvaise communication équipe | Travail redondant | Standup quotidien strict |
| Oublier tests | Bugs en présentation | Tests au fur et à mesure |
| Infrastructure mal documentée | Démonstration chaotique | Documenter chaque étape |
| Performance degradée | Mauvaise première impression | Optimiser tôt (indexes BD, etc.) |

---

## 🎁 BONUS: Templates Prêts à l'emploi

### Test API avec Postman

```json
{
  "info": {
    "name": "Ymmo API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Register",
      "request": {
        "method": "POST",
        "url": "http://localhost:5000/api/auth/register",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"user@example.com\",\n  \"password\": \"password123\",\n  \"nom\": \"Dupont\",\n  \"prenom\": \"Jean\"\n}"
        }
      }
    }
  ]
}
```

### Test MongoDB

```javascript
// Mongo Shell
use ymmo
db.users.insertOne({
  email: "test@test.com",
  password_hash: "...",
  nom: "Test",
  role: "agent"
})

db.properties.find({prix: {$gte: 100000, $lte: 500000}})
```

---

**Document créé**: Plan d'action détaillé Ymmo  
**À mettre à jour**: Hebdomadairement selon l'avancement  
**Responsable**: Les 2 membres de l'équipe
