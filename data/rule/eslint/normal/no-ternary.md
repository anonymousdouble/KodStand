

# no-ternary
## Overview

Disallow ternary operators

The ternary operator is used to conditionally assign a value to a variable. Some believe that the use of ternary operators leads to unclear code.


```json
var foo = isBar ? baz : qux;
```

## Rule Details

This rule disallows ternary operators.

Examples of incorrect code for this rule:


```json
/*eslint no-ternary: "error"*/

var foo = isBar ? baz : qux;

function quux() {
  return foo ? bar() : baz();
}
```

Examples of correct code for this rule:


```json
/*eslint no-ternary: "error"*/

var foo;

if (isBar) {
    foo = baz;
} else {
    foo = qux;
}

function quux() {
    if (foo) {
        return bar();
    } else {
        return baz();
    }
}
```


## Related Rules


- 
no-nested-ternary 

- 
no-unneeded-ternary 

## Version

This rule was introduced in ESLint v0.0.9.

## Resources


- Rule source 

- Tests source 

