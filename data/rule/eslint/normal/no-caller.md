

# no-caller
## Overview

Disallow the use of `arguments.caller` or `arguments.callee`

The use of `arguments.caller` and `arguments.callee` make several code optimizations impossible. They have been deprecated in future versions of JavaScript and their use is forbidden in ECMAScript 5 while in strict mode.


```json
function foo() {
    var callee = arguments.callee;
}
```

## Rule Details

This rule is aimed at discouraging the use of deprecated and sub-optimal code by disallowing the use of `arguments.caller` and `arguments.callee`. As such, it will warn when `arguments.caller` and `arguments.callee` are used.

Examples of incorrect code for this rule:


```json
/*eslint no-caller: "error"*/

function foo(n) {
    if (n <= 0) {
        return;
    }

    arguments.callee(n - 1);
}

[1,2,3,4,5].map(function(n) {
    return !(n > 1) ? 1 : arguments.callee(n - 1) * n;
});
```

Examples of correct code for this rule:


```json
/*eslint no-caller: "error"*/

function foo(n) {
    if (n <= 0) {
        return;
    }

    foo(n - 1);
}

[1,2,3,4,5].map(function factorial(n) {
    return !(n > 1) ? 1 : factorial(n - 1) * n;
});
```


## Version

This rule was introduced in ESLint v0.0.6.

## Resources


- Rule source 

- Tests source 

