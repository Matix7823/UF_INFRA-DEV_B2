import pyodbc
import os
from flask import current_app

class DBService:
    def __init__(self):
        # Configuration SQL Server 2025 Express
        # Utilisation de Windows Authentication (Trusted_Connection=yes)
        self.server = 'localhost\\SQLEXPRESS'
        self.database = 'Ymmo_DB'
        self.driver = '{ODBC Driver 18 for SQL Server}'
        
        # Chaîne de connexion
        self.conn_str = (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            "Trusted_Connection=yes;"
            "Encrypt=no;" 
        )

    def get_connection(self):
        try:
            return pyodbc.connect(self.conn_str)
        except Exception as e:
            print(f"Erreur de connexion SQL Server: {e}")
            return None

    def fetch_all_properties(self, prix_min=None, prix_max=None, ville=None):
        conn = self.get_connection()
        if not conn: return []
        
        cursor = conn.cursor()
        query = "SELECT id_bien, titre, ville, prix, type_bien, surface, chambres, description, status, dpe, date_annonce FROM Biens WHERE 1=1"
        params = []
        
        if prix_min:
            query += " AND prix >= ?"
            params.append(prix_min)
        if prix_max:
            query += " AND prix <= ?"
            params.append(prix_max)
        if ville:
            query += " AND ville LIKE ?"
            params.append(f"%{ville}%")
            
        query += " ORDER BY date_annonce DESC"
        
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            
        conn.close()
        return results

    def fetch_property_by_id(self, prop_id):
        conn = self.get_connection()
        if not conn: return None
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Biens WHERE id_bien = ?", (prop_id,))
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        
        conn.close()
        return dict(zip(columns, row)) if row else None

    def add_property(self, data):
        conn = self.get_connection()
        if not conn: return None
        
        cursor = conn.cursor()
        query = """
            INSERT INTO Biens (titre, ville, prix, type_bien, surface, chambres, description, status, dpe)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data.get('titre'),
            data.get('ville'),
            data.get('prix'),
            data.get('type_bien'),
            data.get('surface'),
            data.get('chambres'),
            data.get('description'),
            data.get('status', 'disponible'),
            data.get('dpe', 'A')
        )
        
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.execute("SELECT @@IDENTITY").fetchval()
        conn.close()
        return last_id
