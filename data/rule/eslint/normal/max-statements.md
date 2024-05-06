
# max-statements
## Overview
Enforce a maximum number of statements allowed in function blocks



The `max-statements` rule allows you to specify the maximum number of statements allowed in a function.

```json
function foo() {
  var bar = 1; // one statement
  var baz = 2; // two statements
  var qux = 3; // three statements
}
```
## Rule Details
This rule enforces a maximum number of statements allowed in function blocks.
## Options
This rule has a number or object option:

`"max"` (default `10`) enforces a maximum number of statements allows in function blocks

Deprecated: The object property `maximum` is deprecated; please use the object property `max` instead.
This rule has an object option:

`"ignoreTopLevelFunctions": true` ignores top-level functions

### max
Examples of incorrect code for this rule with the default `{ "max": 10 }` option:


```json
/*eslint max-statements: ["error", 10]*/
/*eslint-env es6*/

function foo() {
  var foo1 = 1;
  var foo2 = 2;
  var foo3 = 3;
  var foo4 = 4;
  var foo5 = 5;
  var foo6 = 6;
  var foo7 = 7;
  var foo8 = 8;
  var foo9 = 9;
  var foo10 = 10;

  var foo11 = 11; // Too many.
}

let bar = () => {
  var foo1 = 1;
  var foo2 = 2;
  var foo3 = 3;
  var foo4 = 4;
  var foo5 = 5;
  var foo6 = 6;
  var foo7 = 7;
  var foo8 = 8;
  var foo9 = 9;
  var foo10 = 10;

  var foo11 = 11; // Too many.
};
```
Examples of correct code for this rule with the default `{ "max": 10 }` option:


```json
/*eslint max-statements: ["error", 10]*/
/*eslint-env es6*/

function foo() {
  var foo1 = 1;
  var foo2 = 2;
  var foo3 = 3;
  var foo4 = 4;
  var foo5 = 5;
  var foo6 = 6;
  var foo7 = 7;
  var foo8 = 8;
  var foo9 = 9;
  return function () { // 10

    // The number of statements in the inner function does not count toward the
    // statement maximum.

    var bar;
    var baz;
    return 42;
  };
}

let bar = () => {
  var foo1 = 1;
  var foo2 = 2;
  var foo3 = 3;
  var foo4 = 4;
  var foo5 = 5;
  var foo6 = 6;
  var foo7 = 7;
  var foo8 = 8;
  var foo9 = 9;
  return function () { // 10

    // The number of statements in the inner function does not count toward the
    // statement maximum.

    var bar;
    var baz;
    return 42;
  };
}
```
Note that this rule does not apply to class static blocks, and that statements in class static blocks do not count as statements in the enclosing function.
Examples of correct code for this rule with `{ "max": 2 }` option:


```json
/*eslint max-statements: ["error", 2]*/

function foo() {
    let one;
    let two = class {
        static {
            let three;
            let four;
            let five;
            if (six) {
                let seven;
                let eight;
                let nine;
            }
        }
    };
}
```
### ignoreTopLevelFunctions
Examples of additional correct code for this rule with the `{ "max": 10 }, { "ignoreTopLevelFunctions": true }` options:


```json
/*eslint max-statements: ["error", 10, { "ignoreTopLevelFunctions": true }]*/

function foo() {
  var foo1 = 1;
  var foo2 = 2;
  var foo3 = 3;
  var foo4 = 4;
  var foo5 = 5;
  var foo6 = 6;
  var foo7 = 7;
  var foo8 = 8;
  var foo9 = 9;
  var foo10 = 10;
  var foo11 = 11;
}
```

## Related Rules


complexity 

max-depth 

max-len 

max-lines 

max-lines-per-function 

max-nested-callbacks 

max-params 


## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 
