# Gestion des Droits d'Accès (Active Directory)

La politique d'accès repose sur le principe du "moindre privilège" et est basée sur la matrice de droits du cahier des charges de la société Ymmo.

## 1. Structure de l'Active Directory (OU)
L'arbre AD est basé sur les grands pôles de l'entreprise :
- `OU=Ymmo`
  - `OU=Direction`
  - `OU=Commercial`
  - `OU=Marketing_Com`
  - `OU=Administratif_RH_Juridique`
  - `OU=IT_Support`

## 2. Groupes de Sécurité Globaux
- `G_Direction`
- `G_Commercial`
- `G_Marketing`
- `G_Administratif`
- `G_IT`

## 3. Matrice des Droits (NTFS) sur le Serveur de Fichiers
Le serveur de fichier partage les dossiers suivants. Voici les attributions des droits.

| Dossier Partagé | Direction | Commercial | Marketing | Admin/RH | IT Support |
|---|---|---|---|---|---|
| `\Direction\` | **Lecture/Écriture** | *Interdit* | *Interdit* | *Interdit* | *Interdit* |
| `\Commercial\` | Lecture | **Lecture/Écriture** | Lecture | Lecture | Lecture |
| `\Marketing\` | Lecture | Lecture | **Lecture/Écriture** | Lecture | Lecture |
| `\Administratif\` | Lecture | *Interdit* | *Interdit* | **Lecture/Écriture** | *Interdit* |
| `\IT_Support\` | Lecture | *Interdit* | *Interdit* | *Interdit* | **Lecture/Écriture** |

*Note sur la configuration Windows Server* : L'activation de l'option *Access-Based Enumeration (ABE)* permettra de masquer les dossiers interdits aux utilisateurs non autorisés.
