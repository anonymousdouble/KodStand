

# no-div-regex
## Overview

Disallow equal signs explicitly at the beginning of regular expressions

Characters `/=` at the beginning of a regular expression literal can be confused with a division assignment operator.


```json
function bar() { return /=foo/; }
```

## Rule Details

This rule forbids equal signs (`=`) after the slash (`/`) at the beginning of a regular expression literal, because the characters `/=` can be confused with a division assignment operator.

Examples of incorrect code for this rule:


```json
/*eslint no-div-regex: "error"*/

function bar() { return /=foo/; }
```

Examples of correct code for this rule:


```json
/*eslint no-div-regex: "error"*/

function bar() { return /[=]foo/; }
```


## Related Rules


- 
no-control-regex 

- 
no-regex-spaces 

## Version

This rule was introduced in ESLint v0.1.0.

## Resources


- Rule source 

- Tests source 

