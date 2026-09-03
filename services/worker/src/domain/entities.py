from datetime import UTC, datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

# Замість Any описуємо реальні типи, які можуть прийти з Feature Store
FeatureValue = int | float | str | bool | None


class InferenceCommand(BaseModel):
    """An inference execution command that comes from the message bus."""

    request_id: str
    respondent_id: int


class ModelSwapCommand(BaseModel):
    """Command to hot-swap the model weights in the worker's memory."""

    model_name: str


class RespondentFeatures(BaseModel):
    """Respondent features retrieved from the Feature Store."""

    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

    database_servers: float | None = Field(None, alias="DatabaseServers")
    survey_year: int | None = Field(None, alias="Survey Year")
    primary_database: str | None = Field(None, alias="PrimaryDatabase")
    other_databases: str | None = Field(None, alias="OtherDatabases")
    career_plans_this_year: str | None = Field(None, alias="CareerPlansThisYear")
    employment_sector: str | None = Field(None, alias="EmploymentSector")
    manage_staff: bool | None = Field(None, alias="ManageStaff")
    salary_usd: float | None = Field(None, alias="SalaryUSD")
    employment_status: str | None = Field(None, alias="EmploymentStatus")
    other_people_on_your_team: int | None = Field(None, alias="OtherPeopleOnYourTeam")
    job_title: str | None = Field(None, alias="JobTitle")
    years_with_this_type_of_job: int | None = Field(None, alias="YearsWithThisTypeOfJob")
    how_many_companies: str | None = Field(None, alias="HowManyCompanies")
    gender: str | None = Field(None, alias="Gender")
    years_with_this_database: int | None = Field(None, alias="YearsWithThisDatabase")
    country: str | None = Field(None, alias="Country")
    population_of_largest_city: str | None = Field(None, alias="PopulationOfLargestCityWithin20Miles")


class PredictionResult(BaseModel):
    """The model's output, to be saved to the database or sent to the client."""

    request_id: str
    respondent_id: int
    prediction: dict[str, FeatureValue]
    processed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
