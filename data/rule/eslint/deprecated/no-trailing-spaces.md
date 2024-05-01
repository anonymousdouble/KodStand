
# no-trailing-spaces
## Overview
Disallow trailing whitespace at the end of lines


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .
Sometimes in the course of editing files, you can end up with extra whitespace at the end of lines. These whitespace differences can be picked up by source control systems and flagged as diffs, causing frustration for developers. While this extra whitespace causes no functional issues, many code conventions require that trailing spaces be removed before check-in.
## Rule Details
This rule disallows trailing whitespace (spaces, tabs, and other Unicode whitespace characters) at the end of lines.
Examples of incorrect code for this rule:


```json
/*eslint no-trailing-spaces: "error"*/

var foo = 0;/* trailing whitespace */     
var baz = 5;/* trailing whitespace */  
/* trailing whitespace */     
```
Examples of correct code for this rule:


```json
/*eslint no-trailing-spaces: "error"*/

var foo = 0;
var baz = 5;
```
## Options
This rule has an object option:

`"skipBlankLines": false` (default) disallows trailing whitespace on empty lines
`"skipBlankLines": true` allows trailing whitespace on empty lines
`"ignoreComments": false` (default) disallows trailing whitespace in comment blocks
`"ignoreComments": true` allows trailing whitespace in comment blocks

### skipBlankLines
Examples of correct code for this rule with the `{ "skipBlankLines": true }` option:


```json
/*eslint no-trailing-spaces: ["error", { "skipBlankLines": true }]*/

var foo = 0;
var baz = 5;
// ↓ a line with whitespace only ↓
     
```
### ignoreComments
Examples of correct code for this rule with the `{ "ignoreComments": true }` option:


```json
/*eslint no-trailing-spaces: ["error", { "ignoreComments": true }]*/

// ↓ these comments have trailing whitespace → 
//     
/**
 * baz
 *  
 * bar
 */
```

## Version
This rule was introduced in ESLint v0.7.1.
## Resources

Rule source 
Tests source 

