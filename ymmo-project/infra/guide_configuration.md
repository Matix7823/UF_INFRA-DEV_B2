# Guide de Configuration (Tutoriel Oral Partique)

Ce document résume les manipulations à réaliser sur vos VM pour l'Oral.

## 1. Installation de l'Active Directory (AD DS)
1. Ouvrez le **Gestionnaire de Serveur**.
2. Cliquez sur **Gérer > Ajouter des rôles et fonctionnalités**.
3. Cochez **Services AD DS**. Validez l'installation.
4. Dans le petit drapeau de notification, cliquez sur **Promouvoir ce serveur en contrôleur de domaine**.
5. Choisissez "Ajouter une nouvelle forêt" et nommez-la `ymmo.local`.
6. Terminez l'assistant et redémarrez.

## 2. Configuration DNS & DHCP
1. Le DNS s'installe avec l'AD. Les requêtes hors `ymmo.local` doivent être redirigées (Redirecteurs) vers `8.8.8.8` ou celui du FAI.
2. Ajoutez le rôle **Serveur DHCP**.
3. Créez une étendue (ex: `192.168.1.100` à `192.168.1.200` si vous êtes en /24 classique pour la démo).
4. Configurez les options d'étendue : 
   - Routeur (Passerelle) : L'IP de votre pare-feu
   - Serveurs DNS : L'IP de ce serveur Windows.

## 3. Configuration des GPO (Options obligatoires)
1. Touche Win + R -> `gpmc.msc`
2. Créer une GPO sur l'OU cible : `GPO_Securite_Ymmo`.
3. Éditez-la :
   - Complexité du mot de passe (*Configuration Ordinateur > Stratégies > Paramètres Windows > Paramètres de sécurité > Stratégies de compte > Stratégie de mot de passe*). Exigences : 12 caractères mini.
   - Verrouillage (*Stratégie de verrouillage du compte*) : 5 tentatives invalides = verrouillage de 30 min.

## 4. Partage de fichier & NTFS
1. Sur le disque `C:` ou `D:`, créer un dossier "Partage_Ymmo".
2. Clic droit -> Propriétés -> Partage Avancé -> Autorisations : Mettre "Tout le monde" en "Contrôle total" (Le filtrage se fera via l'onglet Sécurité !).
3. Onglet Sécurité -> Avancé -> Désactiver l'héritage.
4. Supprimer les utilisateurs locaux et ajouter uniquement les Groupes créés dans l'AD (Ex: `G_Direction`) avec les droits de "Modification" ou "Lecture/exécution".
