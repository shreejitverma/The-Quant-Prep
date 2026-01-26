import pytest
import pandas as pd
import numpy as np
from crypto_strategy.strategies.bo_strategy import InspectBoStrategy


@pytest.fixture
def xrp_positions_prior():
    return pd.read_pickle('./tests/positions_XRPUSDT-4h-bo-100-15-ts_stop-0.10-vol-10-2-20211230.pkl')


@pytest.fixture
def btc_positions_prior():
    return pd.read_pickle('./tests/positions_BTCUSDT-4h-bo-165-50-ts_stop-0.15-vol-30-1-20211207.pkl')


def test_regression_xrp(xrp_positions_prior):
    stats = InspectBoStrategy(
        'XRPUSDT', '4h',
        long_window=100, short_window=15,
        stop_vars={'ts_stop': 0.1},
        flag_filter='vol', timeperiod=10, multiplier=2, show_fig=False)
    positions = stats.portfolio.positions.records_readable
    positions = positions[positions["Entry Timestamp"] < "2021-12-30"]
    np.testing.assert_allclose(positions["Size"].values, xrp_positions_prior["Size"].values)
    np.testing.assert_equal(positions['Entry Timestamp'].values, xrp_positions_prior['Entry Date'].values)


def test_regression_btc(btc_positions_prior):
    stats = InspectBoStrategy(
        'BTCUSDT', '4h',
        long_window=165, short_window=50,
        stop_vars={'ts_stop': 0.15},
        flag_filter='vol', timeperiod=30, multiplier=1, show_fig=False)
    positions = stats.portfolio.positions.records_readable
    positions = positions[positions["Entry Timestamp"] < "2021-12-30"]
    np.testing.assert_allclose(positions["Size"].values, btc_positions_prior["Size"].values)
    np.testing.assert_equal(positions['Entry Timestamp'].values, btc_positions_prior['Entry Date'].values)