
# no-plusplus
## Overview
Disallow the unary operators `++` and `--`



Because the unary `++` and `--` operators are subject to automatic semicolon insertion, differences in whitespace can change semantics of source code.

```json
var i = 10;
var j = 20;

i ++
j
// i = 11, j = 20
```

```json
var i = 10;
var j = 20;

i
++
j
// i = 10, j = 21
```
## Rule Details
This rule disallows the unary operators `++` and `--`.
Examples of incorrect code for this rule:


```json
/*eslint no-plusplus: "error"*/

var foo = 0;
foo++;

var bar = 42;
bar--;

for (i = 0; i < l; i++) {
    doSomething(i);
}
```
Examples of correct code for this rule:


```json
/*eslint no-plusplus: "error"*/

var foo = 0;
foo += 1;

var bar = 42;
bar -= 1;

for (i = 0; i < l; i += 1) {
    doSomething(i);
}
```
## Options
This rule has an object option.

`"allowForLoopAfterthoughts": true` allows unary operators `++` and `--` in the afterthought (final expression) of a `for` loop.

### allowForLoopAfterthoughts
Examples of correct code for this rule with the `{ "allowForLoopAfterthoughts": true }` option:


```json
/*eslint no-plusplus: ["error", { "allowForLoopAfterthoughts": true }]*/

for (i = 0; i < l; i++) {
    doSomething(i);
}

for (i = l; i >= 0; i--) {
    doSomething(i);
}

for (i = 0, j = l; i < l; i++, j--) {
    doSomething(i, j);
}
```
Examples of incorrect code for this rule with the `{ "allowForLoopAfterthoughts": true }` option:


```json
/*eslint no-plusplus: ["error", { "allowForLoopAfterthoughts": true }]*/

for (i = 0; i < l; j = i++) {
    doSomething(i, j);
}

for (i = l; i--;) {
    doSomething(i);
}

for (i = 0; i < l;) i++;
```

## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 
