
# template-tag-spacing
## Overview
Require or disallow spacing between template tags and their literals


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .
 markdownlint-disable-next-line MD051 
With ES6, it’s possible to create functions called tagged template literals  where the function parameters consist of a template literal’s strings and expressions.
When using tagged template literals, it’s possible to insert whitespace between the tag function and the template literal. Since this whitespace is optional, the following lines are equivalent:

```json
let hello = func`Hello world`;
let hello = func `Hello world`;
```
## Rule Details
This rule aims to maintain consistency around the spacing between template tag functions and their template literals.
## Options

```json
{
    "template-tag-spacing": ["error", "never"]
}
```
This rule has one option whose value can be set to `"never"` or `"always"`

`"never"` (default) - Disallows spaces between a tag function and its template literal.
`"always"` - Requires one or more spaces between a tag function and its template literal.

## Examples
### never
Examples of incorrect code for this rule with the default `"never"` option:


```json
/*eslint template-tag-spacing: "error"*/

func `Hello world`;
```
Examples of correct code for this rule with the default `"never"` option:


```json
/*eslint template-tag-spacing: "error"*/

func`Hello world`;
```
### always
Examples of incorrect code for this rule with the `"always"` option:


```json
/*eslint template-tag-spacing: ["error", "always"]*/

func`Hello world`;
```
Examples of correct code for this rule with the `"always"` option:


```json
/*eslint template-tag-spacing: ["error", "always"]*/

func `Hello world`;
```
## When Not To Use It
If you don’t want to be notified about usage of spacing between tag functions and their template literals, then it’s safe to disable this rule.
## Version
This rule was introduced in ESLint v3.15.0.
## Further Reading





Template literals (Template strings) - JavaScript | MDN 
 developer.mozilla.org










8. Template literals 
 exploringjs.com





## Resources

Rule source 
Tests source 

