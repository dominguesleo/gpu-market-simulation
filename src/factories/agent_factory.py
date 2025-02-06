from typing import Dict

from src.agents.agent_base_model import AgentBaseModel
from src.agents.agent_random import AgentRandom
from src.agents.agent_trend_follower import AgentTrendFollower
from src.agents.agent_contrarian import AgentContrarian
from src.agents.agent_custom import AgentCustom

class AgentFactory:
    """
    Factory class for creating different types of agents.

    This class provides a static method to instantiate various agent types based on a given identifier.

    Methods:
        create_agent(agent_type: str, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int], total_iterations: int = None) -> AgentBaseModel:
            Creates and returns an agent of the specified type.

    Raises:
        ValueError: If the provided `agent_type` is unknown.
    """

    @staticmethod
    def create_agent(agent_type: str, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int], total_iterations: int = None) -> AgentBaseModel:
        """
        Creates an agent instance based on the specified type.

        Args:
            agent_type (str): The type of agent to create. Options: "random", "trend_follower", "contrarian", "custom".
            available_capital (float): The initial capital available to the agent.
            owned_gpus (int): The number of GPUs owned by the agent.
            total_agents (int): The total number of agents in the market.
            distribution (Dict[str, int]): A mapping representing the distribution of policies among agents.
            total_iterations (int, optional): The total number of iterations in the simulation (only required for "custom" agents).

        Returns:
            AgentBaseModel: An instance of the requested agent type.

        Raises:
            ValueError: If an unknown `agent_type` is provided.
        """
        if agent_type == "random":
            return AgentRandom(available_capital, owned_gpus, total_agents, distribution)
        elif agent_type == "trend_follower":
            return AgentTrendFollower(available_capital, owned_gpus, total_agents, distribution)
        elif agent_type == "contrarian":
            return AgentContrarian(available_capital, owned_gpus, total_agents, distribution)
        elif agent_type == "custom":
            if total_iterations is None:
                raise ValueError("total_iterations is required for custom agents.")
            return AgentCustom(available_capital, owned_gpus, total_agents, distribution, total_iterations)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")