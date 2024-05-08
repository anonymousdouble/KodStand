

# require-yield
## Overview

Require generator functions to contain `yield`

## Rule Details

This rule generates warnings for generator functions that do not have the `yield` keyword.

## Examples

Examples of incorrect code for this rule:


```json
/*eslint require-yield: "error"*/
/*eslint-env es6*/

function* foo() {
  return 10;
}
```

Examples of correct code for this rule:


```json
/*eslint require-yield: "error"*/
/*eslint-env es6*/

function* foo() {
  yield 5;
  return 10;
}

function bar() {
  return 10;
}

// This rule does not warn on empty generator functions.
function* baz() { }
```

## When Not To Use It

If you don’t want to notify generator functions that have no `yield` expression, then it’s safe to disable this rule.

## Related Rules


- 
require-await 

## Version

This rule was introduced in ESLint v1.0.0-rc-1.

## Resources


- Rule source 

- Tests source 

