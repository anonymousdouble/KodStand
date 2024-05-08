

# prefer-reflect
## Overview

Require `Reflect` methods where applicable

This rule was deprecated in ESLint v3.9.0 and will not be replaced. The original intent of this rule now seems misguided as we have come to understand that `Reflect` methods are not actually intended to replace the `Object` counterparts the rule suggests, but rather exist as low-level primitives to be used with proxies in order to replicate the default behavior of various previously existing functionality.

Please note: This rule contains an incorrect behavior - it will suggest you to use `Reflect.getOwnPropertyNames` rather than `Object.getOwnPropertyNames`, but the former one doesn’t exist in the specification . We suggest using the `exceptions` option with `"getOwnPropertyNames"` to avoid this false suggestion.

The ES6 Reflect API comes with a handful of methods which somewhat deprecate methods on old constructors:


- Reflect.apply  effectively deprecates Function.prototype.apply  and Function.prototype.call 

- Reflect.deleteProperty  effectively deprecates the delete keyword 

- Reflect.getOwnPropertyDescriptor  effectively deprecates Object.getOwnPropertyDescriptor 

- Reflect.getPrototypeOf  effectively deprecates Object.getPrototypeOf 

- Reflect.setPrototypeOf  effectively deprecates Object.setPrototypeOf 

- Reflect.preventExtensions   effectively deprecates Object.preventExtensions 

The prefer-reflect rule will flag usage of any older method, suggesting to instead use the newer Reflect version.

## Rule Details

## Options

### Exceptions


```json
"prefer-reflect": [<enabled>, { "exceptions": [<...exceptions>] }]
```

The `exceptions` option allows you to pass an array of methods names you’d like to continue to use in the old style.

For example if you wish to use all Reflect methods, except for `Function.prototype.apply` then your config would look like `prefer-reflect: [2, { "exceptions": ["apply"] }]`.

If you want to use Reflect methods, but keep using the `delete` keyword, then your config would look like `prefer-reflect: [2, { "exceptions": ["delete"] }]`.

These can be combined as much as you like. To make all methods exceptions (thereby rendering this rule useless), use `prefer-reflect: [2, { "exceptions": ["apply", "call", "defineProperty", "getOwnPropertyDescriptor", "getPrototypeOf", "setPrototypeOf", "isExtensible", "getOwnPropertyNames", "preventExtensions", "delete"] }]`

### Reflect.apply

Deprecates `Function.prototype.apply()` and `Function.prototype.call()`

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

myFunction.apply(undefined, args);
myFunction.apply(null, args);
obj.myMethod.apply(obj, args);
obj.myMethod.apply(other, args);

myFunction.call(undefined, arg);
myFunction.call(null, arg);
obj.myMethod.call(obj, arg);
obj.myMethod.call(other, arg);
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Reflect.apply(myFunction, undefined, args);
Reflect.apply(myFunction, null, args);
Reflect.apply(obj.myMethod, obj, args);
Reflect.apply(obj.myMethod, other, args);
Reflect.apply(myFunction, undefined, [arg]);
Reflect.apply(myFunction, null, [arg]);
Reflect.apply(obj.myMethod, obj, [arg]);
Reflect.apply(obj.myMethod, other, [arg]);
```

Examples of correct code for this rule with the `{ "exceptions": ["apply"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["apply"] }]*/

// in addition to Reflect.apply(...):
myFunction.apply(undefined, args);
myFunction.apply(null, args);
obj.myMethod.apply(obj, args);
obj.myMethod.apply(other, args);
```

Examples of correct code for this rule with the `{ "exceptions": ["call"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["call"] }]*/

// in addition to Reflect.apply(...):
myFunction.call(undefined, arg);
myFunction.call(null, arg);
obj.myMethod.call(obj, arg);
obj.myMethod.call(other, arg);
```

### Reflect.defineProperty

Deprecates `Object.defineProperty()`

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Object.defineProperty({}, 'foo', {value: 1})
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Reflect.defineProperty({}, 'foo', {value: 1})
```

Examples of correct code for this rule with the `{ "exceptions": ["defineProperty"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["defineProperty"] }]*/

Object.defineProperty({}, 'foo', {value: 1})
Reflect.defineProperty({}, 'foo', {value: 1})
```

### Reflect.getOwnPropertyDescriptor

Deprecates `Object.getOwnPropertyDescriptor()`

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Object.getOwnPropertyDescriptor({}, 'foo')
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Reflect.getOwnPropertyDescriptor({}, 'foo')
```

Examples of correct code for this rule with the `{ "exceptions": ["getOwnPropertyDescriptor"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["getOwnPropertyDescriptor"] }]*/

Object.getOwnPropertyDescriptor({}, 'foo')
Reflect.getOwnPropertyDescriptor({}, 'foo')
```

### Reflect.getPrototypeOf

Deprecates `Object.getPrototypeOf()`

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Object.getPrototypeOf({}, 'foo')
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Reflect.getPrototypeOf({}, 'foo')
```

Examples of correct code for this rule with the `{ "exceptions": ["getPrototypeOf"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["getPrototypeOf"] }]*/

Object.getPrototypeOf({}, 'foo')
Reflect.getPrototypeOf({}, 'foo')
```

### Reflect.setPrototypeOf

Deprecates `Object.setPrototypeOf()`

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Object.setPrototypeOf({}, Object.prototype)
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Reflect.setPrototypeOf({}, Object.prototype)
```

Examples of correct code for this rule with the `{ "exceptions": ["setPrototypeOf"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["setPrototypeOf"] }]*/

Object.setPrototypeOf({}, Object.prototype)
Reflect.setPrototypeOf({}, Object.prototype)
```

### Reflect.isExtensible

Deprecates `Object.isExtensible`

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Object.isExtensible({})
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Reflect.isExtensible({})
```

Examples of correct code for this rule with the `{ "exceptions": ["isExtensible"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["isExtensible"] }]*/

Object.isExtensible({})
Reflect.isExtensible({})
```

### Reflect.preventExtensions

Deprecates `Object.preventExtensions()`

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Object.preventExtensions({})
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

Reflect.preventExtensions({})
```

Examples of correct code for this rule with the `{ "exceptions": ["preventExtensions"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["preventExtensions"] }]*/

Object.preventExtensions({})
Reflect.preventExtensions({})
```

### Reflect.deleteProperty

Deprecates the `delete` keyword

Examples of incorrect code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

delete foo.bar; // deleting object property
```

Examples of correct code for this rule when used without exceptions:


```json
/*eslint prefer-reflect: "error"*/

delete bar; // deleting variable
Reflect.deleteProperty(foo, 'bar');
```

Note: For a rule preventing deletion of variables, see no-delete-var instead 

Examples of correct code for this rule with the `{ "exceptions": ["delete"] }` option:


```json
/*eslint prefer-reflect: ["error", { "exceptions": ["delete"] }]*/

delete bar
delete foo.bar
Reflect.deleteProperty(foo, 'bar');
```

## When Not To Use It

This rule should not be used in ES3/5 environments.

In ES2015 (ES6) or later, if you don’t want to be notified about places where Reflect could be used, you can safely disable this rule.

## Related Rules


- 
no-useless-call 

- 
prefer-spread 

- 
no-delete-var 

## Version

This rule was introduced in ESLint v1.0.0-rc-2.

## Resources


- Rule source 

- Tests source 

