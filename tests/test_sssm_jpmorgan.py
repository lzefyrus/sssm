#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sssm_jpmorgan` functions."""

import time

import pytest

from sssm_jpmorgan.sssm_jpmorgan import setup
from sssm_jpmorgan.utils import *

MOCK = {
    'trade': [{'stock': 'TEA', 'action': 'buy', 'quantity': 1, 'price': 1.0},
              {'stock': 'POP', 'action': 'sell', 'quantity': 1, 'price': 1.0},
              {'stock': 'GIN', 'action': 'sell', 'quantity': 1, 'price': 65.0},
              ],
    'dividendpe': [{'stock': 'TEA', 'price': 10}, {'stock': 'GIN', 'price': 10}, {'stock': 'POP', 'price': 10}],
    'roa': pd.DataFrame(),
    'ra': pd.DataFrame()
}


def test_import():
    global MOCK
    ra = setup()
    assert (ra.empty == False)
    assert (list(ra.columns.get_values()) == ['Stock Symbol', 'Type', 'Last Dividend', 'Fixed Dividend', 'Par Value'])
    assert (MOCK['roa'].empty == True)
    MOCK['ra'] = ra


@pytest.fixture
def ra():
    return setup()


@pytest.fixture
def roa():
    roa = pd.DataFrame()
    old_date = datetime.datetime.now() - datetime.timedelta(minutes=60)
    roa = record_trade(MOCK['trade'][0], roa)
    time.sleep(1)
    roa = record_trade(MOCK['trade'][1], roa)
    roa = record_trade(MOCK['trade'][2], roa, old_date)
    return roa


def test_dividend_yield(ra):
    zero = dividend_yield(MOCK['dividendpe'][0], ra)
    assert (zero == 0.0)
    prefered = dividend_yield(MOCK['dividendpe'][1], ra)
    assert (prefered == 0.2)

    common = dividend_yield(MOCK['dividendpe'][2], ra)
    assert (common == 0.8)


def test_pe(ra):
    zero = pe_ratio(MOCK['dividendpe'][0], ra)
    assert (zero == 0.0)
    prefered = pe_ratio(MOCK['dividendpe'][1], ra)
    assert (prefered == 0.02)

    common = pe_ratio(MOCK['dividendpe'][2], ra)
    assert (common == 0.08)


def test_record_trade():
    roa = MOCK['roa']
    assert (roa.empty == True)

    roa = record_trade(MOCK['trade'][0], roa)
    assert (roa.empty == False)
    assert (roa['tpq'].any() == 1)

    roa = record_trade(MOCK['trade'][1], roa)
    assert (len(roa) == 2)


def test_volume_weighted_stock_price(roa):
    assert (roa.empty == False)
    assert (len(roa) == 3)

    series_15 = by_time_series(roa, 15)
    assert (len(series_15) == 2)

    series_200 = by_time_series(roa, 200)
    assert (len(series_200) == 3)

    vwsp_15 = volume_weighted_stock_price(series_15)
    assert (vwsp_15 == 1.0)

    vwsp_200 = volume_weighted_stock_price(series_200)
    assert (vwsp_200 == 22.333333333333332)


def test_gbce(roa):
    series_15 = by_time_series(roa, 15)
    assert (len(series_15) == 2)

    gbce_15 = gbce(series_15)
    assert (gbce_15 == 1)

    series_200 = by_time_series(roa, 200)
    assert (len(series_200) == 3)

    gbce_200 = gbce(series_200)
    assert (round(gbce_200, 6) == round((65 ** (1. / 3.)), 6))
