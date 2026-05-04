# 🏠 Ymmo

[![Bachelor 2](https://img.shields.io/badge/Ynov-Bachelor_2-blue.svg)](https://www.ynov.com/)
[![Speciality](https://img.shields.io/badge/UF-INFRA_%26_DEV-orange.svg)](https://www.ynov.com/)
[![Tech Stack](https://img.shields.io/badge/Stack-Python_%7C_JS_%7C_MongoDB-green.svg)](https://www.ynov.com/)

## 📝 Présentation du Projet

**Ymmo** est un projet de fin d'unité de formation (UF) pour le cursus Bachelor 2 chez Ynov Informatique. L'objectif est de concevoir et réaliser une solution complète pour un groupe immobilier national fictif nommé **Ymmo**, basé à Aix-en-Provence et disposant de 12 agences réparties en France.

La solution combine deux piliers majeurs :
1.  **Développement (DEV)** : Une plateforme web centralisée permettant la gestion des transactions immobilières, enrichie par des outils d'analyse de données (IA) pour l'aide à la décision.
2.  **Infrastructure (INFRA)** : Une architecture réseau sécurisée et évolutive reliant le siège social aux agences via des tunnels VPN/IPSec.

---

## 🚀 Fonctionnalités Clés

### 💻 Partie Développement
- **Gestion Immobilière** : Interface complète pour l'achat, la vente et la consultation de biens résidentiels et professionnels.
- **Analyse de Données & IA** : Scripts Python exploitant les tendances du marché pour prédire les prix et identifier les zones d'investissement stratégiques.
- **Dashboard Analytique** : Visualisation des performances commerciales et des rapports de ventes.
- **Authentification Sécurisée** : Système de connexion avec gestion des rôles (Admin, Agent, Client).
- **Responsive Design** : Interface optimisée pour Desktop, Tablette et Smartphone.

### 🛡️ Partie Infrastructure
- **Réseau Hybride** : Connexion sécurisée du siège (Aix) et des 12 agences via **VPN/IPSec Site-to-Site**.
- **Services Windows Server** : Déploiement d'Active Directory (AD), DNS, DHCP et gestion fine des droits via GPO.
- **Sécurité Réseau** : Mise en œuvre de pare-feu, filtrage de paquets et politique de sécurité stricte.
- **Plan de Sauvegarde** : Stratégie de backup et de haute disponibilité des données critiques.

---

## 🛠️ Stack Technologique

| Composant | Technologie |
| :--- | :--- |
| **Backend** | Python / Flask (REST API) |
| **Base de Données** | MongoDB (NoSQL) |
| **Frontend** | HTML5 / CSS3 / JavaScript Vanilla |
| **Analyse de Données** | Pandas, NumPy, Matplotlib |
| **Infrastructure** | Windows Server 2022, Cisco/Pfsense (Virtualisé) |
| **Versionning** | Git / GitHub |

---

## 📂 Structure du Projet

```text
ymmo-project/
├── backend/            # API Flask, modèles de données et services
│   ├── routes/         # Endpoints de l'API
│   ├── models/         # Définition des documents MongoDB
│   └── services/       # Logique métier et analyse de données
├── frontend/           # Interface utilisateur (HTML/CSS/JS)
│   ├── pages/          # Différentes vues de l'application
│   ├── css/            # Styles (incluant accessibilité & responsive)
│   └── js/             # Logique client et appels API
├── infra/              # Documentation et schémas d'infrastructure
│   ├── network/        # Schémas d'architecture et plans d'adressage
│   └── security/       # Politiques de sécurité et guides AD/GPO
└── docs/               # Documentation fonctionnelle et technique
```

---

## ⚙️ Installation et Démarrage

### Prérequis
- Python 3.9+
- MongoDB (local ou Atlas)
- Un navigateur moderne

### Installation du Backend
1. Naviguez dans le dossier backend :
   ```bash
   cd backend
   ```
2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Configurez votre fichier `.env` avec votre `MONGO_URI`.

### Lancement du Frontend
Ouvrez simplement `frontend/index.html` dans votre navigateur ou utilisez l'extension "Live Server" de VS Code.

---

## 👥 Équipe & Collaboration
Le projet est réalisé en équipe de 2 personnes, suivant les principes **SOLID**, **DRY** et **KISS** pour la qualité de code, et utilisant **Git** pour le versionning collaboratif.

---
