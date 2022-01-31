from pydantic import BaseModel


def to_title(field: str) -> str:
    return field.title()


class CarEntity(BaseModel):
    make_name: str
    model_name: str

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_title

    def __eq__(self, other: "CarEntity") -> bool:
        return (
            self.make_name.lower() == other.make_name.lower() and self.model_name.lower() == other.model_name.lower()
        )


class ResponseEntity(BaseModel):
    count: int
    message: str
    results: list[CarEntity]

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_title
