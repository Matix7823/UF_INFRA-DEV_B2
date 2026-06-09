# Guide de Déploiement - Projet Ymmo (VM 1)

Ce guide détaille les étapes pour déployer l'application sur votre serveur Windows (IIS + SQL Server).

## 1. Prérequis sur la VM 1
*   **IIS (Internet Information Services)** activé.
*   **Python 3.10+** installé et ajouté au PATH.
*   **SQL Server 2025 Express** installé avec l'instance `SQLEXPRESS`.
*   **Pilote ODBC 18 for SQL Server** (Indispensable pour Python).

## 2. Déploiement des fichiers
Glissez les dossiers dans les emplacements suivants :

*   **Frontend (Site Web)** :
    👉 `C:\inetpub\wwwroot\ymmo\`
    *Y glisser tout le contenu du dossier `frontend`.*

*   **Backend (API Python)** :
    👉 `C:\Ymmo_Project\backend\`
    *Y glisser tout le contenu du dossier `backend`.*

## 3. Configuration de la Base de Données
1.  Ouvrez **SQL Server Management Studio (SSMS)**.
2.  Connectez-vous à `localhost\SQLEXPRESS`.
3.  Ouvrez et exécutez le fichier `database_setup.sql` situé dans votre dossier backend.
    *Cela créera la base `Ymmo_DB` et la table `Biens` avec des données de test.*

## 4. Installation des dépendances Python
Ouvrez un terminal (PowerShell) en tant qu'administrateur et exécutez :
```powershell
cd C:\Ymmo_Project\backend
pip install -r requirements.txt
```
*(Si le fichier requirements.txt est manquant, installez manuellement : `pip install flask flask-cors pyodbc pandas matplotlib seaborn`)*

## 5. Lancement des Services

### A. Lancer l'API
Dans le terminal PowerShell :
```powershell
python app.py
```
*L'API sera accessible sur `http://localhost:5000`.*

### B. Générer les rapports (Analyse de données)
Pour générer les graphiques demandés pour votre dossier :
```powershell
python generate_reports.py
```
*Les graphiques seront créés dans le dossier `C:\Ymmo_Project\backend\reports\`.*

## 6. Accès au site
Ouvrez votre navigateur sur : `http://localhost/ymmo/index.html`

---
**Note pour le jury** : L'architecture est orientée services, séparant la logique de présentation (Frontend), la logique métier (API Flask) et la persistance des données (SQL Server).
