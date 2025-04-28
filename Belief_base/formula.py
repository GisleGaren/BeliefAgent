class Formula:
    """
    This is an abstract base class (a.k.a interface) for all formula types, like a template.
    """
    
    # Define how to convert formula into a readable string like (p ∧ q)
    def __str__(self):
        raise NotImplementedError
    
    # Example: And(Atom("p"), Atom("q")).symbols() becomes {"p", "q"}
    def symbols(self):
        """Returns the set of propositional symbols in the formula."""
        raise NotImplementedError
    
    # An assignment is a dictionary that looks like {"p": True, "q": False}
    # Example: Implies(Atom("p"), Atom("q")).evaluate({"p": True, "q": False}) becomes False
    def evaluate(self, assignment):
        """
        Evaluates the formula under the given assignment.
        assignment is a dictionary mapping symbols to boolean values.
        """
        raise NotImplementedError
    
    # Example: r ↔ p ∨ s goes to 
    # (r → p ∨ s) ∧ (p ∨ s → r ) which goes to 
    # (¬r ∨ p ∨ s) ∧ (¬(p ∨ s) ∨ r ) then the right side of ∧ via demorgan's law becomes
    # (¬r ∨ p ∨ s) ∧ ((¬p ∧ ¬s) ∨ r ), now the right side can use distributive law to become
    # (¬r ∨ p ∨ s) ∧ (¬p ∨ r ) ∧ (¬s ∨ r ) to be in CNF form
    def to_cnf(self):
        """Converts the formula to Conjunctive Normal Form."""
        raise NotImplementedError

# Each atom represents a propositional symbol, like "p", "q", "r" etc
# This inherits the interface of Formula and MUST implement all these methods
class Atom(Formula):
    """A propositional symbol/atom."""
    def __init__(self, name):
        self.name = name
        
    # print(Atom("p"))  # Output: p
    def __str__(self):
        return self.name
    
    # Atom("p") == Atom("p")  # True
    # Atom("p") == Atom("q")  # False
    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.name == other.name
        return False
    
    # This function is here so that if we have a1 = Atom("p") and a2 = Atom("q"), it will only keep one of them in a set to avoid duplicates!
    def __hash__(self):
        return hash(self.name)
    
    # Returns the set of symbols used in the formula — in this case, just the one atom itself.
    # Like Atom("p").symbols()  # {'p'}
    def symbols(self):
        return {self.name}
    
    # This is how we determine whether the formula is True or False given a model (assignment of truth values):
    # assignment = {"p": True, "q": False}, so Atom("p").evaluate(assignment)  # True
    # Atom("q").evaluate(assignment)  # False and Atom("r").evaluate(assignment)  # False (default if not in assignment)
    def evaluate(self, assignment):
        return assignment.get(self.name, False)
    
    # Atoms are already in Conjunctive Normal Form by definition. "p" is as simple as it gets
    def to_cnf(self):
        return self

# Represents the negation of a formula, like ¬p or ¬(p ∧ q)
class Not(Formula):
    """Negation of a formula."""
    def __init__(self, formula):
        self.formula = formula
    
    # print(Not(Atom("p")))  # Output: ¬(p)
    def __str__(self):
        return f"¬({str(self.formula)})"
    
    # Formula to check if two Not objects are equal
    def __eq__(self, other):
        if isinstance(other, Not):
            return self.formula == other.formula
        return False
    
    # Without it, order sensitive like Not(And(p, q)) != Not(And(q, p)) # True so we need this to avoid that 
    def __hash__(self):
        return hash(("not", hash(self.formula)))
    
    # Returns all variables inside the negated formulas
    # Not(And(Atom("p"), Atom("q"))).symbols()
    # becomes {"p", "q"}
    def symbols(self):
        return self.formula.symbols()
    
    # Evaluates the negation of the formula
    # assignment = {"p": True}
    # Not(Atom("p")).evaluate(assignment) returns false
    def evaluate(self, assignment):
        return not self.formula.evaluate(assignment)
    
    # Method to recursively convert the negation to CNF
    def to_cnf(self):
        # Handle negation of complex formulas based on DeMorgan's laws and double negation
        if isinstance(self.formula, Not):
            # Double negation: ¬¬A ≡ A
            # Example: f = Not(Not(Atom("p"))) the system checks f is a Not object, then calls f.to_cnf() again
            # Then in this stack, we have f.formula and we check if this is a Not object again, which it is and we call f.formula.to_cnf()
            # We are now in f.formula.formula which is Atom("p") and we return that as the CNF, which we can see in the else at the bottom of this function
            return self.formula.formula.to_cnf()
        elif isinstance(self.formula, And):
            # DeMorgan: ¬(A ∧ B) ≡ ¬A ∨ ¬B
            return Or(*[Not(f).to_cnf() for f in self.formula.formulas]).to_cnf()
        elif isinstance(self.formula, Or):
            # DeMorgan: ¬(A ∨ B) ≡ ¬A ∧ ¬B
            return And(*[Not(f).to_cnf() for f in self.formula.formulas]).to_cnf()
        elif isinstance(self.formula, Implies):
            # ¬(A → B) ≡ A ∧ ¬B
            return And(self.formula.premise.to_cnf(), Not(self.formula.conclusion).to_cnf()).to_cnf()
        elif isinstance(self.formula, Equiv):
            # ¬(A ↔ B) ≡ (A ∧ ¬B) ∨ (¬A ∧ B)
            a, b = self.formula.left, self.formula.right
            return Or(And(a, Not(b)), And(Not(a), b)).to_cnf()
        else:
            # For atoms, just return the negation
            return self

class And(Formula):
    
    # Pass arguments And(p,q,r) because *formulas means we can pass any number of arguments
    def __init__(self, *formulas):
        self.formulas = formulas
    
    # print(And(Atom("p"), Atom("q")))  # Output: (p) ∧ (q)
    def __str__(self):
        return " ∧ ".join(f"({str(f)})" for f in self.formulas)
    
    # And(p, q) == And(q, p)  # True
    def __eq__(self, other):
        if isinstance(other, And):
            return set(self.formulas) == set(other.formulas)
        return False
    
    # Hashes so that we can use And(p, q) and And(q, p) in a set and it will only keep one of them
    def __hash__(self):
        return hash(("and", frozenset(self.formulas)))
    
    # Returns all symbols inside the And formula example: And(Atom("p"), Atom("q")).symbols() becomes {"p", "q"}
    def symbols(self):
        return set().union(*[f.symbols() for f in self.formulas])
    
    # Returns true if all formulas inside the And formula are true, otherwise false
    def evaluate(self, assignment):
        return all(f.evaluate(assignment) for f in self.formulas)
    
    # Takes something like p ∧ (q ∧ r) which is the same as And(p, And(q, r)) and returns 
    # a flat, clean CNF friendly version And(p,q,r)
    def to_cnf(self):
        # Convert all subformulas to CNF first
        # If we have And(p, Implies(q, r)), the Imples(q,r) becomes Or(Not(q), r) and p.to_cnf() becomes p
        # cnf_formulas = [p, Or(Not(q), r)]
        cnf_formulas = [f.to_cnf() for f in self.formulas]
        
        # Flatten nested ANDs
        # If there's for example And(p, And(q, r)), we want to flatten it to And(p, q, r)
        # In our example, our cnf_formulas is [p, Or(Not(q), r)], but there is no And inside it so we just return it as is
        flattened = []
        for f in cnf_formulas:
            if isinstance(f, And):
                flattened.extend(f.formulas)
            else:
                flattened.append(f)
        
        return And(*flattened)

class Or(Formula):
    """Disjunction of formulas."""
    def __init__(self, *formulas):
        self.formulas = formulas
    
    def __str__(self):
        return " ∨ ".join(f"({str(f)})" for f in self.formulas)
    
    def __eq__(self, other):
        if isinstance(other, Or):
            return set(self.formulas) == set(other.formulas)
        return False
    
    def __hash__(self):
        return hash(("or", frozenset(self.formulas)))
    
    def symbols(self):
        return set().union(*[f.symbols() for f in self.formulas])
    
    def evaluate(self, assignment):
        return any(f.evaluate(assignment) for f in self.formulas)
    
    def to_cnf(self):
        # Convert all subformulas to CNF first
        cnf_formulas = [f.to_cnf() for f in self.formulas]
        
        # Flatten nested ORs
        flattened = []
        for f in cnf_formulas:
            if isinstance(f, Or):
                flattened.extend(f.formulas)
            else:
                flattened.append(f)
        
        # Apply distributivity of OR over AND
        and_formulas = [f for f in flattened if isinstance(f, And)]
        if not and_formulas:
            return Or(*flattened)
        
        # Pick an AND to distribute over
        and_formula = and_formulas[0]
        other_formulas = [f for f in flattened if f != and_formula]
        
        # Distribute OR over AND
        distributed = []
        for conj in and_formula.formulas:
            new_or = Or(conj, *other_formulas).to_cnf()
            distributed.append(new_or)
        
        return And(*distributed)

class Implies(Formula):
    """Implication formula (P → Q)."""
    def __init__(self, premise, conclusion):
        self.premise = premise
        self.conclusion = conclusion
    
    def __str__(self):
        return f"({str(self.premise)}) → ({str(self.conclusion)})"
    
    def __eq__(self, other):
        if isinstance(other, Implies):
            return self.premise == other.premise and self.conclusion == other.conclusion
        return False
    
    def __hash__(self):
        return hash(("implies", hash(self.premise), hash(self.conclusion)))
    
    def symbols(self):
        return self.premise.symbols().union(self.conclusion.symbols())
    
    def evaluate(self, assignment):
        return (not self.premise.evaluate(assignment)) or self.conclusion.evaluate(assignment)
    
    def to_cnf(self):
        # P → Q is equivalent to ¬P ∨ Q
        return Or(Not(self.premise), self.conclusion).to_cnf()

class Equiv(Formula):
    """Equivalence formula (P ↔ Q)."""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"({str(self.left)}) ↔ ({str(self.right)})"
    
    def __eq__(self, other):
        if isinstance(other, Equiv):
            return (self.left == other.left and self.right == other.right) or \
                  (self.left == other.right and self.right == other.left)
        return False
    
    def __hash__(self):
        return hash(("equiv", frozenset([hash(self.left), hash(self.right)])))
    
    def symbols(self):
        return self.left.symbols().union(self.right.symbols())
    
    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)
    
    def to_cnf(self):
        # P ↔ Q is equivalent to (P → Q) ∧ (Q → P), or (¬P ∨ Q) ∧ (¬Q ∨ P)
        return And(
            Or(Not(self.left), self.right),
            Or(Not(self.right), self.left)
        ).to_cnf()
