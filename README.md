# jnpath
_TL;DR:_ 

_A lightweight, ad-hoc toolkit that **unambitiously** provides minimal XPath-like declarative capability for JSON._

_A JNPath pattern expression (`jnpattern`) is a match expression. Pattern notation is a superset of JSON path notation, with additional matching syntax based closely on JSON path notation._

_The fundamental operation of JNPath is the matching of a JSON instance node to a `jnpattern`._

_JNPath includes reciprocal operations for:_
 - _decomposing a JSON object into a set of instance paths, and_
 - _composing a set of instance paths into a JSON object._
_This provides a straightforward utility for applying `jnpattern` tests to any JSON object, and composing new JSON objects out of any set of generated paths._

## `jnpattern` examples

`['stores']['*parrot'][*]`                  get all child nodes of any child of the  
                                            "stores" top-level node, whose name ends
                                            in "parrot"

`['stores'][**]['inventory'][*]`            get any child nodes of any "inventory"   
                                            descendants of the "stores" top-level node

`['student'](['first_name'] == 'Ann')[*]`   get the enture contents of every "student"
                                            record where the record's "first_name"
                                            property has a value of "Ann"

`[0]`                                       get the first top-level element of a JSON
                                            array object

`[-2]`                                      get the next to last top-level element
                                            of a JSON array object

`[**](['herp'] == 'derp')`                  get all nodes in the JSON object for
                                            which the "herp" property has a value
                                            of "derp"

`['books'][](no ['donor'])`                 get any nodes from the "books" top-level
                                            array that have no "donor" property

`['books'][](yes ['donor'])`                get any nodes from the "books" top-level
                                            array that do have a "donor" property
                                            (irrespective of "donor"'s value or
                                            lack of value)

`['books'][](falsy ['donor'])`              get any nodes from the "books" top-level
                                            array that have a "donor" property whose
                                            value is falsy `(null`, empty string,
                                            boolean `false`, etc)

`['books'][](empty ['donor'])`              get any nodes from the "books" top-level
                                            array that have a "donor" property whose
                                            value is an empty object or array

`['album']['tracks'][3][*]`                 get the fourth node from the "tracks" array 
                                            in the "album" top-level object

`['album']['tracks'][-1][*]`                get the last node from the "tracks" array
                                            in the "album" top-level object

`['album']['tracks'][2:7][*]`               get the third through seventh node from the  
                                            "tracks" array in the "album" top-level object

`['album']['tracks'][3, 5, 8][*]`           get the fourth, sixth, and ninth nodes from the  
                                            "tracks" array in the "album" top-level object

`['album']['tracks'][1:-1][*]`              get all nodes _except_ the first and last from
                                            the "tracks" array in the "album" top-level
                                            object

`[*]`                                       get all top-level nodes of a JSON object

----
## why
### declarative programming
The declarative programming style is highly beneficial. The overwhelming advantage of declarative programming is that _the programmer needs only to state the desired outcome._ This is very unlike the much more common _imperative_ style of programming, in which the programmer has to state _how_ to achieve that desired result. The practical difference is that declarative languages tend not to have bugs (defining "bug" as "a non-obvious logic problem"). Errors in declarative code tend to be casual blunders, more at the level of "Oh shit, I forgot to stipulate that". Bugs, in the sense I'm using it here, crop up in imperative languages with depressing frequency, largely because programmers must typically invent situational logic on the fly.

Successful declarative languages include SQL and most of the unix command line. Some of the best declarative languages in general use are the XPath technologies: XML Schema, XSLT, XQuery _et al_. All of them depend on the powerful and well-designed XPath node selection notation; which is in turn made possible by the constrained nature of the XML datamodel that it works against. The payoffs are pretty spectacular: the complex data tree transformations produced by XSLT, for example, would be prohibitively costly to reproduce using ad hoc imperative means; and those ad hoc solutions would generally not scale very well if built.

### why not JSON, eh?
Since the JSON datamodel is a much-simplified but still valid subset of the XML datamodel, it would seem to be an obvious move to create, e.g., "JSONPath", "JSONSLT", "JSONQuery" to translate comparable benefits to the JSON data type. It's been tried; unfortunately, worthy efforts to get something going seem to have foundered.

There are many reasons for this, and considering them in any detail is far beyond the scope of this document. However, there are several plausible considerations, which have guided the development of JNPath:

 - The JavaScript developer community has an apparent widespread cultural dislike of all things XML. Avoidance of XML-related concepts and syntax is prudent for any project that hopes to be useful to JavaScript developers.
 
 - When replicating the benefits of XPath, it's not necessary to borrow the syntax by which XPath was implemented. The value of XPath is as a successfully implemented logical model: to be emulated but not reproduced.
 
 - XPath explicitly targets the XML datamodel. When replicating the benefits of XPath to JSON, it's important to discard any XPath features (or implicit/embedded logical assumptions) that are not relevant to the JSON datamodel.
 
 - Logical completism is the devil. The W3C was obliged to design and build its specification to a 100% logical standard. A pragmatic logical subset of the XPath-for-JSON problem space is arguably superior to a forced march to that 100%.

----
## how

### "JNPath"
Other projects have used various names for their JSON + XPath adaptations. "JNPath" seems like a simple, adequately salient, adequately representative name whose googlespace isn't much colonized.

### 80% solution
JNPath is defined, from the outset, as a sort of Pareto solution. Its intent is to be realistically completable and pragmatically useful. The subset of possible features is severely restricted, based mainly on balancing concerns of utility vs. complication.

### syntax: familiar and not forbidding
Hopefully, anyway.

Rather than using the XPath syntax, JNPath uses a matching syntax designed explicitly for JSON. The intent is to provide a language that the target audience will naturally understand. `jnpattern` syntax is a superset of the normal notation for extracting values from JSON objects. The path notation is augmented by:

 - the **shortcut** step `[**]`, which skips zero or more steps in a path;

 - **wildcard/multiselect** steps:
 
  - `[*]` which matches any step, whether name of property or index of array
 
  - `[]`, `[m:n]`, [-n]` for array index steps;
  
  - partial glob wildcarding (e.g. `[*]`, `["ab*ve"]`) for named steps
  
 - a **very limited set of boolean conditionals**, with syntactic sugar, that can be injected into path steps.

...and that's it.


