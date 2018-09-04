#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""Main module."""

import os
import sys

import colorama
import pandas as pd
from PyInquirer import prompt

try:
    from contents import *
except ImportError:
    from .contents import *
try:
    from utils import *
except ImportError:
    from .utils import *

colorama.init()

# setup globals
ra = None
roa = pd.DataFrame()


def setup():
    """
    Reads the initial data and creates the record object
    updates the questions data from the CSV sample for consistency
    :return: mixed
    """
    try:
        global ra
        ra = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/sample.csv', sep='|', encoding='latin-1',
                         converters={'Fixed Dividend': lambda x: int(x) / 100 if x != '' else 0})

        STOCK_QUESTION['choices'] = [stock for stock in ra.loc[:, 'Stock Symbol']]
        STOCK_QUESTIONS.insert(0, STOCK_QUESTION.copy())
        TRADE_QUESTIONS.insert(0, STOCK_QUESTION.copy())

        return ra
    except Exception as e:
        raise


def main():
    """
    Main caller for data entry
    :return:
    """
    global ra, roa
    answers = {}
    main_action = prompt(INITIAL_QUESTION, style=COLORS)
    maction = main_action.get('action', '')

    if maction == 'exit':
        cprint('bye, bye!', 'red')
        sys.exit()

    elif maction == 'calculate':
        answers = prompt(STOCK_QUESTIONS, style=COLORS)
        cprint(dividend_yield(answers, ra), 'green', 'percentage', 'Dividend yield: ')

    elif maction in 'pe':
        answers = prompt(STOCK_QUESTIONS, style=COLORS)
        cprint(pe_ratio(answers, ra), 'green', 'decimal', 'P/E ratio: ')

    elif maction == 'record':
        answers = prompt(TRADE_QUESTIONS, style=COLORS)
        roa = record_trade(answers, roa)
        cprint(roa, 'yellow', 'trade')

    elif maction == 'volume':
        series = by_time_series(roa, 15)
        if series.empty:
            cprint('Series empty. Please add trades.', 'red')
        else:
            cprint(volume_weighted_stock_price(series), 'yellow', 'bigdecimal', 'Volume Weighted Stock Price: ')

    elif maction == 'gbce':
        series = by_time_series(roa)
        if series.empty:
            cprint('Series empty. Please add trades.', 'red')
        else:
            cprint(gbce(roa), 'yellow', 'bigdecimal', 'GBCE: ')

    else:
        print('none', COLORS)

    main()


if __name__ == "__main__":
    ra = setup()
    main()
