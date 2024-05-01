
# no-confusing-arrow
## Overview
Disallow arrow functions where they could be confused with comparisons


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .
Arrow functions (`=>`) are similar in syntax to some comparison operators (`>`, `<`, `<=`, and `>=`). This rule warns against using the arrow function syntax in places where it could be confused with a comparison operator.
Here’s an example where the usage of `=>` could be confusing:

```json
// The intent is not clear
var x = a => 1 ? 2 : 3;
// Did the author mean this
var x = function (a) {
    return 1 ? 2 : 3;
};
// Or this
var x = a <= 1 ? 2 : 3;
```
## Rule Details
Examples of incorrect code for this rule:


```json
/*eslint no-confusing-arrow: "error"*/
/*eslint-env es6*/

var x = a => 1 ? 2 : 3;
var x = (a) => 1 ? 2 : 3;
```
Examples of correct code for this rule:


```json
/*eslint no-confusing-arrow: "error"*/
/*eslint-env es6*/
var x = a => (1 ? 2 : 3);
var x = (a) => (1 ? 2 : 3);
var x = (a) => {
    return 1 ? 2 : 3;
};
var x = a => { return 1 ? 2 : 3; };
```
## Options
This rule accepts two options argument with the following defaults:

```json
{
    "rules": {
        "no-confusing-arrow": [
            "error",
            { "allowParens": true, "onlyOneSimpleParam": false }
        ]
    }
}
```
`allowParens` is a boolean setting that can be `true`(default) or `false`:

`true` relaxes the rule and accepts parenthesis as a valid “confusion-preventing” syntax.
`false` warns even if the expression is wrapped in parenthesis

Examples of incorrect code for this rule with the `{"allowParens": false}` option:


```json
/*eslint no-confusing-arrow: ["error", {"allowParens": false}]*/
/*eslint-env es6*/
var x = a => (1 ? 2 : 3);
var x = (a) => (1 ? 2 : 3);
```
`onlyOneSimpleParam` is a boolean setting that can be `true` or `false`(default):

`true` relaxes the rule and doesn’t report errors if the arrow function has 0 or more than 1 parameters, or the parameter is not an identifier.
`false` warns regardless of parameters.

Examples of correct code for this rule with the `{"onlyOneSimpleParam": true}` option:


```json
/*eslint no-confusing-arrow: ["error", {"onlyOneSimpleParam": true}]*/
/*eslint-env es6*/
() => 1 ? 2 : 3;
(a, b) => 1 ? 2 : 3;
(a = b) => 1 ? 2 : 3;
({ a }) => 1 ? 2 : 3;
([a]) => 1 ? 2 : 3;
(...a) => 1 ? 2 : 3;
```

## Related Rules


no-constant-condition 

arrow-parens 


## Version
This rule was introduced in ESLint v2.0.0-alpha-2.
## Resources

Rule source 
Tests source 

