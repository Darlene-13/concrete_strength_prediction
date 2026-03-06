"""
    Pydantic schemas define the shape and validation rules of your API's input and output. FastAPI uses them to:
        Automatically validate incoming JSON — if cement is missing or negative FastAPI rejects it before it reaches your model
        Auto-generate API documentation at /docs
        Serialize response back to clean JSON

    What We Need — Two Schemas
    Schema 1 — ConcreteInput
        Defines what the API expects to receive. Maps to the 8 raw ingredients plus age. Each field needs:

        A type (float or int)
        A default value or ... (meaning required)
        Validation constraints — no negative values allowed physically

    Schema 2 — PredictionOutput
        Defines what the API returns back to Spring Boot.
"""

# Pydantic is the most used data validation method for python.

from pydantic import BaseModel, Field

class ConcreteInput(BaseModel):
    """
    Input schema for concrete mix ingredients
    All quantities in kg/m^3 except Age
    """

    cement: float = Field(..., gt=0, description="Cement in kg/m^3")
    blast_furnace_slag: float= Field(0.0, ge = 0, description="Blast furnace slag in kg/m^3")
    fly_ash:float = Field(0.0, ge = 0, description="Fly ash in kg/m^3")
    water:float = Field(..., gt=0, description="Water in concrete in kg/m^3")
    superplasticizer: float = Field(0.0, ge = 0, description="Superplasticizer in kg/m^3")
    coarse_aggregate: float = Field(..., gt = 0, description="Coarse aggregate in kg/m^3")
    fine_aggregate: float = Field(0.0, ge = 0, description="Fine aggregate in kg/m^3")
    age: int = Field(..., gt = 0, description="Age in kg/m^3")

    class Config:
        json_schema_extra = {
            "example": {
                "cement": 350.0,
                "blast_furnace_slag": 0.0,
                "fly_ash": 0.0,
                "water": 175.0,
                "superplasticizer": 0.0,
                "coarse_aggregate": 1050.0,
                "fine_aggregate": 800.0,
                "age": 28
            }
        }


class PredictionOutput(BaseModel):
    """
    Output schema for strength predictions
    """

    predict_strength_mpa: float
    model_version: str
    status: str


