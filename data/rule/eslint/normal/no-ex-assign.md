

# no-ex-assign
## Overview

Disallow reassigning exceptions in `catch` clauses

If a `catch` clause in a `try` statement accidentally (or purposely) assigns another value to the exception parameter, it is impossible to refer to the error from that point on.
Since there is no `arguments` object to offer alternative access to this data, assignment of the parameter is absolutely destructive.

## Rule Details

This rule disallows reassigning exceptions in `catch` clauses.

Examples of incorrect code for this rule:


```json
/*eslint no-ex-assign: "error"*/

try {
    // code
} catch (e) {
    e = 10;
}
```

Examples of correct code for this rule:


```json
/*eslint no-ex-assign: "error"*/

try {
    // code
} catch (e) {
    var foo = 10;
}
```


## Version

This rule was introduced in ESLint v0.0.9.

## Further Reading

The 
 bocoup.com

## Resources


- Rule source 

- Tests source 

