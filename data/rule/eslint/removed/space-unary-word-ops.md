

# space-unary-word-ops
## Overview

Requires spaces after unary word operators.

## Rule Details

Examples of incorrect code for this rule:


```json
typeof!a
```


```json
void{a:0}
```


```json
new[a][0]
```


```json
delete(a.b)
```

Examples of correct code for this rule:


```json
delete a.b
```


```json
new C
```


```json
void 0
```


## Version

This rule was introduced in ESLint v0.1.4
                 and removed in v0.10.0.


## Replaced by
space-unary-ops