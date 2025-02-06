# GPU Market Simulation

This project simulates a market where agents buy, sell, or do nothing with GPUs based on different strategies.

## Requirements

- Market with a limited stock of 100,000 GPUs.
- 100 economic agents that buy and sell GPUs.
- Each iteration, agents can buy, sell, or do nothing.
- The price of GPUs increases by 0.5% with each purchase and decreases by 0.5% with each sale.
- Distribution of agents:
  - 51 random agents.
  - 24 trend-following agents.
  - 24 contrarian agents.
  - 1 custom agent to maximize its economic balance.

## Initial Conditions

- Each agent starts with $1,000.
- They cannot borrow money or sell more GPUs than they own.
- The initial price of GPUs is $200.00.
- 1,000 iterations are simulated.

## Project Structure

    .
    ├── __main__.py
    ├── README.md
    ├── src/
    │   ├── agents/
    │   │   ├── agent_base_model.py
    │   │   ├── agent_contrarian.py
    │   │   ├── agent_custom.py
    │   │   ├── agent_random.py
    │   │   └── agent_trend_follower.py
    │   ├── factories/
    │   │   └── agent_factory.py
    │   ├── market/
    │   │   └── market_model.py
    │   ├── strategies/
    │   │   ├── strategy_base_model.py
    │   │   ├── strategy_contrarian.py
    │   │   ├── strategy_custom.py
    │   │   ├── strategy_random.py
    │   │   └── strategy_trend_follower.py
    │   └── logger_config.py
    └──  test/
        ├── agents/
        ├── factories/
        ├── market/
        └── strategies/

The project is divided into 4 main directories:

- **Agents**: Defines the logic of the agents and their implementations based on their strategies.
- **Factories**: Implements the Factory design pattern to simplify the creation of agents.
- **Strategies**: Implements the Strategy design pattern to define the different strategies of the agents.
- **Market**: Contains the Market model to handle the simulation and interaction of agents within the established parameters.

## Installation

No dependencies are required to run the simulation. To execute the simulation, simply run the `__main__.py` file:

```sh
python __main__.py
```

A detailed log of the simulation will be generated in the market_simulation.txt file located in the root directory.

To run the tests, you need to install the testing dependencies. You can do this by running:

```sh
pip install pytest==8.3.4
```

## Logic Used

For clarity, docstrings have been omitted in the code examples below, but they will be visible in the implementation of each one.

### Agent

Part of an abstract class to define the common attributes and methods of the different agents:

- The buy and sell logic is defined. It is checked whether the action can be performed, the `available_capital` and `owned_gpus` values are updated as appropriate. And `True` or `False` is returned depending on whether the buy or sell action is executed.
- A more detailed record is obtained that allows knowing if the purchase or sale was not executed due to lack of resources or if, on the contrary, the "do_nothing" action was executed.
- The `run` method is implemented, which will take the strategy implemented in the child classes and return a dictionary with the action taken by the agent and whether it was successful or not.
- The `_update_price_and_stock` method is implemented, which updates the price and stock of GPUs based on the agent's action.

```python
class AgentBaseModel(ABC):
    def __init__(self, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int]):
        if available_capital < 0:
            raise ValueError("Available capital cannot be negative.")
        if owned_gpus < 0:
            raise ValueError("Number of owned GPUs cannot be negative.")

        self._available_capital = available_capital
        self._owned_gpus = owned_gpus
        self.total_agents = total_agents
        self.distribution = distribution
        self.current_stock = None # Will be set in the run method
        self.strategy = None  # This will be set in the subclasses

    @property
    def available_capital(self) -> float:
        return self._available_capital

    @available_capital.setter
    def available_capital(self, value: float) -> None:
        if value < 0:
            raise ValueError("Available capital cannot be negative.")
        self._available_capital = value

    @property
    def owned_gpus(self) -> int:
        return self._owned_gpus

    @owned_gpus.setter
    def owned_gpus(self, value: int) -> None:
        if value < 0:
            raise ValueError("Number of owned GPUs cannot be negative.")
        self._owned_gpus = value

    def _buy(self, gpu_price: float) -> bool:
        if gpu_price <= 0:
            raise ValueError("GPU price must be positive.")
        if self._available_capital >= gpu_price and self.current_stock > 0:
            self._available_capital -= gpu_price
            self._owned_gpus += 1
            return True
        return False

    def _sell(self, gpu_price: float) -> bool:
        if gpu_price <= 0:
            raise ValueError("GPU price must be positive.")
        if self._owned_gpus > 0:
            self._available_capital += gpu_price
            self._owned_gpus -= 1
            return True
        return False

    def run(self, gpu_price: float, turn: int, current_stock:int) -> Dict[str, bool]:
        self.current_stock = current_stock
        if self.strategy is None:
            raise NotImplementedError("Strategy not set for the agent.")
        return self.strategy.decide(self, gpu_price, turn)
```

The child classes that implement `AgentBaseModel` define the strategy to be used and additional attributes such as `previous_price` for the proper functioning of trend-following and contrarian agents.

```python
class AgentTrendFollower(AgentBaseModel):
    def __init__(self, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int]):
        super().__init__(available_capital, owned_gpus, total_agents, distribution)
        self.previous_price = None
        self.strategy = TrendFollowerStrategy()
```

### Factories

Implements the Factory design pattern to simplify the creation of agents. The `AgentFactory` class provides a static method `create_agent` that takes as parameters the type of agent, available capital, number of GPUs owned, total agents, policy distribution, and total iterations (optional). Depending on the type of agent, an instance of the corresponding agent is created.

```python
class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int], total_iterations: int = None):
        if agent_type == "random":
            return AgentRandom(available_capital, owned_gpus, total_agents, distribution)
        elif agent_type == "trend_follower":
            return AgentTrendFollower(available_capital, owned_gpus, total_agents, distribution)
        elif agent_type == "contrarian":
            return AgentContrarian(available_capital, owned_gpus, total_agents, distribution)
        elif agent_type == "custom":
            return AgentCustom(available_capital, owned_gpus, total_agents, distribution, total_iterations)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
```

### Strategies

Implements the Strategy design pattern to define the different strategies of the agents. The `StrategyBaseModel` class is an abstract class that defines the `decide` method, which must be implemented by the child classes to decide the action to be taken (buy, sell, or do nothing) based on the specific strategy.

```python
class StrategyBaseModel(ABC):
    @abstractmethod
    def decide(self, agent:AgentBaseModel, gpu_price: float, turn: int) -> Dict[str, bool]:
        raise NotImplementedError("The decide method is not implemented.")
```

An implementation of this abstract class is `TrendFollowerStrategy`, which follows market trends. If the price has increased by 1% or more since the previous iteration, the agent has a 75% chance of buying and a 25% chance of doing nothing. Otherwise, the agent has a 20% chance of selling and an 80% chance of doing nothing.

```python
class TrendFollowerStrategy(StrategyBaseModel):
    def decide(self, agent:AgentBaseModel, gpu_price: float, turn: int) -> Dict[str, bool]:
        if hasattr(agent, "previous_price") and agent.previous_price is not None:
            price_change = (gpu_price - agent.previous_price) / agent.previous_price
        else:
            price_change = None

        if price_change is None or price_change >= 0.01:
            action = random.choices(["buy", "do_nothing"], [0.75, 0.25])[0]
        else:
            action = random.choices(["sell", "do_nothing"], [0.20, 0.80])[0]

        result = {"action": action, "success": True}

        if action == "buy":
            result["success"] = agent._buy(gpu_price)
        elif action == "sell":
            result["success"] = agent._sell(gpu_price)

        agent.previous_price = gpu_price
        return result
```

### Market

Contains the `Market` model to handle the simulation and interaction of agents within the established parameters. The `Market` class initializes the market with the initial price, number of iterations, and agents. It simulates the market for the specified number of iterations, updating the price of GPUs based on the actions of the agents and recording a summary of each iteration.

```python
class Market:
    def __init__(self, initial_price: float, iterations: int, stock:int, agents: List[AgentBaseModel], verbose: bool = False, log_to_file: bool = False):
        if initial_price < 0:
            raise ValueError("Initial price cannot be negative.")
        if iterations < 0:
            raise ValueError("Iterations must be non-negative.")
        if stock < 0:
            raise ValueError("Stock must be non-negative.")

        self._price = initial_price
        self._iterations = iterations
        self._stock = stock
        self.agents = agents
        self.history = []
        self.logger = configure_logger(verbose, log_to_file)

    @property
    def price(self) -> float:
        """Returns the current price of the GPU."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def iterations(self) -> int:
        return self._iterations

    @iterations.setter
    def iterations(self, value: int) -> None:
        if value < 0:
            raise ValueError("Iterations must be non-negative.")
        self._iterations = value

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        self._stock = value

    def _update_price_and_stock(self, result: Dict) -> None:
        if result["action"] == "buy" and result["success"]:
            self.price *= 1.005
            self.stock -= 1

        elif result["action"] == "sell" and result["success"]:
            self.price *= 0.995
            self.stock += 1

    def simulate(self) -> None:
        for iteration in range(self.iterations):
            random.shuffle(self.agents)
            agent_results = []
            for agent in self.agents:
                result = agent.run(self.price, iteration, self.stock)
                self._update_price_and_stock(result)
                agent_results.append({
                    "type": type(agent).__name__,
                    "available_capital": agent.available_capital,
                    "owned_gpus": agent.owned_gpus,
                    "action": result["action"],
                    "success": result["success"],
                    "current_stock": self.stock,
                    "current_price": self.price
                })
            self._record_iteration(iteration, agent_results)

        self.logger.handlers.clear()

    def _record_iteration(self, iteration: int, agent_results: List[Dict]) -> None:
        output = []
        output.append(f"\n--- Iteration {iteration + 1} ---")
        for i, agent_summary in enumerate(agent_results, start=1):
            output.append(f"Interaction {i} | Agent: {agent_summary['type']}, Capital: ${agent_summary['available_capital']:.2f}, "
                        f"GPUs: {agent_summary['owned_gpus']}, Action: {agent_summary['action']}, Success: {agent_summary['success']} | Current Stock: {agent_summary['current_stock']} | Current Price: ${agent_summary['current_price']:.2f}")
        self.logger.info("\n".join(output))
```

### Main

The `__main__.py` file contains the main entry point to run the market simulation. It initializes the initial price, number of iterations, and distribution of agents. Then, it creates the agents using the `AgentFactory` and runs the market simulation.

```python
def main():
    initial_price = 200.0
    iterations = 1000
    stock = 100000

    distribution = {
        "random": 51,
        "trend_follower": 24,
        "contrarian": 24,
        "custom": 1
    }

    total_agents = sum(distribution.values())

    agents = []
    for _ in range(distribution["random"]):
        agents.append(AgentFactory.create_agent("random", available_capital=1000, owned_gpus=0, total_agents=total_agents, distribution=distribution))
    for _ in range(distribution["trend_follower"]):
        agents.append(AgentFactory.create_agent("trend_follower", available_capital=1000, owned_gpus=0, total_agents=total_agents, distribution=distribution))
    for _ in range(distribution["contrarian"]):
        agents.append(AgentFactory.create_agent("contrarian", available_capital=1000, owned_gpus=0, total_agents=total_agents, distribution=distribution))
    for _ in range(distribution["custom"]):
        agents.append(AgentFactory.create_agent("custom", available_capital=1000, owned_gpus=0, total_agents=total_agents, distribution=distribution, total_iterations=iterations))


    market = Market(initial_price, iterations, stock, agents, verbose=True, log_to_file=True)
    market.simulate()
```

## Logic of `strategy_custom.py`

The custom strategy (`CustomStrategy`) is designed to maximize the agent's balance by buying at low prices and selling at high prices, ensuring that the agent ends up with zero GPUs. The specific logic is as follows:

- **Buy**: If the current price is at least 10% lower than the historical average price.
- **Sell**: If the current price is at least 5% higher than the historical average price.
- **Sell all**: If there are few iterations left, sell all remaining GPUs.

### Implementation Details

- **Price History**: A history of the last 10 prices is maintained to calculate the average price.
- **Reference Prices**: The lowest and highest observed prices are updated.
- **Safety Margin**: A safety margin is used to decide when to sell all remaining GPUs.

```python
class CustomStrategy(StrategyBaseModel):
    def __init__(self, total_iterations: int):
        self.total_iterations = total_iterations
        self.iteration_count = 0
        self.lowest_price = None
        self.highest_price = None
        self.price_history = []
        self.target_profit_percentage = 0.1
        self.buy_threshold = 0.10
        self.sell_threshold = 0.05
        self.safety_margin = 1

    def decide(self, agent: AgentBaseModel, gpu_price: float, turn: int) -> Dict[str, bool]:
        current_iteration = self.iteration_count
        self.iteration_count += 1
        iterations_left = self.total_iterations - current_iteration

        # Add the current price to the history for analysis
        self.price_history.append(gpu_price)
        if len(self.price_history) > 10:
            self.price_history.pop(0)

        # Set reference prices
        if self.lowest_price is None or gpu_price < self.lowest_price:
            self.lowest_price = gpu_price
        if self.highest_price is None or gpu_price > self.highest_price:
            self.highest_price = gpu_price

        # Calculate the historical average price
        avg_price = sum(self.price_history) / len(self.price_history)

        # If there are few iterations left, sell all remaining GPUs
        if iterations_left <= agent.owned_gpus + self.safety_margin:
            action = "sell" if agent.owned_gpus > 0 else "do_nothing"
        else:
            # Buy only if the price is at least 10% lower than the average price
            if gpu_price <= avg_price * (1 - self.buy_threshold) and agent.available_capital >= gpu_price:
                action = "buy"
            # Sell if the price is at least 5% higher than the average purchase price
            elif gpu_price >= avg_price * (1 + self.sell_threshold) and agent.owned_gpus > 0:
                action = "sell"
            else:
                action = "do_nothing"

        agent.previous_price = gpu_price

        result = {"action": action, "success": True}

        if action == "buy":
            result["success"] = agent._buy(gpu_price)
        elif action == "sell":
            result["success"] = agent._sell(gpu_price)

        return result
```
