import random
import time
from typing import List

class SwarmGovernanceOrchestrator:
    def __init__(self, agents: List["Agent"]):
        self.agents = agents
        self.proposals = []
        self.voting_power = {agent: 1 for agent in agents}
        self.voting_results = {}

    def submit_proposal(self, agent: "Agent", proposal: "Proposal"):
        self.proposals.append(proposal)
        self.voting_results[proposal] = {}

    def vote_on_proposal(self, agent: "Agent", proposal: "Proposal", vote: bool):
        if proposal not in self.proposals:
            raise ValueError("Proposal not found")
        self.voting_results[proposal][agent] = vote
        total_votes = sum(self.voting_results[proposal].values())
        total_voting_power = sum(self.voting_power.values())
        if total_votes / total_voting_power >= 0.51:
            self.apply_proposal(proposal)
            self.proposals.remove(proposal)
            del self.voting_results[proposal]

    def apply_proposal(self, proposal: "Proposal"):
        proposal.apply(self.agents)

class Proposal:
    def __init__(self, description: str, apply_func: callable):
        self.description = description
        self.apply = apply_func

class Agent:
    def __init__(self, name: str):
        self.name = name

if __name__ == "__main__":
    agents = [Agent(f"Agent {i}") for i in range(10)]
    orchestrator = SwarmGovernanceOrchestrator(agents)

    def increase_speed_proposal(agents: List[Agent]):
        for agent in agents:
            agent.speed += 1

    proposal = Proposal("Increase agent speed", increase_speed_proposal)
    orchestrator.submit_proposal(agents[0], proposal)

    for agent in agents:
        orchestrator.vote_on_proposal(agent, proposal, random.choice([True, False]))

    time.sleep(1)
    print("Agents speeds after proposal application:")
    for agent in agents:
        print(f"{agent.name}: {agent.speed}")
