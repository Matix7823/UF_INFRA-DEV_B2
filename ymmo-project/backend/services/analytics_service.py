import pandas as pd
import pyodbc
import numpy as np

class MarketAnalyzer:
    def __init__(self):
        self.server = 'localhost\\SQLEXPRESS'
        self.database = 'Ymmo_DB'
        self.conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
        )

    def get_market_trends(self):
        """Calcule les statistiques immobilières via SQL Server et Pandas."""
        try:
            conn = pyodbc.connect(self.conn_str)
            
            # Chargement des données de la table Biens
            query = "SELECT * FROM Biens"
            df = pd.read_sql(query, conn)
            conn.close()

            if df.empty:
                return {
                    "total_properties": 0,
                    "avg_price_sqm": 0,
                    "cities_summary": {}
                }

            # Calcul du prix au m² (évite division par zéro)
            df['surface'] = df['surface'].replace(0, np.nan)
            df['price_per_sqm'] = df['prix'] / df['surface']
            
            # Agrégation par ville
            city_stats = df.groupby('ville').agg({
                'id_bien': 'count',
                'prix': 'mean',
                'price_per_sqm': 'mean'
            }).rename(columns={'id_bien': 'count', 'prix': 'avg_price'}).to_dict('index')

            # Nettoyage des NaN pour compatibilité JSON
            for city, stats in city_stats.items():
                if pd.isna(stats['price_per_sqm']):
                    stats['price_per_sqm'] = 0
                else:
                    stats['price_per_sqm'] = float(stats['price_per_sqm'])
                
                stats['avg_price'] = float(stats['avg_price'])
                stats['count'] = int(stats['count'])

            avg_sqm = df['price_per_sqm'].mean()

            return {
                "total_properties": int(len(df)),
                "avg_price_sqm": float(avg_sqm) if not pd.isna(avg_sqm) else 0,
                "cities_summary": city_stats
            }
        except Exception as e:
            return {"error": str(e)}
