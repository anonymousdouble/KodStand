
# lines-around-directive
## Overview
Require or disallow newlines around directives


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


This rule was deprecated in ESLint v4.0.0 and replaced by the padding-line-between-statements  rule.
Directives are used in JavaScript to indicate to the execution environment that a script would like to opt into a feature such as `"strict mode"`. Directives are grouped together in a directive prologue  at the top of either a file or function block and are applied to the scope in which they occur.

```json
// Strict mode is invoked for the entire script
"use strict";

var foo;

function bar() {
  var baz;
}
```

```json
var foo;

function bar() {
  // Strict mode is only invoked within this function
  "use strict";

  var baz;
}
```
## Rule Details
This rule requires or disallows blank newlines around directive prologues. This rule does not enforce any conventions about blank newlines between the individual directives. In addition, it does not require blank newlines before directive prologues unless they are preceded by a comment. Please use the padded-blocks  rule if this is a style you would like to enforce.
## Options
This rule has one option. It can either be a string or an object:

`"always"` (default) enforces blank newlines around directives.
`"never"` disallows blank newlines around directives.

or

```json
{
  "before": "always" or "never"
  "after": "always" or "never",
}
```
### always
This is the default option.
Examples of incorrect code for this rule with the `"always"` option:


```json
/* eslint lines-around-directive: ["error", "always"] */

// comment
"use strict";
var foo;

function foo() {
  "use strict";
  "use asm";
  var bar;
}

function foo() {
  // comment
  "use strict";
  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", "always"] */

// comment
"use strict";
"use asm";
var foo;
```
Examples of correct code for this rule with the `"always"` option:


```json
/* eslint lines-around-directive: ["error", "always"] */

// comment

"use strict";

var foo;

function foo() {
  "use strict";
  "use asm";

  var bar;
}

function foo() {
  // comment

  "use strict";

  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", "always"] */

// comment

"use strict";
"use asm";

var foo;
```
### never
Examples of incorrect code for this rule with the `"never"` option:


```json
/* eslint lines-around-directive: ["error", "never"] */

// comment

"use strict";

var foo;

function foo() {
  "use strict";
  "use asm";

  var bar;
}

function foo() {
  // comment

  "use strict";

  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", "never"] */

// comment

"use strict";
"use asm";

var foo;
```
Examples of correct code for this rule with the `"never"` option:


```json
/* eslint lines-around-directive: ["error", "never"] */

// comment
"use strict";
var foo;

function foo() {
  "use strict";
  "use asm";
  var bar;
}

function foo() {
  // comment
  "use strict";
  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", "never"] */

// comment
"use strict";
"use asm";
var foo;
```
### before & after
Examples of incorrect code for this rule with the `{ "before": "never", "after": "always" }` option:


```json
/* eslint lines-around-directive: ["error", { "before": "never", "after": "always" }] */

// comment

"use strict";
var foo;

function foo() {
  "use strict";
  "use asm";
  var bar;
}

function foo() {
  // comment

  "use strict";
  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", { "before": "never", "after": "always" }] */

// comment

"use strict";
"use asm";
var foo;
```
Examples of correct code for this rule with the `{ "before": "never", "after": "always" }`  option:


```json
/* eslint lines-around-directive: ["error", { "before": "never", "after": "always" }] */

// comment
"use strict";

var foo;

function foo() {
  "use strict";
  "use asm";

  var bar;
}

function foo() {
  // comment
  "use strict";

  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", { "before": "never", "after": "always" }] */

// comment
"use strict";
"use asm";

var foo;
```
Examples of incorrect code for this rule with the `{ "before": "always", "after": "never" }` option:


```json
/* eslint lines-around-directive: ["error", { "before": "always", "after": "never" }] */

// comment
"use strict";

var foo;

function foo() {
  "use strict";
  "use asm";

  var bar;
}

function foo() {
  // comment
  "use strict";

  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", { "before": "always", "after": "never" }] */

// comment
"use strict";
"use asm";

var foo;
```
Examples of correct code for this rule with the `{ "before": "always", "after": "never" }` option:


```json
/* eslint lines-around-directive: ["error", { "before": "always", "after": "never" }] */

// comment

"use strict";
var foo;

function foo() {
  "use strict";
  "use asm";
  var bar;
}

function foo() {
  // comment

  "use strict";
  var bar;
}
```


```json
/* eslint lines-around-directive: ["error", { "before": "always", "after": "never" }] */

// comment

"use strict";
"use asm";
var foo;
```
## When Not To Use It
You can safely disable this rule if you do not have any strict conventions about whether or not directive prologues should have blank newlines before or after them.
## Compatibility

JSCS: requirePaddingNewLinesAfterUseStrict 
JSCS: disallowPaddingNewLinesAfterUseStrict 

## Related Rules


lines-around-comment 

padded-blocks 


## Version
This rule was introduced in ESLint v3.5.0.
## Resources

Rule source 
Tests source 

