from pydantic import BaseModel


class CourseRead(BaseModel):
    id: int
    title: str
    slug: str
    price: int = 0

    model_config = {
        "from_attributes": True
    }
