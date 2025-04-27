class Formula:
    """
    Base class for propositional logic formulas.
    """
    def __str__(self):
        raise NotImplementedError
    
    def symbols(self):
        """Returns the set of propositional symbols in the formula."""
        raise NotImplementedError
    
    def evaluate(self, assignment):
        """
        Evaluates the formula under the given assignment.
        assignment is a dictionary mapping symbols to boolean values.
        """
        raise NotImplementedError
    
    def to_cnf(self):
        """Converts the formula to Conjunctive Normal Form."""
        raise NotImplementedError

class Atom(Formula):
    """A propositional symbol/atom."""
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)
    
    def symbols(self):
        return {self.name}
    
    def evaluate(self, assignment):
        return assignment.get(self.name, False)
    
    def to_cnf(self):
        return self

class Not(Formula):
    """Negation of a formula."""
    def __init__(self, formula):
        self.formula = formula
    
    def __str__(self):
        return f"¬({str(self.formula)})"
    
    def __eq__(self, other):
        if isinstance(other, Not):
            return self.formula == other.formula
        return False
    
    def __hash__(self):
        return hash(("not", hash(self.formula)))
    
    def symbols(self):
        return self.formula.symbols()
    
    def evaluate(self, assignment):
        return not self.formula.evaluate(assignment)
    
    def to_cnf(self):
        # Handle negation of complex formulas based on DeMorgan's laws and double negation
        if isinstance(self.formula, Not):
            # Double negation: ¬¬A ≡ A
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
    """Conjunction of formulas."""
    def __init__(self, *formulas):
        self.formulas = formulas
    
    def __str__(self):
        return " ∧ ".join(f"({str(f)})" for f in self.formulas)
    
    def __eq__(self, other):
        if isinstance(other, And):
            return set(self.formulas) == set(other.formulas)
        return False
    
    def __hash__(self):
        return hash(("and", frozenset(self.formulas)))
    
    def symbols(self):
        return set().union(*[f.symbols() for f in self.formulas])
    
    def evaluate(self, assignment):
        return all(f.evaluate(assignment) for f in self.formulas)
    
    def to_cnf(self):
        # Convert all subformulas to CNF first
        cnf_formulas = [f.to_cnf() for f in self.formulas]
        
        # Flatten nested ANDs
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
