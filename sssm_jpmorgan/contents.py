# -*- coding: utf-8 -*-

"""Constants module"""

from PyInquirer import (Token, style_from_dict, )

try:
    from validators import *
except ImportError:
    from .validators import *

COLORS = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Pointer: '#673ab7 bold',
    Token.Question: '#919191',
})

INITIAL_QUESTION = {
    'type': 'list',
    'name': 'action',
    'message': 'What action do you want to do?',
    'choices': [
        {
            'name': 'Calculate the dividend yield',
            'value': 'calculate'
        },
        {
            'name': 'Calculate the P/E ratio',
            'value': 'pe'
        },
        {
            'name': 'Record a trade',
            'value': 'record'
        },
        {
            'name': 'Calculate Volume Weighted Stock Price',
            'value': 'volume'
        },
        {
            'name': 'Calculate the GBCE All Share Index',
            'value': 'gbce'
        },
        {
            'name': 'Exit',
            'value': 'exit'
        },
    ]
}

STOCK_QUESTION = {
    'type': 'list',
    'name': 'stock',
    'message': 'Please select a Stock',
    'choices': [],
}

STOCK_QUESTIONS = [
    {
        'type': 'input',
        'name': 'price',
        'message': 'Price',
        'filter': lambda val: float(val),
        'validate': CurrencyValidator
    },
]

TRADE_QUESTIONS = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'Buy or sell?',
        'choices': ['Buy', 'Sell'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'quantity',
        'message': 'How many shares',
        'validate': IntegerValidator,
        'filter': lambda val: int(val)
    },
    {
        'type': 'input',
        'name': 'price',
        'message': 'Traded price',
        'filter': lambda val: float(val),
        'validate': CurrencyValidator
    }

]
