
# prefer-object-has-own
## Overview
Disallow use of `Object.prototype.hasOwnProperty.call()` and prefer use of `Object.hasOwn()`


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


It is very common to write code like:

```json
if (Object.prototype.hasOwnProperty.call(object, "foo")) {
  console.log("has property foo");
}
```
This is a common practice because methods on `Object.prototype` can sometimes be unavailable or redefined (see the no-prototype-builtins  rule).
Introduced in ES2022, `Object.hasOwn()` is a shorter alternative to `Object.prototype.hasOwnProperty.call()`:

```json
if (Object.hasOwn(object, "foo")) {
  console.log("has property foo")
}
```
## Rule Details
Examples of incorrect code for this rule:


```json
/*eslint prefer-object-has-own: "error"*/

Object.prototype.hasOwnProperty.call(obj, "a");

Object.hasOwnProperty.call(obj, "a");

({}).hasOwnProperty.call(obj, "a");

const hasProperty = Object.prototype.hasOwnProperty.call(object, property);
```
Examples of correct code for this rule:


```json
/*eslint prefer-object-has-own: "error"*/

Object.hasOwn(obj, "a");

const hasProperty = Object.hasOwn(object, property);
```
## When Not To Use It
This rule should not be used unless ES2022 is supported in your codebase.
## Version
This rule was introduced in ESLint v8.5.0.
## Further Reading





Object.hasOwn() - JavaScript | MDN 
 developer.mozilla.org





## Resources

Rule source 
Tests source 

