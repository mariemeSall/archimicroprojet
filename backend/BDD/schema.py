from pydantic import BaseModel


class Coordonnee(BaseModel):
    longitude : float
    latitude: float
    ip : str
    date: str

    class Config:
        orm_mode = True
