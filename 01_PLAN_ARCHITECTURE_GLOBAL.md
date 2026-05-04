# 🏗️ PLAN GLOBAL D'ARCHITECTURE - Projet Ymmo

**Projet**: Plateforme immobilière Ymmo  
**Équipe**: 2 personnes  
**Stack**: Python (Backend) + HTML/CSS/JS vanilla (Frontend) + MongoDB (BDD)  

---

## 📊 ARCHITECTURE GLOBALE

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE YMMO                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │   FRONTEND        │         │    BACKEND       │              │
│  │  (Client-side)    │◄────────│   (API REST)     │              │
│  ├──────────────────┤         ├──────────────────┤              │
│  │ • HTML            │         │ • Python/Flask   │              │
│  │ • CSS             │         │ • Routes CRUD    │              │
│  │ • Vanilla JS      │         │ • Authentification│              │
│  │ • Responsive      │         │ • Traitement     │              │
│  │ • Accessible      │         │  données        │              │
│  └──────────────────┘         └────────┬─────────┘              │
│           │                             │                        │
│           │                    ┌────────▼─────────┐              │
│           │                    │   MONGODB        │              │
│           │                    ├──────────────────┤              │
│           │                    │ • Collections    │              │
│           │                    │ • Documents      │              │
│           │                    │ • Indexing       │              │
│           │                    └──────────────────┘              │
│           │                                                      │
│           └──────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │          MODULE ANALYSE & DONNÉES (Python)              │   │
│  │  • Scripts d'analyse de tendances                       │   │
│  │  • Prédictions de prix / zones populaires              │   │
│  │  • Rapports de ventes                                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ STACK TECHNOLOGIQUE

### Backend
```
Flask (Framework Python léger)
├── Routes REST (GET, POST, PUT, DELETE)
├── Authentification (JWT ou Sessions)
├── Validation des données
├── Gestion des erreurs
└── CORS pour le frontend

MongoDB
├── Collections: Users, Properties, Listings, Analytics
├── Indexation pour performance
└── Backups réguliers
```

### Frontend
```
HTML+ CSS + Vanilla JavaScript
├── Responsive Design (Mobile, Tablet, Desktop)
├── Accessibilité (WCAG 2.1)
├── Fetch API pour communiquer avec le backend
├── DOM Manipulation
└── LocalStorage pour données persistantes
```

### Outils & Services
```
Git + GitHub (Versionning)
├── Branches: main, dev, feature/*
├── Pull Requests
└── Documentation de commits

Documentation
├── Fonctionnelle (User stories, workflows)
├── Technique (API, installation, déploiement)
└── Code comments en français

Testing & Validation
├── Tests unitaires (Python: pytest)
├── Tests manuels (Navigateur)
└── Validation HTML/CSS/JS
```

---

## 👥 RÉPARTITION POUR 2 PERSONNES

### Option A: Répartition par domaine (RECOMMANDÉE)

**Personne 1 - DÉVELOPPEUR BACKEND + INFRA**
- Architecture API REST (Flask)
- Modèles de données (MongoDB)
- Authentification & sécurité
- Analyse de données (scripts Python)
- Infrastructure réseau (Windows Server, VPN)
- Documentation technique

**Personne 2 - DÉVELOPPEUR FRONTEND**
- Interface utilisateur (HTML/CSS)
- Interactions JavaScript
- Responsive design & accessibilité
- Intégration API
- Tests frontend
- Documentation utilisateur

### Option B: Répartition par feature
```
Sprint 1: Both work together on auth + basic structure
Sprint 2: P1 does API endpoints, P2 does UI pages
Sprint 3: Both integrate + P1 does analysis module
Sprint 4: Both do testing + documentation
```

---

## 📋 PHASES DU PROJET

### Phase 1: Planification & Setup (1-2 semaines)
**Livrables**:
- [ ] Spécifications détaillées (Document)
- [ ] Schéma base de données (MCD/MLD)
- [ ] Design UI mockups (Figma ou papier)
- [ ] Setup repo Git
- [ ] Setup environnements (local, test, prod)

**Tâches**:
```
Backend:
- Installer Flask + dépendances
- Configurer MongoDB local
- Structure de projet Flask
- Models/schemas de base

Frontend:
- Setup structure HTML de base
- Fichiers CSS organisés
- Fichier JS structure
- Assets (images, icons)
```

---

### Phase 2: Développement Core (3-4 semaines)
**Livrables**:
- [ ] API REST fonctionnelle (tous endpoints)
- [ ] Pages web principales (listing, détail, formulaires)
- [ ] Authentification complète
- [ ] Base de données peuplée

**Tâches Backend**:
```
1. Routes d'authentification (login/register)
2. CRUD Biens immobiliers
3. CRUD Utilisateurs
4. CRUD Annonces
5. Recherche & filtrage
6. Upload images
```

**Tâches Frontend**:
```
1. Page d'accueil
2. Listing des biens
3. Détail d'un bien
4. Formulaire de création/édition
5. Dashboard utilisateur
6. Authentification (login/register)
7. Responsive design global
```

---

### Phase 3: Fonctionnalités Avancées (2-3 semaines)
**Livrables**:
- [ ] Module analyse de données
- [ ] Dashboard analytique
- [ ] Rapports de ventes
- [ ] Prédictions prix

**Tâches**:
```
Backend:
- Scripts d'analyse (Pandas, Numpy)
- Endpoints pour statistiques
- Caching des résultats

Frontend:
- Graphiques (Chart.js ou Canvas)
- Pages de statistiques
- Formulaires filtrage
```

---

### Phase 4: Infrastructure & Sécurité (2-3 semaines)
**Livrables**:
- [ ] Windows Server configuré (AD, GPO)
- [ ] Architecture réseau sécurisée
- [ ] VPN/IPSec site-to-site
- [ ] Documention complète

**Tâches Infra**:
```
- Setup Windows Server
- Active Directory
- Stratégies de groupe
- Configuration VPN
- Plan d'adressage IP
- Pare-feu/Filtrage
- Sauvegarde & Monitoring
```

---

### Phase 5: Documentation & Déploiement (1-2 semaines)
**Livrables**:
- [ ] Documentation fonctionnelle
- [ ] Documentation technique
- [ ] Guide déploiement
- [ ] Guide utilisateur
- [ ] Code bien commenté

**Tâches**:
```
Documentation Fonctionnelle:
- User stories
- Workflows
- Screenshots annotés
- FAQ

Documentation Technique:
- Installation & setup
- Architecture détaillée
- API documentation
- Guide configuration serveurs
```

---

### Phase 6: Tests & Optimisation (1 semaine)
**Livrables**:
- [ ] Tests complétés
- [ ] Bugs corrigés
- [ ] Performance optimisée
- [ ] Sécurité vérifiée

**Tâches**:
```
- Tests fonctionnels complets
- Tests de sécurité
- Tests de performance
- Tests d'accessibilité
- Tests cross-browser
- Corrections bugs
```

---

### Phase 7: Préparation Oral & Démo (1 semaine)
**Livrables**:
- [ ] Présentation prête
- [ ] Démo en live prête
- [ ] VMs en fonctionnement
- [ ] Slides/vidéo

**Tâches**:
```
- Préparation présentation
- Séquences de démo
- Tests démo (edge cases)
- Slides professionnels
- Répétition orale
```

---

## 🗄️ MODÈLE DE DONNÉES (MongoDB)

### Collections et Documents

```javascript
// Collection: users
{
  _id: ObjectId,
  email: String,
  password_hash: String,
  nom: String,
  prenom: String,
  role: String, // "agent", "client", "admin"
  telephone: String,
  adresse: String,
  agence_id: ObjectId,
  date_creation: Date,
  actif: Boolean
}

// Collection: properties
{
  _id: ObjectId,
  titre: String,
  description: String,
  type: String, // "maison", "appartement", etc.
  prix: Number,
  surface: Number,
  chambres: Number,
  salles_bain: Number,
  localisation: {
    rue: String,
    code_postal: String,
    ville: String,
    latitude: Number,
    longitude: Number,
    region: String
  },
  images: [String], // URLs images
  agent_id: ObjectId,
  agence_id: ObjectId,
  date_ajout: Date,
  status: String, // "disponible", "vendue", "en_cours"
  caracteristiques: {
    parking: Boolean,
    jardin: Boolean,
    ascenseur: Boolean,
    chauffage: String
  }
}

// Collection: listings (annonces)
{
  _id: ObjectId,
  property_id: ObjectId,
  type: String, // "vente", "location"
  prix: Number,
  date_creation: Date,
  date_expiration: Date,
  agent_id: ObjectId,
  actif: Boolean
}

// Collection: analytics
{
  _id: ObjectId,
  date: Date,
  region: String,
  prix_moyen: Number,
  nombre_ventes: Number,
  tendance: String,
  donnees_brutes: Object
}

// Collection: agencies
{
  _id: ObjectId,
  nom: String,
  ville: String,
  adresse: String,
  telephone: String,
  manager_id: ObjectId,
  nombre_agents: Number
}
```

---

## 🔐 SÉCURITÉ & AUTHENTIFICATION

### Authentification
```
1. Registration/Login avec validation
2. Password hashing (bcrypt)
3. JWT tokens (or Flask sessions)
4. Refresh tokens pour sécurité
5. HTTPS en production
```

### Autorisation (RBAC)
```
Rôles:
- Admin: Accès complet
- Agent: Gestion biens, listings, clients
- Client: Consultation, sauvegarde favoris
```

### Protection CSRF/XSS
```
- CSRF tokens dans formulaires
- Content-Security-Policy headers
- Input validation & sanitization
- SQL Injection protection (MongoDB)
```

---

## 📂 STRUCTURE DE PROJET RECOMMANDÉE

```
ymmo-project/
│
├── backend/
│   ├── app.py (Point d'entrée Flask)
│   ├── config.py (Configuration)
│   ├── requirements.txt (Dépendances Python)
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── properties.py
│   │   ├── users.py
│   │   ├── listings.py
│   │   └── analytics.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── property.py
│   │   ├── listing.py
│   │   └── analytics.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── property_service.py
│   │   └── analytics_service.py
│   │
│   ├── utils/
│   │   ├── db_connection.py
│   │   └── validators.py
│   │
│   └── tests/
│       ├── test_auth.py
│       └── test_properties.py
│
├── frontend/
│   ├── index.html
│   ├── pages/
│   │   ├── listing.html
│   │   ├── property-detail.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── analytics.html
│   │
│   ├── css/
│   │   ├── style.css (Main)
│   │   ├── responsive.css
│   │   ├── components.css
│   │   └── accessibility.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── api.js (Communication backend)
│   │   ├── auth.js (Auth logic)
│   │   ├── ui.js (DOM manipulation)
│   │   └── utils.js
│   │
│   └── assets/
│       ├── images/
│       ├── icons/
│       └── fonts/
│
├── docs/
│   ├── SPECIFICATIONS.md
│   ├── API_DOCUMENTATION.md
│   ├── TECHNICAL_GUIDE.md
│   ├── USER_GUIDE.md
│   └── DEPLOYMENT.md
│
├── infra/
│   ├── network-architecture.md
│   ├── server-configuration.md
│   ├── vpn-setup.md
│   ├── security-policy.md
│   └── backup-plan.md
│
└── README.md
```

---

## 🚀 DÉMARRAGE IMMÉDIAT

### Jour 1: Setup initial

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install flask flask-cors pymongo python-dotenv bcrypt pyjwt pandas numpy

# Créer .env
MONGO_URI=mongodb://localhost:27017/ymmo
SECRET_KEY=votre_clé_secrète
DEBUG=True

# Test connexion MongoDB
python -c "import pymongo; print('MongoDB OK')"
```

```bash
# Frontend
cd frontend
# Simplement ouvrir index.html dans le navigateur
# Ou utiliser un serveur local:
python -m http.server 8000
```

### Jour 2-3: Spécifications détaillées

Créer:
- Document spécifications (qui fait quoi, UI mockups)
- Schéma base de données détaillé
- User stories par fonctionnalité

---

## 📊 TIMELINE ESTIMÉE

```
Semaine 1: Architecture + Setup + Specs
Semaine 2-3: Core API + Pages principales
Semaine 4: Authentification + Intégration complète
Semaine 5: Analyse de données + Module advanced
Semaine 6: Infrastructure + Documentation
Semaine 7: Tests + Optimisation
Semaine 8: Préparation présentation + Démo
```
---

## ✅ CHECKLIST LIVRABLES

### DEV
- [ ] Code source sur GitHub
- [ ] API REST documentée
- [ ] Site web responsive fonctionnel
- [ ] Authentification complète
- [ ] Base de données peuplée
- [ ] Module analyse données
- [ ] Documentation fonctionnelle
- [ ] Documentation technique
- [ ] Tests passants
- [ ] Code bien commenté

### INFRA
- [ ] Windows Server configuré
- [ ] Active Directory en place
- [ ] VPN/IPSec fonctionnel
- [ ] Architecture réseau schématisée
- [ ] Plan d'adressage IP
- [ ] Politique de sécurité documentée
- [ ] Droits d'accès configurés
- [ ] Plan de sauvegarde
- [ ] Démonstration en VMs
- [ ] Guides de configuration

---