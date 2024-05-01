
# no-sparse-arrays
## Overview
Disallow sparse arrays


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        


Sparse arrays contain empty slots, most frequently due to multiple commas being used in an array literal, such as:

```json
var items = [,,];
```
While the `items` array in this example has a `length` of 2, there are actually no values in `items[0]` or `items[1]`. The fact that the array literal is valid with only commas inside, coupled with the `length` being set and actual item values not being set, make sparse arrays confusing for many developers. Consider the following:

```json
var colors = [ "red",, "blue" ];
```
In this example, the `colors` array has a `length` of 3. But did the developer intend for there to be an empty spot in the middle of the array? Or is it a typo?
The confusion around sparse arrays defined in this manner is enough that it’s recommended to avoid using them unless you are certain that they are useful in your code.
## Rule Details
This rule disallows sparse array literals which have “holes” where commas are not preceded by elements. It does not apply to a trailing comma following the last element.
Examples of incorrect code for this rule:


```json
/*eslint no-sparse-arrays: "error"*/

var items = [,];
var colors = [ "red",, "blue" ];
```
Examples of correct code for this rule:


```json
/*eslint no-sparse-arrays: "error"*/

var items = [];
var items = new Array(23);

// trailing comma (after the last element) is not a problem
var colors = [ "red", "blue", ];
```
## When Not To Use It
If you want to use sparse arrays, then it is safe to disable this rule.
## Version
This rule was introduced in ESLint v0.4.0.
## Further Reading





Inconsistent array literals 
 www.nczonline.net





## Resources

Rule source 
Tests source 

