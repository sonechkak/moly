import re
from abc import ABC, abstractmethod
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


class PasswordValidatorBase(ABC):
    """Базовый класс для валидаторов пароля."""

    def __init__(self, successor=None):
        self._successor = successor

    @abstractmethod
    def validate(self, value, user=None):
        pass

    def _validate_next(self, value, user=None):
        if self._successor:
            return self._successor.validate(value, user)
        return value


class NotEmptyValidator(PasswordValidatorBase):
    """Проверка, что пароль не пустой."""

    def validate(self, value, user=None):
        if not value or not value.strip():
            raise forms.ValidationError("Поле не может быть пустым.")
        return self._validate_next(value, user)


class MinLengthValidator(PasswordValidatorBase):
    """Проверка минимальной длины пароля."""

    def validate(self, value, user=None):
        if len(value) < MIN_LENGTH:
            raise forms.ValidationError(f"Пароль слишком короткий. Пароль должен быть минимум {MIN_LENGTH} символов.")
        return self._validate_next(value, user)


class SpecialSymbolsValidator(PasswordValidatorBase):
    """Проверка наличия специальных символов."""

    def validate(self, value, user=None):
        if not SPECIAL_SYMBOLS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы один специальный символ.")
        return self._validate_next(value, user)


class UppercaseLettersValidator(PasswordValidatorBase):
    """Проверка наличия заглавных букв."""

    def validate(self, value, user=None):
        if not UPPERCASE_LETTERS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        return self._validate_next(value, user)


class LowercaseLettersValidator(PasswordValidatorBase):
    """Проверка наличия строчных букв."""

    def validate(self, value, user=None):
        if not LOWERCASE_LETTERS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        return self._validate_next(value, user)


class DigitsValidator(PasswordValidatorBase):
    """Проверка наличия цифр."""

    def validate(self, value, user=None):
        if not DIGITS_PATTERN.search(value):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        return self._validate_next(value, user)


class UserCredentialsValidator(PasswordValidatorBase):
    """Проверка, что пароль не совпадает с username или email."""

    def validate(self, value, user=None):
        if user and (user.username == value or user.email == value):
            raise forms.ValidationError("Пароль не должен совпадать с username и(или) e-mail.")
        return self._validate_next(value, user)


class PasswordValidator:
    """Основной класс валидации пароля, объединяющий все проверки."""

    def __init__(self):
        self.validator_chain = NotEmptyValidator(
            MinLengthValidator(
                SpecialSymbolsValidator(
                    UppercaseLettersValidator(LowercaseLettersValidator(DigitsValidator(UserCredentialsValidator())))
                )
            )
        )

    def __call__(self, value) -> None:
        self.validate(value)

    def validate(self, value, user=None) -> str:
        return self.validator_chain.validate(value, user)
