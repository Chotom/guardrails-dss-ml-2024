"""Modules for answers models to validate responses from LLMs."""

from abc import ABC

from pydantic import BaseModel

from src.utils.logger import create_logger

logger = create_logger(__name__)


class BaseAnswerModel(BaseModel, ABC):
    """Base class for all google forms answer questions.

    Attributes:
        answer: Answer to the question.
    """

    answer: int | str | list[str]


class TextQuestionAnswer(BaseAnswerModel):
    """Answer for text question."""

    answer: str
