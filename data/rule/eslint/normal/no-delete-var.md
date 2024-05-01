
# no-delete-var
## Overview
Disallow deleting variables


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


The purpose of the `delete` operator is to remove a property from an object. Using the `delete` operator on a variable might lead to unexpected behavior.
## Rule Details
This rule disallows the use of the `delete` operator on variables.
If ESLint parses code in strict mode, the parser (instead of this rule) reports the error.
Examples of incorrect code for this rule:


```json
/*eslint no-delete-var: "error"*/

var x;
delete x;
```

## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 

