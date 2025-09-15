import os
import psycopg2
import json

DATABASE_URL = os.getenv("DATABASE_URL")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def restore_json_file_from_db(filename):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT content FROM json_backups WHERE filename = %s", (filename,))
            row = cur.fetchone()
            if not row:
                print(f"Aucune sauvegarde trouvée pour {filename}.")
                return
            content = row[0]
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Restauration de {filename} effectuée.")

def main():
    # Restaure tous les fichiers sauvegardés
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT filename FROM json_backups")
            files = [row[0] for row in cur.fetchall()]
    for filename in files:
        restore_json_file_from_db(filename)

if __name__ == "__main__":
    main()