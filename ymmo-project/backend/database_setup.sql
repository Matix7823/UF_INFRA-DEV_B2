/* 
    Configuration SQL Server : Script d'initialisation de la base de données
    A exécuter dans SQL Server Management Studio (SSMS) sur la VM 1.
*/

-- 1. Création de la base de données
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Ymmo_DB')
BEGIN
    CREATE DATABASE Ymmo_DB;
END
GO

USE Ymmo_DB;
GO

-- 2. Création de la table des Biens (Schéma optimisé pour le Frontend Premium)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Biens]') AND type in (N'U'))
BEGIN
    CREATE TABLE Biens (
        id_bien INT PRIMARY KEY IDENTITY(1,1),
        titre NVARCHAR(255) NOT NULL,
        ville NVARCHAR(100) NOT NULL,
        prix DECIMAL(18, 2) NOT NULL,
        type_bien NVARCHAR(50), -- Villa, Appartement, Penthouse
        surface INT,
        chambres INT,
        description NVARCHAR(MAX),
        status NVARCHAR(20) DEFAULT 'disponible', -- disponible, vendu
        dpe NCHAR(1) DEFAULT 'A',
        date_annonce DATETIME DEFAULT GETDATE(),
        equipements NVARCHAR(MAX) -- Stockage JSON pour les options luxe
    );
END
GO

-- 3. Insertion de données de démonstration (Seed Data)
INSERT INTO Biens (titre, ville, prix, type_bien, surface, chambres, description, dpe, equipements)
VALUES 
('Villa Méditerranéenne', 'Aix-en-Provence', 1250000, 'Villa', 250, 5, 'Magnifique villa avec piscine à débordement et vue sur la Sainte-Victoire.', 'A', '["Piscine", "Domotique", "Cave à vin"]'),
('Penthouse Haussmannien', 'Paris', 2800000, 'Penthouse', 180, 4, 'Dernier étage avec terrasse panoramique sur la Tour Eiffel. Prestations exceptionnelles.', 'B', '["Terrasse", "Ascenseur privé", "Climatisation"]'),
('Appartement Loft Industriel', 'Lyon', 650000, 'Appartement', 120, 3, 'Ancien atelier rénové par architecte. Grands volumes et luminosité constante.', 'C', '["Cuisine équipée", "Parking"]'),
('Bastide Provençale', 'Marseille', 890000, 'Villa', 210, 6, 'Charme de l''ancien avec rénovation moderne. Grand jardin arboré.', 'B', '["Jardin", "Cheminée"]');
GO

PRINT 'Base de données Ymmo_DB initialisée avec succès.';
