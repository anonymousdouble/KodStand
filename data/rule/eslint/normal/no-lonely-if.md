

# no-lonely-if
## Overview

Disallow `if` statements as the only statement in `else` blocks

If an `if` statement is the only statement in the `else` block, it is often clearer to use an `else if` form.


```json
if (foo) {
    // ...
} else {
    if (bar) {
        // ...
    }
}
```

should be rewritten as


```json
if (foo) {
    // ...
} else if (bar) {
    // ...
}
```

## Rule Details

This rule disallows `if` statements as the only statement in `else` blocks.

Examples of incorrect code for this rule:


```json
/*eslint no-lonely-if: "error"*/

if (condition) {
    // ...
} else {
    if (anotherCondition) {
        // ...
    }
}

if (condition) {
    // ...
} else {
    if (anotherCondition) {
        // ...
    } else {
        // ...
    }
}
```

Examples of correct code for this rule:


```json
/*eslint no-lonely-if: "error"*/

if (condition) {
    // ...
} else if (anotherCondition) {
    // ...
}

if (condition) {
    // ...
} else if (anotherCondition) {
    // ...
} else {
    // ...
}

if (condition) {
    // ...
} else {
    if (anotherCondition) {
        // ...
    }
    doSomething();
}
```

## When Not To Use It

Disable this rule if the code is clearer without requiring the `else if` form.

## Version

This rule was introduced in ESLint v0.6.0.

## Resources


- Rule source 

- Tests source 

