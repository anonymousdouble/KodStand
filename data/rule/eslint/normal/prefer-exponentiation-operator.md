
# prefer-exponentiation-operator
## Overview
Disallow the use of `Math.pow` in favor of the `**` operator


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


Introduced in ES2016, the infix exponentiation operator `**` is an alternative for the standard `Math.pow` function.
Infix notation is considered to be more readable and thus more preferable than the function notation.
## Rule Details
This rule disallows calls to `Math.pow` and suggests using the `**` operator instead.
Examples of incorrect code for this rule:


```json
/*eslint prefer-exponentiation-operator: "error"*/

const foo = Math.pow(2, 8);

const bar = Math.pow(a, b);

let baz = Math.pow(a + b, c + d);

let quux = Math.pow(-1, n);
```
Examples of correct code for this rule:


```json
/*eslint prefer-exponentiation-operator: "error"*/

const foo = 2 ** 8;

const bar = a ** b;

let baz = (a + b) ** (c + d);

let quux = (-1) ** n;
```
## When Not To Use It
This rule should not be used unless ES2016 is supported in your codebase.
## Version
This rule was introduced in ESLint v6.7.0.
## Further Reading





Exponentiation (**) - JavaScript | MDN 
 developer.mozilla.org










5848 - v8 - V8 JavaScript Engine - Monorail 
 bugs.chromium.org





## Resources

Rule source 
Tests source 

