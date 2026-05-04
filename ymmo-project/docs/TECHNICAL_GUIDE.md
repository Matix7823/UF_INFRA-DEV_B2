# Guide Technique & Schéma de Base de Données

Ce document décrit l'architecture des données choisie pour le backend Python/Flask et sa liaison avec la base de données MongoDB.

## 1. Schéma de Base de Données Détaillé (MongoDB)

Le système utilise MongoDB, une base de données NoSQL orientée documents (JSON/BSON), qui offre une grande flexibilité pour les données immobilières dont les attributs peuvent varier en fonction du bien.

### A. Collection `Users`
Stocke les informations des utilisateurs, gère les profils et l'authentification.
```json
{
  "_id": "ObjectId('...')",
  "email": "agent@ymmo.fr",
  "password_hash": "$2b$12$...", // Hash sécurisé par Bcrypt
  "role": "AGENT", // Peut être "ADMIN", "AGENT", "VISITOR", "STANDARD"
  "first_name": "Jean",
  "last_name": "Dupont",
  "phone": "+33123456789",
  "created_at": "2024-04-01T10:00:00Z",
  "updated_at": "2024-04-05T14:30:00Z"
}
```

### B. Collection `Properties`
Représente les données physiques et descriptives d'un bien immobilier, indépendamment de savoir s'il est en vente ou en location.
```json
{
  "_id": "ObjectId('...')",
  "agent_id": "ObjectId('User_Id_Here')",
  "property_type": "APARTMENT", // "HOUSE", "STUDIO", "COMMERCIAL"
  "location": {
    "address": "12 Rue de la Paix",
    "city": "Paris",
    "zipCode": "75002",
    "coordinates": {"lat": 48.8689, "lng": 2.3303}
  },
  "features": {
    "surface_area_sqm": 85,
    "rooms": 4,
    "bedrooms": 2,
    "bathrooms": 1,
    "has_balcony": true,
    "has_parking": false,
    "energy_rating": "C"
  },
  "description": "Superbe appartement lumineux en plein coeur de Paris...",
  "images_urls": ["/assets/images/prop1-a.jpg", "/assets/images/prop1-b.jpg"],
  "created_at": "2024-04-02T09:15:00Z",
  "updated_at": "2024-04-02T09:15:00Z"
}
```

### C. Collection `Listings`
Représente l'annonce en elle-même. Lie une propriété à une intention commerciale (Vente / Location) et gère la visibilité publique.
```json
{
  "_id": "ObjectId('...')",
  "property_id": "ObjectId('Property_Id_Here')",
  "listing_type": "SALE", // ou "RENTAL"
  "price": 450000,
  "currency": "EUR",
  "status": "ACTIVE", // "SOLD", "RENTED", "INACTIVE", "DRAFT"
  "visibility": "PUBLIC",
  "created_at": "2024-04-03T11:00:00Z",
  "updated_at": "2024-04-03T11:00:00Z"
}
```

### D. Collection `Analytics`
Stocke les métriques de performance et l'engagement des utilisateurs par rapport aux annonces. Cette structure est pensée pour de l'agrégation de données (via Pandas/Numpy côté back-end si besoin).
```json
{
  "_id": "ObjectId('...')",
  "listing_id": "ObjectId('Listing_Id_Here')",
  "views_count": 1250,
  "unique_visitors": 980,
  "contact_requests": 15,
  "favorites_count": 42,
  "last_viewed": "2024-04-07T10:15:00Z"
}
```

---

## 2. Relations Fonctionnelles & Workflows

Bien que MongoDB soit NoSQL, des schémas de références logiques existent entre les collections :

1. **Création d'un bien** : Un utilisateur (`User` avec le rôle `AGENT`) crée un bien (`Property`). La référence `agent_id` garantit qu'il est l'unique créateur et propriétaire du droit de modification de ces données.
2. **Mise sur le marché** : L'Agent crée ensuite une offre (`Listing`) et la lie à son bien (`property_id`). Un bien peut avoir plusieurs contrats passés historiquement, mais un seul actif à la fois.
3. **Tracking & Statistiques** : Chaque interaction publique (clic sur un bien depuis la page de recherche) déclenche une mise à jour d'un document `Analytics` associé au `listing_id` de l'annonce affichée.
