
# no-empty-label
## Overview

Disallows labels for anything other than loops and switches.
Labeled statements are only used in conjunction with labeled break and continue statements. ECMAScript has no goto statement.
## Rule Details
This error occurs when a label is used to mark a statement that is not an iteration or switch
Example of incorrect code for this rule:

```json
/*eslint no-empty-label: "error"*/

labeled:
var x = 10;
```
Example of correct code for this rule:

```json
/*eslint no-empty-label: "error"*/

labeled:
for (var i=10; i; i--) {
    // ...
}
```
## When Not To Use It
If you don’t want to be notified about usage of labels, then it’s safe to disable this rule.
## Related Rules


no-labels 

no-label-var 

no-unused-labels 


## Version
This rule was introduced in ESLint v0.0.9
                 and removed in v2.0.0-rc.0.

## Replaced by
no-labels