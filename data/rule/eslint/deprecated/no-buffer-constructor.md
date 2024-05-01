
# no-buffer-constructor
## Overview
Disallow use of the `Buffer()` constructor



This rule was deprecated in ESLint v7.0.0. Please use the corresponding rule in eslint-plugin-n .
In Node.js, the behavior of the `Buffer` constructor is different depending on the type of its argument. Passing an argument from user input to `Buffer()` without validating its type can lead to security vulnerabilities such as remote memory disclosure and denial of service. As a result, the `Buffer` constructor has been deprecated and should not be used. Use the producer methods `Buffer.from`, `Buffer.alloc`, and `Buffer.allocUnsafe` instead.
## Rule Details
This rule disallows calling and constructing the `Buffer()` constructor.
Examples of incorrect code for this rule:


```json
/* eslint no-buffer-constructor: error */

new Buffer(5);
new Buffer([1, 2, 3]);

Buffer(5);
Buffer([1, 2, 3]);

new Buffer(res.body.amount);
new Buffer(res.body.values);
```
Examples of correct code for this rule:


```json
/* eslint no-buffer-constructor: error */

Buffer.alloc(5);
Buffer.allocUnsafe(5);
Buffer.from([1, 2, 3]);

Buffer.alloc(res.body.amount);
Buffer.from(res.body.values);
```
## When Not To Use It
If you don’t use Node.js, or you still need to support versions of Node.js that lack methods like `Buffer.from`, then you should not enable this rule.
## Version
This rule was introduced in ESLint v4.0.0-alpha.0.
## Further Reading





Buffer | Node.js v18.2.0 Documentation 
 nodejs.org










notes/Lets-fix-Buffer-API.md at master · ChALkeR/notes 
 github.com










Buffer(number) is unsafe · Issue #4660 · nodejs/node 
 github.com





## Resources

Rule source 
Tests source 

