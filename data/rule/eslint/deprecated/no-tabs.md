
# no-tabs
## Overview
Disallow all tabs



This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .
Some style guides don’t allow the use of tab characters at all, including within comments.
## Rule Details
This rule looks for tabs anywhere inside a file: code, comments or anything else.
Examples of incorrect code for this rule:
 markdownlint-capture 
 markdownlint-disable MD010 


```json
/* eslint no-tabs: "error" */

var a 	= 2;

/**
* 		 it's a test function
*/
function test(){}

var x = 1; // 	 test
```
 markdownlint-restore 
Examples of correct code for this rule:


```json
/* eslint no-tabs: "error" */

var a = 2;

/**
* it's a test function
*/
function test(){}

var x = 1; // test
```
### Options
This rule has an optional object option with the following properties:

`allowIndentationTabs` (default: false): If this is set to true, then the rule will not report tabs used for indentation.

#### allowIndentationTabs
Examples of correct code for this rule with the `allowIndentationTabs: true` option:
 markdownlint-capture 
 markdownlint-disable MD010 


```json
/* eslint no-tabs: ["error", { allowIndentationTabs: true }] */

function test() {
	doSomething();
}

	// comment with leading indentation tab
```
 markdownlint-restore 
## When Not To Use It
If you have established a standard where having tabs is fine, then you can disable this rule.
## Compatibility

JSCS: disallowTabs 

## Version
This rule was introduced in ESLint v3.2.0.
## Resources

Rule source 
Tests source 
