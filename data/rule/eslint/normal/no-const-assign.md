
# no-const-assign
## Overview
Disallow reassigning `const` variables


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


We cannot modify variables that are declared using `const` keyword.
It will raise a runtime error.
Under non ES2015 environment, it might be ignored merely.
## Rule Details
This rule is aimed to flag modifying variables that are declared using `const` keyword.
Examples of incorrect code for this rule:


```json
/*eslint no-const-assign: "error"*/
/*eslint-env es6*/

const a = 0;
a = 1;
```


```json
/*eslint no-const-assign: "error"*/
/*eslint-env es6*/

const a = 0;
a += 1;
```


```json
/*eslint no-const-assign: "error"*/
/*eslint-env es6*/

const a = 0;
++a;
```
Examples of correct code for this rule:


```json
/*eslint no-const-assign: "error"*/
/*eslint-env es6*/

const a = 0;
console.log(a);
```


```json
/*eslint no-const-assign: "error"*/
/*eslint-env es6*/

for (const a in [1, 2, 3]) { // `a` is re-defined (not modified) on each loop step.
    console.log(a);
}
```


```json
/*eslint no-const-assign: "error"*/
/*eslint-env es6*/

for (const a of [1, 2, 3]) { // `a` is re-defined (not modified) on each loop step.
    console.log(a);
}
```
## When Not To Use It
If you don’t want to be notified about modifying variables that are declared using `const` keyword, you can safely disable this rule.
## Handled by TypeScript

                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            
## Version
This rule was introduced in ESLint v1.0.0-rc-1.
## Resources

Rule source 
Tests source 

