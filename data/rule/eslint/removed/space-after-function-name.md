
# space-after-function-name
## Overview

Enforces consistent spacing after name in function definitions.
Whitespace between a function name and its parameter list is optional.

```json
function withoutSpace(x) {
    // ...
}

function withSpace (x) {
    // ...
}
```
Some style guides may require a consistent spacing for function names.
## Rule Details
This rule aims to enforce a consistent spacing after function names. It takes one argument. If it is `"always"` then all function names must be followed by at least one space. If `"never"` then there should be no spaces between the name and the parameter list. The default is `"never"`.
Examples of incorrect code for this rule:

```json
function foo (x) {
    // ...
}

var x = function named (x) {};

// When ["error", "always"]
function bar(x) {
    // ...
}
```
Examples of correct code for this rule:

```json
function foo(x) {
    // ...
}

var x = function named(x) {};

// When ["error", "always"]
function bar (x) {
    // ...
}
```

## Version
This rule was introduced in ESLint v0.11.0
                 and removed in v1.0.0-rc-1.

## Replaced by
space-before-function-paren