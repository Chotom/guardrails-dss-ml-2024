import json

import pytest

from src.google_forms.form_model import Form


@pytest.fixture()
def googleapis_forms_get_response() -> dict:
    with open("tests/tests_data/test_forms_question_models/googleapis_forms_get_response.json") as json_file:
        json_data = json.load(json_file)

    return json_data


class TestFormsQuestionModels:
    def test_forms_question_models(self, googleapis_forms_get_response: dict):
        form = Form(**googleapis_forms_get_response)

        assert form.info.title == "Title of form"
        assert len(form.items) == 10
