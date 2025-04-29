from Belief_base.belief_base import BeliefBase
from Belief_base.formula import Implies, Or, Not, Atom
from Belief_base.entailment import cnf_clauses_for_query
from Belief_base.entailment import resolution_entails

def test_entailment():
    KB = BeliefBase()
    p, q = Atom("p"), Atom("q")
    KB.add(Implies(p, q))
    KB.add(p)
    assert resolution_entails(KB, q)    # should be True
    assert not resolution_entails(KB, Not(q))  # KB ⊭ ¬q

if __name__ == "__main__":
    test_entailment()
    print("All tests passed ✅")