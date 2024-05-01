
# no-empty-class
## Overview

Disallows empty character classes in regular expressions.
Empty character classes in regular expressions do not match anything and can result in code that may not work as intended.

```json
var foo = /^abc[]/;
```
## Rule Details
This rule is aimed at highlighting possible typos and unexpected behavior in regular expressions which may arise from the use of empty character classes.
Examples of incorrect code for this rule:

```json
var foo = /^abc[]/;

/^abc[]/.test(foo);

bar.match(/^abc[]/);
```
Examples of correct code for this rule:

```json
var foo = /^abc/;

var foo = /^abc[a-z]/;

var bar = new RegExp("^abc[]");
```

## Version
This rule was introduced in ESLint v0.0.9
                 and removed in v1.0.0-rc-1.

## Replaced by
no-empty-character-class