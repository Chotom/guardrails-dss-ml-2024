"""Module with questions models."""

import enum
from abc import ABC

from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseModelCamelConfig(BaseModel, ABC):
    """Base class for all google forms classes, where response model from APi is in camelCase."""

    model_config = ConfigDict(alias_generator=to_camel)


class TextQuestion(BaseModelCamelConfig):
    """Docs: https://developers.google.com/forms/api/reference/rest/v1/forms#TextQuestion."""

    paragraph: bool = False


class ChoiceQuestionType(str, enum.Enum):
    """Possible choice question types: https://developers.google.com/forms/api/reference/rest/v1/forms#ChoiceType."""

    RADIO = "RADIO"
    CHECKBOX = "CHECKBOX"
    DROP_DOWN = "DROP_DOWN"


class Option(BaseModelCamelConfig):
    """Possible text option to choose from choice question."""

    value: str = ""
    is_other: bool = False


class ChoiceQuestion(BaseModelCamelConfig):
    """Docs: https://developers.google.com/forms/api/reference/rest/v1/forms#ChoiceQuestion.

    Attributes:
        type: Type of choice question.
        options: List of values to choose from.
    """

    type: ChoiceQuestionType
    options: list[Option]


class ScaleQuestion(BaseModelCamelConfig):
    """Docs: https://developers.google.com/forms/api/reference/rest/v1/forms#ScaleQuestion."""

    low: int
    high: int
    low_label: str
    high_label: str


class DateQuestion(BaseModelCamelConfig):
    """Docs: https://developers.google.com/forms/api/reference/rest/v1/forms#DateQuestion."""

    include_time: bool = False
    include_year: bool = False


class TimeQuestion(BaseModelCamelConfig):
    """Docs: https://developers.google.com/forms/api/reference/rest/v1/forms#TimeQuestion."""

    duration: bool = False


BaseQuestionModel = TextQuestion | ChoiceQuestion | ScaleQuestion | DateQuestion | TimeQuestion
"""Union of all possible question types."""

BaseQuestionModelAlias = {"textQuestion", "choiceQuestion", "scaleQuestion", "dateQuestion", "timeQuestion"}
"""Aliases from google API for all possible question types."""


class Question(BaseModelCamelConfig):
    """Question class that represents one of the question types.

    Supported question types:
        - TextQuestion
        - ChoiceQuestion
        - ScaleQuestion
        - DateQuestion
        - TimeQuestion

    Attributes:
        question_id: Note that the question id is differed from entry ID used in the pre-filled link.
        question: Question object
    """

    question_id: str
    question: BaseQuestionModel = Field(validation_alias=AliasChoices(*BaseQuestionModelAlias))
