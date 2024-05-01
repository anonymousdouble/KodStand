
# no-iterator
## Overview
Disallow the use of the `__iterator__` property



The `__iterator__` property was a SpiderMonkey extension to JavaScript that could be used to create custom iterators that are compatible with JavaScript’s `for in` and `for each` constructs. However, this property is now obsolete, so it should not be used. Here’s an example of how this used to work:

```json
Foo.prototype.__iterator__ = function() {
    return new FooIterator(this);
}
```
You should use ECMAScript 6 iterators and generators instead.
## Rule Details
This rule is aimed at preventing errors that may arise from using the `__iterator__` property, which is not implemented in several browsers. As such, it will warn whenever it encounters the `__iterator__` property.
Examples of incorrect code for this rule:


```json
/*eslint no-iterator: "error"*/

Foo.prototype.__iterator__ = function() {
    return new FooIterator(this);
};

foo.__iterator__ = function () {};

foo["__iterator__"] = function () {};

```
Examples of correct code for this rule:


```json
/*eslint no-iterator: "error"*/

var __iterator__ = foo; // Not using the `__iterator__` property.
```

## Version
This rule was introduced in ESLint v0.0.9.
## Further Reading





Iterators and generators - JavaScript | MDN 
 developer.mozilla.org










null 
 kangax.github.io










Deprecated and obsolete features - JavaScript | MDN 
 developer.mozilla.org





## Resources

Rule source 
Tests source 

