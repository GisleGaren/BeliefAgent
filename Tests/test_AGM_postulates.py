from Agent.agent import BeliefRevisionAgent
from Belief_base.formula import Atom, Not, Or

def test_success_postulate():
    print("Running test_success_postulate")
    agent = BeliefRevisionAgent()
    
    p = Atom("p")               # "Light is on"
    q = Atom("q")               # "Switch is broken"

    # Add: p and p → q   (which is ¬p ∨ q)
    agent.base.add(p)
    agent.base.add(Or(Not(p), q))

    print("🧠 Belief base before revision:")
    print(agent.base)

    # Revise with ¬q — "Switch is NOT broken"
    agent.revise(Not(q))

    # Because of modus ponens, we should now have ¬p in the belief base
    # But that contradicts the original belief base because p, p → q entails q
    print("\n🧠 Belief base after revise(¬q):")
    print(agent.base)

    # Assert expected outcomes
    assert not agent.ask(q), "Expected q not to be entailed after revising with ¬q"
    assert agent.ask(Not(q)), "Expected ¬q to be entailed after revising with ¬q"

    print("test_success_postulate (conflict case) passed\n")

def test_inclusion_postulate():
    print("Running test_inclusion_postulate")
    agent = BeliefRevisionAgent()
    p, q = Atom("p"), Atom("q")
    p, q = Atom("p"), Atom("q")
    agent.base.add(p)
    original_beliefs = set(agent.base.get_beliefs())
    print("🧠 Belief base before contraction with q:")
    print(agent.base)
    agent.contract_partial_meet(q)  # q not entailed => no change
    print("\n🧠 Belief base after contraction:")
    print(agent.base)
    new_beliefs = set(agent.base.get_beliefs())
    assert new_beliefs.issubset(original_beliefs), "Inclusion postulate failed: new base not a subset"
    print("test_inclusion_postulate passed\n")

def test_vacuity_postulate():
    print("Running test_vacuity_postulate")
    agent = BeliefRevisionAgent()
    p, q = Atom("p"), Atom("q")
    agent.base.add(p)
    original_beliefs = set(agent.base.get_beliefs())
    print("🧠 Belief base before vacuous contraction with q:")
    print(agent.base)
    # q not entailed => contraction does nothing
    agent.contract_partial_meet(q)
    print("\n🧠 Belief base after vacuous contraction:")
    print(agent.base)
    new_beliefs = set(agent.base.get_beliefs())
    assert original_beliefs == new_beliefs, "Vacuity postulate failed: base changed even though formula not entailed"
    print("test_vacuity_postulate passed\n")

def test_consistency_postulate():
    print("Running test_consistency_postulate")
    agent = BeliefRevisionAgent()
    p, q = Atom("p"), Atom("q")
    # p → q, add them so q is entailed
    agent.base.add(p)
    agent.base.add(Or(Not(p), q))
    print("🧠 Belief base before consistency contraction with q:")
    print(agent.base)
    agent.contract_partial_meet(q)
    print("\n🧠 Belief base after consistency contraction:")
    print(agent.base)
    assert not agent.ask(q), "Consistency postulate failed: new base still entails q"
    print("test_consistency_postulate passed\n")

def test_extensionality_postulate():
    print("Running test_extensionality_postulate")
    agent1 = BeliefRevisionAgent()
    agent2 = BeliefRevisionAgent()
    p, q, r = Atom("p"), Atom("q"), Atom("r")
    # Two formulas that are logically equivalent: (p ∨ q) and (q ∨ p)
    print("🧠 Belief base of agent1 before contraction:")
    print(agent1.base)
    agent1.contract_partial_meet(Or(p, q))
    print("🧠 Belief base of agent1 after contraction:")
    print(agent1.base)
    print("\n🧠 Belief base of agent2 before contraction:")
    print(agent2.base)
    agent2.contract_partial_meet(Or(q, p))
    print("🧠 Belief base of agent2 after contraction:")
    print(agent2.base)
    # Compare sets of beliefs
    b1 = set(agent1.base.get_beliefs())
    b2 = set(agent2.base.get_beliefs())
    assert b1 == b2, "Extensionality postulate failed: logically equivalent formulas gave different results"
    print("test_extensionality_postulate passed\n")

if __name__ == "__main__":
    test_success_postulate()
    test_inclusion_postulate()
    test_vacuity_postulate()
    test_consistency_postulate()
    test_extensionality_postulate()