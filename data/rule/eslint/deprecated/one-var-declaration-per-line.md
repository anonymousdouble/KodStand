

# one-var-declaration-per-line
## Overview

Require or disallow newlines around variable declarations

This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .

Some developers declare multiple var statements on the same line:


```json
var foo, bar, baz;
```

Others prefer to declare one var per line.


```json
var foo,
    bar,
    baz;
```

Keeping to one of these styles across a project’s codebase can help with maintaining code consistency.

## Rule Details

This rule enforces a consistent newlines around variable declarations. This rule ignores variable declarations inside `for` loop conditionals.

## Options

This rule has a single string option:


- `"initializations"` (default) enforces a newline around variable initializations

- `"always"` enforces a newline around variable declarations

### initializations

Examples of incorrect code for this rule with the default `"initializations"` option:


```json
/*eslint one-var-declaration-per-line: ["error", "initializations"]*/
/*eslint-env es6*/

var a, b, c = 0;

let d,
    e = 0, f;
```

Examples of correct code for this rule with the default `"initializations"` option:


```json
/*eslint one-var-declaration-per-line: ["error", "initializations"]*/
/*eslint-env es6*/

var a, b;

let c,
    d;

let e,
    f = 0;
```

### always

Examples of incorrect code for this rule with the `"always"` option:


```json
/*eslint one-var-declaration-per-line: ["error", "always"]*/
/*eslint-env es6*/

var a, b;

let c, d = 0;

const e = 0, f = 0;
```

Examples of correct code for this rule with the `"always"` option:


```json
/*eslint one-var-declaration-per-line: ["error", "always"]*/
/*eslint-env es6*/

var a,
    b;

let c,
    d = 0;
```


## Related Rules


- 
one-var 

## Version

This rule was introduced in ESLint v2.0.0-beta.3.

## Resources


- Rule source 

- Tests source 

