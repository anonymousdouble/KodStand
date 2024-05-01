
# no-underscore-dangle
## Overview
Disallow dangling underscores in identifiers



As far as naming conventions for identifiers go, dangling underscores may be the most polarizing in JavaScript. Dangling underscores are underscores at either the beginning or end of an identifier, such as:

```json
var _foo;
```
There is a long history of marking “private” members with dangling underscores in JavaScript, beginning with SpiderMonkey adding nonstandard methods such as `__defineGetter__()`. Since that time, using a single underscore prefix has become the most popular convention for indicating a member is not part of the public interface of an object.
It is recommended to use the formal private class features  introduced in ECMAScript 2022 for encapsulating private data and methods rather than relying on naming conventions.
Allowing dangling underscores in identifiers is purely a convention and has no effect on performance, readability, or complexity. They do not have the same encapsulation benefits as private class features, even with this rule enabled.
## Rule Details
This rule disallows dangling underscores in identifiers.
Examples of incorrect code for this rule:


```json
/*eslint no-underscore-dangle: "error"*/

var foo_;
var __proto__ = {};
foo._bar();
```
Examples of correct code for this rule:


```json
/*eslint no-underscore-dangle: "error"*/

var _ = require('underscore');
var obj = _.contains(items, item);
obj.__proto__ = {};
var file = __filename;
function foo(_bar) {};
const bar = { onClick(_bar) {} };
const baz = (_bar) => {};
```
## Options
This rule has an object option:

`"allow"` allows specified identifiers to have dangling underscores
`"allowAfterThis": false` (default) disallows dangling underscores in members of the `this` object
`"allowAfterSuper": false` (default) disallows dangling underscores in members of the `super` object
`"allowAfterThisConstructor": false` (default) disallows dangling underscores in members of the `this.constructor` object
`"enforceInMethodNames": false` (default) allows dangling underscores in method names
`"enforceInClassFields": false` (default) allows dangling underscores in es2022 class fields names
`"allowInArrayDestructuring": true` (default) allows dangling underscores in variable names assigned by array destructuring
`"allowInObjectDestructuring": true` (default) allows dangling underscores in variable names assigned by object destructuring
`"allowFunctionParams": true` (default) allows dangling underscores in function parameter names

### allow
Examples of additional correct code for this rule with the `{ "allow": ["foo_", "_bar"] }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allow": ["foo_", "_bar"] }]*/

var foo_;
foo._bar();
```
### allowAfterThis
Examples of correct code for this rule with the `{ "allowAfterThis": true }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allowAfterThis": true }]*/

var a = this.foo_;
this._bar();
```
### allowAfterSuper
Examples of correct code for this rule with the `{ "allowAfterSuper": true }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allowAfterSuper": true }]*/

class Foo extends Bar {
  doSomething() {
    var a = super.foo_;
    super._bar();
  }
}
```
### allowAfterThisConstructor
Examples of correct code for this rule with the `{ "allowAfterThisConstructor": true }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allowAfterThisConstructor": true }]*/

var a = this.constructor.foo_;
this.constructor._bar();
```
### enforceInMethodNames
Examples of incorrect code for this rule with the `{ "enforceInMethodNames": true }` option:


```json
/*eslint no-underscore-dangle: ["error", { "enforceInMethodNames": true }]*/

class Foo {
  _bar() {}
}

class Bar {
  bar_() {}
}

const o1 = {
  _bar() {}
};

const o2 = {
  bar_() {}
};
```
### enforceInClassFields
Examples of incorrect code for this rule with the `{ "enforceInClassFields": true }` option:


```json
/*eslint no-underscore-dangle: ["error", { "enforceInClassFields": true }]*/

class Foo {
    _bar;
}

class Bar {
    _bar = () => {};
}

class Baz {
    bar_;
}

class Qux {
    #_bar;
}

class FooBar {
    #bar_;
}
```
### allowInArrayDestructuring
Examples of incorrect code for this rule with the `{ "allowInArrayDestructuring": false }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allowInArrayDestructuring": false }]*/

const [_foo, _bar] = list;
const [foo_, ..._qux] = list;
const [foo, [bar, _baz]] = list;
```
### allowInObjectDestructuring
Examples of incorrect code for this rule with the `{ "allowInObjectDestructuring": false }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allowInObjectDestructuring": false }]*/

const { foo, bar: _bar } = collection;
const { qux, xyz, _baz } = collection;
```
Examples of correct code for this rule with the `{ "allowInObjectDestructuring": false }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allowInObjectDestructuring": false }]*/

const { foo, bar, _baz: { a, b } } = collection;
const { qux, xyz, _baz: baz } = collection;
```
### allowFunctionParams
Examples of incorrect code for this rule with the `{ "allowFunctionParams": false }` option:


```json
/*eslint no-underscore-dangle: ["error", { "allowFunctionParams": false }]*/

function foo1 (_bar) {}
function foo2 (_bar = 0) {}
function foo3 (..._bar) {}

const foo4 = function onClick (_bar) {}
const foo5 = function onClick (_bar = 0) {}
const foo6 = function onClick (..._bar) {}

const foo7 = (_bar) => {};
const foo8 = (_bar = 0) => {};
const foo9 = (..._bar) => {};
```
## When Not To Use It
If you want to allow dangling underscores in identifiers, then you can safely turn this rule off.
## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 

