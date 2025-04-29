from typing import List, Set, Tuple
from Belief_base.formula import Formula, And, Or, Not, Atom

# Literal is for (atom name, is_positive) example: ("p", False) means ¬p
Literal = Tuple[str, bool]
# Clause is the frozenset of literals
Clause  = frozenset[Literal]

""" 
Something like this:

And(
  Or(Atom("p"), Not(Atom("q"))),   # clause 1: p ∨ ¬q
  Atom("r")                        # clause 2: r
)

Will give 

[
  frozenset({("p", True),  ("q", False)}),
  frozenset({("r", True)})
]

via extract_clauses()

"""
def extract_clauses(formula: Formula) -> List[Clause]:
    # Double check if the formula is in CNF
    cnf = formula.to_cnf()
    
    # If the formula has ∧, break up the conjunction into separate clauses
    if isinstance(cnf, And):
        # Example: And(Or(p,q), Or(r,s)) becomes [Or(p,q), Or(r,s)]
        subformulas = list(cnf.subformulas)
    else:
        # If there is no ∧, treat the whole formula as a single clause
        subformulas = [cnf]
        
    # Create empty formula list 
    clauses: List[Clause] = []
    
    # Now we split up the subformulas based on the ∨ operator
    for sub in subformulas:
        # If there is an or operator, that means we have a clause with multiple literals like Or(p, Not(q)) has p and ¬q, 2 literals
        # Example: Or(p, Not(q)) becomes [p, ¬q]
        if isinstance(sub, Or):
            disjunctions = list(sub.formulas)
        else:
            # If there is no or operator, then we have a unit clause like Atom("p") or Not(Atom("q")) which is a single literal
            disjunctions = [sub]
            
    # set of literals to turn each disjunction into a (atom, is_positive) tuple
    lits: Set[Literal] = set()
    
    # Loop through each literal in the disjunctions list
    for lit in disjunctions:
        # Check if the literal is true
        if isinstance(lit, Atom):
            lits.add((lit.name, True))  # Positive literal
        # Check if the literal is a negation (false) and that it is an atom
        elif isinstance(lit, Not) and isinstance(lit.formula, Atom):
            lits.add((lit.formula.name, False))
        else:
            # In every proper CNF, every literal must be either an Atom or Not(Atom)
            raise ValueError(f"Non literal in clause: {lit}")
        
    # Finally add the set of literals to the clauses list as a frozenset
    clauses.append(frozenset(lits)) 
