from pydantic import BaseModel
from typing import List

class ExtractedTourData(BaseModel):
    """
    Input schema for Tour Machine Learning model.
    """
    behaviors: List[str]
    id: str
    locations: List[str]
    rating: float
    
class BehaviorLocations(BaseModel):
    """
    Input schema for Tour Machine Learning model.
    """
    locations: List[str]
