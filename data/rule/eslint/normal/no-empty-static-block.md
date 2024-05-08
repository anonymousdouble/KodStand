

# no-empty-static-block
## Overview

Disallow empty static blocks

Empty static blocks, while not technically errors, usually occur due to refactoring that wasn’t completed. They can cause confusion when reading code.

## Rule Details

This rule disallows empty static blocks. This rule ignores static blocks which contain a comment.

Examples of incorrect code for this rule:


```json
/*eslint no-empty-static-block: "error"*/

class Foo {
    static {}
}
```

Examples of correct code for this rule:


```json
/*eslint no-empty-static-block: "error"*/

class Foo {
    static {
        bar();
    }
}

class Bar {
    static {
        // comment
    }
}
```

## When Not To Use It

This rule should not be used in environments prior to ES2022.

## Related Rules


- 
no-empty 

- 
no-empty-function 

## Version

This rule was introduced in ESLint v8.27.0.

## Further Reading

GitHub - tc39/proposal-class-static-block: ECMAScript class static initialization blocks 
 github.com

## Resources


- Rule source 

- Tests source 

