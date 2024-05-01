
# no-regex-spaces
## Overview
Disallow multiple spaces in regular expressions


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        

🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


Regular expressions can be very complex and difficult to understand, which is why it’s important to keep them as simple as possible in order to avoid mistakes. One of the more error-prone things you can do with a regular expression is to use more than one space, such as:

```json
var re = /foo   bar/;
```
In this regular expression, it’s very hard to tell how many spaces are intended to be matched. It’s better to use only one space and then specify how many spaces are expected, such as:

```json
var re = /foo {3}bar/;
```
Now it is very clear that three spaces are expected to be matched.
## Rule Details
This rule disallows multiple spaces in regular expression literals.
Examples of incorrect code for this rule:


```json
/*eslint no-regex-spaces: "error"*/

var re = /foo   bar/;
var re = new RegExp("foo   bar");
```
Examples of correct code for this rule:


```json
/*eslint no-regex-spaces: "error"*/

var re = /foo {3}bar/;
var re = new RegExp("foo {3}bar");
```
## When Not To Use It
If you want to allow multiple spaces in a regular expression, then you can safely turn this rule off.
## Related Rules


no-div-regex 

no-control-regex 


## Version
This rule was introduced in ESLint v0.4.0.
## Resources

Rule source 
Tests source 

