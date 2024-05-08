

# no-new
## Overview

Disallow `new` operators outside of assignments or comparisons

The goal of using `new` with a constructor is typically to create an object of a particular type and store that object in a variable, such as:


```json
var person = new Person();
```

It’s less common to use `new` and not store the result, such as:


```json
new Person();
```

In this case, the created object is thrown away because its reference isn’t stored anywhere, and in many cases, this means that the constructor should be replaced with a function that doesn’t require `new` to be used.

## Rule Details

This rule is aimed at maintaining consistency and convention by disallowing constructor calls using the `new` keyword that do not assign the resulting object to a variable.

Examples of incorrect code for this rule:


```json
/*eslint no-new: "error"*/

new Thing();
```

Examples of correct code for this rule:


```json
/*eslint no-new: "error"*/

var thing = new Thing();

Foo();
```


## Version

This rule was introduced in ESLint v0.0.7.

## Resources


- Rule source 

- Tests source 

