from pydantic import BaseModel


class CreateBentoModel(BaseModel):
    algorithm: str

