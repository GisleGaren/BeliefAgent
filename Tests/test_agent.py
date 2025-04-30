
from Agent.agent import BeliefRevisionAgent
from Belief_base.formula import Atom, Implies, Not

def test_contract_partial_meet():
    agent = BeliefRevisionAgent()
    
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")
    
    agent.base.add(Implies(p, q), priority=2)  # p → q
    agent.base.add(p, priority=1)              # p
    agent.base.add(Not(q), priority=3)         # ¬q
    
    print("Initial Belief Base:")
    print(agent.base)
    
    # Perform partial meet contraction with respect to ¬q
    agent.contract_partial_meet(Not(q))
    
    # Verify the updated belief base
    print("\nBelief Base After Contracting ¬q:")
    print(agent.base)
    
    
    # ¬q should be removed, and the remaining beliefs should be consistent
    assert Not(q) not in agent.base.get_beliefs()
    assert agent.ask(q) is True  # After contraction, KB ⊨ q

if __name__ == "__main__":
    test_contract_partial_meet()
    print("\nTest passed ✅")