"""Module with main form class."""
from pydantic import model_validator

from src.google_forms.forms_question_models import BaseModelCamelConfig, Question
from src.utils.logger import create_logger

logger = create_logger(__name__)


class QuestionItem(BaseModelCamelConfig):
    """Class with question attribute."""

    question: Question


class Item(BaseModelCamelConfig):
    """Forms item class, docs: https://developers.google.com/forms/api/reference/rest/v1/forms#item.

    Note:
        Only QuestionItem class is supported. This means that the QuestionGroupItem for
        Grid questions is not handled, this is due to the differently assigned entry ID
        in Google forms.

    Attributes:
        item_id: The ID of the item. Note that this is different from the question ID.
        title: Text of the question.
        question_item: Optional question item for chosen question styles. If None, the item is not the question.
    """

    item_id: str
    title: str
    question_item: QuestionItem | None = None

    @model_validator(mode="after")
    def _log_unsupported_question(self) -> "Item":
        if self.question_item is None:
            logger.warning("'Grid' type questions are not supported. Skipped question: %s", self.title)
        return self


class Info(BaseModelCamelConfig):
    """Information class with survey description.

    Attributes:
        title: The title of the form which is visible to responders.
        description: The title of the document which is visible in Google Drive.
        document_title: The description of the form.
    """

    title: str
    description: str
    document_title: str


class Form(BaseModelCamelConfig):
    """Google Form class, docs: https://developers.google.com/forms/api/reference/rest/v1/forms#Form.

    Attributes:
        form_id: The form ID.
        info: Information object with survey description.
        responder_uri: The form URI to share with responders.
        items: A list of the form's items - in this case question.
    """

    form_id: str
    info: Info
    responder_uri: str
    items: list[Item]
