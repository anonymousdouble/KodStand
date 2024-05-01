
# no-obj-calls
## Overview
Disallow calling global object properties as functions


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


ECMAScript provides several global objects that are intended to be used as-is. Some of these objects look as if they could be constructors due their capitalization (such as `Math` and `JSON`) but will throw an error if you try to execute them as functions.
The ECMAScript 5 specification  makes it clear that both `Math` and `JSON` cannot be invoked:

The Math object does not have a `[[Call]]` internal property; it is not possible to invoke the Math object as a function.

The ECMAScript 2015 specification  makes it clear that `Reflect` cannot be invoked:

The Reflect object also does not have a `[[Call]]` internal method; it is not possible to invoke the Reflect object as a function.

The ECMAScript 2017 specification  makes it clear that `Atomics` cannot be invoked:

The Atomics object does not have a `[[Call]]` internal method; it is not possible to invoke the Atomics object as a function.

And the ECMAScript Internationalization API Specification  makes it clear that `Intl` cannot be invoked:

The Intl object does not have a `[[Call]]` internal method; it is not possible to invoke the Intl object as a function.

## Rule Details
This rule disallows calling the `Math`, `JSON`, `Reflect`, `Atomics` and `Intl` objects as functions.
This rule also disallows using these objects as constructors with the `new` operator.
Examples of incorrect code for this rule:


```json
/*eslint no-obj-calls: "error"*/
/*eslint-env es2017, browser */

var math = Math();

var newMath = new Math();

var json = JSON();

var newJSON = new JSON();

var reflect = Reflect();

var newReflect = new Reflect();

var atomics = Atomics();

var newAtomics = new Atomics();

var intl = Intl();

var newIntl = new Intl();
```
Examples of correct code for this rule:


```json
/*eslint no-obj-calls: "error"*/
/*eslint-env es2017, browser*/

function area(r) {
    return Math.PI * r * r;
}

var object = JSON.parse("{}");

var value = Reflect.get({ x: 1, y: 2 }, "x");

var first = Atomics.load(foo, 0);

var segmenterFr = new Intl.Segmenter("fr", { granularity: "word" });
```

## Handled by TypeScript

                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            
## Version
This rule was introduced in ESLint v0.0.9.
## Further Reading





Annotated ES5 
 es5.github.io





## Resources

Rule source 
Tests source 

