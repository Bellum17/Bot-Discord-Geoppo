import os
import psycopg2
import json

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def clean_pib_data():
    """Nettoie les données PIB dans PostgreSQL pour ne garder que la structure PIB pure."""
    
    # Structure vide pour pib.json (seulement PIB, plus de personnel)
    clean_pib_structure = {}
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Mettre à jour pib.json avec une structure vide
            cur.execute("""
                INSERT INTO json_backups (filename, content)
                VALUES (%s, %s)
                ON CONFLICT (filename) DO UPDATE SET content = EXCLUDED.content
            """, ("pib.json", json.dumps(clean_pib_structure, indent=2)))
            
            # Supprimer les anciennes données personnel.json si elles existent
            cur.execute("DELETE FROM json_backups WHERE filename = %s", ("personnel.json",))
            
            conn.commit()
    
    print("Nettoyage des données PIB dans PostgreSQL effectué.")
    print("Structure PIB réinitialisée (vide).")
    print("Anciennes données personnel.json supprimées de PostgreSQL.")

if __name__ == "__main__":
    clean_pib_data()
