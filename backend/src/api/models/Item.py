from pydantic import BaseModel, validator
import re


class Item (BaseModel):    
    id: int = -1 # Server-generated  
    city: str # UTF-8!!!
    start_date: str # more like date, US-locale formatted
    end_date: str # more like date
    price: str # More like decimal, 2 digits
    status: str # Looks like Enum: Never, Seldom, Yearly, Monthly, Weekly, Daily. We could validate, but let's not make too many assumptions...
    color: str # "#RRGGBB"

    def isUsDateFormat (date: str) -> bool:
        pattern = re.compile ("^(\d{1,2}/\d{1,2}/\d+)$")
        if pattern.match (date):
            return True
        
        return False

    @validator("start_date")
    def start_date_UsFormat(cls, start_date):        
        if Item.isUsDateFormat (start_date):
            return start_date
        else:
            raise ValueError(f"start_date '{start_date}' is not of format 'MM/DD/YYYY'")
        
    @validator("end_date")
    def end_date_UsFormat(cls, end_date):
        if Item.isUsDateFormat (end_date):
            return end_date
        else:
            raise ValueError(f"start_date '{end_date}' is not of format 'MM/DD/YYYY'")
    
    @validator("color")
    def color_RgbFormat(cls, color):
        pattern = re.compile ("^(#[0-9a-fA-F]{6})$")
        if pattern.match (color):
            return color
        else:
            raise ValueError(f"color '{color}' is not of format '#RRGGBB'")
        
    @validator("price")
    def price_DecimalFormat(cls, price):
        pattern = re.compile ("^(\d+\.\d{2})$")
        if pattern.match (price):
            return price
        else:
            raise ValueError(f"price '{price}' is not of decimal format 'X.YY'")