

# generator-star
## Overview

Enforces consistent spacing around the asterisk in generator functions.

Generators are a new type of function in ECMAScript 6 that can return multiple values over time.
These special functions are indicated by placing an `*` after the `function` keyword.

Here is an example of a generator function:


```json
/*eslint-env es6*/

function* generator() {
    yield "44";
    yield "55";
}
```

This is also valid:


```json
/*eslint-env es6*/

function *generator() {
    yield "44";
    yield "55";
}
```

This is valid as well:


```json
/*eslint-env es6*/

function * generator() {
    yield "44";
    yield "55";
}
```

To keep a sense of consistency when using generators this rule enforces a single position for the `*`.

## Rule Details

This rule enforces that the `*` is either placed next to the `function` keyword or the name of the function. The single
option for this rule is a string specifying the placement of the asterisk. For this option you may pass
`"start"`, `"middle"` or `"end"`. The default is `"end"`.

You can set the style in configuration like this:


```json
"generator-star": ["error", "start"]
```

When using `"start"` this placement will be enforced:


```json
/*eslint-env es6*/

function* generator() {
}
```

When using `"middle"` this placement will be enforced:


```json
/*eslint-env es6*/

function * generator() {
}
```

When using `"end"` this placement will be enforced:


```json
/*eslint-env es6*/

function *generator() {
}
```

When using the expression syntax `"start"` will be enforced here:


```json
/*eslint-env es6*/

var generator = function* () {
}
```

When using the expression syntax `"middle"` will be enforced here:


```json
/*eslint-env es6*/

var generator = function * () {
}
```

When using the expression syntax `"end"` will be enforced here:


```json
/*eslint-env es6*/

var generator = function *() {
}
```

When using the expression syntax this is valid for both `"start"` and `"end"`:


```json
/*eslint-env es6*/

var generator = function*() {
}
```

The shortened object literal syntax for generators is not affected by this rule.

## When Not To Use It

If your project will not be using generators you do not need this rule.

## Version

This rule was introduced in ESLint v0.12.0
                 and removed in v1.0.0-rc-1.

## Further Reading

Read Understanding ECMAScript 6 | Leanpub 
 leanpub.com


## Replaced by
generator-star-spacing