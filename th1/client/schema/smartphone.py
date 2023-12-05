import pydantic


class Smartphone(pydantic.BaseModel):
    name: str
    vendor_id: str
    phone_type: int
    push_token: str
