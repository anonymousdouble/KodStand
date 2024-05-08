

# no-label-var
## Overview

Disallow labels that share a name with a variable

## Rule Details

This rule aims to create clearer code by disallowing the bad practice of creating a label that shares a name with a variable that is in scope.

Examples of incorrect code for this rule:


```json
/*eslint no-label-var: "error"*/

var x = foo;
function bar() {
x:
  for (;;) {
    break x;
  }
}
```

Examples of correct code for this rule:


```json
/*eslint no-label-var: "error"*/

// The variable that has the same name as the label is not in scope.

function foo() {
  var q = t;
}

function bar() {
q:
  for(;;) {
    break q;
  }
}
```

## When Not To Use It

If you don’t want to be notified about usage of labels, then it’s safe to disable this rule.

## Related Rules


- 
no-extra-label 

- 
no-labels 

- 
no-unused-labels 

## Version

This rule was introduced in ESLint v0.0.9.

## Resources


- Rule source 

- Tests source 

