
# no-continue
## Overview
Disallow `continue` statements



The `continue` statement terminates execution of the statements in the current iteration of the current or labeled loop, and continues execution of the loop with the next iteration. When used incorrectly it makes code less testable, less readable and less maintainable. Structured control flow statements such as `if` should be used instead.

```json
var sum = 0,
    i;

for(i = 0; i < 10; i++) {
    if(i >= 5) {
        continue;
    }

    sum += i;
}
```
## Rule Details
This rule disallows `continue` statements.
Examples of incorrect code for this rule:


```json
/*eslint no-continue: "error"*/

var sum = 0,
    i;

for(i = 0; i < 10; i++) {
    if(i >= 5) {
        continue;
    }

    sum += i;
}
```


```json
/*eslint no-continue: "error"*/

var sum = 0,
    i;

labeledLoop: for(i = 0; i < 10; i++) {
    if(i >= 5) {
        continue labeledLoop;
    }

    sum += i;
}
```
Examples of correct code for this rule:


```json
/*eslint no-continue: "error"*/

var sum = 0,
    i;

for(i = 0; i < 10; i++) {
    if(i < 5) {
       sum += i;
    }
}
```
## Compatibility

JSLint: `continue`

## Version
This rule was introduced in ESLint v0.19.0.
## Resources

Rule source 
Tests source 

