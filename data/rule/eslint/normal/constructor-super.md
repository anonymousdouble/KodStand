
# constructor-super
## Overview
Require `super()` calls in constructors


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


Constructors of derived classes must call `super()`.
Constructors of non derived classes must not call `super()`.
If this is not observed, the JavaScript engine will raise a runtime error.
This rule checks whether or not there is a valid `super()` call.
## Rule Details
This rule is aimed to flag invalid/missing `super()` calls.
This is a syntax error because there is no `extends` clause in the class:

```json
class A {
    constructor() {
        super();
    }
}
```
Examples of incorrect code for this rule:


```json
/*eslint constructor-super: "error"*/
/*eslint-env es6*/

class A extends B {
    constructor() { }  // Would throw a ReferenceError.
}

// Classes which inherits from a non constructor are always problems.
class C extends null {
    constructor() {
        super();  // Would throw a TypeError.
    }
}

class D extends null {
    constructor() { }  // Would throw a ReferenceError.
}
```
Examples of correct code for this rule:


```json
/*eslint constructor-super: "error"*/
/*eslint-env es6*/

class A {
    constructor() { }
}

class B extends C {
    constructor() {
        super();
    }
}
```
## When Not To Use It
If you don’t want to be notified about invalid/missing `super()` callings in constructors, you can safely disable this rule.
## Handled by TypeScript

                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            
## Version
This rule was introduced in ESLint v0.24.0.
## Resources

Rule source 
Tests source 

