# Budget, Matériel et Solution Cloud

## 1. Budget Matériel Siège (Aix-en-Provence)
| Item | Description | Quantité | Prix Un. | Total |
|---|---|---|---|---|
| Serveur Hyperviseur | Dell PowerEdge T350 (Xeon, 64Go RAM, 2To SSD RAID1) | 2 | 2 500 € | 5 000 € |
| Pare-feu / Routeur | Fortinet FortiGate 60F (Gestion VPN avancée) | 1 | 800 € | 800 € |
| Switch Coeur de rés. | Cisco Catalyst 9200 (48 ports PoE) | 2 | 1 500 € | 3 000 € |
| Licences Windows | Windows Server 2022 Standard | 2 | 900 € | 1 800 € |

## 2. Budget Matériel par Agence (x12)
| Item | Description | Prix Un. | Total (12) |
|---|---|---|---|
| Routeur VPN | Meraki MX67 (ou FortiGate 40F) | 500 € | 6 000 € |
| Imprimante | MFP Laser Réseau standard | 400 € | 4 800 € |

### Budget Infra Local Estimé : ~21 400 € HT

---

## 3. Proposition de Solution Cloud (Hybride)
Plutôt que d'héberger le frontend et le backend public de l'application Ymmo sur les serveurs locaux d'Aix-en-Provence (risque de goulot d'étranglement ou de panne matérielle), la solution recommande le **Cloud Azure**.

**Architecture Cloud proposée :**
1. **Azure App Service** : Pour héberger l'API Flask backend et servir les assets frontend. (Mise à l'échelle automatique selon le trafic).
2. **Azure Cosmos DB** (API MongoDB) ou **Azure SQL** : Pour la base de données. Sauvegardes automatisées et redondance géographique.
3. **Azure ExpressRoute ou VPN Site-à-Site Azure** : Pour relier le serveur du siège (qui contient l'Active Directory) au Cloud Azure, ce qui permet de lier la base de données métiers au réseau local des commerciaux.
