

# wrap-regex
## Overview

Require parenthesis around regex literals

This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .

When a regular expression is used in certain situations, it can end up looking like a division operator. For example:


```json
function a() {
    return /foo/.test("bar");
}
```

## Rule Details

This is used to disambiguate the slash operator and facilitates more readable code.

Example of incorrect code for this rule:


```json
/*eslint wrap-regex: "error"*/

function a() {
    return /foo/.test("bar");
}
```

Example of correct code for this rule:


```json
/*eslint wrap-regex: "error"*/

function a() {
    return (/foo/).test("bar");
}
```


## Version

This rule was introduced in ESLint v0.1.0.

## Resources


- Rule source 

- Tests source 

