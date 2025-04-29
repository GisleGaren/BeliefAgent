from Belief_base.belief_base import BeliefBase
from Belief_base.formula import Implies, Or, Not, Atom

def tryClauses():
    # Create the belief base
    KB = BeliefBase()
    # Define the variables
    p, q = Atom("p"), Atom("q")
    
    KB.add(Implies(p, q), priority=1)  # (¬p ∨ q)
    KB.add(p, priority=0)              # (p)
    
    # Query: q and method to get CNF clauses 
    clauses = cnf_clauses_for_query(KB, q)
    for c in clauses:
        print(c)
        
    # You should see:
    #  frozenset({('p', False), ('q', True)})   # from ¬p ∨ q
    #  frozenset({('p', True)})                 # from p
    #  frozenset({('q', False)})                # from ¬q (the negated query)

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
    
if __name__ == "__main__":
    example()