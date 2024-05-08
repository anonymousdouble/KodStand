

# no-eq-null
## Overview

Disallow `null` comparisons without type-checking operators

Comparing to `null` without a type-checking operator (`==` or `!=`), can have unintended results as the comparison will evaluate to true when comparing to not just a `null`, but also an `undefined` value.


```json
if (foo == null) {
  bar();
}
```

## Rule Details

The `no-eq-null` rule aims reduce potential bug and unwanted behavior by ensuring that comparisons to `null` only match `null`, and not also `undefined`. As such it will flag comparisons to null when using `==` and `!=`.

Examples of incorrect code for this rule:


```json
/*eslint no-eq-null: "error"*/

if (foo == null) {
  bar();
}

while (qux != null) {
  baz();
}
```

Examples of correct code for this rule:


```json
/*eslint no-eq-null: "error"*/

if (foo === null) {
  bar();
}

while (qux !== null) {
  baz();
}
```

## When Not To Use It

If you want to enforce type-checking operations in general, use the more powerful eqeqeq  instead.

## Compatibility


- JSHint: This rule corresponds to `eqnull` rule of JSHint.

## Version

This rule was introduced in ESLint v0.0.9.

## Resources


- Rule source 

- Tests source 

