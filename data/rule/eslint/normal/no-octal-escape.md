
# no-octal-escape
## Overview
Disallow octal escape sequences in string literals



As of the ECMAScript 5 specification, octal escape sequences in string literals are deprecated and should not be used. Unicode escape sequences should be used instead.

```json
var foo = "Copyright \251";
```
## Rule Details
This rule disallows octal escape sequences in string literals.
If ESLint parses code in strict mode, the parser (instead of this rule) reports the error.
Examples of incorrect code for this rule:


```json
/*eslint no-octal-escape: "error"*/

var foo = "Copyright \251";
```
Examples of correct code for this rule:


```json
/*eslint no-octal-escape: "error"*/

var foo = "Copyright \u00A9";   // unicode

var foo = "Copyright \xA9";     // hexadecimal
```

## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 

