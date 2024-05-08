

# no-wrap-func
## Overview

Disallows unnecessary parentheses around function expressions.

Although it’s possible to wrap functions in parentheses, this can be confusing when the code also contains immediately-invoked function expressions (IIFEs) since parentheses are often used to make this distinction. For example:


```json
var foo = (function() {
    // IIFE
}());

var bar = (function() {
    // not an IIFE
});
```

## Rule Details

This rule will raise a warning when it encounters a function expression wrapped in parentheses with no following invoking parentheses.

Example of incorrect code for this rule:


```json
var a = (function() {/*...*/});
```

Examples of correct code for this rule:


```json
var a = function() {/*...*/};

(function() {/*...*/})();
```


## Version

This rule was introduced in ESLint v0.0.9
                 and removed in v1.0.0-rc-1.


## Replaced by
no-extra-paren