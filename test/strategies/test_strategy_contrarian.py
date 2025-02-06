import pytest
from unittest.mock import MagicMock
from src.strategies.strategy_contrarian import ContrarianStrategy
from src.agents.agent_base_model import AgentBaseModel

@pytest.fixture
def setup_agent():
    strategy = ContrarianStrategy()
    agent = AgentBaseModel(
        available_capital=1000.0,
        owned_gpus=5,
        total_agents=10,
        distribution={"random": 5, "contrarian": 5}
    )
    agent._buy = MagicMock(return_value=True)
    agent._sell = MagicMock(return_value=True)
    return strategy, agent

def test_decide_buy(setup_agent):
    strategy, agent = setup_agent
    agent.previous_price = 100.0
    gpu_price = 99.0  # Price decreased by 1%
    result = strategy.decide(agent, gpu_price, 1)
    assert result["action"] in ["buy", "do_nothing"]
    if result["action"] == "buy":
        assert result["success"]
        agent._buy.assert_called_once_with(gpu_price)

def test_decide_sell(setup_agent):
    strategy, agent = setup_agent
    agent.previous_price = 100.0
    gpu_price = 101.0  # Price increased by 1%
    result = strategy.decide(agent, gpu_price, 1)
    assert result["action"] in ["sell", "do_nothing"]
    if result["action"] == "sell":
        assert result["success"]
        agent._sell.assert_called_once_with(gpu_price)

def test_decide_first_turn(setup_agent):
    strategy, agent = setup_agent
    agent.previous_price = None
    gpu_price = 100.0
    result = strategy.decide(agent, gpu_price, 1)
    assert result["action"] in ["buy", "do_nothing"]
    if result["action"] == "buy":
        assert result["success"]
        agent._buy.assert_called_once_with(gpu_price)
