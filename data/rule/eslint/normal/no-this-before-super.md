
# no-this-before-super
## Overview
Disallow `this`/`super` before calling `super()` in constructors


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


In the constructor of derived classes, if `this`/`super` are used before `super()` calls, it raises a reference error.
This rule checks `this`/`super` keywords in constructors, then reports those that are before `super()`.
## Rule Details
This rule is aimed to flag `this`/`super` keywords before `super()` callings.
## Examples
Examples of incorrect code for this rule:


```json
/*eslint no-this-before-super: "error"*/
/*eslint-env es6*/

class A1 extends B {
    constructor() {
        this.a = 0;
        super();
    }
}

class A2 extends B {
    constructor() {
        this.foo();
        super();
    }
}

class A3 extends B {
    constructor() {
        super.foo();
        super();
    }
}

class A4 extends B {
    constructor() {
        super(this.foo());
    }
}
```
Examples of correct code for this rule:


```json
/*eslint no-this-before-super: "error"*/
/*eslint-env es6*/

class A1 {
    constructor() {
        this.a = 0; // OK, this class doesn't have an `extends` clause.
    }
}

class A2 extends B {
    constructor() {
        super();
        this.a = 0; // OK, this is after `super()`.
    }
}

class A3 extends B {
    foo() {
        this.a = 0; // OK. this is not in a constructor.
    }
}
```
## When Not To Use It
If you don’t want to be notified about using `this`/`super` before `super()` in constructors, you can safely disable this rule.
## Handled by TypeScript

                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            
## Version
This rule was introduced in ESLint v0.24.0.
## Resources

Rule source 
Tests source 

