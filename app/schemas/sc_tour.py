from pydantic import BaseModel
from typing import List

class TourDataExtracted(BaseModel):
    """
    Input schema for Tour Machine Learning model.
    """
    id: str
    locations: List[str]
    rating: float
class BehaviorLocations(BaseModel):
    """
    Input schema for Tour Machine Learning model.
    """
    locations: List[str]