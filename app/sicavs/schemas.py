
from pydantic import BaseModel

from app.sicavs.examples import ex_sicav


class Sicav(BaseModel):
    name: str
    registry_number: int
    registry_date: str
    address: str
    initial_share_capital: float
    maximum_statutory_capital: float
    isin: str
    date_latest_brochure: str

    class Config:
        schema_extra = {"example": ex_sicav}


class SearchResponse(BaseModel):
    status: bool = True
    message: str = "Success"
    data: list[Sicav]
