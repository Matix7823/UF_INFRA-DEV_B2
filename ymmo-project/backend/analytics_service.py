import pandas as pd
import sqlite3
import numpy as np

class MarketAnalyzer:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_market_trends(self):
        """Calcule les statistiques du marché immobilier avec Pandas et Numpy."""
        try:
            conn = sqlite3.connect(self.db_path)
            # Chargement des données dans un DataFrame Pandas
            df = pd.read_sql_query("SELECT * FROM properties", conn)
            conn.close()

            if df.empty:
                return {
                    "total_properties": 0,
                    "avg_price_sqm": 0,
                    "cities_summary": {}
                }

            # Nettoyage et Calcul: Prix au mètre carré
            # On utilise numpy pour éviter les divisions par zéro
            df['surface'] = df['surface'].replace(0, np.nan) 
            df['price_per_sqm'] = df['prix'] / df['surface']
            
            # Agrégation par ville
            city_stats = df.groupby('ville').agg({
                'id': 'count',
                'prix': 'mean',
                'price_per_sqm': 'mean'
            }).rename(columns={'id': 'count', 'prix': 'avg_price'}).to_dict('index')

            # Formater les NaN possibles en None pour JSON
            for city, stats in city_stats.items():
                if pd.isna(stats['price_per_sqm']):
                    stats['price_per_sqm'] = 0

            avg_sqm = df['price_per_sqm'].mean()

            return {
                "total_properties": int(len(df)),
                "avg_price_sqm": float(avg_sqm) if not pd.isna(avg_sqm) else 0,
                "cities_summary": city_stats
            }
        except Exception as e:
            return {"error": str(e)}
