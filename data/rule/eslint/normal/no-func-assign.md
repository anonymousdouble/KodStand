
# no-func-assign
## Overview
Disallow reassigning `function` declarations


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


JavaScript functions can be written as a FunctionDeclaration `function foo() { ... }` or as a FunctionExpression `var foo = function() { ... };`. While a JavaScript interpreter might tolerate it, overwriting/reassigning a function written as a FunctionDeclaration is often indicative of a mistake or issue.

```json
function foo() {}
foo = bar;
```
## Rule Details
This rule disallows reassigning `function` declarations.
Examples of incorrect code for this rule:


```json
/*eslint no-func-assign: "error"*/

function foo() {}
foo = bar;

function baz() {
    baz = bar;
}

var a = function hello() {
  hello = 123;
};
```
Examples of incorrect code for this rule, unlike the corresponding rule in JSHint:


```json
/*eslint no-func-assign: "error"*/

foo = bar;
function foo() {}
```
Examples of correct code for this rule:


```json
/*eslint no-func-assign: "error"*/

var foo = function () {}
foo = bar;

function baz(baz) { // `baz` is shadowed.
    baz = bar;
}

function qux() {
    var qux = bar;  // `qux` is shadowed.
}
```

## Handled by TypeScript

                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            
## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 

