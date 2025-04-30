from Belief_base.belief_base import BeliefBase
from Belief_base.formula import Formula, Atom, Not, Or, And
from Belief_base.entailment import resolution_entails
# Class to represent the interface 

class BeliefRevisionAgent:
    def __init__(self):
        self.base = BeliefBase()
        
    # Method to ask AI agent if a given belief base entails a query φ
    def ask(self,query: Formula) -> bool:
        return resolution_entails(self.base, query)
    
    # Method to add beliefs to the belief base with a given priority
    
    # Contract
    def contract_partial_meet(self, formula: Formula):
        """
        Remove a belief from the belief base using partial meet contraction.
        """
        # Compute all maximal subsets of the belief base that do not entail the formula
        remainders = self.base.compute_remainders(formula)
        
        # Selection function
        
        # Intersection = indexes to keep
        
        # Then rebuild KB in place: Keep only the beliefs in the intersection of all remainders