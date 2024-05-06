
# no-misleading-character-class
## Overview
Disallow characters which are made with multiple code points in character class syntax


✅ Recommended

            The `"extends": "eslint:recommended"` property in a configuration file  enables this rule
        

💡 hasSuggestions

            Some problems reported by this rule are manually fixable by editor suggestions 



Unicode includes the characters which are made with multiple code points.
RegExp character class syntax (`/[abc]/`) cannot handle characters which are made by multiple code points as a character; those characters will be dissolved to each code point. For example, `❇️` is made by `❇` (`U+2747`) and VARIATION SELECTOR-16 (`U+FE0F`). If this character is in RegExp character class, it will match to either `❇` (`U+2747`) or VARIATION SELECTOR-16 (`U+FE0F`) rather than `❇️`.
This rule reports the regular expressions which include multiple code point characters in character class syntax. This rule considers the following characters as multiple code point characters.
A character with combining characters:
The combining characters are characters which belong to one of `Mc`, `Me`, and `Mn` Unicode general categories .

```json
/^[Á]$/u.test("Á"); //→ false
/^[❇️]$/u.test("❇️"); //→ false
```
A character with Emoji modifiers:

```json
/^[👶🏻]$/u.test("👶🏻"); //→ false
/^[👶🏽]$/u.test("👶🏽"); //→ false
```
A pair of regional indicator symbols:

```json
/^[🇯🇵]$/u.test("🇯🇵"); //→ false
```
Characters that ZWJ joins:

```json
/^[👨‍👩‍👦]$/u.test("👨‍👩‍👦"); //→ false
```
A surrogate pair without Unicode flag:

```json
/^[👍]$/.test("👍"); //→ false

// Surrogate pair is OK if with u flag.
/^[👍]$/u.test("👍"); //→ true
```
## Rule Details
This rule reports the regular expressions which include multiple code point characters in character class syntax.
Examples of incorrect code for this rule:


```json
/*eslint no-misleading-character-class: error */

/^[Á]$/u;
/^[❇️]$/u;
/^[👶🏻]$/u;
/^[🇯🇵]$/u;
/^[👨‍👩‍👦]$/u;
/^[👍]$/;
```
Examples of correct code for this rule:


```json
/*eslint no-misleading-character-class: error */

/^[abc]$/;
/^[👍]$/u;
/^[\q{👶🏻}]$/v;
```
## When Not To Use It
You can turn this rule off if you don’t want to check RegExp character class syntax for multiple code point characters.
## Version
This rule was introduced in ESLint v5.3.0.
## Resources

Rule source 
Tests source 
