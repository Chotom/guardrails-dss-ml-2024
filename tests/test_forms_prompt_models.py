from src.google_forms.forms_prompt_models import TextQuestionPrompt
from src.google_forms.forms_question_models import TextQuestion


class TestFormsQuestionModels:
    def test_forms_question_models(self):
        text_question_prompt = TextQuestionPrompt(
            question_id="1",
            question_text="What is the highest mountain?",
            question_form=TextQuestion(paragraph=True),
        )

        assert text_question_prompt.question_id == "1"
