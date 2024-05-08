

# no-undef
## Overview

Disallow the use of undeclared variables unless mentioned in `/*global */` comments

This rule can help you locate potential ReferenceErrors resulting from misspellings of variable and parameter names, or accidental implicit globals (for example, from forgetting the `var` keyword in a `for` loop initializer).

## Rule Details

Any reference to an undeclared variable causes a warning, unless the variable is explicitly mentioned in a `/*global ...*/` comment, or specified in the globals key in the configuration file . A common use case for these is if you intentionally use globals that are defined elsewhere (e.g. in a script sourced from HTML).

Examples of incorrect code for this rule:


```json
/*eslint no-undef: "error"*/

var foo = someFunction();
var bar = a + 1;
```

Examples of correct code for this rule with `global` declaration:


```json
/*global someFunction, a*/
/*eslint no-undef: "error"*/

var foo = someFunction();
var bar = a + 1;
```

Note that this rule does not disallow assignments to read-only global variables.
See no-global-assign  if you also want to disallow those assignments.

This rule also does not disallow redeclarations of global variables.
See no-redeclare  if you also want to disallow those redeclarations.

## Options


- `typeof` set to true will warn for variables used inside typeof check (Default false).

### typeof

Examples of correct code for the default `{ "typeof": false }` option:


```json
/*eslint no-undef: "error"*/

if (typeof UndefinedIdentifier === "undefined") {
    // do something ...
}
```

You can use this option if you want to prevent `typeof` check on a variable which has not been declared.

Examples of incorrect code for the `{ "typeof": true }` option:


```json
/*eslint no-undef: ["error", { "typeof": true }] */

if(typeof a === "string"){}
```

Examples of correct code for the `{ "typeof": true }` option with `global` declaration:


```json
/*global a*/
/*eslint no-undef: ["error", { "typeof": true }] */

if(typeof a === "string"){}
```

## Environments

For convenience, ESLint provides shortcuts that pre-define global variables exposed by popular libraries and runtime environments. This rule supports these environments, as listed in Specifying Environments .  A few examples are given below.

### browser

Examples of correct code for this rule with `browser` environment:


```json
/*eslint no-undef: "error"*/
/*eslint-env browser*/

setTimeout(function() {
    alert("Hello");
});
```

### Node.js

Examples of correct code for this rule with `node` environment:


```json
/*eslint no-undef: "error"*/
/*eslint-env node*/

var fs = require("fs");
module.exports = function() {
    console.log(fs);
};
```

## When Not To Use It

If explicit declaration of global variables is not to your taste.

## Compatibility

This rule provides compatibility with treatment of global variables in JSHint  and JSLint .

## Handled by TypeScript


                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            

## Related Rules


- 
no-global-assign 

- 
no-redeclare 

## Version

This rule was introduced in ESLint v0.0.9.

## Resources


- Rule source 

- Tests source 

