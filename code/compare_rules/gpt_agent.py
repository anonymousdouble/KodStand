import json
import os
import re
import shutil

from gpt_wrapper import GPTWrapper

prompt='''
Please generate an ESLint configuration based on the following style convention and ESLint rules.

Style Convention:
"Do not use the variadic Array constructor. The constructor is error-prone if arguments are added or removed. Use a literal instead."

ESLint Rules:
Skip to main content

Donate
	•	Team
	•	Blog
	•	Docs
	•	Store
	•	Playground
Selecting a version will take you to the chosen version of the ESLint docs.
Version
            
            HEAD
            
            v9.2.0
            
            v8.57.0
            
        
Selecting a version will take you to the chosen version of the ESLint docs.
Version
            
            HEAD
            
            v9.2.0
            
            v8.57.0
            
        
Index
Search
Results will be shown and updated as you type.



	•	Use ESLint in Your Project
	◦	Getting Started
	◦	Core Concepts
	◦	Configure ESLint
	▪	Configuration Files (New)
	▪	Configuration Files
	▪	Configure Language Options
	▪	Configure Rules
	▪	Configure Plugins
	▪	Configure a Parser
	▪	Ignore Files
	▪	Configuration Migration Guide
	◦	Command Line Interface Reference
	◦	Rules Reference
	◦	Formatters Reference
	◦	Integrations
	◦	Migrate to v8.x
	•	Extend ESLint
	◦	Ways to Extend ESLint
	◦	Create Plugins
	▪	Custom Rule Tutorial
	▪	Custom Rules
	▪	Custom Processors
	▪	Migration to Flat Config
	◦	Share Configurations
	◦	Custom Formatters
	◦	Custom Parsers
	•	integrate ESLint
	◦	Integrate with the Node.js API Tutorial
	◦	Node.js API Reference
	•	Contribute to ESLint
	◦	Code of Conduct
	◦	Report Bugs
	◦	Propose a New Rule
	◦	Propose a Rule Change
	◦	Request a Change
	◦	Architecture
	◦	Set up a Development Environment
	◦	Run the Tests
	◦	Package.json Conventions
	◦	Work on Issues
	◦	Submit a Pull Request
	◦	Contribute to Core Rules
	◦	Governance
	◦	Report a Security Vulnerability
	•	Maintain ESLint
	◦	How ESLint is Maintained
	◦	Manage Issues and Pull Requests
	◦	Review Pull Requests
	◦	Manage Releases
	◦	Working Groups
Rules Reference
Table of Contents
	1	Possible Problems
	2	Suggestions
	3	Layout & Formatting
	4	Deprecated
	5	Removed
Rules in ESLint are grouped by type to help you understand their purpose. Each rule has emojis denoting:
✅ Recommended
The "extends": "eslint:recommended" property in a configuration file enables this rule
🔧 Fixable
Some problems reported by this rule are automatically fixable by the --fix command line option
💡 hasSuggestions
Some problems reported by this rule are manually fixable by editor suggestions
Possible Problems
These rules relate to possible logic errors in code:
array-callback-return
Enforce return statements in callbacks of array methods
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
constructor-super
Require super() calls in constructors
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
for-direction
Enforce “for” loop update clause moving the counter in the right direction
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
getter-return
Enforce return statements in getters
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-async-promise-executor
Disallow using an async function as a Promise executor
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-await-in-loop
Disallow await inside of loops
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-class-assign
Disallow reassigning class members
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-compare-neg-zero
Disallow comparing against -0
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-cond-assign
Disallow assignment operators in conditional expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-const-assign
Disallow reassigning const variables
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-constant-binary-expression
Disallow expressions where the operation doesn’t affect the value
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-constant-condition
Disallow constant expressions in conditions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-constructor-return
Disallow returning value from constructor
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-control-regex
Disallow control characters in regular expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-debugger
Disallow the use of debugger
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-dupe-args
Disallow duplicate arguments in function definitions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-dupe-class-members
Disallow duplicate class members
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-dupe-else-if
Disallow duplicate conditions in if-else-if chains
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-dupe-keys
Disallow duplicate keys in object literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-duplicate-case
Disallow duplicate case labels
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-duplicate-imports
Disallow duplicate module imports
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-empty-character-class
Disallow empty character classes in regular expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-empty-pattern
Disallow empty destructuring patterns
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-ex-assign
Disallow reassigning exceptions in catch clauses
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-fallthrough
Disallow fallthrough of case statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-func-assign
Disallow reassigning function declarations
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-import-assign
Disallow assigning to imported bindings
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-inner-declarations
Disallow variable or function declarations in nested blocks
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-invalid-regexp
Disallow invalid regular expression strings in RegExp constructors
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-irregular-whitespace
Disallow irregular whitespace
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-loss-of-precision
Disallow literal numbers that lose precision
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-misleading-character-class
Disallow characters which are made with multiple code points in character class syntax
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-new-native-nonconstructor
Disallow new operators with global non-constructor functions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-new-symbol
Disallow new operators with the Symbol object
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-obj-calls
Disallow calling global object properties as functions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-promise-executor-return
Disallow returning values from Promise executor functions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-prototype-builtins
Disallow calling some Object.prototype methods directly on objects
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-self-assign
Disallow assignments where both sides are exactly the same
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-self-compare
Disallow comparisons where both sides are exactly the same
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-setter-return
Disallow returning values from setters
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-sparse-arrays
Disallow sparse arrays
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-template-curly-in-string
Disallow template literal placeholder syntax in regular strings
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-this-before-super
Disallow this/super before calling super() in constructors
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-undef
Disallow the use of undeclared variables unless mentioned in /*global */ comments
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unexpected-multiline
Disallow confusing multiline expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unmodified-loop-condition
Disallow unmodified loop conditions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unreachable
Disallow unreachable code after return, throw, continue, and break statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unreachable-loop
Disallow loops with a body that allows only one iteration
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unsafe-finally
Disallow control flow statements in finally blocks
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unsafe-negation
Disallow negating the left operand of relational operators
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unsafe-optional-chaining
Disallow use of optional chaining in contexts where the undefined value is not allowed
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unused-private-class-members
Disallow unused private class members
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unused-vars
Disallow unused variables
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-use-before-define
Disallow the use of variables before they are defined
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-backreference
Disallow useless backreferences in regular expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
require-atomic-updates
Disallow assignments that can lead to race conditions due to usage of await or yield
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
use-isnan
Require calls to isNaN() when checking for NaN
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
valid-typeof
Enforce comparing typeof expressions against valid strings
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
Suggestions

These rules suggest alternate ways of doing things:
accessor-pairs
Enforce getter and setter pairs in objects and classes
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
arrow-body-style
Require braces around arrow function bodies
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
block-scoped-var
Enforce the use of variables within the scope they are defined
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
camelcase
Enforce camelcase naming convention
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
capitalized-comments
Enforce or disallow capitalization of the first letter of a comment
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
class-methods-use-this
Enforce that class methods utilize this
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
complexity
Enforce a maximum cyclomatic complexity allowed in a program
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
consistent-return
Require return statements to either always or never specify values
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
consistent-this
Enforce consistent naming when capturing the current execution context
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
curly
Enforce consistent brace style for all control statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
default-case
Require default cases in switch statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
default-case-last
Enforce default clauses in switch statements to be last
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
default-param-last
Enforce default parameters to be last
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
dot-notation
Enforce dot notation whenever possible
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
eqeqeq
Require the use of === and !==
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
func-name-matching
Require function names to match the name of the variable or property to which they are assigned
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
func-names
Require or disallow named function expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
func-style
Enforce the consistent use of either function declarations or expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
grouped-accessor-pairs
Require grouped accessor pairs in object literals and classes
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
guard-for-in
Require for-in loops to include an if statement
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
id-denylist
Disallow specified identifiers
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
id-length
Enforce minimum and maximum identifier lengths
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
id-match
Require identifiers to match a specified regular expression
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
init-declarations
Require or disallow initialization in variable declarations
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
logical-assignment-operators
Require or disallow logical assignment operator shorthand
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
max-classes-per-file
Enforce a maximum number of classes per file
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
max-depth
Enforce a maximum depth that blocks can be nested
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
max-lines
Enforce a maximum number of lines per file
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
max-lines-per-function
Enforce a maximum number of lines of code in a function
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
max-nested-callbacks
Enforce a maximum depth that callbacks can be nested
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
max-params
Enforce a maximum number of parameters in function definitions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
max-statements
Enforce a maximum number of statements allowed in function blocks
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
multiline-comment-style
Enforce a particular style for multiline comments
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
new-cap
Require constructor names to begin with a capital letter
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-alert
Disallow the use of alert, confirm, and prompt
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-array-constructor
Disallow Array constructors
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-bitwise
Disallow bitwise operators
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-caller
Disallow the use of arguments.caller or arguments.callee
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-case-declarations
Disallow lexical declarations in case clauses
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-console
Disallow the use of console
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-continue
Disallow continue statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-delete-var
Disallow deleting variables
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-div-regex
Disallow equal signs explicitly at the beginning of regular expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-else-return
Disallow else blocks after return statements in if statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-empty
Disallow empty block statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-empty-function
Disallow empty functions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-empty-static-block
Disallow empty static blocks
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-eq-null
Disallow null comparisons without type-checking operators
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-eval
Disallow the use of eval()
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-extend-native
Disallow extending native types
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-extra-bind
Disallow unnecessary calls to .bind()
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-extra-boolean-cast
Disallow unnecessary boolean casts
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-extra-label
Disallow unnecessary labels
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-global-assign
Disallow assignments to native objects or read-only global variables
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-implicit-coercion
Disallow shorthand type conversions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-implicit-globals
Disallow declarations in the global scope
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-implied-eval
Disallow the use of eval()-like methods
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-inline-comments
Disallow inline comments after code
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-invalid-this
Disallow use of this in contexts where the value of this is undefined
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-iterator
Disallow the use of the __iterator__ property
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-label-var
Disallow labels that share a name with a variable
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-labels
Disallow labeled statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-lone-blocks
Disallow unnecessary nested blocks
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-lonely-if
Disallow if statements as the only statement in else blocks
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-loop-func
Disallow function declarations that contain unsafe references inside loop statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-magic-numbers
Disallow magic numbers
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-multi-assign
Disallow use of chained assignment expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-multi-str
Disallow multiline strings
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-negated-condition
Disallow negated conditions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-nested-ternary
Disallow nested ternary expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-new
Disallow new operators outside of assignments or comparisons
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-new-func
Disallow new operators with the Function object
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-new-wrappers
Disallow new operators with the String, Number, and Boolean objects
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-nonoctal-decimal-escape
Disallow &#92;8 and &#92;9 escape sequences in string literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-object-constructor
Disallow calls to the Object constructor without an argument
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-octal
Disallow octal literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-octal-escape
Disallow octal escape sequences in string literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-param-reassign
Disallow reassigning function parameters
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-plusplus
Disallow the unary operators ++ and --
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-proto
Disallow the use of the __proto__ property
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-redeclare
Disallow variable redeclaration
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-regex-spaces
Disallow multiple spaces in regular expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-restricted-exports
Disallow specified names in exports
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-restricted-globals
Disallow specified global variables
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-restricted-imports
Disallow specified modules when loaded by import
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-restricted-properties
Disallow certain properties on certain objects
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-restricted-syntax
Disallow specified syntax
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-return-assign
Disallow assignment operators in return statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-script-url
Disallow javascript: urls
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-sequences
Disallow comma operators
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-shadow
Disallow variable declarations from shadowing variables declared in the outer scope
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-shadow-restricted-names
Disallow identifiers from shadowing restricted names
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-ternary
Disallow ternary operators
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-throw-literal
Disallow throwing literals as exceptions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-undef-init
Disallow initializing variables to undefined
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-undefined
Disallow the use of undefined as an identifier
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-underscore-dangle
Disallow dangling underscores in identifiers
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unneeded-ternary
Disallow ternary operators when simpler alternatives exist
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unused-expressions
Disallow unused expressions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-unused-labels
Disallow unused labels
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-call
Disallow unnecessary calls to .call() and .apply()
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-catch
Disallow unnecessary catch clauses
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-computed-key
Disallow unnecessary computed property keys in objects and classes
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-concat
Disallow unnecessary concatenation of literals or template literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-constructor
Disallow unnecessary constructors
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-escape
Disallow unnecessary escape characters
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-rename
Disallow renaming import, export, and destructured assignments to the same name
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-useless-return
Disallow redundant return statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-var
Require let or const instead of var
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-void
Disallow void operators
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-warning-comments
Disallow specified warning terms in comments
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
no-with
Disallow with statements
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
object-shorthand
Require or disallow method and property shorthand syntax for object literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
one-var
Enforce variables to be declared either together or separately in functions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
operator-assignment
Require or disallow assignment operator shorthand where possible
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-arrow-callback
Require using arrow functions for callbacks
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-const
Require const declarations for variables that are never reassigned after declared
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-destructuring
Require destructuring from arrays and/or objects
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-exponentiation-operator
Disallow the use of Math.pow in favor of the ** operator
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-named-capture-group
Enforce using named capture group in regular expression
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-numeric-literals
Disallow parseInt() and Number.parseInt() in favor of binary, octal, and hexadecimal literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-object-has-own
Disallow use of Object.prototype.hasOwnProperty.call() and prefer use of Object.hasOwn()
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-object-spread
Disallow using Object.assign with an object literal as the first argument and prefer the use of object spread instead
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-promise-reject-errors
Require using Error objects as Promise rejection reasons
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-regex-literals
Disallow use of the RegExp constructor in favor of regular expression literals
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-rest-params
Require rest parameters instead of arguments
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-spread
Require spread operators instead of .apply()
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
prefer-template
Require template literals instead of string concatenation
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
radix
Enforce the consistent use of the radix argument when using parseInt()
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
require-await
Disallow async functions which have no await expression
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
require-unicode-regexp
Enforce the use of u or v flag on RegExp
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
require-yield
Require generator functions to contain yield
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
sort-imports
Enforce sorted import declarations within modules
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
sort-keys
Require object keys to be sorted
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
sort-vars
Require variables within the same declaration block to be sorted
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
strict
Require or disallow strict mode directives
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
symbol-description
Require symbol descriptions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
vars-on-top
Require var declarations be placed at the top of their containing scope
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
yoda
Require or disallow “Yoda” conditions
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
Layout & Formatting

These rules care about how the code looks rather than how it executes:
line-comment-position
Enforce position of line comments
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
unicode-bom
Require or disallow Unicode byte order mark (BOM)
Categories:
✅ Extends
🔧 Fix
💡 Suggestions
Deprecated

These rules have been deprecated in accordance with the deprecation policy, and replaced by newer rules:
array-bracket-newline deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
array-bracket-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
array-element-newline deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
arrow-parens deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
arrow-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
block-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
brace-style deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
callback-return deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
comma-dangle deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
comma-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
comma-style deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
computed-property-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
dot-location deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
eol-last deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
func-call-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
function-call-argument-newline deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
function-paren-newline deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
generator-star-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
global-require deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
handle-callback-err deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
id-blacklist deprecated
Replaced by id-denylist
Categories:
❌
🔧 Fix
💡 Suggestions
implicit-arrow-linebreak deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
indent deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
indent-legacy deprecated
Replaced by indent
Categories:
❌
🔧 Fix
💡 Suggestions
jsx-quotes deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
key-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
keyword-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
linebreak-style deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
lines-around-comment deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
lines-around-directive deprecated
Replaced by padding-line-between-statements
Categories:
❌
🔧 Fix
💡 Suggestions
lines-between-class-members deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
max-len deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
max-statements-per-line deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
multiline-ternary deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
new-parens deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
newline-after-var deprecated
Replaced by padding-line-between-statements
Categories:
❌
🔧 Fix
💡 Suggestions
newline-before-return deprecated
Replaced by padding-line-between-statements
Categories:
❌
🔧 Fix
💡 Suggestions
newline-per-chained-call deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-buffer-constructor deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-catch-shadow deprecated
Replaced by no-shadow
Categories:
❌
🔧 Fix
💡 Suggestions
no-confusing-arrow deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-extra-parens deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-extra-semi deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-floating-decimal deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-mixed-operators deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-mixed-requires deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-mixed-spaces-and-tabs deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-multi-spaces deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-multiple-empty-lines deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-native-reassign deprecated
Replaced by no-global-assign
Categories:
❌
🔧 Fix
💡 Suggestions
no-negated-in-lhs deprecated
Replaced by no-unsafe-negation
Categories:
❌
🔧 Fix
💡 Suggestions
no-new-object deprecated
Replaced by no-object-constructor
Categories:
❌
🔧 Fix
💡 Suggestions
no-new-require deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-path-concat deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-process-env deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-process-exit deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-restricted-modules deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-return-await deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-spaced-func deprecated
Replaced by func-call-spacing
Categories:
❌
🔧 Fix
💡 Suggestions
no-sync deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-tabs deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-trailing-spaces deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
no-whitespace-before-property deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
nonblock-statement-body-position deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
object-curly-newline deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
object-curly-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
object-property-newline deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
one-var-declaration-per-line deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
operator-linebreak deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
padded-blocks deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
padding-line-between-statements deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
prefer-reflect deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
quote-props deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
quotes deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
require-jsdoc deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
rest-spread-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
semi deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
semi-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
semi-style deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
space-before-blocks deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
space-before-function-paren deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
space-in-parens deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
space-infix-ops deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
space-unary-ops deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
spaced-comment deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
switch-colon-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
template-curly-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
template-tag-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
valid-jsdoc deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
wrap-iife deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
wrap-regex deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
yield-star-spacing deprecated

Categories:
❌
🔧 Fix
💡 Suggestions
Removed

These rules from older versions of ESLint (before the deprecation policy existed) have been replaced by newer rules:
generator-star removed
Replaced by generator-star-spacing
global-strict removed
Replaced by strict
no-arrow-condition removed
Replaced by no-confusing-arrowno-constant-condition
no-comma-dangle removed
Replaced by comma-dangle
no-empty-class removed
Replaced by no-empty-character-class
no-empty-label removed
Replaced by no-labels
no-extra-strict removed
Replaced by strict
no-reserved-keys removed
Replaced by quote-props
no-space-before-semi removed
Replaced by semi-spacing
no-wrap-func removed
Replaced by no-extra-parens
space-after-function-name removed
Replaced by space-before-function-paren
space-after-keywords removed
Replaced by keyword-spacing
space-before-function-parentheses removed
Replaced by space-before-function-paren
space-before-keywords removed
Replaced by keyword-spacing
space-in-brackets removed
Replaced by object-curly-spacingarray-bracket-spacing
space-return-throw-case removed
Replaced by keyword-spacing
space-unary-word-ops removed
Replaced by space-unary-ops
spaced-line-comment removed
Replaced by spaced-comment

Edit this page
￼
Neurelo's AI-Powered instant auto-generated REST and GraphQL APIs for MongoDB & Postgres. Get started
Ads by EthicalAds
Table of Contents
	1	Possible Problems
	2	Suggestions
	3	Layout & Formatting
	4	Deprecated
	5	Removed
	•	
	•	
	•	
	•	
© OpenJS Foundation and ESLint contributors, www.openjsf.org. Content licensed under MIT License.
Theme Switcher
Light Dark
Selecting a language will take you to the ESLint website in that language.
Language
            
            
                🇺🇸 English (US)
                
            
            
            
                🇨🇳 简体中文
                (最新)
            
            
        


Response Format Should be a json object:
{
    "Answer": You respond with Yes or No for whether exists an ESLint configuration for the given style convention,
    
    "Configuration": [

        rule-name1: [
            'error', 
            {
                option1: value1,
                ...
                optionn: valuen
            }
        ],
        ...
        rule-namen: [
            'error',
            {
                option1: value1,
                ...
                optionn: valuen
            }
        ]
    ]
}

'''
class CoTPatterns:
    MAPPING_TASK = [
        {
            "role": "user",
            "content": "Given a rule:\n\nquotes\n\nCan you find a corresponding rule in the following rule set?\n\nNested functions and closures\nUse single quotes\nNo line continuations",
        },
        {
            "role": "assistant",
            "content": "Use single quotes",
        },
        {
            "role": "user",
            "content": "Given a rule:\n\lines-around-directive\n\nCan you find a corresponding rule in the following rule set?\n\nNested functions and closures\nUse single quotes\nNo line continuations",
        },
        {
            "role": "assistant",
            "content": "No matching rule in the rule set",
        },
    ]


class GPTAgent:

    def __init__(self):
        self.wrapper = GPTWrapper.get_wrapper()
        # self.rule_set_root1 = "data\\rule\\google\\jsguide.json"
        # self.rule_set_root2 = "data\\rule\\eslint"

    def compare_rules_simple(self, rule: str):
        eslint_rules_simple = ""
        simple_path = "data\\rule\\eslint\\overview.md"
        with open(simple_path, 'r', encoding='utf-8') as f:
            eslint_rules_simple = f.read()

        if len(eslint_rules_simple) > 0:
            question = "Given a rule:\n\n"
            question += rule
            question += "\n\nCan you find a corresponding rule in the following rule set?\n\n"
            question += eslint_rules_simple
            answer = self.wrapper.ask(question)
            print(answer)

    def e2g(self, rule):
        if not hasattr(self, 'titles'):
            self.google_rules = []
            with open("data\\rule\\google\\jsguide.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for r in data:
                    self.google_rules.append(r)
            self.titles = [" ".join(case["title"].split()[1:])
                           for case in self.google_rules if len(case["cases"]) > 0]

        question = "Given a rule:\n\n"
        question += rule
        question += "\n\nCan you find a corresponding rule in the following rule set?\n\n"

        question += '\n'.join(self.titles)

        question += "\n\n Only provide the most likely option."

        try:
            answer = self.wrapper.ask(question)
            print(answer)
        except Exception as e:
            print(e)
            return None
        # print(answer)
        for t in self.titles:
            if t in answer:
                return t

        return None


if __name__ == "__main__":
    agent = GPTAgent()
    # rule_desc = "Do not use the variadic Array constructor. The constructor is error-prone if arguments are added or removed. Use a literal instead."
    # agent.compare_rules_simple(rule_desc)
    rules = []
    with open("data\\config\\eslint\\google_config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for r in data:
            rules.append(f"{r}")

    res = {}
    for r in rules:
        print(f"finding mapping of rule: {r}")
        correspond_rule = agent.e2g(r)
        print(f"corresponding rule is : {correspond_rule}")
        if correspond_rule is not None:
            res[r] = correspond_rule
        else:
            res[r] = None
        break
    # with open("output.json", "w", encoding="utf-8") as f:
    #     json.dump(res, f, ensure_ascii=False, indent=4)
