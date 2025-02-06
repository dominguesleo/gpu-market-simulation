import pytest
from src.agents.agent_base_model import AgentBaseModel

def test_init_valid_parameters():
    agent = AgentBaseModel(available_capital=1000.0, owned_gpus=5, total_agents=10, distribution={"random": 5, "trend_follower": 5})
    assert agent.available_capital == 1000.0
    assert agent.owned_gpus == 5
    assert agent.total_agents == 10
    assert agent.distribution == {"random": 5, "trend_follower": 5}
    assert agent.strategy is None

def test_init_negative_available_capital():
    with pytest.raises(ValueError) as context:
        AgentBaseModel(available_capital=-1000.0, owned_gpus=5, total_agents=10, distribution={"random": 5, "trend_follower": 5})
    assert str(context.value) == "Available capital cannot be negative."

def test_init_negative_owned_gpus():
    with pytest.raises(ValueError) as context:
        AgentBaseModel(available_capital=1000.0, owned_gpus=-5, total_agents=10, distribution={"random": 5, "trend_follower": 5})
    assert str(context.value) == "Number of owned GPUs cannot be negative."
