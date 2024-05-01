
# no-extra-semi
## Overview
Disallow unnecessary semicolons


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        

🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .
Typing mistakes and misunderstandings about where semicolons are required can lead to semicolons that are unnecessary. While not technically an error, extra semicolons can cause confusion when reading code.
## Rule Details
This rule disallows unnecessary semicolons.
Problems reported by this rule can be fixed automatically, except when removing a semicolon would cause a following statement to become a directive such as `"use strict"`.
Examples of incorrect code for this rule:


```json
/*eslint no-extra-semi: "error"*/

var x = 5;;

function foo() {
    // code
};

class C {
    field;;

    method() {
        // code
    };

    static {
        // code
    };
};
```
Examples of correct code for this rule:


```json
/*eslint no-extra-semi: "error"*/

var x = 5;

function foo() {
    // code
}

var bar = function() {
    // code
};

class C {
    field;

    method() {
        // code
    }

    static {
        // code
    }
}
```
## When Not To Use It
If you intentionally use extra semicolons then you can disable this rule.
## Related Rules


semi 

semi-spacing 


## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 

