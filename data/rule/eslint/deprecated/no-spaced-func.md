

# no-spaced-func
## Overview

Disallow spacing between function identifiers and their applications (deprecated)

This rule was deprecated in ESLint v3.3.0 and replaced by the func-call-spacing  rule.

While it’s possible to have whitespace between the name of a function and the parentheses that execute it, such patterns tend to look more like errors.

## Rule Details

This rule disallows spacing between function identifiers and their applications.

Examples of incorrect code for this rule:


```json
/*eslint no-spaced-func: "error"*/

fn ()

fn
()
```

Examples of correct code for this rule:


```json
/*eslint no-spaced-func: "error"*/

fn()
```


## Version

This rule was introduced in ESLint v0.1.2.

## Resources


- Rule source 

- Tests source 

