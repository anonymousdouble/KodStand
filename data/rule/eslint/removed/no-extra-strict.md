

# no-extra-strict
## Overview

Disallows strict mode directives when already in strict mode.

The `"use strict";` directive applies to the scope in which it appears and all inner scopes contained within that scope. Therefore, using the `"use strict";` directive in one of these inner scopes is unnecessary.


```json
"use strict";

(function () {
    "use strict";
    var foo = true;
}());
```

## Rule Details

This rule is aimed at preventing unnecessary `"use strict";` directives. As such, it will warn when it encounters a `"use strict";` directive when already in strict mode.

Example of incorrect code for this rule:


```json
"use strict";

(function () {
    "use strict";
    var foo = true;
}());
```

Examples of correct code for this rule:


```json
"use strict";

(function () {
    var foo = true;
}());
```


```json
(function () {
    "use strict";
    var foo = true;
}());
```


## Version

This rule was introduced in ESLint v0.3.0
                 and removed in v1.0.0-rc-1.

## Further Reading

Annotated ES5 
 es5.github.io


## Replaced by
stric