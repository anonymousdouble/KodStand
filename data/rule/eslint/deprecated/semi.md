

# semi
## Overview

Require or disallow semicolons instead of ASI

This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .

JavaScript doesn’t require semicolons at the end of each statement. In many cases, the JavaScript engine can determine that a semicolon should be in a certain spot and will automatically add it. This feature is known as automatic semicolon insertion (ASI) and is considered one of the more controversial features of JavaScript. For example, the following lines are both valid:


```json
var name = "ESLint"
var website = "eslint.org";
```

On the first line, the JavaScript engine will automatically insert a semicolon, so this is not considered a syntax error. The JavaScript engine still knows how to interpret the line and knows that the line end indicates the end of the statement.

In the debate over ASI, there are generally two schools of thought. The first is that we should treat ASI as if it didn’t exist and always include semicolons manually. The rationale is that it’s easier to always include semicolons than to try to remember when they are or are not required, and thus decreases the possibility of introducing an error.

However, the ASI mechanism can sometimes be tricky to people who are using semicolons. For example, consider this code:


```json
return
{
    name: "ESLint"
};
```

This may look like a `return` statement that returns an object literal, however, the JavaScript engine will interpret this code as:


```json
return;
{
    name: "ESLint";
}
```

Effectively, a semicolon is inserted after the `return` statement, causing the code below it (a labeled literal inside a block) to be unreachable. This rule and the no-unreachable  rule will protect your code from such cases.

On the other side of the argument are those who say that since semicolons are inserted automatically, they are optional and do not need to be inserted manually. However, the ASI mechanism can also be tricky to people who don’t use semicolons. For example, consider this code:


```json
var globalCounter = { }

(function () {
    var n = 0
    globalCounter.increment = function () {
        return ++n
    }
})()
```

In this example, a semicolon will not be inserted after the first line, causing a run-time error (because an empty object is called as if it’s a function). The no-unexpected-multiline  rule can protect your code from such cases.

Although ASI allows for more freedom over your coding style, it can also make your code behave in an unexpected way, whether you use semicolons or not. Therefore, it is best to know when ASI takes place and when it does not, and have ESLint protect your code from these potentially unexpected cases. In short, as once described by Isaac Schlueter, a `\n` character always ends a statement (just like a semicolon) unless one of the following is true:


- The statement has an unclosed paren, array literal, or object literal or ends in some other way that is not a valid way to end a statement. (For instance, ending with `.` or `,`.)

- The line is `--` or `++` (in which case it will decrement/increment the next token.)

- It is a `for()`, `while()`, `do`, `if()`, or `else`, and there is no `{`

- The next line starts with `[`, `(`, `+`, `*`, `/`, `-`, `,`, `.`, or some other binary operator that can only be found between two tokens in a single expression.

## Rule Details

This rule enforces consistent use of semicolons.

## Options

This rule has two options, a string option and an object option.

String option:


- `"always"` (default) requires semicolons at the end of statements

- `"never"` disallows semicolons at the end of statements (except to disambiguate statements beginning with `[`, `(`, `/`, `+`, or `-`)

Object option (when `"always"`):


- `"omitLastInOneLineBlock": true` disallows the last semicolon in a block in which its braces (and therefore the content of the block) are in the same line

- `"omitLastInOneLineClassBody": true` disallows the last semicolon in a class body in which its braces (and therefore the content of the class body) are in the same line

Object option (when `"never"`):


- `"beforeStatementContinuationChars": "any"` (default) ignores semicolons (or lacking semicolon) at the end of statements if the next line starts with `[`, `(`, `/`, `+`, or `-`.

- `"beforeStatementContinuationChars": "always"` requires semicolons at the end of statements if the next line starts with `[`, `(`, `/`, `+`, or `-`.

- `"beforeStatementContinuationChars": "never"` disallows semicolons at the end of statements if it doesn’t make ASI hazard even if the next line starts with `[`, `(`, `/`, `+`, or `-`.

Note: `beforeStatementContinuationChars` does not apply to class fields because class fields are not statements.

### always

Examples of incorrect code for this rule with the default `"always"` option:


```json
/*eslint semi: ["error", "always"]*/

var name = "ESLint"

object.method = function() {
    // ...
}

class Foo {
    bar = 1
}
```

Examples of correct code for this rule with the default `"always"` option:


```json
/*eslint semi: "error"*/

var name = "ESLint";

object.method = function() {
    // ...
};

class Foo {
    bar = 1;
}
```

#### omitLastInOneLineBlock

Examples of additional correct code for this rule with the `"always", { "omitLastInOneLineBlock": true }` options:


```json
/*eslint semi: ["error", "always", { "omitLastInOneLineBlock": true}] */

if (foo) { bar() }

if (foo) { bar(); baz() }

function f() { bar(); baz() }

class C {
    foo() { bar(); baz() }

    static { bar(); baz() }
}
```

#### omitLastInOneLineClassBody

Examples of additional correct code for this rule with the `"always", { "omitLastInOneLineClassBody": true }` options:


```json
/*eslint semi: ["error", "always", { "omitLastInOneLineClassBody": true}] */

export class SomeClass{
    logType(){
        console.log(this.type);
        console.log(this.anotherType);
    }
}

export class Variant1 extends SomeClass{type=1}
export class Variant2 extends SomeClass{type=2; anotherType=3}
```

### never

Examples of incorrect code for this rule with the `"never"` option:


```json
/*eslint semi: ["error", "never"]*/

var name = "ESLint";

object.method = function() {
    // ...
};

class Foo {
    bar = 1;
}
```

Examples of correct code for this rule with the `"never"` option:


```json
/*eslint semi: ["error", "never"]*/

var name = "ESLint"

object.method = function() {
    // ...
}

var name = "ESLint"

;(function() {
    // ...
})()

import a from "a"
(function() {
    // ...
})()

import b from "b"
;(function() {
    // ...
})()

class Foo {
    bar = 1
}
```

#### beforeStatementContinuationChars

Examples of additional incorrect code for this rule with the `"never", { "beforeStatementContinuationChars": "always" }` options:


```json
/*eslint semi: ["error", "never", { "beforeStatementContinuationChars": "always"}] */
import a from "a"

(function() {
    // ...
})()
```

Examples of additional incorrect code for this rule with the `"never", { "beforeStatementContinuationChars": "never" }` options:


```json
/*eslint semi: ["error", "never", { "beforeStatementContinuationChars": "never"}] */
import a from "a"

;(function() {
    // ...
})()
```

## When Not To Use It

If you do not want to enforce semicolon usage (or omission) in any particular way, then you can turn this rule off.

## Related Rules


- 
no-extra-semi 

- 
no-unexpected-multiline 

- 
semi-spacing 

## Version

This rule was introduced in ESLint v0.0.6.

## Further Reading

An Open Letter to JavaScript Leaders Regarding Semicolons 
 blog.izs.me

JavaScript Semicolon Insertion 
 web.archive.org

## Resources


- Rule source 

- Tests source 

