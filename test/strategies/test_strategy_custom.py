import pytest
from unittest.mock import MagicMock
from src.strategies.strategy_custom import CustomStrategy
from src.agents.agent_base_model import AgentBaseModel

@pytest.fixture
def setup_agent():
    total_iterations = 100
    strategy = CustomStrategy(total_iterations=total_iterations)
    agent = AgentBaseModel(
        available_capital=1000.0,
        owned_gpus=5,
        total_agents=10,
        distribution={"random": 5, "trend_follower": 5}
    )
    agent.owned_gpus = 0
    agent.available_capital = 1000
    agent._buy = MagicMock(return_value=True)
    agent._sell = MagicMock(return_value=True)
    return strategy, agent

def test_buy_action(setup_agent):
    strategy, agent = setup_agent
    strategy.price_history = [100] * 10
    gpu_price = 80  # 20% lower than average price
    result = strategy.decide(agent, gpu_price, turn=1)
    assert result["action"] == "buy"
    assert result["success"]
    agent._buy.assert_called_once_with(gpu_price)

def test_sell_action(setup_agent):
    strategy, agent = setup_agent
    strategy.price_history = [100] * 10
    agent.owned_gpus = 1
    gpu_price = 110  # 10% higher than average price
    result = strategy.decide(agent, gpu_price, turn=1)
    assert result["action"] == "sell"
    assert result["success"]
    agent._sell.assert_called_once_with(gpu_price)

def test_sell_all_remaining_gpus(setup_agent):
    strategy, agent = setup_agent
    strategy.price_history = [100] * 10
    agent.owned_gpus = 5
    gpu_price = 100
    strategy.iteration_count = 95  # Few iterations left
    result = strategy.decide(agent, gpu_price, turn=96)
    assert result["action"] == "sell"
    assert result["success"]
    agent._sell.assert_called_once_with(gpu_price)
