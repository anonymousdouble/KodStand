
# no-extra-bind
## Overview
Disallow unnecessary calls to `.bind()`


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


The `bind()` method is used to create functions with specific `this` values and, optionally, binds arguments to specific values. When used to specify the value of `this`, it’s important that the function actually uses `this` in its function body. For example:

```json
var boundGetName = (function getName() {
    return this.name;
}).bind({ name: "ESLint" });

console.log(boundGetName());      // "ESLint"
```
This code is an example of a good use of `bind()` for setting the value of `this`.
Sometimes during the course of code maintenance, the `this` value is removed from the function body. In that case, you can end up with a call to `bind()` that doesn’t accomplish anything:

```json
// useless bind
var boundGetName = (function getName() {
    return "ESLint";
}).bind({ name: "ESLint" });

console.log(boundGetName());      // "ESLint"
```
In this code, the reference to `this` has been removed but `bind()` is still used. In this case, the `bind()` is unnecessary overhead (and a performance hit) and can be safely removed.
## Rule Details
This rule is aimed at avoiding the unnecessary use of `bind()` and as such will warn whenever an immediately-invoked function expression (IIFE) is using `bind()` and doesn’t have an appropriate `this` value. This rule won’t flag usage of `bind()` that includes function argument binding.
Note: Arrow functions can never have their `this` value set using `bind()`. This rule flags all uses of `bind()` with arrow functions as a problem
Examples of incorrect code for this rule:


```json
/*eslint no-extra-bind: "error"*/
/*eslint-env es6*/

var x = function () {
    foo();
}.bind(bar);

var x = (() => {
    foo();
}).bind(bar);

var x = (() => {
    this.foo();
}).bind(bar);

var x = function () {
    (function () {
      this.foo();
    }());
}.bind(bar);

var x = function () {
    function foo() {
      this.bar();
    }
}.bind(baz);
```
Examples of correct code for this rule:


```json
/*eslint no-extra-bind: "error"*/

var x = function () {
    this.foo();
}.bind(bar);

var x = function (a) {
    return a + 1;
}.bind(foo, bar);
```
## When Not To Use It
If you are not concerned about unnecessary calls to `bind()`, you can safely disable this rule.
## Version
This rule was introduced in ESLint v0.8.0.
## Further Reading





Function.prototype.bind() - JavaScript | MDN 
 developer.mozilla.org










Understanding JavaScript Bind () — Smashing Magazine 
 www.smashingmagazine.com





## Resources

Rule source 
Tests source 
