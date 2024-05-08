

# no-dupe-args
## Overview

Disallow duplicate arguments in `function` definitions

If more than one parameter has the same name in a function definition, the last occurrence “shadows” the preceding occurrences. A duplicated name might be a typing error.

## Rule Details

This rule disallows duplicate parameter names in function declarations or expressions. It does not apply to arrow functions or class methods, because the parser reports the error.

If ESLint parses code in strict mode, the parser (instead of this rule) reports the error.

Examples of incorrect code for this rule:


```json
/*eslint no-dupe-args: "error"*/

function foo(a, b, a) {
    console.log("value of the second a:", a);
}

var bar = function (a, b, a) {
    console.log("value of the second a:", a);
};
```

Examples of correct code for this rule:


```json
/*eslint no-dupe-args: "error"*/

function foo(a, b, c) {
    console.log(a, b, c);
}

var bar = function (a, b, c) {
    console.log(a, b, c);
};
```


## Handled by TypeScript


                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            

## Version

This rule was introduced in ESLint v0.16.0.

## Resources


- Rule source 

- Tests source 

