
# space-after-keywords
## Overview

Enforces consistent spacing after keywords.
Some style guides will require or disallow spaces following the certain keywords.

```json
if (condition) {
    doSomething();
} else {
    doSomethingElse();
}

if(condition) {
    doSomething();
}else{
    doSomethingElse();
}
```
## Rule Details
This rule will enforce consistency of spacing after the keywords `if`, `else`, `for`, `while`, `do`, `switch`, `try`, `catch`, `finally`, and `with`.
This rule takes one argument. If it is `"always"` then the keywords must be followed by at least one space. If `"never"`
then there should be no spaces following. The default is `"always"`.
Examples of incorrect code for this rule:

```json
/*eslint space-after-keywords: "error"*/

if(a) {}

if (a) {} else{}

do{} while (a);
```

```json
/*eslint space-after-keywords: ["error", "never"]*/

if (a) {}
```
Examples of correct code for this rule:

```json
/*eslint space-after-keywords: "error"*/

if (a) {}

if (a) {} else {}
```

```json
/*eslint space-after-keywords: ["error", "never"]*/

if(a) {}
```

## Version
This rule was introduced in ESLint v0.6.0
                 and removed in v2.0.0-beta.3.

## Replaced by
keyword-spacing