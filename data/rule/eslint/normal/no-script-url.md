

# no-script-url
## Overview

Disallow `javascript:` urls

Using `javascript:` URLs is considered by some as a form of `eval`. Code passed in `javascript:` URLs has to be parsed and evaluated by the browser in the same way that `eval` is processed.

## Rule Details

Examples of incorrect code for this rule:


```json
/*eslint no-script-url: "error"*/

location.href = "javascript:void(0)";

location.href = `javascript:void(0)`;
```

## Compatibility


- JSHint: This rule corresponds to `scripturl` rule of JSHint.

## Version

This rule was introduced in ESLint v0.0.9.

## Further Reading

What is the matter with script-targeted URLs? 
 stackoverflow.com

## Resources


- Rule source 

- Tests source 

