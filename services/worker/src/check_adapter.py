import logging
from pathlib import Path

from src.adapters.outbound.feast_provider import FeastFeatureProvider

logging.basicConfig(level=logging.INFO)


def main():
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    repo_path = str(project_root / "infra" / "feast")

    print(f"Looking for Feast config in: {repo_path}")
    print("Initialization of Feast-adapter...")
    provider = FeastFeatureProvider(repo_path=repo_path)

    test_id = 1
    print(f"Requesting data for respondent_id={test_id}...\n")

    features = provider.get_features(respondent_id=test_id)

    if features:
        print("Success! Pydantic model has built succesfully:")
        print(features.model_dump_json(indent=2))
    else:
        print("Data has not been found or error has occured.")


if __name__ == "__main__":
    main()
