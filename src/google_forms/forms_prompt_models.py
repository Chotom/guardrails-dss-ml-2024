"""Models for prompts for all google forms questions for LLMs."""

from abc import ABC

from pydantic import BaseModel

from src.google_forms.forms_answer_models import BaseAnswerModel
from src.google_forms.forms_question_models import (
    BaseQuestionModel,
)
from src.utils.logger import create_logger

logger = create_logger(__name__)


class BasePromptModel(BaseModel, ABC):
    """Base class for prompts for all google forms questions.

    Attributes:
        question_id: ID of the item (Item.item_id).
        question_text: Text of the question (Item.title).
        question_form: Concrete question class from item (Item.question_item.question.question).
        answer_form: Concrete answer class that match question.
    """

    question_id: str
    question_text: str
    question_form: BaseQuestionModel
    answer_form: BaseAnswerModel

    def question_instruction_prompt(self) -> str:
        """Return prompt explaining how to answer the question."""
        raise NotImplementedError
