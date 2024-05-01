
# no-reserved-keys
## Overview

Disallows unquoted reserved words as property names in object literals.
ECMAScript 3 described as series of keywords and reserved words, such as `if` and `public`, that are used or intended to be used for a core language feature. The specification also indicated that these keywords and reserved words could not be used as object property names without being enclosed in strings. An error occurs in an ECMAScript 3 environment when you use a keyword or reserved word in an object literal. For example:

```json
var values = {
    enum: ["red", "blue", "green"]  // throws an error in ECMAScript 3
}
```
In this code, `enum` is used as an object key and will throw an error in an ECMAScript 3 environment (such as Internet Explorer 8).
ECMAScript 5 loosened the restriction such that keywords and reserved words can be used as object keys without causing an error. However, any code that needs to run in ECMAScript 3 still needs to avoid using keywords and reserved words as keys.
## Rule Details
This rule is aimed at eliminating the use of ECMAScript 3 keywords and reserved words as object literal keys. As such, it warns whenever an object key would throw an error in an ECMAScript 3 environment.
Examples of incorrect code for this rule:

```json
var superman = {
    class: "Superhero",
    private: "Clark Kent"
};

var values = {
    enum: ["red", "blue", "green"]
};
```
Examples of correct code for this rule:

```json
var superman = {
    "class": "Superhero",
    "private": "Clark Kent"
};

var values = {
    "enum": ["red", "blue", "green"]
};
```
## When Not To Use It
If your code is only going to be executed in an ECMAScript 5 or higher environment, then you can safely leave this rule off.
## Version
This rule was introduced in ESLint v0.8.0
                 and removed in v1.0.0.
## Further Reading





ECMAScript 5 compatibility table 
 kangax.github.io






## Replaced by
quote-props