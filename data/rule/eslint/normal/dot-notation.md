

# dot-notation
## Overview

Enforce dot notation whenever possible

In JavaScript, one can access properties using the dot notation (`foo.bar`) or square-bracket notation (`foo["bar"]`). However, the dot notation is often preferred because it is easier to read, less verbose, and works better with aggressive JavaScript minimizers.


```json
foo["bar"];
```

## Rule Details

This rule is aimed at maintaining code consistency and improving code readability by encouraging use of the dot notation style whenever possible. As such, it will warn when it encounters an unnecessary use of square-bracket notation.

Examples of incorrect code for this rule:


```json
/*eslint dot-notation: "error"*/

var x = foo["bar"];
```

Examples of correct code for this rule:


```json
/*eslint dot-notation: "error"*/

var x = foo.bar;

var x = foo[bar];    // Property name is a variable, square-bracket notation required
```

## Options

This rule accepts a single options argument:


- Set the `allowKeywords` option to `false` (default is `true`) to follow ECMAScript version 3 compatible style, avoiding dot notation for reserved word properties.

- Set the `allowPattern` option to a regular expression string to allow bracket notation for property names that match a pattern (by default, no pattern is tested).

### allowKeywords

Examples of correct code for the `{ "allowKeywords": false }` option:


```json
/*eslint dot-notation: ["error", { "allowKeywords": false }]*/

var foo = { "class": "CS 101" }
var x = foo["class"]; // Property name is a reserved word, square-bracket notation required
```

Examples of additional correct code for the `{ "allowKeywords": false }` option:


```json
/*eslint dot-notation: ["error", { "allowKeywords": false }]*/

class C {
    #in;
    foo() {
        this.#in; // Dot notation is required for private identifiers
    }
}
```

### allowPattern

For example, when preparing data to be sent to an external API, it is often required to use property names that include underscores.  If the `camelcase` rule is in effect, these snake case  properties would not be allowed.  By providing an `allowPattern` to the `dot-notation` rule, these snake case properties can be accessed with bracket notation.

Examples of incorrect code for the sample `{ "allowPattern": "^[a-z]+(_[a-z]+)+$" }` (pattern to find snake case named properties) option:


```json
/*eslint dot-notation: ["error", { "allowPattern": "^[a-z]+(_[a-z]+)+$" }]*/

var data = {};
data["fooBar"] = 42;
```

Examples of correct code for the sample `{ "allowPattern": "^[a-z]+(_[a-z]+)+$" }` (pattern to find snake case named properties) option:


```json
/*eslint dot-notation: ["error", { "allowPattern": "^[a-z]+(_[a-z]+)+$" }]*/

var data = {};
data["foo_bar"] = 42;
```


## Version

This rule was introduced in ESLint v0.0.7.

## Resources


- Rule source 

- Tests source 

