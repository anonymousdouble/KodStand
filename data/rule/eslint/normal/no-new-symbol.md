

# no-new-symbol
## Overview

Disallow `new` operators with the `Symbol` object

`Symbol` is not intended to be used with the `new` operator, but to be called as a function.


```json
var foo = new Symbol("foo");
```

This throws a `TypeError` exception.

## Rule Details

This rule is aimed at preventing the accidental calling of `Symbol` with the `new` operator.

## Examples

Examples of incorrect code for this rule:


```json
/*eslint no-new-symbol: "error"*/
/*eslint-env es6*/

var foo = new Symbol('foo');
```

Examples of correct code for this rule:


```json
/*eslint no-new-symbol: "error"*/
/*eslint-env es6*/

var foo = Symbol('foo');

// Ignores shadowed Symbol.
function bar(Symbol) {
    const baz = new Symbol("baz");
}

```

## When Not To Use It

This rule should not be used in ES3/5 environments.

## Handled by TypeScript


                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            

## Version

This rule was introduced in ESLint v2.0.0-beta.1.

## Further Reading

ECMAScript 2015 Language Specification – ECMA-262 6th Edition 
 www.ecma-international.org

## Resources


- Rule source 

- Tests source 

