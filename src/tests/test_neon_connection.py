import psycopg2
import os


def test_neon_connection():
    """Teste la connexion à la base NeonDB.
    
    utilisation:
    Depuis la racine du projet
    python src/tests/test_neon_connection.py
    
    avec la variable env directement:
    NEON_DATABASE_URL="postgresql://user:pass@host.neon.tech/db?sslmode=require" \
    python src/tests/test_neon_connection.py
    """
    database_url = os.getenv("NEON_DATABASE_URL")
    
    if not database_url:
        print("ERREUR: Variable d'environnement NEON_DATABASE_URL non définie")
        return False

    try:
        print("🔌 Test de connexion à NeonDB...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print("OK!:  Connexion réussie à NeonDB !")
        print(f"   Version PostgreSQL : {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f" Erreur de connexion : {e}")
        return False


if __name__ == "__main__":
    test_neon_connection()
