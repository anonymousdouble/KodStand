

# no-new-native-nonconstructor
## Overview

Disallow `new` operators with global non-constructor functions

It is a convention in JavaScript that global variables beginning with an uppercase letter typically represent classes that can be instantiated using the `new` operator, such as `new Array` and `new Map`. Confusingly, JavaScript also provides some global variables that begin with an uppercase letter that cannot be called using the `new` operator and will throw an error if you attempt to do so. These are typically functions that are related to data types and are easy to mistake for classes. Consider the following example:


```json
// throws a TypeError
let foo = new Symbol("foo");

// throws a TypeError
let result = new BigInt(9007199254740991);
```

Both `new Symbol` and `new BigInt` throw a type error because they are functions and not classes. It is easy to make this mistake by assuming the uppercase letters indicate classes.

## Rule Details

This rule is aimed at preventing the accidental calling of native JavaScript global functions with the `new` operator. These functions are:


- `Symbol`

- `BigInt`

## Examples

Examples of incorrect code for this rule:


```json
/*eslint no-new-native-nonconstructor: "error"*/
/*eslint-env es2022*/

var foo = new Symbol('foo');
var bar = new BigInt(9007199254740991);
```

Examples of correct code for this rule:


```json
/*eslint no-new-native-nonconstructor: "error"*/
/*eslint-env es2022*/

var foo = Symbol('foo');
var bar = BigInt(9007199254740991);

// Ignores shadowed Symbol.
function baz(Symbol) {
    const qux = new Symbol("baz");
}
function quux(BigInt) {
    const corge = new BigInt(9007199254740991);
}

```

## When Not To Use It

This rule should not be used in ES3/5 environments.

## Related Rules


- 
no-obj-calls 

## Version

This rule was introduced in ESLint v8.27.0.

## Further Reading

ECMAScript® 2023 Language Specification 
 tc39.es

ECMAScript® 2023 Language Specification 
 tc39.es

## Resources


- Rule source 

- Tests source 

