from pydantic import BaseModel
from typing import List, Optional
from fastapi import File, UploadFile

class PushNotification(BaseModel):
    title: str
    body: str
    
    def __str__(self):
        return f"Title: {self.title}\nBody: {self.body}"
    
    def dict(self):
        return {"title": self.title, "body": self.body}
    
class PushRequest(BaseModel):
    push_type: str
    cast_name: Optional[str] = None
    series_name: str
    creativity: float
    demographics: List[int]
    isEmojis: bool = True
    isSlangs: bool = True
    addRequirements: Optional[str] = None
    otherSupportingDocuments: Optional[List[UploadFile]] = None
    selected_trend: Optional[str] = None

class PushResponse(BaseModel):
    english: PushNotification
    malay: PushNotification
    
    def dict(self):
        return {"english": dict(self.english), "malay": dict(self.malay)}
    
class PushRegenerateRequest(BaseModel):
    basePush: Optional[PushNotification] = None
    addRequirements: Optional[str] = None
    
class TrendResponse(BaseModel):
    classification_type: str
    trend_title: str    