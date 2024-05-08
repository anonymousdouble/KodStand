

# yield-star-spacing
## Overview

Require or disallow spacing around the `*` in `yield*` expressions

This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .

## Rule Details

This rule enforces spacing around the `*` in `yield*` expressions.

## Options

The rule takes one option, an object, which has two keys `before` and `after` having boolean values `true` or `false`.


- 
`before` enforces spacing between the `yield` and the `*`.
If `true`, a space is required, otherwise spaces are disallowed.


- 
`after` enforces spacing between the `*` and the argument.
If it is `true`, a space is required, otherwise spaces are disallowed.

The default is `{"before": false, "after": true}`.


```json
"yield-star-spacing": ["error", {"before": true, "after": false}]
```

The option also has a string shorthand:


- `{"before": false, "after": true}` → `"after"`

- `{"before": true, "after": false}` → `"before"`

- `{"before": true, "after": true}` → `"both"`

- `{"before": false, "after": false}` → `"neither"`


```json
"yield-star-spacing": ["error", "after"]
```

## Examples

### after

Examples of correct code for this rule with the default `"after"` option:


```json
/*eslint yield-star-spacing: ["error", "after"]*/
/*eslint-env es6*/

function* generator() {
  yield* other();
}
```

### before

Examples of correct code for this rule with the `"before"` option:


```json
/*eslint yield-star-spacing: ["error", "before"]*/
/*eslint-env es6*/

function *generator() {
  yield *other();
}
```

### both

Examples of correct code for this rule with the `"both"` option:


```json
/*eslint yield-star-spacing: ["error", "both"]*/
/*eslint-env es6*/

function * generator() {
  yield * other();
}
```

### neither

Examples of correct code for this rule with the `"neither"` option:


```json
/*eslint yield-star-spacing: ["error", "neither"]*/
/*eslint-env es6*/

function*generator() {
  yield*other();
}
```

## When Not To Use It

If your project will not be using generators or you are not concerned with spacing consistency, you do not need this rule.

## Version

This rule was introduced in ESLint v2.0.0-alpha-1.

## Further Reading

Read Understanding ECMAScript 6 | Leanpub 
 leanpub.com

## Resources


- Rule source 

- Tests source 

