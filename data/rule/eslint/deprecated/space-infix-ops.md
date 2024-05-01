
# space-infix-ops
## Overview
Require spacing around infix operators


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .
While formatting preferences are very personal, a number of style guides require spaces around operators, such as:

```json
var sum = 1 + 2;
```
Proponents of this rule believe that it makes code easier to read and can more easily highlight potential errors, such as:

```json
var sum = i+++2;
```
While this is valid JavaScript syntax, it is hard to determine what the author intended.
## Rule Details
This rule is aimed at ensuring there are spaces around infix operators.
## Options
This rule accepts a single options argument with the following defaults:

```json
"space-infix-ops": ["error", { "int32Hint": false }]
```
### int32Hint
Set the `int32Hint` option to `true` (default is `false`) to allow write `a|0` without space.

```json
var foo = bar|0; // `foo` is forced to be signed 32 bit integer
```
Examples of incorrect code for this rule:


```json
/*eslint space-infix-ops: "error"*/
/*eslint-env es6*/

a+b

a+ b

a +b

a?b:c

const a={b:1};

var {b=0}=bar;

function foo(a=0) { }
```
Examples of correct code for this rule:


```json
/*eslint space-infix-ops: "error"*/
/*eslint-env es6*/

a + b

a       + b

a ? b : c

const a = {b:1};

var {b = 0} = bar;

function foo(a = 0) { }
```
## When Not To Use It
You can turn this rule off if you are not concerned with the consistency of spacing around infix operators.
## Version
This rule was introduced in ESLint v0.2.0.
## Resources

Rule source 
Tests source 

