from apps.qa.models import Answer, Question
from django import forms


class QuestionForm(forms.Form):
    """Форма для вопросов пользователей."""

    class Meta:
        model = Question
        fields = ("text",)
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваш вопрос"}),
        }


class AnswerForm(forms.Form):
    """Форма для ответов админа на вопросы."""

    class Meta:
        model = Answer
        fields = ("text",)
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваш ответ"}),
        }
