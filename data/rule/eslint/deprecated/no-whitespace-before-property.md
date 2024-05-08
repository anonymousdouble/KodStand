

# no-whitespace-before-property
## Overview

Disallow whitespace before properties

This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .

JavaScript allows whitespace between objects and their properties. However, inconsistent spacing can make code harder to read and can lead to errors.


```json
foo. bar .baz . quz
```

## Rule Details

This rule disallows whitespace around the dot or before the opening bracket before properties of objects if they are on the same line. This rule allows whitespace when the object and property are on separate lines, as it is common to add newlines to longer chains of properties:


```json
foo
  .bar()
  .baz()
  .qux()
```

Examples of incorrect code for this rule:


```json
/*eslint no-whitespace-before-property: "error"*/

foo [bar]

foo. bar

foo .bar

foo. bar. baz

foo. bar()
  .baz()

foo
  .bar(). baz()
```

Examples of correct code for this rule:


```json
/*eslint no-whitespace-before-property: "error"*/

foo.bar

foo[bar]

foo[ bar ]

foo.bar.baz

foo
  .bar().baz()

foo
  .bar()
  .baz()

foo.
  bar().
  baz()
```

## When Not To Use It

Turn this rule off if you do not care about allowing whitespace around the dot or before the opening bracket before properties of objects if they are on the same line.

## Version

This rule was introduced in ESLint v2.0.0-beta.1.

## Resources


- Rule source 

- Tests source 

