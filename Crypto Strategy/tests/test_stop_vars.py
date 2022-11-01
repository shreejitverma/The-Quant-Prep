import pytest
import numpy as np
import pandas as pd
import vectorbt as vbt
from finlab_crypto.utility import (
    stop_early,
    enumerate_variables,
    migrate_stop_vars
)


@pytest.fixture
def price():
    price = pd.DataFrame({
        'open': [10, 11, 12, 11, 10, 9],
        'high': [11, 12, 13, 12, 11, 10],
        'low': [9, 10, 11, 10, 10, 8],
        'close': [10, 11, 12, 11, 10, 9]
    })
    return price


@pytest.fixture
def entries():
    return pd.DataFrame([True] + [False]*5)


@pytest.fixture
def exits():
    return pd.DataFrame([False] * 6)


@pytest.fixture
def tp_stop():
    return {'tp_stop': 0.3}


@pytest.fixture
def ts_stop():
    return {'ts_stop': 0.1}


@pytest.fixture
def sl_stop():
    return {'sl_stop': 0.1}


@pytest.fixture
def combined_stops():
    return {'sl_stop': 0.1, 'tp_stop': 0.1}


@pytest.fixture
def transform_stop_vars(ts_stop):
    stop_vars = enumerate_variables(ts_stop)
    stop_vars = {key: [stop_vars[i][key] for i in range(len(stop_vars))] for key in stop_vars[0].keys()}
    stop_vars = migrate_stop_vars(stop_vars)
    return stop_vars


def test_transform_stop_vars(transform_stop_vars):
    assert transform_stop_vars == {'sl_stop': [0.1], 'sl_trail': [True], 'ts_stop': [0.1]}


def test_ohlcstx(entries, price, transform_stop_vars):
    ohlcstx = vbt.OHLCSTX.run(
        entries,
        price['open'],
        price['high'],
        price['low'],
        price['close'],
        **transform_stop_vars,
    )
    np.testing.assert_array_equal(
        ohlcstx.exits.squeeze(),
        [False, False, False, True, False, False]
        )
    np.testing.assert_allclose(
        ohlcstx.stop_price.squeeze(),
        [np.nan, np.nan, np.nan, 11.7, np.nan, np.nan],
        rtol=1e-10, atol=0
        )
    np.testing.assert_array_equal(
        ohlcstx.stop_type_readable.squeeze(),
        [None, None, None, 'TrailStop', None, None]
        )


def test_tp_stop(price, entries, exits, tp_stop):
    entries_after, exits_after = stop_early(price, entries, exits, tp_stop)
    assert (entries.values == entries_after.values).all()
    assert (exits_after.values.squeeze() == [False, False, True, False, False, False]).all()


def test_ts_stop(price, entries, exits, ts_stop):
    entries_after, exits_after = stop_early(price, entries, exits, ts_stop)
    assert (entries.values == entries_after.values).all()
    assert (exits_after.values.squeeze() == [False, False, False, True, False, False]).all()


def test_sl_stop(price, entries, exits, sl_stop):
    entries_after, exits_after = stop_early(price, entries, exits, sl_stop)
    assert (entries.values == entries_after.values).all()
    assert (exits_after.values.squeeze() == [False, False, False, False, False, True]).all()


# TODO: investigate this
def test_combined_stops(price, entries, exits, combined_stops):
    entries_after, exits_after = stop_early(price, entries, exits, combined_stops)
    assert (entries.values == entries_after.values).all()
    assert (exits_after.values.squeeze() == [False, True, False, False, False, False]).all()
