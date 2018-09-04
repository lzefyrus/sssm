# -*- coding: utf-8 -*-

"""Validators module"""

from PyInquirer import (ValidationError, Validator)


class CurrencyValidator(Validator):
    """
    Simple currency validation
    """

    def validate(self, document):
        try:
            float(document.text)
            if float(document.text) <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError(
                message='Please enter the value in pennies',
                cursor_position=len(document.text))


class IntegerValidator(Validator):
    """
    Simple integer validation
    """

    def validate(self, document):
        try:
            int(document.text)
            if int(document.text) <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError(
                message='Please enter amount',
                cursor_position=len(document.text))
