

# no-extra-label
## Overview

Disallow unnecessary labels

If a loop contains no nested loops or switches, labeling the loop is unnecessary.


```json
A: while (a) {
    break A;
}
```

You can achieve the same result by removing the label and using `break` or `continue` without a label.
Probably those labels would confuse developers because they expect labels to jump to further.

## Rule Details

This rule is aimed at eliminating unnecessary labels.

Examples of incorrect code for this rule:


```json
/*eslint no-extra-label: "error"*/

A: while (a) {
    break A;
}

B: for (let i = 0; i < 10; ++i) {
    break B;
}

C: switch (a) {
    case 0:
        break C;
}
```

Examples of correct code for this rule:


```json
/*eslint no-extra-label: "error"*/

while (a) {
    break;
}

for (let i = 0; i < 10; ++i) {
    break;
}

switch (a) {
    case 0:
        break;
}

A: {
    break A;
}

B: while (a) {
    while (b) {
        break B;
    }
}

C: switch (a) {
    case 0:
        while (b) {
            break C;
        }
        break;
}
```

## When Not To Use It

If you don’t want to be notified about usage of labels, then it’s safe to disable this rule.

## Related Rules


- 
no-labels 

- 
no-label-var 

- 
no-unused-labels 

## Version

This rule was introduced in ESLint v2.0.0-rc.0.

## Resources


- Rule source 

- Tests source 

