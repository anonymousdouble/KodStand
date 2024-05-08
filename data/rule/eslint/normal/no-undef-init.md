

# no-undef-init
## Overview

Disallow initializing variables to `undefined`

In JavaScript, a variable that is declared and not initialized to any value automatically gets the value of `undefined`. For example:


```json
var foo;

console.log(foo === undefined);     // true
```

It’s therefore unnecessary to initialize a variable to `undefined`, such as:


```json
var foo = undefined;
```

It’s considered a best practice to avoid initializing variables to `undefined`.

## Rule Details

This rule aims to eliminate `var` and `let` variable declarations that initialize to `undefined`.

Examples of incorrect code for this rule:


```json
/*eslint no-undef-init: "error"*/

var foo = undefined;
let bar = undefined;
```

Examples of correct code for this rule:


```json
/*eslint no-undef-init: "error"*/

var foo;
let bar;
```

Please note that this rule does not check `const` declarations, destructuring patterns, function parameters, and class fields.

Examples of additional correct code for this rule:


```json
/*eslint no-undef-init: "error"*/

const foo = undefined;

let { bar = undefined } = baz;

[quux = undefined] = quuux;

(foo = undefined) => {};

class Foo {
    bar = undefined;
}
```

## When Not To Use It

There is one situation where initializing to `undefined` behaves differently than omitting the initialization, and that’s when a `var` declaration occurs inside of a loop. For example:

Example of incorrect code for this rule:


```json
/*eslint no-undef-init: "error"*/

for (i = 0; i < 10; i++) {
    var x = undefined;
    console.log(x);
    x = i;
}
```

In this case, the `var x` is hoisted out of the loop, effectively creating:


```json
var x;

for (i = 0; i < 10; i++) {
    x = undefined;
    console.log(x);
    x = i;
}
```

If you were to remove the initialization, then the behavior of the loop changes:


```json
for (i = 0; i < 10; i++) {
    var x;
    console.log(x);
    x = i;
}
```

This code is equivalent to:


```json
var x;

for (i = 0; i < 10; i++) {
    console.log(x);
    x = i;
}
```

This produces a different outcome than defining `var x = undefined` in the loop, as `x` is no longer reset to `undefined` each time through the loop.

If you’re using such an initialization inside of a loop, then you should disable this rule.

Example of correct code for this rule, because it is disabled on a specific line:


```json
/*eslint no-undef-init: "error"*/

for (i = 0; i < 10; i++) {
    var x = undefined; // eslint-disable-line no-undef-init
    console.log(x);
    x = i;
}
```


## Related Rules


- 
no-undefined 

- 
no-void 

## Version

This rule was introduced in ESLint v0.0.6.

## Resources


- Rule source 

- Tests source 

