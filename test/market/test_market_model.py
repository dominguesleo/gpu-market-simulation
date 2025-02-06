import pytest
from src.market.market_model import Market

@pytest.fixture
def setup_market():
    agents = []
    market = Market(initial_price=100.0, iterations=10, stock=1000, agents=agents)
    return market

def test_market_initialization(setup_market):
    """Test that Market initializes correctly with valid values."""
    market = setup_market
    assert market.price == 100.0
    assert market.iterations == 10
    assert market.stock == 1000
    assert market.agents == []

def test_market_negative_initial_price():
    """Should raise ValueError if the initial price is negative."""
    with pytest.raises(ValueError, match="Initial price cannot be negative."):
        Market(initial_price=-10.0, iterations=10, stock=1000, agents=[])

def test_price_setter(setup_market):
    """Test that the price setter raises a ValueError with negative values."""
    market = setup_market
    with pytest.raises(ValueError, match="Price cannot be negative."):
        market.price = -5

def test_update_price_and_stock_buy(setup_market):
    """The price should increase by 0.5% and stock should decrease by 1 if an agent successfully buys."""
    market = setup_market
    market._update_price_and_stock({"action": "buy", "success": True})
    assert market.price == pytest.approx(100.5, rel=1e-9)  # 100.0 * 1.005
    assert market.stock == 999

def test_update_price_and_stock_sell(setup_market):
    """The price should decrease by 0.5% and stock should increase by 1 if an agent successfully sells."""
    market = setup_market
    market._update_price_and_stock({"action": "sell", "success": True})
    assert market.price == pytest.approx(99.5, rel=1e-9)  # 100.0 * 0.995
    assert market.stock == 1001

def test_update_price_and_stock_no_change(setup_market):
    """The price and stock should not change if the action is 'do_nothing' or was not successful."""
    market = setup_market
    market._update_price_and_stock({"action": "do_nothing", "success": True})
    assert market.price == 100.0
    assert market.stock == 1000

    market._update_price_and_stock({"action": "buy", "success": False})
    assert market.price == 100.0
    assert market.stock == 1000