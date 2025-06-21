from agents.agent_core import SentientAgent

class SequentialPlanner:
    def __init__(self, agent: SentientAgent):
        self.agent = agent

    def plan(self, context, goal, steps=3):
        plan = []
        for i in range(steps):
            subgoal = f"Step {i+1} toward: {goal}"
            action = self.agent.suggest(context, subgoal).strip()
            plan.append(action)
            context += f"\nAction {i+1}: {action}"
        return plan
