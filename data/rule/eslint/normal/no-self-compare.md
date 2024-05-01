
# no-self-compare
## Overview
Disallow comparisons where both sides are exactly the same



Comparing a variable against itself is usually an error, either a typo or refactoring error. It is confusing to the reader and may potentially introduce a runtime error.
The only time you would compare a variable against itself is when you are testing for `NaN`. However, it is far more appropriate to use `typeof x === 'number' && isNaN(x)` or the Number.isNaN ES2015 function  for that use case rather than leaving the reader of the code to determine the intent of self comparison.
## Rule Details
This error is raised to highlight a potentially confusing and potentially pointless piece of code. There are almost no situations in which you would need to compare something to itself.
Examples of incorrect code for this rule:


```json
/*eslint no-self-compare: "error"*/

var x = 10;
if (x === x) {
    x = 20;
}
```

## Version
This rule was introduced in ESLint v0.0.9.
## Resources

Rule source 
Tests source 

