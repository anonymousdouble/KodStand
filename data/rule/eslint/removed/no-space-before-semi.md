

# no-space-before-semi
## Overview

Disallows spaces before semicolons.

JavaScript allows for placing unnecessary spaces between an expression and the closing semicolon.

Space issues can also cause code to look inconsistent and harder to read.


```json
var thing = function () {
  var test = 12 ;
}  ;
```

## Rule Details

This rule prevents the use of spaces before a semicolon in expressions.

Examples of incorrect code for this rule:


```json
var foo = "bar" ;

var foo = function() {} ;

var foo = function() {
} ;

var foo = 1 + 2 ;
```

Examples of correct code for this rule:


```json
;(function(){}());

var foo = "bar";
```


## Related Rules


- 
semi 

- 
no-extra-semi 

## Version

This rule was introduced in ESLint v0.4.3
                 and removed in v1.0.0-rc-1.


## Replaced by
semi-spacing