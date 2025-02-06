import pytest
from src.factories.agent_factory import AgentFactory
from src.agents.agent_random import AgentRandom
from src.agents.agent_trend_follower import AgentTrendFollower
from src.agents.agent_contrarian import AgentContrarian
from src.agents.agent_custom import AgentCustom

@pytest.fixture
def setup_params():
    return {
        "available_capital": 1000.0,
        "owned_gpus": 10,
        "total_agents": 5,
        "distribution": {"random": 2, "trend_follower": 1, "contrarian": 1, "custom": 1},
        "total_iterations": 100
    }

def test_create_random_agent(setup_params):
    params = setup_params
    agent = AgentFactory.create_agent("random", params["available_capital"], params["owned_gpus"], params["total_agents"], params["distribution"])
    assert isinstance(agent, AgentRandom)

def test_create_trend_follower_agent(setup_params):
    params = setup_params
    agent = AgentFactory.create_agent("trend_follower", params["available_capital"], params["owned_gpus"], params["total_agents"], params["distribution"])
    assert isinstance(agent, AgentTrendFollower)

def test_create_contrarian_agent(setup_params):
    params = setup_params
    agent = AgentFactory.create_agent("contrarian", params["available_capital"], params["owned_gpus"], params["total_agents"], params["distribution"])
    assert isinstance(agent, AgentContrarian)

def test_create_custom_agent(setup_params):
    params = setup_params
    agent = AgentFactory.create_agent("custom", params["available_capital"], params["owned_gpus"], params["total_agents"], params["distribution"], params["total_iterations"])
    assert isinstance(agent, AgentCustom)

def test_create_custom_agent_without_iterations(setup_params):
    params = setup_params
    with pytest.raises(ValueError):
        AgentFactory.create_agent("custom", params["available_capital"], params["owned_gpus"], params["total_agents"], params["distribution"])

def test_create_unknown_agent(setup_params):
    params = setup_params
    with pytest.raises(ValueError):
        AgentFactory.create_agent("unknown", params["available_capital"], params["owned_gpus"], params["total_agents"], params["distribution"])
