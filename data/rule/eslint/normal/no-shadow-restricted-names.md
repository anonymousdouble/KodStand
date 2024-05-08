

# no-shadow-restricted-names
## Overview

Disallow identifiers from shadowing restricted names

ES5 §15.1.1 Value Properties of the Global Object (`NaN`, `Infinity`, `undefined`) as well as strict mode restricted identifiers `eval` and `arguments` are considered to be restricted names in JavaScript. Defining them to mean something else can have unintended consequences and confuse others reading the code. For example, there’s nothing preventing you from writing:


```json
var undefined = "foo";
```

Then any code used within the same scope would not get the global `undefined`, but rather the local version with a very different meaning.

## Rule Details

Examples of incorrect code for this rule:


```json
/*eslint no-shadow-restricted-names: "error"*/

function NaN(){}

!function(Infinity){};

var undefined = 5;

try {} catch(eval){}
```

Examples of correct code for this rule:


```json
/*eslint no-shadow-restricted-names: "error"*/

var Object;

function f(a, b){}

// Exception: `undefined` may be shadowed if the variable is never assigned a value.
var undefined;
```


## Related Rules


- 
no-shadow 

## Version

This rule was introduced in ESLint v0.1.4.

## Further Reading

Annotated ES5 
 es5.github.io

Annotated ES5 
 es5.github.io

## Resources


- Rule source 

- Tests source 

