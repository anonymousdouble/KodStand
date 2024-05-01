
# no-empty-pattern
## Overview
Disallow empty destructuring patterns


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


When using destructuring, it’s possible to create a pattern that has no effect. This happens when empty curly braces are used to the right of an embedded object destructuring pattern, such as:

```json
// doesn't create any variables
var {a: {}} = foo;
```
In this code, no new variables are created because `a` is just a location helper while the `{}` is expected to contain the variables to create, such as:

```json
// creates variable b
var {a: { b }} = foo;
```
In many cases, the empty object pattern is a mistake where the author intended to use a default value instead, such as:

```json
// creates variable a
var {a = {}} = foo;
```
The difference between these two patterns is subtle, especially because the problematic empty pattern looks just like an object literal.
## Rule Details
This rule aims to flag any empty patterns in destructured objects and arrays, and as such, will report a problem whenever one is encountered.
Examples of incorrect code for this rule:


```json
/*eslint no-empty-pattern: "error"*/

var {} = foo;
var [] = foo;
var {a: {}} = foo;
var {a: []} = foo;
function foo({}) {}
function bar([]) {}
function baz({a: {}}) {}
function qux({a: []}) {}
```
Examples of correct code for this rule:


```json
/*eslint no-empty-pattern: "error"*/

var {a = {}} = foo;
var {a = []} = foo;
function foo({a = {}}) {}
function bar({a = []}) {}
```
## Options
This rule has an object option for exceptions:
### allowObjectPatternsAsParameters
Set to `false` by default. Setting this option to `true` allows empty object patterns as function parameters.
Note: This rule doesn’t allow empty array patterns as function parameters.
Examples of incorrect code for this rule with the `{"allowObjectPatternsAsParameters": true}` option:


```json
/*eslint no-empty-pattern: ["error", { "allowObjectPatternsAsParameters": true }]*/

function foo({a: {}}) {}
var bar = function({a: {}}) {};
var bar = ({a: {}}) => {};
var bar = ({} = bar) => {};
var bar = ({} = { bar: 1 }) => {};

function baz([]) {}
```
Examples of correct code for this rule with the `{"allowObjectPatternsAsParameters": true}` option:


```json
/*eslint no-empty-pattern: ["error", { "allowObjectPatternsAsParameters": true }]*/

function foo({}) {}
var bar = function({}) {};
var bar = ({}) => {};

function baz({} = {}) {}
```

## Version
This rule was introduced in ESLint v1.7.0.
## Resources

Rule source 
Tests source 

