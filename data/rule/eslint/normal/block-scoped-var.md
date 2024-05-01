
# block-scoped-var
## Overview
Enforce the use of variables within the scope they are defined



The `block-scoped-var` rule generates warnings when variables are used outside of the block in which they were defined. This emulates C-style block scope.
## Rule Details
This rule aims to reduce the usage of variables outside of their binding context and emulate traditional block scope from other languages. This is to help newcomers to the language avoid difficult bugs with variable hoisting.
Examples of incorrect code for this rule:


```json
/*eslint block-scoped-var: "error"*/

function doIf() {
    if (true) {
        var build = true;
    }

    console.log(build);
}

function doIfElse() {
    if (true) {
        var build = true;
    } else {
        var build = false;
    }
}

function doTryCatch() {
    try {
        var build = 1;
    } catch (e) {
        var f = build;
    }
}

function doFor() {
    for (var x = 1; x < 10; x++) {
        var y = f(x);
    }
    console.log(y);
}

class C {
    static {
        if (something) {
            var build = true;
        }
        build = false;
    }
}
```
Examples of correct code for this rule:


```json
/*eslint block-scoped-var: "error"*/

function doIf() {
    var build;

    if (true) {
        build = true;
    }

    console.log(build);
}

function doIfElse() {
    var build;

    if (true) {
        build = true;
    } else {
        build = false;
    }
}

function doTryCatch() {
    var build;
    var f;

    try {
        build = 1;
    } catch (e) {
        f = build;
    }
}

function doFor() {
    for (var x = 1; x < 10; x++) {
        var y = f(x);
        console.log(y);
    }
}

class C {
    static {
        var build = false;
        if (something) {
            build = true;
        }
    }
}
```

## Version
This rule was introduced in ESLint v0.1.0.
## Further Reading





JavaScript Scoping and Hoisting 
 www.adequatelygood.com










var - JavaScript | MDN 
 developer.mozilla.org





## Resources

Rule source 
Tests source 

