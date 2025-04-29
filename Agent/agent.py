from Belief_base.belief_base import BeliefBase
from Belief_base.formula import Formula, Atom, Not, Or, And
from Belief_base.entailment import resolution_entails
# Class to represent the interface 

class BeliefRevisionAgent:
    def __init__(self):
        self.base = BeliefBase()
        
    def ask(self,query: Formula) -> bool:
        return resolution_entails(self.base, query)
    # Method to add beliefs to the belief base with a given priority
    
    # Contract
    
    # Expand