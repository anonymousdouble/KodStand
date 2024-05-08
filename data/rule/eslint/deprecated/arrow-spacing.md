

# arrow-spacing
## Overview

Enforce consistent spacing before and after the arrow in arrow functions

This rule was deprecated in ESLint v8.53.0. Please use the corresponding rule  in @stylistic/eslint-plugin-js .

This rule normalize style of spacing before/after an arrow function’s arrow(`=>`).


```json
/*eslint-env es6*/

// { "before": true, "after": true }
(a) => {}

// { "before": false, "after": false }
(a)=>{}
```

## Rule Details

This rule takes an object argument with `before` and `after` properties, each with a Boolean value.

The default configuration is `{ "before": true, "after": true }`.

`true` means there should be one or more spaces and `false` means no spaces.

Examples of incorrect code for this rule with the default `{ "before": true, "after": true }` option:


```json
/*eslint arrow-spacing: "error"*/
/*eslint-env es6*/

()=> {};
() =>{};
(a)=> {};
(a) =>{};
a =>a;
a=> a;
()=> {'\n'};
() =>{'\n'};
```

Examples of correct code for this rule with the default `{ "before": true, "after": true }` option:


```json
/*eslint arrow-spacing: "error"*/
/*eslint-env es6*/

() => {};
(a) => {};
a => a;
() => {'\n'};
```

Examples of incorrect code for this rule with the `{ "before": false, "after": false }` option:


```json
/*eslint arrow-spacing: ["error", { "before": false, "after": false }]*/
/*eslint-env es6*/

() =>{};
(a) => {};
()=> {'\n'};
```

Examples of correct code for this rule with the `{ "before": false, "after": false }` option:


```json
/*eslint arrow-spacing: ["error", { "before": false, "after": false }]*/
/*eslint-env es6*/

()=>{};
(a)=>{};
()=>{'\n'};
```

Examples of incorrect code for this rule with the `{ "before": false, "after": true }` option:


```json
/*eslint arrow-spacing: ["error", { "before": false, "after": true }]*/
/*eslint-env es6*/

() =>{};
(a) => {};
()=>{'\n'};
```

Examples of correct code for this rule with the `{ "before": false, "after": true }` option:


```json
/*eslint arrow-spacing: ["error", { "before": false, "after": true }]*/
/*eslint-env es6*/

()=> {};
(a)=> {};
()=> {'\n'};
```


## Version

This rule was introduced in ESLint v1.0.0-rc-1.

## Resources


- Rule source 

- Tests source 

