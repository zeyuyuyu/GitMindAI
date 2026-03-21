import random
import json

class SwarmGovernanceOrchestrator:
    def __init__(self, num_agents, voting_threshold):
        self.num_agents = num_agents
        self.voting_threshold = voting_threshold
        self.agent_states = [{'id': i, 'vote': None} for i in range(num_agents)]

    def propose_action(self, action_proposal):
        """Propose an action for the swarm to vote on."""
        for agent in self.agent_states:
            agent['vote'] = random.choice(['yes', 'no'])

        yes_votes = sum(1 for agent in self.agent_states if agent['vote'] == 'yes')
        if yes_votes >= self.voting_threshold:
            print(f"Action '{action_proposal}' passed with {yes_votes}/{self.num_agents} votes.")
            return True
        else:
            print(f"Action '{action_proposal}' failed with {yes_votes}/{self.num_agents} votes.")
            return False

    def get_agent_states(self):
        """Return the current state of all agents."""
        return self.agent_states

    def save_state(self, filename):
        """Save the current state of the swarm governance orchestrator to a file."""
        with open(filename, 'w') as f:
            json.dump({
                'num_agents': self.num_agents,
                'voting_threshold': self.voting_threshold,
                'agent_states': self.agent_states
            }, f)

    def load_state(self, filename):
        """Load the state of the swarm governance orchestrator from a file."""
        with open(filename, 'r') as f:
            state = json.load(f)
            self.num_agents = state['num_agents']
            self.voting_threshold = state['voting_threshold']
            self.agent_states = state['agent_states']
