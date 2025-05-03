from Agent.agent import BeliefRevisionAgent
from Belief_base.formula import Atom, Not, Or, And

# B ∗ ϕ = Cn(B ∗ ϕ) so we can use the B ∗ ϕ := (B ÷ ¬ϕ) + ϕ Levi Identity for this
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
    phi = Not(q)  # ¬q
    # In this case, φ=¬q and when we pass this into the revise method
    # we contract by ¬φ, which is ¬(¬q) = q.
    agent.revise(phi)

    # Because of modus ponens, we should now have ¬p in the belief base
    # But that contradicts the original belief base because p, p → q entails q
    print("\n🧠 Belief base after revise(¬q):")
    print(agent.base)

    # Assert expected outcomes
    assert not agent.ask(q), "Expected q not to be entailed after revising with ¬q"
    assert agent.ask(Not(q)), "Expected ¬q to be entailed after revising with ¬q"

    print("test_success_postulate (conflict case) passed\n")
    
# After contracting the belief base by some formula φ, the resulting belief base should be a subset of the original belief base.
def test_inclusion_postulate():
    print("Running test_inclusion_postulate")
    agent = BeliefRevisionAgent()

    # Define atoms
    p, q, r = Atom("p"), Atom("q"), Atom("r")

    # Add beliefs: p and p → q (which is ¬p ∨ q)
    agent.base.add(p)
    agent.base.add(Or(p, r))
    agent.base.add(Or(Not(p), q))  # This implies q via modus ponens

    print("🧠 Belief base before contraction with q:")
    print(agent.base)

    # Take a snapshot of current beliefs (CNF already applied)
    original_beliefs = set(agent.base.get_beliefs())

    # Now contract q
    agent.contract_partial_meet(q)

    # Based on our success postulate previously, both p and p → q gets removed, which leaves us with p ∨ r
    # Which is a subset
    print("\n🧠 Belief base after contraction:")
    print(agent.base)

    # Get the updated beliefs
    new_beliefs = set(agent.base.get_beliefs())

    # Check that nothing new was added — only removed or unchanged
    assert new_beliefs.issubset(original_beliefs), "Inclusion postulate failed: new base not a subset"

    print("test_inclusion_postulate passed\n")

# If a formula ϕ is not entailed by the belief base, then contracting ϕ should not change anything.
# In short: you can't remove what you don't believe, so the base should stay the same.
def test_vacuity_postulate():
    print("Running test_vacuity_postulate")

    agent = BeliefRevisionAgent()
    
    p = Atom("p")  # "my car is red"
    r = Atom("r")  # "It's raining"
    s = Atom("s")  # "The sun is shining"

    # Add belief "raining" and "My car is red" ∧ "It's raining"
    agent.base.add(r)
    agent.base.add(And(p,r))

    # get original belifs
    original_beliefs = set(agent.base.get_beliefs())

    print("🧠 Belief base before vacuous contraction with 's':")
    print(agent.base)

    # Try to contract "sun is shining" — which we don't believe
    agent.contract_partial_meet(s)

    print("\n🧠 Belief base after vacuous contraction:")
    print(agent.base)

    # Belief base should be unchanged
    new_beliefs = set(agent.base.get_beliefs())
    assert original_beliefs == new_beliefs, "Vacuity postulate failed: base changed even though formula not entailed"

    print("test_vacuity_postulate passed\n")

# In the slides in week 11, the consistency postulate is a part of the revision postulates
def test_consistency_postulate():
    print("Running test_consistency_postulate")
    agent = BeliefRevisionAgent()
    
    # Pick a simple atom and seeed base with somethig consistent
    p = Atom("p")
    q = Atom("q")
    agent.base.add(Or(p, q))      # p ∨ q
    agent.base.add(Or(Not(p), q)) # p → q (which is ¬p ∨ q)
    
    print("🧠 Belief base before revision:")
    print(agent.base)
    
    # Revise by p (which is consistent)
    agent.revise(p)
    
    print("\n🧠 Belief base after revising with p:")
    print(agent.base)
    
    # Build an explicit contradiction: p ∧ ¬p
    contradiction = And(p, Not(p))
    
    # Test bug entailing contradiction
    print("Entails p ∧ ¬p?", agent.ask(contradiction))
    print("Entails p?", agent.ask(p))
    print("Entails ¬p?", agent.ask(Not(p)))
    
    # The base *should not* entail a contradiction
    # In other words, does our current belief base logically imply p ∧ ¬p?
    # If it does, then we have an inconsistency in our belief base
    assert not agent.ask(contradiction), \
        "Consistency postulate failed: belief base is inconsistent after revision"
    
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