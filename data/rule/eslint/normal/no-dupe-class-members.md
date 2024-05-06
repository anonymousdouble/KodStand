
# no-dupe-class-members
## Overview
Disallow duplicate class members


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


If there are declarations of the same name in class members, the last declaration overwrites other declarations silently.
It can cause unexpected behaviors.

```json
/*eslint-env es6*/

class Foo {
  bar() { console.log("hello"); }
  bar() { console.log("goodbye"); }
}

var foo = new Foo();
foo.bar(); // goodbye
```
## Rule Details
This rule is aimed to flag the use of duplicate names in class members.
## Examples
Examples of incorrect code for this rule:


```json
/*eslint no-dupe-class-members: "error"*/

class A {
  bar() { }
  bar() { }
}

class B {
  bar() { }
  get bar() { }
}

class C {
  bar;
  bar;
}

class D {
  bar;
  bar() { }
}

class E {
  static bar() { }
  static bar() { }
}
```
Examples of correct code for this rule:


```json
/*eslint no-dupe-class-members: "error"*/

class A {
  bar() { }
  qux() { }
}

class B {
  get bar() { }
  set bar(value) { }
}

class C {
  bar;
  qux;
}

class D {
  bar;
  qux() { }
}

class E {
  static bar() { }
  bar() { }
}
```
## When Not To Use It
This rule should not be used in ES3/5 environments.
In ES2015 (ES6) or later, if you don’t want to be notified about duplicate names in class members, you can safely disable this rule.
## Handled by TypeScript

                It is safe to disable this rule when using TypeScript because TypeScript's compiler enforces this check.
            
## Version
This rule was introduced in ESLint v1.2.0.
## Resources

Rule source 
Tests source 
