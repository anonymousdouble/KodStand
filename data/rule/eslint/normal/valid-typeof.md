
# valid-typeof
## Overview
Enforce comparing `typeof` expressions against valid strings


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        

💡 hasSuggestions

            Some problems reported by this rule are manually fixable by editor suggestions 



For a vast majority of use cases, the result of the `typeof` operator is one of the following string literals: `"undefined"`, `"object"`, `"boolean"`, `"number"`, `"string"`, `"function"`, `"symbol"`, and `"bigint"`. It is usually a typing mistake to compare the result of a `typeof` operator to other string literals.
## Rule Details
This rule enforces comparing `typeof` expressions to valid string literals.
## Options
This rule has an object option:

`"requireStringLiterals": true` requires `typeof` expressions to only be compared to string literals or other `typeof` expressions, and disallows comparisons to any other value.

Examples of incorrect code for this rule:


```json
/*eslint valid-typeof: "error"*/

typeof foo === "strnig"
typeof foo == "undefimed"
typeof bar != "nunber"
typeof bar !== "fucntion"
```
Examples of correct code for this rule:


```json
/*eslint valid-typeof: "error"*/

typeof foo === "string"
typeof bar == "undefined"
typeof foo === baz
typeof bar === typeof qux
```
Examples of incorrect code with the `{ "requireStringLiterals": true }` option:


```json
/*eslint valid-typeof: ["error", { "requireStringLiterals": true }]*/

typeof foo === undefined
typeof bar == Object
typeof baz === "strnig"
typeof qux === "some invalid type"
typeof baz === anotherVariable
typeof foo == 5
```
Examples of correct code with the `{ "requireStringLiterals": true }` option:


```json
/*eslint valid-typeof: ["error", { "requireStringLiterals": true }]*/

typeof foo === "undefined"
typeof bar == "object"
typeof baz === "string"
typeof bar === typeof qux
```
## When Not To Use It
You may want to turn this rule off if you will be using the `typeof` operator on host objects.
## Version
This rule was introduced in ESLint v0.5.0.
## Further Reading





typeof - JavaScript | MDN 
 developer.mozilla.org





## Resources

Rule source 
Tests source 

