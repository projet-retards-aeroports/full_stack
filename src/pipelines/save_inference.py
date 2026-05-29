import argparse
import pandas as pd
import boto3
from io import BytesIO
from datetime import datetime
import uuid
import psycopg2
import os


def save_inference_results(df: pd.DataFrame, run_id: str) -> str:
    """
    Sauvegarde le DataFrame de prédiction sur S3 
    et enregistre les métadonnées dans NeonDB.
    Retourne le run_id_inference généré.

    utilisation via api:
    from src.pipelines.save_inference import save_inference_results
    run_id_inference = save_inference_results(df, request.run_id)

    utilisation via ligne de commande:
    python src/pipelines/save_inference.py \
    --run_id 2026-05-28_123456_abc123 \
    --input_file ./predictions.parquet
    """
    # === Génération du run_id_inference ===
    run_id_inference = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    now = datetime.now()

    # === 1. Sauvegarde sur S3 ===
    year = now.strftime("%Y")
    week = now.strftime("%U")
    s3_key = f"projet_final_lead/inferences/weekly/{year}/{week}/{run_id_inference}/dataframe.parquet"
    bucket = "pat-jedha-lead-bucket-2026"

    buffer = BytesIO()
    df.to_parquet(buffer, index=False, compression="gzip")

    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=s3_key, Body=buffer.getvalue())
    print(f" DataFrame sauvegardé sur S3 → s3://{bucket}/{s3_key}")

    # === 2. Insertion dans NeonDB ===
    try:
        conn = psycopg2.connect(os.getenv("NEON_DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inferences (run_id, run_id_inference, inference_date)
            VALUES (%s, %s, %s)
        """, (run_id, run_id_inference, now))
        conn.commit()
        cursor.close()
        conn.close()
        print(f" Enregistré dans NeonDB → run_id_inference: {run_id_inference}")
    except Exception as e:
        print(f" Erreur NeonDB: {e}")

    return run_id_inference


# ====================== MODE LIGNE DE COMMANDE ======================
def main():
    parser = argparse.ArgumentParser(description="Sauvegarde des résultats d'inférence")
    parser.add_argument("--run_id", type=str, required=True, help="Run ID reçu de Streamlit")
    parser.add_argument("--input_file", type=str, required=True, help="Chemin du fichier parquet à sauvegarder")
    args = parser.parse_args()

    print(f"=== Sauvegarde des résultats pour run_id: {args.run_id} ===")
    
    df = pd.read_parquet(args.input_file)
    run_id_inference = save_inference_results(df, args.run_id)
    
    print(f"Terminé. run_id_inference généré: {run_id_inference}")


if __name__ == "__main__":
    main()
