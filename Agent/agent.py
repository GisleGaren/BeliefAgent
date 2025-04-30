from Belief_base.belief_base import BeliefBase
from Belief_base.formula import Formula, Atom, Not, Or, And
from Belief_base.entailment import resolution_entails

class BeliefRevisionAgent:
    def __init__(self):
        # Initialize the belief base
        self.base = BeliefBase()
        
    # Method to ask the agent if the belief base entails a query φ
    def ask(self, query: Formula) -> bool:
        # Use resolution-based entailment to check if KB ⊨ φ
        return resolution_entails(self.base, query)
    
    # Selection function for remainders
    def select_remainders(self, remainders: list[set[int]]) -> list[set[int]]:
        
        # Selects a subset of remainders for partial meet contraction.
        
        
        # Trivial selection: pick all remainders
        return remainders

    def contract_partial_meet(self, formula: Formula):
        """
        Perform partial meet contraction on the belief base with respect to a formula.
        This removes the formula from the belief base while maintaining consistency.
        """
        # Compute all maximal subsets of the belief base that do not entail the formula
        remainders = self.base.compute_remainders(formula)
        
        # Select a subset of remainders using the selection function
        selected = self.select_remainders(remainders)
        
        # Compute the intersection of all selected sets
        # If no remainders are selected, the intersection is empty
        intersection = set.intersection(*selected) if selected else set()
        
        # Rebuild the belief base with only the beliefs whose indices are in the intersection
        old_beliefs = self.base.get_prioritized_beliefs()  # Get all beliefs with priorities
        new_beliefs = [old_beliefs[i] for i in intersection]  # Filter beliefs by intersection
        self.base.beliefs = new_beliefs  # Update the belief base