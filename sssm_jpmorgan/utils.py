# -*- coding: utf-8 -*-

"""functions module"""

import datetime

import pandas as pd
from money import Money
from scipy.stats.mstats import gmean
from termcolor import colored


def dividend_yield(answers, ra):
    """
    Calculates the dividend yield for the stock

    :param answers: dict answers
    :param ra: DataFrame data
    :return: string question
    """
    try:
        row = ra.loc[ra['Stock Symbol'] == answers.get('stock')]
        if row['Type'].item() == 'Common':
            return row['Last Dividend'].item() / answers.get('price')
        return row['Fixed Dividend'].item() * row['Par Value'].item() / answers.get('price')

    except ZeroDivisionError:
        return 0.0
    except Exception as e:
        print(e)


def pe_ratio(answers, ra):
    """
    Calculates the P/E ratio

    :param answers: dict answers
    :param ra: DataFrame data
    :return: string question
    """
    try:
        row = ra.loc[ra['Stock Symbol'] == answers.get('stock')]
        dividend = dividend_yield(answers, ra)
        assert dividend > 0
        return dividend / answers.get('price')

    except AssertionError or ZeroDivisionError:
        return 0.0

    except Exception as e:
        return 0.0


def record_trade(answers, roa, custom_date=None):
    """
    Adds a record of a trade, the traded price and quantity are constants after the input,
    so it's pre calculated for performance sake in VWSP

    :param answers: dict answers
    :param roa: DataFrame data
    :param custom_date: datetime
    :return: DataFrame
    """
    if custom_date and type(custom_date) == datetime.datetime:
        answers['timestamp'] = custom_date
    else:
        answers['timestamp'] = datetime.datetime.now()
    answers['tpq'] = answers['quantity'] * answers['price']
    answers = pd.DataFrame([answers])
    answers.set_index('timestamp', inplace=True)
    if roa.empty:
        return answers
    roa = roa.append(answers)
    return roa


def volume_weighted_stock_price(series):
    """
    Returns the volume weighted stock price for the given time in minutes

    :param series: Series series to be calculated
    :return: float
    """
    return series['tpq'].sum() / series['quantity'].sum()


def gbce(series):
    """
    Returns the geometric mean of all shares
    if time is given calculates from the X minutes

    :param series: Series series to be calculated
    :return: float
    """
    return gmean(series.loc[:, "price"])


def by_time_series(roa, time=0):
    """
    helper method to return timed series of data, all data or empty dataset

    :param roa: DataFrame data
    :param time: int time in minutes
    :return: DataFrame
    """
    if time:
        now = datetime.datetime.now()
        d = now - datetime.timedelta(minutes=time)
        return roa.sort_index().truncate(before=d)
    series = roa

    return series


def cprint(text, color='gray', format=None, pre=''):
    """
    simple color printing to console
    :param text: any
    :param color: string
    :param format: string
    :param pre: string to be added before the formatting
    :return: bool
    """
    if format == 'currency':
        print(colored(pre + str(Money(amount=text, currency='GBP')), color))
    elif format == 'percentage':
        print(colored(pre + "{0:.0f}%".format(text * 100), color))
    elif format == 'decimal':
        print(colored(pre + "{0:.2f}".format(text), color))
    elif format == 'bigdecimal':
        print(colored(pre + "{0:.5f}".format(text), color))
    elif format == 'trade':
        print(colored('Trades\n', 'green'))
        for index, row in text.iterrows():
            print(colored(
                '  stock:{} | action:{} | qtd:{} | price:{} | date: {}'.format(row['stock'],
                                                                               row['action'],
                                                                               row['quantity'],
                                                                               str(Money(amount=row['price'],
                                                                                         currency='GBP')),
                                                                               str(index).split('.')[0]), color))
        print(colored('\nTotal trades: {}'.format(len(text)), 'green'))
    else:
        print(colored(text, color))
