# Spécifications du Projet Ymmo

## 1. Vue d'ensemble (Qui fait quoi ?)
**Ymmo** est une plateforme de gestion et de publication d'annonces immobilières. Les utilisateurs peuvent visualiser des propriétés, publier des annonces, et consulter des statistiques (Analytics) sur les performances de leurs annonces.

### Rôles Utilisateurs
*   **Visiteur (Non connecté)** : Peut parcourir les annonces publiques, voir les détails d'un bien, et s'inscrire pour devenir un utilisateur standard.
*   **Utilisateur Standard / Chercheur** : Peut sauvegarder ses annonces favorites et contacter directement un agent/propriétaire via la plateforme.
*   **Agent Immobilier / Propriétaire** : Peut créer, modifier et supprimer des biens (properties) et des annonces (listings). A un accès exclusif au *Dashboard* pour piloter son activité et voir les statistiques d'engagement (vues, contacts).
*   **Administrateur** : A une vue globale sur toutes les annonces, utilisateurs et statistiques de la plateforme. Dispose d'un module de modération et de suivi de KPIs globaux.

---

## 2. User Stories par Fonctionnalité

### A. Authentification (Auth)
*   *En tant que visiteur*, je veux pouvoir m'inscrire avec mon email et un mot de passe pour gérer mes annonces ou mes favoris.
*   *En tant qu'utilisateur*, je veux me connecter de manière sécurisée afin d'accéder à mon profil ou à mon Dashboard.
*   *En tant qu'utilisateur*, je veux pouvoir réinitialiser mon mot de passe si je l'oublie pour ne pas perdre accès à mon compte.

### B. Gestion des Biens (Properties) & Annonces (Listings)
*   *En tant qu'Agent*, je veux ajouter une nouvelle propriété avec ses caractéristiques physiques (surface, pièces, localisation) pour la recenser dans ma base.
*   *En tant qu'Agent*, je veux télécharger et gérer les images de ma propriété afin de la rendre attrayante pour les clients.
*   *En tant qu'Agent*, je veux lier une propriété à une offre ("Listing" - Vente/Location) avec un prix, pour qu'elle devienne publique sur le marché.
*   *En tant que Visiteur*, je veux filtrer les annonces (par prix, localisation, type) pour trouver rapidement un logement qui me correspond.

### C. Analytics (Statistiques)
*   *En tant qu'Agent*, je veux voir le nombre de visites et de clics sur mes annonces pour évaluer leur attractivité.
*   *En tant qu'Admin*, je veux visualiser les métriques globales d'utilisation (volume de biens postés par jour, utilisateurs actifs) sur la plateforme.

---

## 3. UI Mockups (Structure simplifiée des Pages)

### Page d'Accueil (`index.html` / `listing.html`)
Cette page sert de vitrine et permet la recherche de biens.
```text
+-------------------------------------------------------------+
| [Logo] Ymmo            [Rechercher...]    [Login / Register]|
+-------------------------------------------------------------+
|                       [Barre de filtres]                    |
| Prix min/max | Localisation | Type (Appartement, Maison)    |
+-------------------------------------------------------------+
|                                                             |
|  +----------------+  +----------------+  +----------------+ |
|  | [ Image ]      |  | [ Image ]      |  | [ Image ]      | |
|  | Titre de l'ap. |  | Titre de l'ap. |  | Titre de l'ap. | |
|  | Prix - Details |  | Prix - Details |  | Prix - Details | |
|  | [Favoris/Voir] |  | [Favoris/Voir] |  | [Favoris/Voir] | |
|  +----------------+  +----------------+  +----------------+ |
+-------------------------------------------------------------+
```

### Dashboard Agent (`dashboard.html`)
Cette zone est privée et réservée aux agents/propriétaires.
```text
+-------------------------------------------------------------+
| [Logo] Ymmo              [Notifications]       [Mon Profil] |
+-----------------------------+-------------------------------+
| Menu Latéral                | Vue Principale (Tableau)      |
| - Vue Synthétique           |  +-------------------------+  |
| - Mes Biens (Properties)    |  | KPIs: 1250 Vues Globales|  |
| - Mes Annonces (Listings)   |  |       15 Contacts       |  |
| - Statistiques (Analytics)  |  +-------------------------+  |
| - Paramètres                |  [Ajouter un bien +]          |
|                             |  - Appartement T3 Paris    [Éditer]
|                             |  - Maison 120m² Lyon       [Éditer]
+-----------------------------+-------------------------------+
```

### Page Détail Propriété (`property-detail.html`)
```text
+-------------------------------------------------------------+
| [Retour aux résultats]                                      |
+-------------------------------------------------------------+
| [Galerie d'Images Principale]           [ Prix : 450 000 € ]|
|                                         [     Contacter    ]|
+-------------------------------------------------------------+
| Description complète :                                      |
| Appartement lumineux, proche commodités...                  |
|                                                             |
| Caractéristiques :                                          |
| - 4 Pièces                 - 85 m²                          |
| - 2 Chambres               - Balcon                         |
+-------------------------------------------------------------+
```
