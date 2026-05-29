import argparse
import psycopg2
import os
import urllib.parse as urlparse

def create_inferences_table():
    """Crée la table inferences sur NeonDB si elle n'existe pas."""
    try:
        url = urlparse.urlparse(os.getenv("NEON_DATABASE_URL"))
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            sslmode='require'
        )
        cursor = conn.cursor()
        print(" Création de la table 'inferences'...")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inferences (
                id SERIAL PRIMARY KEY,
                run_id_future VARCHAR(100) NOT NULL,
                run_id_inference VARCHAR(100) NOT NULL UNIQUE,
                inference_date TIMESTAMP NOT NULL DEFAULT NOW(),
                status VARCHAR(20) DEFAULT 'success',
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inferences_run_id_future ON inferences(run_id_future);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inferences_date ON inferences(inference_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inferences_status ON inferences(status);")

        conn.commit()
        print(" Table 'inferences' créée avec succès (avec colonne status) !")

    except Exception as e:
        print(f" Erreur lors de la création de la table: {e}")
        raise
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    create_inferences_table()


if __name__ == "__main__":
    main()
