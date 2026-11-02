from typing import Annotated

from pydantic import BaseModel, Field,StringConstraints, ConfigDict


equipmentInt = Annotated[int, Field(gt=0)]
borrower_nameStr = Annotated[str, StringConstraints(min_length=2, max_length=60)]
loanInt = Annotated[int, Field(ge=1, le=14)]
purposeStr = Annotated[str, StringConstraints(min_length=5, max_length=100)]


class EquipCreate(BaseModel):
    equipment_id : equipmentInt
    borrower_name : borrower_nameStr
    loan_days : loanInt
    purpose : purposeStr

class EquipRead(BaseModel):

    model_config=ConfigDict(from_attributes= True)

    id: int
    equipment_id : equipmentInt
    borrower_name : borrower_nameStr
    loan_days : loanInt
    purpose : purposeStr
    status : str
