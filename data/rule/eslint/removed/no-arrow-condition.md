
# no-arrow-condition
## Overview

Disallows arrow functions where test conditions are expected.
Arrow functions (`=>`) are similar in syntax to some comparison operators (`>`, `<`, `<=`, and `>=`). This rule warns against using the arrow function syntax in places where a condition is expected. Even if the arguments of the arrow function are wrapped with parens, this rule still warns about it.
Here’s an example where the usage of `=>` is most likely a typo:

```json
// This is probably a typo
if (a => 1) {}
// And should instead be
if (a >= 1) {}
```
There are also cases where the usage of `=>` can be ambiguous and should be rewritten to more clearly show the author’s intent:

```json
// The intent is not clear
var x = a => 1 ? 2 : 3
// Did the author mean this
var x = function (a) { return a >= 1 ? 2 : 3 }
// Or this
var x = a <= 1 ? 2 : 3
```
## Rule Details
Examples of incorrect code for this rule:

```json
/*eslint no-arrow-condition: "error"*/
/*eslint-env es6*/

if (a => 1) {}
while (a => 1) {}
for (var a = 1; a => 10; a++) {}
a => 1 ? 2 : 3
(a => 1) ? 2 : 3
var x = a => 1 ? 2 : 3
var x = (a) => 1 ? 2 : 3
```

## Related Rules


arrow-parens 

no-confusing-arrow 

no-constant-condition 


## Version
This rule was introduced in ESLint v1.8.0
                 and removed in v2.0.0-beta.3.

## Replaced by
no-confusing-arrow
no-constant-condition