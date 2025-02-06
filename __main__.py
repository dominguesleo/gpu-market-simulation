from src.market.market_model import Market
from src.factories.agent_factory import AgentFactory

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

    custom_agents = [agent for agent in agents if type(agent).__name__ == "AgentCustom"]
    if custom_agents:
        custom_agent = custom_agents[0]
        print( "-" * 50)
        print(f"Custom agent final capital: ${custom_agent.available_capital:.2f}")
        print(f"Custom agent final GPU count: {custom_agent.owned_gpus}")
    print(f"Final GPU price: ${market.price:.2f}")
    print(f"Final GPU stock: {market.stock}")

if __name__ == "__main__":
    main()