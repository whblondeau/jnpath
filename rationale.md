## why define and build JNPath?

### declarative programming is a big win
The declarative programming style is highly beneficial.

The overwhelming advantage of declarative programming is that _the programmer needs only to state the desired outcome._ This is very unlike the much more common _imperative_ style of programming, in which the programmer has to state _how_ to achieve that desired result. The practical difference is that declarative languages tend not to have bugs (defining "bug" as "a non-obvious logic problem"). Errors in declarative code tend to be casual blunders, more at the level of "Oh shit, I forgot to stipulate that". Bugs, in the sense I'm using it here, crop up in imperative languages with depressing frequency, largely because programmers must typically invent situational logic on the fly.

Successful declarative languages include SQL and most of the unix command line. Some of the best declarative languages in general use are the XPath technologies: XML Schema, XSLT, XQuery _et al_. All of them depend on the powerful and well-designed XPath node selection notation; which is in turn made possible by the constrained nature of the XML datamodel that it works against. The payoffs are pretty spectacular: the complex data tree transformations produced by XSLT, for example, would be prohibitively costly to reproduce using ad hoc imperative means; and those ad hoc solutions would generally not scale very well if built.

### why not JSON, eh?
Since the JSON datamodel is a much-simplified but still valid subset of the XML datamodel, it would seem to be an obvious move to create, e.g., "JSONPath", "JSONSLT", "JSONQuery" to translate comparable benefits to the JSON data type. It's been tried; unfortunately, worthy efforts to get something going seem to have foundered.

There are many reasons for this, and considering them in any detail is far beyond the scope of this document. However, there are several plausible considerations, which have guided the development of JNPath:

 - The JavaScript developer community has an apparent widespread cultural dislike of all things XML. Avoidance of XML-related concepts and syntax is prudent for any project that hopes to be useful to JavaScript developers.
 
 - When replicating the benefits of XPath, it's not necessary to borrow the syntax by which XPath was implemented. The value of XPath is as a successfully implemented logical model: to be emulated but not literally reproduced.
 
 - XPath explicitly targets the XML datamodel. When replicating the benefits of XPath to JSON, it's important to discard any XPath features (or implicit/embedded logical assumptions) that are not relevant to the JSON datamodel.
 
 - Logical completism is the devil. The W3C was obliged to design and build its specification to a 100% logical standard. A pragmatic logical subset of the XPath-for-JSON problem space is arguably superior to a forced march to that 100%.


