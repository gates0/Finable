from pydantic import BaseModel

class OTPVerify(BaseModel):
    user_id: str
    otp: str
