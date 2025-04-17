import re
from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits,
    punctuation,
)

from django import forms


MIN_LENGTH = 8
SPECIAL_SYMBOLS_PATTERN = re.compile(f"[{re.escape(punctuation)}]")
UPPERCASE_LETTERS_PATTERN = re.compile(f"[{ascii_uppercase}]")
LOWERCASE_LETTERS_PATTERN = re.compile(f"[{ascii_lowercase}]")
DIGITS_PATTERN = re.compile(f"[{digits}]")


class PasswordValidator:
    """Класс валидации пароля."""

    def __call__(self, value) -> None:
        self.validate(value)

    def validate(self, value, user=None) -> str:
        if not value or not value.strip():
            raise forms.ValidationError("Поле не может быть пустым.")

        if len(value) < MIN_LENGTH:
            raise forms.ValidationError(f"Пароль слишком короткий. Пароль должен быть минимум {MIN_LENGTH} символов")

        if not SPECIAL_SYMBOLS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы один специальный символ.")

        if not UPPERCASE_LETTERS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

        if not LOWERCASE_LETTERS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну строчную букву.")

        if not DIGITS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")

        if user.username == value or user.email == value:
            raise forms.ValidationError("Пароль не должен совпадать с username и(или) e-mail.")

        return value
