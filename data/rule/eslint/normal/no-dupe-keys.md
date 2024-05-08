

# no-dupe-keys
## Overview

Disallow duplicate keys in object literals

Multiple properties with the same key in object literals can cause unexpected behavior in your application.


```json
var foo = {
    bar: "baz",
    bar: "qux"
};
```

## Rule Details

This rule disallows duplicate keys in object literals.

Examples of incorrect code for this rule:


```json
/*eslint no-dupe-keys: "error"*/

var foo = {
    bar: "baz",
    bar: "qux"
};

var foo = {
    "bar": "baz",
    bar: "qux"
};

var foo = {
    0x1: "baz",
    1: "qux"
};
```

Examples of correct code for this rule:


```json
/*eslint no-dupe-keys: "error"*/

var foo = {
    bar: "baz",
    quxx: "qux"
};
```


## Handled by TypeScript


                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            

## Version

This rule was introduced in ESLint v0.0.9.

## Resources


- Rule source 

- Tests source 

