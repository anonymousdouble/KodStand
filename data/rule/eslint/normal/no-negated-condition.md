
# no-negated-condition
## Overview
Disallow negated conditions



Negated conditions are more difficult to understand. Code can be made more readable by inverting the condition instead.
## Rule Details
This rule disallows negated conditions in either of the following:

`if` statements which have an `else` branch
ternary expressions

Examples of incorrect code for this rule:


```json
/*eslint no-negated-condition: "error"*/

if (!a) {
    doSomething();
} else {
    doSomethingElse();
}

if (a != b) {
    doSomething();
} else {
    doSomethingElse();
}

if (a !== b) {
    doSomething();
} else {
    doSomethingElse();
}

!a ? c : b
```
Examples of correct code for this rule:


```json
/*eslint no-negated-condition: "error"*/

if (!a) {
    doSomething();
}

if (!a) {
    doSomething();
} else if (b) {
    doSomething();
}

if (a != b) {
    doSomething();
}

a ? b : c
```

## Version
This rule was introduced in ESLint v1.6.0.
## Resources

Rule source 
Tests source 
