import pytest
from pydantic import ValidationError
from app.schemas import CarInput


def test_blank_model_is_rejected():
    with pytest.raises(ValidationError):
        CarInput(make="Mazda", model=" ", year=2020)