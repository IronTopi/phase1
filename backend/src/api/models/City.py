from pydantic import BaseModel

class City (BaseModel):    
    id: int    
    city: str # UTF-8!!!
    start_date: str # more like date, US-locale formatted
    end_data: str # more like date
    price: str # More like decimal, 2 digits
    status: str # Looks like Enum: Never, Seldom, Yearly, Monthly, Weekly, Daily
    color: str # "#RRGGBB" -> check!