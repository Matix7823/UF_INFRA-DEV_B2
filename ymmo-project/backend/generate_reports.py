import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_business_reports():
    """
    Génère des graphiques d'analyse immobilière pour le dossier de projet.
    Lit les données directement depuis SQL Server 2025.
    """
    print("--- Génération des Rapports Business Ymmo ---")
    
    # Connexion SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=Ymmo_DB;"
        "Trusted_Connection=yes;"
        "Encrypt=no;"
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql("SELECT * FROM Biens", conn)
        conn.close()
        
        if df.empty:
            print("Erreur: La base de données est vide. Veuillez ajouter des biens avant de lancer l'analyse.")
            return

        # Dossier de sortie pour les graphiques
        output_dir = 'reports'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Style des graphiques
        sns.set_theme(style="whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)

        # 1. Répartition des types de biens
        plt.figure()
        type_counts = df['type_bien'].value_counts()
        type_counts.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        plt.title('Répartition du Portefeuille par Type de Bien')
        plt.ylabel('')
        plt.savefig(f'{output_dir}/repartition_types.png')
        print(f"Graphique 1 généré: {output_dir}/repartition_types.png")

        # 2. Prix moyen par ville
        plt.figure()
        avg_price_city = df.groupby('ville')['prix'].mean().sort_values(ascending=False)
        sns.barplot(x=avg_price_city.index, y=avg_price_city.values, palette='viridis')
        plt.title('Prix Moyen des Biens par Ville')
        plt.xlabel('Ville')
        plt.ylabel('Prix Moyen (€)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/prix_moyen_ville.png')
        print(f"Graphique 2 généré: {output_dir}/prix_moyen_ville.png")

        # 3. Évolution des prix au m² (Si surface présente)
        if 'surface' in df.columns:
            df['prix_m2'] = df['prix'] / df['surface']
            plt.figure()
            sns.histplot(df['prix_m2'], kde=True, color='gold')
            plt.title('Distribution des Prix au Mètre Carré')
            plt.xlabel('Prix au m² (€)')
            plt.savefig(f'{output_dir}/distribution_prix_m2.png')
            print(f"Graphique 3 généré: {output_dir}/distribution_prix_m2.png")

        print("\n--- Analyse terminée avec succès ! ---")

    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")

if __name__ == "__main__":
    generate_business_reports()
