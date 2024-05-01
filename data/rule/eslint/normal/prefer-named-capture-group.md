
# prefer-named-capture-group
## Overview
Enforce using named capture group in regular expression


💡 hasSuggestions

            Some problems reported by this rule are manually fixable by editor suggestions 



## Rule Details
With the landing of ECMAScript 2018, named capture groups can be used in regular expressions, which can improve their readability.
This rule is aimed at using named capture groups instead of numbered capture groups in regular expressions:

```json
const regex = /(?<year>[0-9]{4})/;
```
Alternatively, if your intention is not to capture the results, but only express the alternative, use a non-capturing group:

```json
const regex = /(?:cauli|sun)flower/;
```
Examples of incorrect code for this rule:


```json
/*eslint prefer-named-capture-group: "error"*/

const foo = /(ba[rz])/;
const bar = new RegExp('(ba[rz])');
const baz = RegExp('(ba[rz])');

foo.exec('bar')[1]; // Retrieve the group result.
```
Examples of correct code for this rule:


```json
/*eslint prefer-named-capture-group: "error"*/

const foo = /(?<id>ba[rz])/;
const bar = new RegExp('(?<id>ba[rz])');
const baz = RegExp('(?<id>ba[rz])');
const xyz = /xyz(?:zy|abc)/;

foo.exec('bar').groups.id; // Retrieve the group result.
```
## When Not To Use It
If you are targeting ECMAScript 2017 and/or older environments, you should not use this rule, because this ECMAScript feature is only supported in ECMAScript 2018 and/or newer environments.
## Related Rules


no-invalid-regexp 


## Version
This rule was introduced in ESLint v5.15.0.
## Resources

Rule source 
Tests source 

