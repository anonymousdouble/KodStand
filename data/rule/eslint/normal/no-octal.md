
# no-octal
## Overview
Disallow octal literals


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


Octal literals are numerals that begin with a leading zero, such as:

```json
var num = 071;      // 57
```
Because the leading zero which identifies an octal literal has been a source of confusion and error in JavaScript code, ECMAScript 5 deprecates the use of octal numeric literals.
## Rule Details
The rule disallows octal literals.
If ESLint parses code in strict mode, the parser (instead of this rule) reports the error.
Examples of incorrect code for this rule:


```json
/*eslint no-octal: "error"*/

var num = 071;
var result = 5 + 07;
```
Examples of correct code for this rule:


```json
/*eslint no-octal: "error"*/

var num  = "071";
```
## Compatibility

JSHint: W115

## Version
This rule was introduced in ESLint v0.0.6.
## Resources

Rule source 
Tests source 

