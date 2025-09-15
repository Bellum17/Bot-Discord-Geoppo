import os
import psycopg2
import json

DATABASE_URL = os.getenv("DATABASE_URL")  # Mets l'URL Railway dans tes variables d'environnement
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def save_json_file_to_db(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Fichier {filename} non trouvé.")
        return
    with open(filepath, "r") as f:
        content = f.read()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO json_backups (filename, content)
                VALUES (%s, %s)
                ON CONFLICT (filename) DO UPDATE SET content = EXCLUDED.content
            """, (filename, content))
            conn.commit()
    print(f"Backup de {filename} effectué.")

def main():
    json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    for filename in json_files:
        save_json_file_to_db(filename)

if __name__ == "__main__":
    main()