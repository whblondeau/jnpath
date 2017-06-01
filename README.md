# jnpath
_tl;dr: a lightweight, ad-hoc toolkit that **unambitiously** provides minimal XPATH/XSLT-like declarative capability for JSON._

## why
### XPath-like benefits for JSON
The declarative programming style is highly beneficial. Some of the best declarative languages are the XPath technologies: XSLT and XQuery. Since the JSON datamodel is a much-simplified but still valid subset of the XML datamodel, it would seem to be an obvious move to create, e.g., "JSONPath", "JSONSLT", "JSONQuery" to translate the benefits to the JavaScript world. Unfortunately, worthy efforts to get something going seem to have foundered.

### 80% solution
One common failing of projects that try to provide broad support is that they compulsively attempt to bring all the things. This runs up hard against the general principle that "if the first 90% takes eight months, the second 90% will take fifteen months." JNPath is defined, from the outset, as a sort of Pareto solution.
