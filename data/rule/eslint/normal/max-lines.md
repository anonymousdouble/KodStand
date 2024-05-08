

# max-lines
## Overview

Enforce a maximum number of lines per file

Some people consider large files a code smell. Large files tend to do a lot of things and can make it hard following what’s going. While there is not an objective maximum number of lines considered acceptable in a file, most people would agree it should not be in the thousands. Recommendations usually range from 100 to 500 lines.

## Rule Details

This rule enforces a maximum number of lines per file, in order to aid in maintainability and reduce complexity.

Please note that most editors show an additional empty line at the end if the file ends with a line break. This rule does not count that extra line.

## Options

This rule has a number or object option:


- 
`"max"` (default `300`) enforces a maximum number of lines in a file


- 
`"skipBlankLines": true` ignore lines made up purely of whitespace.


- 
`"skipComments": true` ignore lines containing just comments

### max

Examples of incorrect code for this rule with a max value of `2`:


```json
/*eslint max-lines: ["error", 2]*/
var a,
    b,
    c;
```



```json
/*eslint max-lines: ["error", 2]*/

var a,
    b,c;
```



```json
/*eslint max-lines: ["error", 2]*/
// a comment
var a,
    b,c;
```

Examples of correct code for this rule with a max value of `2`:


```json
/*eslint max-lines: ["error", 2]*/
var a,
    b, c;
```



```json
/*eslint max-lines: ["error", 2]*/

var a, b, c;
```



```json
/*eslint max-lines: ["error", 2]*/
// a comment
var a, b, c;
```

### skipBlankLines

Examples of incorrect code for this rule with the `{ "skipBlankLines": true }` option:


```json
/*eslint max-lines: ["error", {"max": 2, "skipBlankLines": true}]*/

var a,
    b,
    c;
```

Examples of correct code for this rule with the `{ "skipBlankLines": true }` option:


```json
/*eslint max-lines: ["error", {"max": 2, "skipBlankLines": true}]*/

var a,
    b, c;
```

### skipComments

Examples of incorrect code for this rule with the `{ "skipComments": true }` option:


```json
/*eslint max-lines: ["error", {"max": 2, "skipComments": true}]*/
// a comment
var a,
    b,
    c;
```

Examples of correct code for this rule with the `{ "skipComments": true }` option:


```json
/*eslint max-lines: ["error", {"max": 2, "skipComments": true}]*/
// a comment
var a,
    b, c;
```

## When Not To Use It

You can turn this rule off if you are not concerned with the number of lines in your files.

## Compatibility


- JSCS: maximumNumberOfLines 

## Related Rules


- 
complexity 

- 
max-depth 

- 
max-lines-per-function 

- 
max-nested-callbacks 

- 
max-params 

- 
max-statements 

## Version

This rule was introduced in ESLint v2.12.0.

## Further Reading

Software Module size and file size 
 web.archive.org

## Resources


- Rule source 

- Tests source 

