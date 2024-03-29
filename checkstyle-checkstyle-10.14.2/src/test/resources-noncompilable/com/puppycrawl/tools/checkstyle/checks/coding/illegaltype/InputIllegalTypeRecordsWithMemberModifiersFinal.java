/*
IllegalType
validateAbstractClassNames = (default)false
illegalClassNames = (default)HashMap, HashSet, LinkedHashMap, LinkedHashSet, TreeMap, TreeSet, \
                    java.util.HashMap, java.util.HashSet, java.util.LinkedHashMap, \
                    java.util.LinkedHashSet, java.util.TreeMap, java.util.TreeSet
legalAbstractClassNames = (default)
ignoredMethodNames = (default)getEnvironment, getInitialContext
illegalAbstractClassNameFormat = (default)^(.*[.])?Abstract.*$
memberModifiers = FINAL
tokens = (default)ANNOTATION_FIELD_DEF, CLASS_DEF, INTERFACE_DEF, METHOD_CALL, METHOD_DEF, \
         METHOD_REF, PARAMETER_DEF, VARIABLE_DEF, PATTERN_VARIABLE_DEF, RECORD_DEF, \
         RECORD_COMPONENT_DEF


*/

//non-compiled with javac: Compilable with Java14
package com.puppycrawl.tools.checkstyle.checks.coding.illegaltype;

import java.util.*;

public class InputIllegalTypeRecordsWithMemberModifiersFinal
{

    public record IdentifiersPair(
        UUID productId,
        String identifier
    )
    {

    }

    public class IdentifiersPairEquivalent {
        private final UUID productId;
        private final String identifier;

        public IdentifiersPairEquivalent(UUID productId, String identifier) {
            this.productId = productId;
            this.identifier = identifier;
        }
    }

    public record IdentifiersPair2(
        HashSet x, // violation
        String identifier
    )
    {

    }

    public class IdentifiersPairEquivalent2 {
        private final HashSet x; // violation
        private final String identifier;

        public IdentifiersPairEquivalent2(Set x, String identifier) {
            this.x = (HashSet) x;
            this.identifier = identifier;
        }
    }

}
