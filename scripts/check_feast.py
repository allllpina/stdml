from feast import FeatureStore


def main():
    print("Ініціалізація підключення до Feast...")
    store = FeatureStore(repo_path="infra/feast")

    # Отримуємо об'єкт нашого FeatureView та автоматично дістаємо назви всіх фічей
    feature_view = store.get_feature_view("respondent_features")
    feature_refs = [f"{feature_view.name}:{f.name}" for f in feature_view.features]

    test_survey_id = 1
    print(
        f"Запитуємо всі фічі ({len(feature_refs)} шт.) з Redis для survey_id = {test_survey_id}..."
    )

    feature_vector = store.get_online_features(
        features=feature_refs, entity_rows=[{"survey_id": test_survey_id}]
    ).to_dict()

    print("\повний вектор фічей із Redis:")
    for key, values in feature_vector.items():
        print(f"  {key}: {values[0]}")


if __name__ == "__main__":
    main()
