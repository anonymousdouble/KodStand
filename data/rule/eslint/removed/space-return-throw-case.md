
# space-return-throw-case
## Overview

Requires spaces after `return`, `throw`, and `case` keywords.
(fixable) The `--fix` option on the command line  automatically fixed problems reported by this rule.
Require spaces following `return`, `throw`, and `case`.
## Rule Details
Examples of incorrect code for this rule:

```json
/*eslint space-return-throw-case: "error"*/

throw{a:0}

function f(){ return-a; }

switch(a){ case'a': break; }
```
Examples of correct code for this rule:

```json
/*eslint space-return-throw-case: "error"*/

throw {a: 0};

function f(){ return -a; }

switch(a){ case 'a': break; }
```

## Version
This rule was introduced in ESLint v0.1.4
                 and removed in v2.0.0-beta.3.

## Replaced by
keyword-spacing