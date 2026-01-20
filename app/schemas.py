from pydantic import BaseModel, Field

# Input for income prediction
class IncomeRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100, description="Year for predicting per capita income")

class IncomeResponse(BaseModel):
    predicted_income: float = Field(..., description="Predicted per capita income")
