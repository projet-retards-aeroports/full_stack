# src/pipelines/inference_preprocessing.py
import pandas as pd
import numpy as np
from src.pipelines.transform_imputation import impute_missing_values
from src.pipelines.transform_features import (
    enrich_aircraft_features,
    add_holiday_features,
    add_temporal_features,
    add_cyclical_features,
    add_period_of_day
)


def prepare_data_for_inference(df: pd.DataFrame, is_future: bool = True):
    """
    Applique tout le pipeline de transformation (imputation + features)
    """
    print(f"\n{'='*60}")
    print(f" LANCEMENT DU PIPELINE INFERENCE")
    print(f"{'='*60}\n")

    # 1. Imputation (utilise ta fonction actuelle)
    df = impute_missing_values(df)

    # 2. Features Aircraft
    df = enrich_aircraft_features(df)

    # 3. Features Holidays
    df = add_holiday_features(df)

    # 4. Features Temporelles
    df = add_temporal_features(df)

    # 5. Features Cycliques
    df = add_cyclical_features(df)

    # 6. Période de la journée
    df = add_period_of_day(df)

    print(f"\n{'='*60}")
    print(f" PIPELINE TERMINÉ - {len(df)} lignes prêtes pour l'inférence")
    print(f"{'='*60}\n")

    return df
