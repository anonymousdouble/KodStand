
# no-constant-binary-expression
## Overview
Disallow expressions where the operation doesn't affect the value



Comparisons which will always evaluate to true or false and logical expressions (`||`, `&&`, `??`) which either always short-circuit or never short-circuit are both likely indications of programmer error.
These errors are especially common in complex expressions where operator precedence is easy to misjudge. For example:

```json
// One might think this would evaluate as `a + (b ?? c)`:
const x = a + b ?? c;

// But it actually evaluates as `(a + b) ?? c`. Since `a + b` can never be null,
// the `?? c` has no effect.
```
Additionally, this rule detects comparisons to newly constructed objects/arrays/functions/etc. In JavaScript, where objects are compared by reference, a newly constructed object can never `===` any other value. This can be surprising for programmers coming from languages where objects are compared by value.

```json
// Programmers coming from a language where objects are compared by value might expect this to work:
const isEmpty = x === [];

// However, this will always result in `isEmpty` being `false`.
```
## Rule Details
This rule identifies `==` and `===` comparisons which, based on the semantics of the JavaScript language, will always evaluate to `true` or `false`.
It also identifies `||`, `&&` and `??` logical expressions which will either always or never short-circuit.
Examples of incorrect code for this rule:


```json
/*eslint no-constant-binary-expression: "error"*/

const value1 = +x == null;

const value2 = condition ? x : {} || DEFAULT;

const value3 = !foo == null;

const value4 = new Boolean(foo) === true;

const objIsEmpty = someObj === {};

const arrIsEmpty = someArr === [];

const shortCircuit1 = condition1 && false && condition2;

const shortCircuit2 = condition1 || true || condition2;

const shortCircuit3 = condition1 ?? "non-nullish" ?? condition2;
```
Examples of correct code for this rule:


```json
/*eslint no-constant-binary-expression: "error"*/

const value1 = x == null;

const value2 = (condition ? x : {}) || DEFAULT;

const value3 = !(foo == null);

const value4 = Boolean(foo) === true;

const objIsEmpty = Object.keys(someObj).length === 0;

const arrIsEmpty = someArr.length === 0;
```

## Related Rules


no-constant-condition 


## Version
This rule was introduced in ESLint v8.14.0.
## Further Reading





Interesting bugs caught by no-constant-binary-expression - ESLint - Pluggable JavaScript Linter 
 eslint.org





## Resources

Rule source 
Tests source 

