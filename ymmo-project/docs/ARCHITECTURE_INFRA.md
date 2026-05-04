# Dossier Technique d'Infrastructure - Ymmo

Ce document de référence rassemble les liens et le résumé de la politique technique pour le déploiement du réseau des différentes agences du groupe Ymmo.

## 1. Schéma d'Architecture Réseau
*Note au candidat: N'oubliez pas d'inclure votre schéma `draw.io` ou `Lucidchart` final dans ce rapport.*

Le siège centralise les services identitaires et partagés, tandis que chaque agence possède un réseau local plus léger, interconnecté via un tunnel IPsec.

## 2. Plan d'Adressage IP
Les spécificités du routage (découpage VLAN, subnet) et les IPs statiques des serveurs principaux sont détaillées dans le dossier 👉 [Voir le tableau d'adressage IP](../infra/plan_adressage.md).

## 3. Matrice des Droits & Active Directory
Les accès aux données de l'entreprise sont rigoureusement compartimentés via le système NTFS et intégrés aux OU Active Directory.
👉 [Voir la politique des droits et GPO](../infra/droits_acces.md)

## 4. Budget & Matériel
Estimation budgétaire du matériel on-premise et stratégie Cloud associée.
👉 [Voir l'estimation budgétaire](../infra/budget_materiel.md)

## 5. Politique de Sécurité
- Pare-Feu UTM Fortinet en entrée du siège. Tous les flux entrants spontanés sont **Dropés** (Default-Deny). Seuls les ports nécessaires sont ouverts (HTTPS: 443, VPN: 500/4500 UDP).
- Mots de passe sécurisés par GPO (12 caractères, verrouillage au bout de 5 échecs).
- Le serveur Web interroge la base de données en base arrière (jamais accessible directement au public).

## 6. Plan de Sauvegarde & Supervision
- **Supervisor** : Centreon ou Zabbix installé sur une VM dédiée, exploitant SNMPv3 sur tout le matériel réseau.
- **Sauvegarde On-Prem** : Solution intégrée type `Veeam Backup & Replication`. Logiciel configuré sur la règle du 3-2-1 :
  - 3 copies de données.
  - 2 supports différents (NAS sur site, NAS déporté ou bande).
  - 1 copie hors site ou Cloud Inmuable (Contre les ransomwares).
