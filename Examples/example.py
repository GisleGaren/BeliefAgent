from Belief_base.belief_base import BeliefBase
from Belief_base.formula import Implies, Or, Not, Atom

# Example usage
def example():
    # Create a belief base
    belief_base = BeliefBase()
    
    # Define some propositional symbols
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")
    
    # Add beliefs with priorities
    belief_base.add(Implies(p, q), priority=2)  # p → q with priority 2
    belief_base.add(p, priority=1)              # p with priority 1
    belief_base.add(Or(Not(q), r), priority=3)  # ¬q ∨ r with priority 3
    
    print("Belief Base:")
    print(belief_base)
    
    # Show how to retrieve beliefs
    print("\nAll beliefs:")
    for formula in belief_base.get_beliefs():
        print(formula)
    
    # Example of removing a belief
    print("\nAfter removing p → q:")
    belief_base.remove(Implies(p, q).to_cnf())
    print(belief_base)