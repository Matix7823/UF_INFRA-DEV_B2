# ⚡ QUICK START - Démarrer le projet en 30 min

Tu veux commencer maintenant ? Suis ces étapes simple pour avoir une première version fonctionnelle.

---

## 📦 PRÉREQUIS (5 min)

Vérifie que tu as installé:

```bash
# Python 3.9+
python --version

# Git
git --version

# Node.js (optionnel, pour npm)
node --version
```

Si tu manques quelque chose:
- **Python**: https://www.python.org/downloads/
- **Git**: https://git-scm.com/
- **MongoDB**: https://docs.mongodb.com/manual/installation/ (ou utilise MongoDB Atlas en ligne)

---

## 🚀 SETUP INITIAL (10 min)

### Étape 1: Créer le repo Git

```bash
# Clone un repo vide ou crée sur GitHub
# Puis en local:
git clone https://github.com/votrelogin/ymmo-project.git
cd ymmo-project

# Crée la structure
mkdir -p backend frontend docs infra
touch README.md .gitignore

# Branching strategy
git checkout -b develop
```

### Étape 2: Setup Backend

```bash
cd backend

# Créer virtualenv Python
python -m venv venv

# Activer venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer dépendances
pip install Flask Flask-CORS pymongo python-dotenv bcrypt PyJWT pandas numpy

# Générer requirements.txt
pip freeze > requirements.txt
```

### Étape 3: Fichiers de configuration Backend

Crée `backend/.env`:
```
MONGO_URI=mongodb://localhost:27017/ymmo
SECRET_KEY=dev-super-secret-key-change-in-prod
DEBUG=True
FLASK_APP=app.py
```

Crée `backend/.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
.DS_Store
*.log
.vscode/
```

### Étape 4: Fichiers de base Frontend

```bash
cd ../frontend

# Structure minimale
touch index.html
mkdir -p css js assets
touch css/style.css js/main.js
```

---

## 💻 PREMIER LANCEMENT (15 min)

### Backend: Minimal Flask App

Crée `backend/app.py`:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt
import jwt
from datetime import datetime

load_dotenv()

# Configuration
app = Flask(__name__)
CORS(app)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ymmo')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')

# MongoDB Connection
try:
    client = MongoClient(MONGO_URI)
    db = client['ymmo']
    print("✓ MongoDB connecté")
except:
    print("✗ Erreur MongoDB - vérifiez que MongoDB est lancé")
    db = None

# ============ ROUTES ============

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok', 'message': 'Backend fonctionne!'}, 200

# ============ AUTHENTIFICATION ============

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        nom = data.get('nom', 'Utilisateur')
        
        # Validation
        if not email or not password:
            return {'error': 'Email et password requis'}, 400
        
        # Vérifier si user existe déjà
        if db.users.find_one({'email': email}):
            return {'error': 'Email déjà utilisé'}, 400
        
        # Hash password
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        # Créer user
        user_data = {
            'email': email,
            'password_hash': hashed,
            'nom': nom,
            'role': 'client',
            'created_at': datetime.now()
        }
        result = db.users.insert_one(user_data)
        
        return {
            'message': 'User créé',
            'user_id': str(result.inserted_id)
        }, 201
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Trouver user
        user = db.users.find_one({'email': email})
        if not user:
            return {'error': 'User not found'}, 404
        
        # Vérifier password
        if not bcrypt.checkpw(password.encode(), user['password_hash']):
            return {'error': 'Invalid password'}, 401
        
        # Générer JWT token
        token = jwt.encode(
            {'user_id': str(user['_id']), 'email': email},
            SECRET_KEY,
            algorithm='HS256'
        )
        
        return {
            'message': 'Login success',
            'token': token,
            'user': {'id': str(user['_id']), 'email': email, 'nom': user.get('nom')}
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

# ============ PROPRIÉTÉS ============

@app.route('/api/properties', methods=['GET'])
def get_properties():
    try:
        # Filtres optionnels
        prix_min = request.args.get('prix_min', type=int)
        prix_max = request.args.get('prix_max', type=int)
        ville = request.args.get('ville', type=str)
        
        query = {}
        if prix_min:
            query['prix'] = {'$gte': prix_min}
        if prix_max:
            if 'prix' in query:
                query['prix']['$lte'] = prix_max
            else:
                query['prix'] = {'$lte': prix_max}
        if ville:
            query['localisation.ville'] = ville
        
        # Récupérer les propriétés
        properties = list(db.properties.find(query).limit(50))
        
        # Convertir ObjectId en string
        for prop in properties:
            prop['_id'] = str(prop['_id'])
        
        return {'properties': properties}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/properties', methods=['POST'])
def create_property():
    try:
        data = request.json
        
        # Validation
        required = ['titre', 'prix', 'surface', 'localisation']
        if not all(field in data for field in required):
            return {'error': 'Champs obligatoires manquants'}, 400
        
        # Créer propriété
        property_data = {
            'titre': data.get('titre'),
            'description': data.get('description', ''),
            'prix': data.get('prix'),
            'surface': data.get('surface'),
            'chambres': data.get('chambres', 0),
            'localisation': data.get('localisation'),
            'images': data.get('images', []),
            'status': 'disponible',
            'created_at': datetime.now()
        }
        result = db.properties.insert_one(property_data)
        
        return {
            'message': 'Propriété créée',
            'property_id': str(result.inserted_id)
        }, 201
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/properties/<property_id>', methods=['GET'])
def get_property(property_id):
    try:
        from bson import ObjectId
        prop = db.properties.find_one({'_id': ObjectId(property_id)})
        if not prop:
            return {'error': 'Propriété not found'}, 404
        
        prop['_id'] = str(prop['_id'])
        return {'property': prop}, 200
    except Exception as e:
        return {'error': str(e)}, 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Endpoint not found'}, 404

@app.errorhandler(500)
def server_error(error):
    return {'error': 'Server error'}, 500

# ============ MAIN ============

if __name__ == '__main__':
    if db:
        print("\n🚀 Serveur lancé sur http://localhost:5000")
        print("📚 API docs: http://localhost:5000/api/health\n")
        app.run(debug=True, port=5000)
    else:
        print("❌ Impossible de démarrer - MongoDB not connected")
```

**Lance le backend:**

```bash
python app.py
```

Tu devrais voir:
```
✓ MongoDB connecté
🚀 Serveur lancé sur http://localhost:5000
```

---

### Frontend: Minimal HTML

Crée `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ymmo - Immobilier</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="logo">🏠 Ymmo</div>
            <div class="nav-links">
                <a href="#properties">Propriétés</a>
                <a href="#auth">Auth</a>
            </div>
        </nav>
    </header>

    <main class="container">
        <h1>Bienvenue sur Ymmo</h1>
        
        <!-- Section Auth -->
        <section id="auth" class="auth-section">
            <h2>Authentification</h2>
            
            <div class="auth-forms">
                <!-- Register -->
                <div class="form-group">
                    <h3>S'inscrire</h3>
                    <input type="email" id="register-email" placeholder="Email">
                    <input type="password" id="register-password" placeholder="Mot de passe">
                    <input type="text" id="register-nom" placeholder="Nom">
                    <button onclick="register()">S'inscrire</button>
                </div>

                <!-- Login -->
                <div class="form-group">
                    <h3>Se connecter</h3>
                    <input type="email" id="login-email" placeholder="Email">
                    <input type="password" id="login-password" placeholder="Mot de passe">
                    <button onclick="login()">Se connecter</button>
                </div>
            </div>
            
            <div id="auth-result" class="result"></div>
        </section>

        <!-- Section Propriétés -->
        <section id="properties" class="properties-section">
            <h2>Propriétés Disponibles</h2>
            
            <div class="form-group filters">
                <input type="number" id="prix-min" placeholder="Prix min">
                <input type="number" id="prix-max" placeholder="Prix max">
                <button onclick="searchProperties()">Chercher</button>
            </div>

            <div id="properties-list" class="properties-grid"></div>
        </section>

        <!-- Ajouter propriété -->
        <section id="add-property" class="add-property-section">
            <h2>Ajouter une Propriété</h2>
            
            <div class="form-group">
                <input type="text" id="prop-titre" placeholder="Titre">
                <input type="number" id="prop-prix" placeholder="Prix">
                <input type="number" id="prop-surface" placeholder="Surface (m²)">
                <input type="number" id="prop-chambres" placeholder="Chambres">
                <input type="text" id="prop-ville" placeholder="Ville">
                <textarea id="prop-description" placeholder="Description"></textarea>
                <button onclick="createProperty()">Ajouter</button>
            </div>
            
            <div id="add-result" class="result"></div>
        </section>
    </main>

    <script src="js/main.js"></script>
</body>
</html>
```

Crée `frontend/css/style.css`:

```css
:root {
    --primary: #2563eb;
    --secondary: #64748b;
    --danger: #dc2626;
    --success: #16a34a;
    --light: #f8fafc;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #1e293b;
    background: var(--light);
}

header {
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    padding: 1rem;
}

.navbar {
    max-width: 1200px;
    margin: 0 auto;
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
    gap: 2rem;
}

.nav-links a {
    color: var(--secondary);
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--primary);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

h1, h2 {
    margin-bottom: 1rem;
    color: #1e293b;
}

section {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

input, textarea {
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    font-family: inherit;
    font-size: 1rem;
}

input:focus, textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

button {
    padding: 0.75rem 1.5rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.3s;
}

button:hover {
    background: #1d4ed8;
}

.auth-forms {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
}

.properties-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
}

.property-card {
    background: var(--light);
    border-radius: 8px;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
}

.property-card h3 {
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.property-price {
    color: var(--primary);
    font-weight: bold;
    font-size: 1.25rem;
}

.property-details {
    color: var(--secondary);
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.result {
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
    display: none;
}

.result.success {
    display: block;
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
}

.result.error {
    display: block;
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;
}

.filters {
    flex-direction: row;
    gap: 0.5rem;
}

.filters input {
    flex: 1;
}

.filters button {
    flex: 1;
}

@media (max-width: 768px) {
    .auth-forms {
        grid-template-columns: 1fr;
    }

    .properties-grid {
        grid-template-columns: 1fr;
    }
}
```

Crée `frontend/js/main.js`:

```javascript
const API_URL = 'http://localhost:5000/api';
let currentToken = null;

// ============ HELPERS ============

function showResult(elementId, message, isSuccess = true) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = 'result ' + (isSuccess ? 'success' : 'error');
}

// ============ AUTH ============

async function register() {
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const nom = document.getElementById('register-nom').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, nom })
        });
        const data = await response.json();
        
        if (response.ok) {
            showResult('auth-result', '✓ Inscription réussie!', true);
            document.getElementById('register-email').value = '';
            document.getElementById('register-password').value = '';
            document.getElementById('register-nom').value = '';
        } else {
            showResult('auth-result', '✗ ' + (data.error || 'Erreur'), false);
        }
    } catch (error) {
        showResult('auth-result', '✗ Erreur réseau: ' + error.message, false);
    }
}

async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        
        if (response.ok) {
            currentToken = data.token;
            localStorage.setItem('token', data.token);
            showResult('auth-result', `✓ Bienvenue ${data.user.nom}!`, true);
            document.getElementById('login-email').value = '';
            document.getElementById('login-password').value = '';
        } else {
            showResult('auth-result', '✗ ' + (data.error || 'Erreur'), false);
        }
    } catch (error) {
        showResult('auth-result', '✗ Erreur réseau: ' + error.message, false);
    }
}

// ============ PROPERTIES ============

async function searchProperties() {
    const prixMin = document.getElementById('prix-min').value;
    const prixMax = document.getElementById('prix-max').value;
    
    let url = `${API_URL}/properties?`;
    if (prixMin) url += `prix_min=${prixMin}&`;
    if (prixMax) url += `prix_max=${prixMax}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        const list = document.getElementById('properties-list');
        if (!data.properties || data.properties.length === 0) {
            list.innerHTML = '<p>Aucune propriété trouvée.</p>';
            return;
        }

        list.innerHTML = data.properties.map(prop => `
            <div class="property-card">
                <h3>${prop.titre}</h3>
                <p class="property-price">${prop.prix.toLocaleString('fr-FR')} €</p>
                <p class="property-details">
                    ${prop.surface} m² • ${prop.chambres} chambre(s) • ${prop.localisation?.ville || 'N/A'}
                </p>
                <p>${prop.description}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
    }
}

async function createProperty() {
    if (!currentToken) {
        showResult('add-result', '✗ Vous devez être connecté', false);
        return;
    }

    const titre = document.getElementById('prop-titre').value;
    const prix = parseInt(document.getElementById('prop-prix').value);
    const surface = parseInt(document.getElementById('prop-surface').value);
    const chambres = parseInt(document.getElementById('prop-chambres').value);
    const ville = document.getElementById('prop-ville').value;
    const description = document.getElementById('prop-description').value;

    try {
        const response = await fetch(`${API_URL}/properties`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({
                titre,
                prix,
                surface,
                chambres,
                description,
                localisation: { ville }
            })
        });
        const data = await response.json();
        
        if (response.ok) {
            showResult('add-result', '✓ Propriété ajoutée!', true);
            document.getElementById('prop-titre').value = '';
            document.getElementById('prop-prix').value = '';
            document.getElementById('prop-surface').value = '';
            document.getElementById('prop-chambres').value = '';
            document.getElementById('prop-ville').value = '';
            document.getElementById('prop-description').value = '';
            searchProperties();
        } else {
            showResult('add-result', '✗ ' + (data.error || 'Erreur'), false);
        }
    } catch (error) {
        showResult('add-result', '✗ Erreur réseau: ' + error.message, false);
    }
}

// ============ INIT ============

document.addEventListener('DOMContentLoaded', () => {
    currentToken = localStorage.getItem('token');
    searchProperties();
});
```

---

## ✅ TEST RAPIDE (5 min)

### Backend en fonctionnement?

```bash
curl http://localhost:5000/api/health
```

Doit retourner:
```json
{"status": "ok", "message": "Backend fonctionne!"}
```

### Frontend accessible?

Ouvre `frontend/index.html` dans ton navigateur (double-clic OU `python -m http.server 8000` dans le dossier frontend)

Puis accède à: `http://localhost:8000`

Tu devrais voir:
- ✓ Le formulaire d'authentification
- ✓ Le formulaire de recherche
- ✓ Un affichage des propriétés (vide pour l'instant)

---

## 🧪 TESTER LES FONCTIONNALITÉS

### 1. S'inscrire
Remplis le formulaire "S'inscrire":
- Email: `test@test.com`
- Password: `password123`
- Nom: `Dupont`

Clique "S'inscrire" → tu dois voir ✓ Inscription réussie!

### 2. Se connecter
Remplis le formulaire "Se connecter":
- Email: `test@test.com`
- Password: `password123`

Clique "Se connecter" → tu dois voir ✓ Bienvenue Dupont!

### 3. Ajouter une propriété
Remplis le formulaire "Ajouter une Propriété":
- Titre: `Bel appartement à Paris`
- Prix: `350000`
- Surface: `75`
- Chambres: `2`
- Ville: `Paris`
- Description: `Superbe appart au cœur de Paris`

Clique "Ajouter" → tu dois voir ✓ Propriété ajoutée!

### 4. Chercher les propriétés
Clique simplement "Chercher" (sans filtres) → tu dois voir la propriété que tu viens de créer!

---

## 📂 Structure Actuelle

```
ymmo-project/
├── backend/
│   ├── app.py (150 lignes)
│   ├── .env
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/main.js
├── docs/
└── README.md
```

---

## 🎯 PROCHAINES ÉTAPES

Maintenant que tu as une **base fonctionnelle**, tu peux:

1. **Ajouter plus de pages** (détail propriété, dashboard, etc.)
2. **Améliorer le CSS** (responsive design, animations)
3. **Améliorer la sécurité** (validation, sanitization)
4. **Ajouter MongoDB** (s'il n'est pas installé, utilise MongoDB Atlas)
5. **Créer les routes INFRA** (Windows Server, VPN, etc.)

---

## 🐛 DÉPANNAGE

### Erreur: "MongoDB connecté" pas affiché?

**Solution**: MongoDB n'est pas lancé.

**Option 1** - Installer MongoDB en local:
```bash
# Mac avec brew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Linux (Ubuntu)
curl https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-5.0.0.tgz | tar xz
./mongodb-linux-x86_64-ubuntu2004-5.0.0/bin/mongod
```

**Option 2** - Utiliser MongoDB Atlas (cloud):
1. Crée un compte sur https://www.mongodb.com/cloud/atlas
2. Crée un cluster gratuit
3. Récupère la connection string
4. Mets-la dans `.env` comme `MONGO_URI`

### Erreur: "CORS error"?

Ça signifie que le frontend et le backend ne communiquent pas.

**Vérifier**:
- Backend lancé sur http://localhost:5000? ✓
- Frontend lancé sur http://localhost:8000? ✓
- `CORS(app)` dans `app.py`? ✓
- Console des dev tools (F12) → onglet Network → regarde la requête

### Erreur: "Cannot POST /api/..."?

L'endpoint n'existe pas. Vérifiez que `@app.route` est correctement écrit.

---

## 📝 LOGS UTILES

### Dans le terminal Backend:
```
* Running on http://localhost:5000
127.0.0.1 - - [date] "POST /api/auth/register HTTP/1.1" 201 -
```

### Dans la console du navigateur (F12):
```javascript
// Tester une appel API directement
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## 🎉 FÉLICITATIONS!

Tu as maintenant:
- ✅ Un backend Flask fonctionnel
- ✅ Une base de données MongoDB
- ✅ Un frontend HTML/CSS/JS
- ✅ Authentification complète
- ✅ CRUD propriétés

**Commit ton code:**
```bash
git add .
git commit -m "feat: init project with basic auth and properties"
git push origin develop
```

Prochaine étape? Consulte le fichier `02_PLAN_ACTION_DETAILLE.md` pour les semaines suivantes! 🚀

---

## 🆘 QUESTIONS?

Garde à côté:
- **Docs Flask**: https://flask.palletsprojects.com/
- **Docs MongoDB**: https://docs.mongodb.com/
- **Docs PyMongo**: https://pymongo.readthedocs.io/
- **MDN Web Docs**: https://developer.mozilla.org/

Bon courage! 💪
