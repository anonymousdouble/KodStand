

# no-global-assign
## Overview

Disallow assignments to native objects or read-only global variables

JavaScript environments contain a number of built-in global variables, such as `window` in browsers and `process` in Node.js. In almost all cases, you don’t want to assign a value to these global variables as doing so could result in losing access to important functionality. For example, you probably don’t want to do this in browser code:


```json
window = {};
```

While examples such as `window` are obvious, there are often hundreds of built-in global objects provided by JavaScript environments. It can be hard to know if you’re assigning to a global variable or not.

## Rule Details

This rule disallows modifications to read-only global variables.

ESLint has the capability to configure global variables as read-only.


- Specifying Environments 

- Specifying Globals 

Examples of incorrect code for this rule:


```json
/*eslint no-global-assign: "error"*/

Object = null
undefined = 1
```



```json
/*eslint no-global-assign: "error"*/
/*eslint-env browser*/

window = {}
length = 1
top = 1
```



```json
/*eslint no-global-assign: "error"*/
/*global a:readonly*/

a = 1
```

Examples of correct code for this rule:


```json
/*eslint no-global-assign: "error"*/

a = 1
var b = 1
b = 2
```



```json
/*eslint no-global-assign: "error"*/
/*eslint-env browser*/

onload = function() {}
```



```json
/*eslint no-global-assign: "error"*/
/*global a:writable*/

a = 1
```

## Options

This rule accepts an `exceptions` option, which can be used to specify a list of builtins for which reassignments will be allowed:


```json
{
    "rules": {
        "no-global-assign": ["error", {"exceptions": ["Object"]}]
    }
}
```

## When Not To Use It

If you are trying to override one of the native objects.

## Related Rules


- 
no-extend-native 

- 
no-redeclare 

- 
no-shadow 

## Version

This rule was introduced in ESLint v3.3.0.

## Resources


- Rule source 

- Tests source 

