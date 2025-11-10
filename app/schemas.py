from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

NameStr = Annotated[str,StringConstraints(min_length = 1, max_length = 100)]
YearStartedInt = Annotated[int, min = 1900, max = 2100] #revisit later maybe
TitleStr = Annotated[str, StringConstraints(min_length = 1, max_length = 255)]
PagesInt = Annotated[int, min = 1, max = 10000]

class AuthorCreate(BaseModel):
    id: int 
    name: NameStr
    email: EmailStr
    year_started : YearStartedInt

class AuthorRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int 
    name: NameStr
    email: EmailStr
    year_started : YearStartedInt

class AuthorUpdate(BaseModel):
    id: int 
    name: NameStr
    email: EmailStr
    year_started : YearStartedInt

class AuthorPatch(BaseModel):
    id: Optional[int] = None 
    name: Optional[NameStr] = None
    email: Optional[EmailStr] = None
    year_started : Optional[YearStartedInt] = None

class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int 
    title: TitleStr
    pages: PagesInt
    authors_id : int

class BookCreate(BaseModel):

    id: int 
    title: TitleStr
    pages: PagesInt
    authors_id : int