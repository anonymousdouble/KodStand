import globals from "globals";
import googleConfig from "eslint-config-google"
// import pluginJs from "@eslint/js";

export default [
  {languageOptions: { globals: {...globals.browser, ...globals.node} }},
  // pluginJs.configs.recommended,
  googleConfig,
  {
    rules:{
      "linebreak-style":off,
    }
  },
];