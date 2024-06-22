

dsl = '''RuleSet ::= Rule1 [And|Or|; Rule2]* # And means should satisfy Rule1 and Rule2. Or means can satisfy Rule1 or Rule2. ; means Rule1,Rule2 belongs to diffent groups
Rule ::= {{'Optional'| 'Mandatory'}} [ ['Order' of | 'Number' of] TermList [Operator TermList]* | Rule1 '->' Rule2] [ExceptionRule] #'Order' of  means order rule, 'Number' of means numberConstraint, Rule1 '->' Rule2 means applying Rule2 under the premise of Rule1 
ExceptionRule ::= 'Except ' TermList | Rule # means rules not applied to TermList | Rule
Operator = 'is'| 'is not' | '>=' | '<=' | '=' | '!=' | 'for' | 'not for' | 'before' | 'not before' | 'after' | 'not after' | 'between' | 'not between' | 'have' | 'not have' | 'Add' | 'Sub' | 'Mult' | MatMult | 'Div' | 'Mod' | 'Pow' | 'LShift' | 'RShift' | 'BitOr' | 'BitXor' | 'BitAnd' | 'FloorDiv'
TermList ::= Term [, Term]*
Modifier ::= 'some' | 'each' | 'all' | 'except' | 'first' | 'last' | ...
Term :: = JavaTerm | Modifier* Term | Term of Term
JavaTerm means the formal expression using such format [XXX] "XXX" represent a JavaTerm
'''