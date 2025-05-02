from django.urls import path

from .views import (
    AnswerCreateView,
    AnswerRemoveView,
    AnswerUpdateView,
    QuestionCreateView,
    QuestionRemoveView,
)

app_name = "qa"


urlpatterns = [
    path("question/<slug:slug>/add/", QuestionCreateView.as_view(), name="add_question"),
    path("question/<slug:slug>/remove/", QuestionRemoveView.as_view(), name="remove_question"),
    path("answer/<slug:slug>/<int:pk>/add/", AnswerCreateView.as_view(), name="add_answer"),
    path("answer/<slug:slug>/<int:pk>/remove/", AnswerRemoveView.as_view(), name="remove_answer"),
    path("answer/<slug:slug>/<int:pk>/edit/", AnswerUpdateView.as_view(), name="edit_answer"),
]
