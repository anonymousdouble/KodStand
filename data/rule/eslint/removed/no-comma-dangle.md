

# no-comma-dangle
## Overview

Disallows trailing commas in object and array literals.

Trailing commas in object literals are valid according to the ECMAScript 5 (and ECMAScript 3!) spec, however IE8 (when not in IE8 document mode) and below will throw an error when it encounters trailing commas in JavaScript.


```json
var foo = {
    bar: "baz",
    qux: "quux",
};
```

## Rule Details

This rule is aimed at detecting trailing commas in object literals. As such, it will warn whenever it encounters a trailing comma in an object literal.

Examples of incorrect code for this rule:


```json
var foo = {
    bar: "baz",
    qux: "quux",
};

var arr = [1,2,];

foo({
  bar: "baz",
  qux: "quux",
});
```

Examples of correct code for this rule:


```json
var foo = {
    bar: "baz",
    qux: "quux"
};

var arr = [1,2];

foo({
  bar: "baz",
  qux: "quux"
});
```

## When Not To Use It

If your code will not be run in IE8 or below (a Node.js application, for example) and you’d prefer to allow trailing commas, turn this rule off.

## Version

This rule was introduced in ESLint v0.0.9
                 and removed in v1.0.0-rc-1.


## Replaced by
comma-dangle