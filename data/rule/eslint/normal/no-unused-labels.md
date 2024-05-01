
# no-unused-labels
## Overview
Disallow unused labels


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        

🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


Labels that are declared and not used anywhere in the code are most likely an error due to incomplete refactoring.

```json
OUTER_LOOP:
for (const student of students) {
    if (checkScores(student.scores)) {
        continue;
    }
    doSomething(student);
}
```
In this case, probably removing `OUTER_LOOP:` had been forgotten.
Such labels take up space in the code and can lead to confusion by readers.
## Rule Details
This rule is aimed at eliminating unused labels.
Problems reported by this rule can be fixed automatically, except when there are any comments between the label and the following statement, or when removing a label would cause the following statement to become a directive such as `"use strict"`.
Examples of incorrect code for this rule:


```json
/*eslint no-unused-labels: "error"*/

A: var foo = 0;

B: {
    foo();
}

C:
for (let i = 0; i < 10; ++i) {
    foo();
}
```
Examples of correct code for this rule:


```json
/*eslint no-unused-labels: "error"*/

A: {
    if (foo()) {
        break A;
    }
    bar();
}

B:
for (let i = 0; i < 10; ++i) {
    if (foo()) {
        break B;
    }
    bar();
}
```
## When Not To Use It
If you don’t want to be notified about unused labels, then it’s safe to disable this rule.
## Related Rules


no-extra-label 

no-labels 

no-label-var 


## Version
This rule was introduced in ESLint v2.0.0-rc.0.
## Resources

Rule source 
Tests source 

