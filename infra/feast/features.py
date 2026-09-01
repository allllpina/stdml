from datetime import timedelta

from feast import Entity, FeatureView, FileSource, ValueType

respondent = Entity(
    name="survey_id",
    join_keys=["survey_id"],
    description="Унікальний ID респондента опитування",
    value_type=ValueType.INT64,
)

parquet_source = FileSource(
    path="../../ml_workspace/data/data_inf_clean.parquet",
    timestamp_field="Timestamp",
)
# 3. View (Feast сам підтягне SalaryUSD, Country, JobTitle та інші 15 колонок)
respondent_features = FeatureView(
    name="respondent_features",
    entities=[respondent],
    ttl=timedelta(days=3650),
    source=parquet_source,
)
