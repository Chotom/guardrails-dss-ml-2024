"""Models for prompts for all google forms questions for LLMs."""

from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.google_forms.forms_answer_models import BaseAnswerModel, TextQuestionAnswer
from src.google_forms.forms_question_models import (
    BaseQuestionModel,
    TextQuestion,
)
from src.utils.logger import create_logger

logger = create_logger(__name__)


class BasePromptModel(BaseModel, ABC):
    """Base class for prompts for all google forms questions.

    Attributes:
        question_id: ID of the item (Item.item_id).
        question_text: Text of the question (Item.title).
        question_form: Concrete question object from item (Item.question_item.question.question).
        answer_form_model: Concrete answer class used to validate response.
    """

    question_id: str
    question_text: str
    question_form: BaseQuestionModel
    answer_form_model: type[BaseAnswerModel]

    @abstractmethod
    def question_instruction_prompt(self) -> str:
        """Return prompt explaining how to answer the question."""
        raise NotImplementedError


class TextQuestionPrompt(BasePromptModel):
    """Prompt for text question."""

    question_form: TextQuestion
    answer_form_model: type[TextQuestionAnswer] = TextQuestionAnswer

    def question_instruction_prompt(self) -> str:
        """Return prompt for simple text question."""
        question_len_type = "paragraph" if self.question_form.paragraph else "short"

        return f"""Please provide a response to the "Question" using the "JSON Schema" provided below.
        Ensure that the length of your answer corresponds to the specified "Answer length form":

        Question: {self.question_text}
        Answer length form: {question_len_type}
        JSON Schema: {self.answer_form_model.model_json_schema()}
        """
