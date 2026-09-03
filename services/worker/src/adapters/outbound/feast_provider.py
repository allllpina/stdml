import logging
from typing import override

from feast import FeatureStore
from src.domain.entities import FeatureValue, RespondentFeatures
from src.ports.feature_provider import FeatureProvider

logger = logging.getLogger(__name__)


class FeastFeatureProvider(FeatureProvider):
    """Implementation of the FeatureProvider port using Feast and Redis."""

    def __init__(self, repo_path: str):
        self.store: FeatureStore = FeatureStore(repo_path=repo_path)
        self.feature_view_name: str = "respondent_features"

        fv = self.store.get_feature_view(self.feature_view_name)
        self.feature_refs: list[str] = [f"{self.feature_view_name}:{f.name}" for f in fv.features]

    @override
    def get_features(self, respondent_id: int) -> RespondentFeatures | None:
        try:
            features_dict: dict[str, list[FeatureValue]] = self.store.get_online_features(
                features=self.feature_refs, entity_rows=[{"survey_id": respondent_id}]
            ).to_dict()

            row: dict[str, FeatureValue] = {key: values[0] for key, values in features_dict.items()}

            if row.get("survey_id") is None:
                return None

            return RespondentFeatures.model_validate(row)

        except Exception as e:
            logger.error(f"Помилка отримання фічей для {respondent_id} з Feast: {e}")
            return None
