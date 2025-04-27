class BeliefBase:
    """
    A belief base that stores propositional formulas with priorities.
    Higher priority values mean the belief is more important.
    """
    def __init__(self):
        # List of (formula, priority) pairs
        self.beliefs = []
    
    def add(self, formula, priority=0):
        """Add a belief with the given priority."""
        # Convert formula to CNF for more efficient entailment checking later
        cnf_formula = formula.to_cnf()
        self.beliefs.append((cnf_formula, priority))
        # Sort beliefs by priority (descending)
        self.beliefs.sort(key=lambda x: x[1], reverse=True)
    
    def get_beliefs(self):
        """Get all beliefs in the belief base."""
        return [formula for formula, _ in self.beliefs]
    
    def get_prioritized_beliefs(self):
        """Get all beliefs with their priorities."""
        return self.beliefs
    
    def __str__(self):
        return "\n".join([f"{priority}: {formula}" for formula, priority in self.beliefs])
    
    def remove(self, formula):
        """Remove a belief from the belief base."""
        self.beliefs = [(f, p) for f, p in self.beliefs if f != formula]
    
    def clear(self):
        """Remove all beliefs from the belief base."""
        self.beliefs = []