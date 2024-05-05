'''
https://eslint.org/docs/latest/rules/
https://eslint.org/docs/latest/rules/array-callback-return#allowvoid

eslint-8.57.0/docs/src/rules
eslint-8.57.0/docs/src/rules/valid-jsdoc.md

msgs: Rule source
https://github.com/eslint/eslint/blob/main/lib/rules/array-callback-return.js
eslint-8.57.0/lib/rules/array-callback-return.js

code examples ---- test cases: Tests source
https://github.com/eslint/eslint/blob/main/tests/lib/rules/array-callback-return.js
eslint-8.57.0/tests/lib/rules

Google JavaScript style
eslint-config-google-master/index.js
https://github.com/google/eslint-config-google/blob/master/index.js
'''

import os,json
data = []
with open("manual.txt","r",encoding="utf-8") as f:
    data = f.read().split("\n")
res = []
for line in data:
    eslint_rule,google_rule,comment = line.split(",")
    eslint_rule = eslint_rule.strip("\"")
    google_rule = google_rule.strip("\"")
    res.append({
        "eslint_rule":eslint_rule,
        "google_rule":google_rule,
        "comment":comment
    })
with open("manual.json","w",encoding="utf-8") as f:
    json.dump(res,f,indent=4,ensure_ascii=False)
