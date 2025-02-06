from abc import ABC, abstractmethod
from typing import Dict

from src.agents.agent_base_model import AgentBaseModel

class StrategyBaseModel(ABC):
    @abstractmethod
    def decide(self, agent:AgentBaseModel, gpu_price: float, turn: int) -> Dict[str, bool]:
        """
        Decides the action to take based on the strategy.

        Parameters:
            agent (AgentBaseModel): The agent making the decision.
            gpu_price (float): The current price of the GPU.
            turn (int): The current turn or step in the decision-making process.

        Returns:
            Dict[str, bool]: A dictionary with the action taken and whether it was successful.
                            The dictionary has the following structure:
                            {
                                "action": str,  # The action taken: "buy", "sell", or "do_nothing".
                                "success": bool  # Whether the action was successful.
                            }

        Raises:
            NotImplementedError: If the method is called without being overridden in a subclass.
        """
        raise NotImplementedError("The decide method is not implemented.")