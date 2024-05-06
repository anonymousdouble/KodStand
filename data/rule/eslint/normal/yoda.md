
# yoda
## Overview
Require or disallow "Yoda" conditions


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


Yoda conditions are so named because the literal value of the condition comes first while the variable comes second. For example, the following is a Yoda condition:

```json
if ("red" === color) {
    // ...
}
```
This is called a Yoda condition because it reads as, “if red equals the color”, similar to the way the Star Wars character Yoda speaks. Compare to the other way of arranging the operands:

```json
if (color === "red") {
    // ...
}
```
This typically reads, “if the color equals red”, which is arguably a more natural way to describe the comparison.
Proponents of Yoda conditions highlight that it is impossible to mistakenly use `=` instead of `==` because you cannot assign to a literal value. Doing so will cause a syntax error and you will be informed of the mistake early on. This practice was therefore very common in early programming where tools were not yet available.
Opponents of Yoda conditions point out that tooling has made us better programmers because tools will catch the mistaken use of `=` instead of `==` (ESLint will catch this for you). Therefore, they argue, the utility of the pattern doesn’t outweigh the readability hit the code takes while using Yoda conditions.
## Rule Details
This rule aims to enforce consistent style of conditions which compare a variable to a literal value.
## Options
This rule can take a string option:

If it is the default `"never"`, then comparisons must never be Yoda conditions.
If it is `"always"`, then the literal value must always come first.

The default `"never"` option can have exception options in an object literal:

If the `"exceptRange"` property is `true`, the rule allows yoda conditions in range comparisons which are wrapped directly in parentheses, including the parentheses of an `if` or `while` condition. The default value is `false`. A range comparison tests whether a variable is inside or outside the range between two literal values.
If the `"onlyEquality"` property is `true`, the rule reports yoda conditions only for the equality operators `==` and `===`. The default value is `false`.

The `onlyEquality` option allows a superset of the exceptions which `exceptRange` allows, thus both options are not useful together.
### never
Examples of incorrect code for the default `"never"` option:


```json
/*eslint yoda: "error"*/

if ("red" === color) {
    // ...
}

if (`red` === color) {
    // ...
}

if (`red` === `${color}`) {
    // ...
}

if (true == flag) {
    // ...
}

if (5 > count) {
    // ...
}

if (-1 < str.indexOf(substr)) {
    // ...
}

if (0 <= x && x < 1) {
    // ...
}
```
Examples of correct code for the default `"never"` option:


```json
/*eslint yoda: "error"*/

if (5 & value) {
    // ...
}

if (value === "red") {
    // ...
}

if (value === `red`) {
    // ...
}

if (`${value}` === `red`) {

}
```
### exceptRange
Examples of correct code for the `"never", { "exceptRange": true }` options:


```json
/*eslint yoda: ["error", "never", { "exceptRange": true }]*/

function isReddish(color) {
    return (color.hue < 60 || 300 < color.hue);
}

if (x < -1 || 1 < x) {
    // ...
}

if (count < 10 && (0 <= rand && rand < 1)) {
    // ...
}

if (`blue` < x && x < `green`) {
    // ...
}

function howLong(arr) {
    return (0 <= arr.length && arr.length < 10) ? "short" : "long";
}
```
### onlyEquality
Examples of correct code for the `"never", { "onlyEquality": true }` options:


```json
/*eslint yoda: ["error", "never", { "onlyEquality": true }]*/

if (x < -1 || 9 < x) {
}

if (x !== 'foo' && 'bar' != x) {
}

if (x !== `foo` && `bar` != x) {
}
```
### always
Examples of incorrect code for the `"always"` option:


```json
/*eslint yoda: ["error", "always"]*/

if (color == "blue") {
    // ...
}

if (color == `blue`) {
    // ...
}
```
Examples of correct code for the `"always"` option:


```json
/*eslint yoda: ["error", "always"]*/

if ("blue" == value) {
    // ...
}

if (`blue` == value) {
    // ...
}

if (`blue` == `${value}`) {
    // ...
}

if (-1 < str.indexOf(substr)) {
    // ...
}
```

## Version
This rule was introduced in ESLint v0.7.1.
## Further Reading





Yoda conditions - Wikipedia 
 en.wikipedia.org










Coding in Style 
 thomas.tuerke.net





## Resources

Rule source 
Tests source 
