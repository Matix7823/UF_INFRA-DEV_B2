# Plan d'Adressage IP - Ymmo

Ce plan définit le routage réseau pour relier le siège (Aix) et les 12 agences.

## 1. Topologie Globale
- **Réseau global** : `10.0.0.0/8`
- **Siège Social (Aix-en-Provence)** : `10.1.0.0/16`
- **Agences** : `10.2.0.0/16` à `10.13.0.0/16`

## 2. Découpage du Siège (`10.1.0.0/16`)
Pour séparer le trafic de manière sécurisée, 4 VLANs sont prévus :

| VLAN | Nom | Sous-réseau | Passerelle (Firewall) | Description |
|---|---|---|---|---|
| VLAN 10 | SERVEURS | `10.1.10.0/24` | `10.1.10.254` | Web, AD, Fichiers, BDD |
| VLAN 20 | DIRECTION | `10.1.20.0/24` | `10.1.20.254` | 5 postes fixes + Wi-Fi priv. |
| VLAN 30 | EQUIPES | `10.1.30.0/24` | `10.1.30.254` | 25 postes Commerciaux / RH |
| VLAN 40 | GUESTS | `10.1.40.0/24` | `10.1.40.254` | Accès bridé pour les visiteurs |

**Postes clés (Adresses Statiques) :**
- Routeur IPSec Firewall (Passerelle globale) : `10.1.254.254`
- Serveur Contrôleur de Domaine (PDC) : `10.1.10.10`
- Serveur Fichier / Sauvegarde : `10.1.10.11`
- Serveur Web/Base de données (Local) : `10.1.10.20`

## 3. Plan d'Adressage Agences (Exemple pour l'Agence 1)
Réseau affecté : `10.2.0.0/24` (simplifié car petite structure)

| Rôle | Adresse / Plage |
|---|---|
| Routeur/Firewall local | `10.2.0.254` |
| Plage DHCP Postes | `10.2.0.10` à `10.2.0.50` |
| Imprimante Réseau | `10.2.0.200` (Statique) |
