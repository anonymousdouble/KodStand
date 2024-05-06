
# object-curly-newline
## Overview
Enforce consistent line breaks after opening and before closing braces


🔧 Fixable

            Some problems reported by this rule are automatically fixable by the `--fix` command line  option
        


This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .
A number of style guides require or disallow line breaks inside of object braces and other tokens.
## Rule Details
This rule requires or disallows a line break between `{` and its following token, and between `}` and its preceding token of object literals or destructuring assignments.
## Options
This rule has either a string option:

`"always"` requires line breaks after opening and before closing braces
`"never"` disallows line breaks after opening and before closing braces

Or an object option:

`"multiline": true` requires line breaks if there are line breaks inside properties or between properties. Otherwise, it disallows line breaks.
`"minProperties"` requires line breaks if the number of properties is at least the given integer. By default, an error will also be reported if an object contains linebreaks and has fewer properties than the given integer. However, the second behavior is disabled if the `consistent` option is set to `true`
`"consistent": true` (default) requires that either both curly braces, or neither, directly enclose newlines. Note that enabling this option will also change the behavior of the `minProperties` option. (See `minProperties` above for more information)

You can specify different options for object literals, destructuring assignments, and named imports and exports:

```json
{
    "object-curly-newline": ["error", {
        "ObjectExpression": "always",
        "ObjectPattern": { "multiline": true },
        "ImportDeclaration": "never",
        "ExportDeclaration": { "multiline": true, "minProperties": 3 }
    }]
}
```

`"ObjectExpression"` configuration for object literals
`"ObjectPattern"` configuration for object patterns of destructuring assignments
`"ImportDeclaration"` configuration for named imports
`"ExportDeclaration"` configuration for named exports

### always
Examples of incorrect code for this rule with the `"always"` option:


```json
/*eslint object-curly-newline: ["error", "always"]*/
/*eslint-env es6*/

let a = {};
let b = {foo: 1};
let c = {foo: 1, bar: 2};
let d = {foo: 1,
    bar: 2};
let e = {foo() {
    dosomething();
}};

let {} = obj;
let {f} = obj;
let {g, h} = obj;
let {i,
    j} = obj;
let {k = function() {
    dosomething();
}} = obj;
```
Examples of correct code for this rule with the `"always"` option:


```json
/*eslint object-curly-newline: ["error", "always"]*/
/*eslint-env es6*/

let a = {
};
let b = {
    foo: 1
};
let c = {
    foo: 1, bar: 2
};
let d = {
    foo: 1,
    bar: 2
};
let e = {
    foo: function() {
        dosomething();
    }
};

let {
} = obj;
let {
    f
} = obj;
let {
    g, h
} = obj;
let {
    i,
    j
} = obj;
let {
    k = function() {
        dosomething();
    }
} = obj;
```
### never
Examples of incorrect code for this rule with the `"never"` option:


```json
/*eslint object-curly-newline: ["error", "never"]*/
/*eslint-env es6*/

let a = {
};
let b = {
    foo: 1
};
let c = {
    foo: 1, bar: 2
};
let d = {
    foo: 1,
    bar: 2
};
let e = {
    foo: function() {
        dosomething();
    }
};

let {
} = obj;
let {
    f
} = obj;
let {
    g, h
} = obj;
let {
    i,
    j
} = obj;
let {
    k = function() {
        dosomething();
    }
} = obj;
```
Examples of correct code for this rule with the `"never"` option:


```json
/*eslint object-curly-newline: ["error", "never"]*/
/*eslint-env es6*/

let a = {};
let b = {foo: 1};
let c = {foo: 1, bar: 2};
let d = {foo: 1,
    bar: 2};
let e = {foo: function() {
    dosomething();
}};

let {} = obj;
let {f} = obj;
let {g, h} = obj;
let {i,
    j} = obj;
let {k = function() {
    dosomething();
}} = obj;
```
### multiline
Examples of incorrect code for this rule with the `{ "multiline": true }` option:


```json
/*eslint object-curly-newline: ["error", { "multiline": true }]*/
/*eslint-env es6*/

let a = {
};
let b = {
    foo: 1
};
let c = {
    foo: 1, bar: 2
};
let d = {foo: 1,
    bar: 2};
let e = {foo: function() {
    dosomething();
}};

let {
} = obj;
let {
    f
} = obj;
let {
    g, h
} = obj;
let {i,
    j} = obj;
let {k = function() {
    dosomething();
}} = obj;
```
Examples of correct code for this rule with the `{ "multiline": true }` option:


```json
/*eslint object-curly-newline: ["error", { "multiline": true }]*/
/*eslint-env es6*/

let a = {};
let b = {foo: 1};
let c = {foo: 1, bar: 2};
let d = {
    foo: 1,
    bar: 2
};
let e = {
    foo: function() {
        dosomething();
    }
};

let {} = obj;
let {f} = obj;
let {g, h} = obj;
let {
    i,
    j
} = obj;
let {
    k = function() {
        dosomething();
    }
} = obj;
```
### minProperties
Examples of incorrect code for this rule with the `{ "minProperties": 2 }` option:


```json
/*eslint object-curly-newline: ["error", { "minProperties": 2 }]*/
/*eslint-env es6*/

let a = {
};
let b = {
    foo: 1
};
let c = {foo: 1, bar: 2};
let d = {foo: 1,
    bar: 2};
let e = {
    foo: function() {
        dosomething();
    }
};

let {
} = obj;
let {
    f
} = obj;
let {g, h} = obj;
let {i,
    j} = obj;
let {
    k = function() {
        dosomething();
    }
} = obj;
```
Examples of correct code for this rule with the `{ "minProperties": 2 }` option:


```json
/*eslint object-curly-newline: ["error", { "minProperties": 2 }]*/
/*eslint-env es6*/

let a = {};
let b = {foo: 1};
let c = {
    foo: 1, bar: 2
};
let d = {
    foo: 1,
    bar: 2
};
let e = {foo: function() {
    dosomething();
}};

let {} = obj;
let {f} = obj;
let {
    g, h
} = obj;
let {
    i,
    j
} = obj;
let {k = function() {
    dosomething();
}} = obj;
```
### consistent
Examples of incorrect code for this rule with the default `{ "consistent": true }` option:


```json
/*eslint object-curly-newline: ["error", { "consistent": true }]*/
/*eslint-env es6*/

let a = {foo: 1
};
let b = {
    foo: 1};
let c = {foo: 1, bar: 2
};
let d = {
    foo: 1, bar: 2};
let e = {foo: function() {
    dosomething();
    }
};
let f = {
    foo: function() {
    dosomething();}};

let {g
} = obj;
let {
    h} = obj;
let {i, j
} = obj;
let {k, l
} = obj;
let {
    m, n} = obj;
let {
    o, p} = obj;
let {q = function() {
    dosomething();
    }
} = obj;
let {
    r = function() {
        dosomething();
    }} = obj;
```
Examples of correct code for this rule with the default `{ "consistent": true }` option:


```json
/*eslint object-curly-newline: ["error", { "consistent": true }]*/
/*eslint-env es6*/

let empty1 = {};
let empty2 = {
};
let a = {foo: 1};
let b = {
    foo: 1
};
let c = {
    foo: 1, bar: 2
};
let d = {
    foo: 1,
    bar: 2
};
let e = {foo: function() {dosomething();}};
let f = {
    foo: function() {
        dosomething();
    }
};

let {} = obj;
let {
} = obj;
let {g} = obj;
let {
    h
} = obj;
let {i, j} = obj;
let {
    k, l
} = obj;
let {m,
    n} = obj;
let {
    o,
    p
} = obj;
let {q = function() {dosomething();}} = obj;
let {
    r = function() {
        dosomething();
    }
} = obj;
```
### ObjectExpression and ObjectPattern
Examples of incorrect code for this rule with the `{ "ObjectExpression": "always", "ObjectPattern": "never" }` options:


```json
/*eslint object-curly-newline: ["error", { "ObjectExpression": "always", "ObjectPattern": "never" }]*/
/*eslint-env es6*/

let a = {};
let b = {foo: 1};
let c = {foo: 1, bar: 2};
let d = {foo: 1,
    bar: 2};
let e = {foo: function() {
    dosomething();
}};

let {
} = obj;
let {
    f
} = obj;
let {
    g, h
} = obj;
let {
    i,
    j
} = obj;
let {
    k = function() {
        dosomething();
    }
} = obj;
```
Examples of correct code for this rule with the `{ "ObjectExpression": "always", "ObjectPattern": "never" }` options:


```json
/*eslint object-curly-newline: ["error", { "ObjectExpression": "always", "ObjectPattern": "never" }]*/
/*eslint-env es6*/

let a = {
};
let b = {
    foo: 1
};
let c = {
    foo: 1, bar: 2
};
let d = {
    foo: 1,
    bar: 2
};
let e = {
    foo: function() {
        dosomething();
    }
};

let {} = obj;
let {f} = obj;
let {g, h} = obj;
let {i,
    j} = obj;
let {k = function() {
    dosomething();
}} = obj;
```
### ImportDeclaration and ExportDeclaration
Examples of incorrect code for this rule with the `{ "ImportDeclaration": "always", "ExportDeclaration": "never" }` options:


```json
/*eslint object-curly-newline: ["error", { "ImportDeclaration": "always", "ExportDeclaration": "never" }]*/
/*eslint-env es6*/

import {foo, bar} from 'foo-bar';
import {foo as f, baz} from 'foo-bar';
import {qux,
    foobar} from 'foo-bar';

export {
   foo,
   bar
};
export {
   foo as f,
   baz
} from 'foo-bar';
```
Examples of correct code for this rule with the `{ "ImportDeclaration": "always", "ExportDeclaration": "never" }` options:


```json
/*eslint object-curly-newline: ["error", { "ImportDeclaration": "always", "ExportDeclaration": "never" }]*/
/*eslint-env es6*/

import {
    foo,
    bar
} from 'foo-bar';
import {
    baz, qux
} from 'foo-bar';
import {
    foo as f,
    foobar
} from 'foo-bar';

export { foo, bar } from 'foo-bar';
export { foo as f, baz } from 'foo-bar';
```
## When Not To Use It
If you don’t want to enforce consistent line breaks after opening and before closing braces, then it’s safe to disable this rule.
## Compatibility

JSCS: requirePaddingNewLinesInObjects 
JSCS: disallowPaddingNewLinesInObjects 

## Related Rules


comma-spacing 

key-spacing 

object-curly-spacing 

object-property-newline 


## Version
This rule was introduced in ESLint v2.12.0.
## Resources

Rule source 
Tests source 
