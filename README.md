# jnpath
_tl;dr: a lightweight, ad-hoc toolkit that **unambitiously** provides minimal XPATH/XSLT-like declarative capability for JSON._

## Examples

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


## why
### XPath-like benefits for JSON
The declarative programming style is highly beneficial. Some of the best declarative languages are the XPath technologies: XSLT and XQuery. Since the JSON datamodel is a much-simplified but still valid subset of the XML datamodel, it would seem to be an obvious move to create, e.g., "JSONPath", "JSONSLT", "JSONQuery" to translate the benefits to the JavaScript world. Unfortunately, worthy efforts to get something going seem to have foundered.

### 80% solution
One common failing of projects that try to provide broad support is that they compulsively attempt to bring all the things. This runs up hard against the general principle that "if the first 90% takes eight months, the second 90% will take fifteen months." JNPath is defined, from the outset, as a sort of Pareto solution.



#### Things the examples show

JNPaths are composed of square-bracketed **steps**. Each step represents traversal down into the JSON object. Typically, this is a direct traversal to a child node. (The special descent shortcut expression `[**]` is the only exception to this.)

**`namexpr` name expressions:**

When the square brackets contain a string, that's the name of a node. The name can be exact, or it can be a glob expression.

**`indexpr` index expressions:**

When the square brackets contain a number, that's the index of the node in its parent array.

`[nonnegative index]` is a zero-based index for a node's position in its parent array.

`[negative index]` is a one-based index counting backwards from the last item in the parent array. This is a very elegant and powerful syntax taken directly from Python. Its Javascript equivalent would be `parent.length + negativeindex`.

`[startwith:endbefore]` is slicing syntax, cribbed directly from Python but consistent with Javascript's `.slice(startwith, endbefore)`.

**Commas inside square brackets are boolean OR expressions:**

`[indexpr, indexpr,...]` is syntactic sugar allowing multiple numeric index expressions so you don't have to write a lot of separate JNPaths.

`[namexpr, namexpr,...]` is syntactic sugar allowing multiple name expressions so you don't have to write a lot of separate JNPaths.

**Wildcard node expressions**

`[]` means "any number" for an array index.

`['*']` means "any named node" -- really just a special case of glob.

`[*]` means "any node" irrespective of whether its parent is an object or an array.

`[**]` means "any descendant sequence" of zero or more nodes.

**where**

`(boolean expression)` is a WHERE clause applied to the immediately preceding step. (For those who know XPath, the irony will not be lost: in XPath the notation is "[boolean expression]".)

**Special boolean operators**

`yes` is syntactic sugar for "does the following expression find at least one existing node?"

`no` is syntactic sugar for "does the following expression find no existing nodes?"

`falsy` is syntactic sugar for "does the following expression find no nodes at all whose value is truthy?" Sense of this is equivalent to JavaScript's `truthy`/`falsy` semantics (NOT the same as Python's! Sorry, Pythonistas.)

`empty` is syntactic sugar for "does the following expression find at leaast one node whose value is an empty collection (i.e., JSON lists the value as `[]` or `{}`)?"

`not` is the boolean negative, same as Javascript's `!` or Python's `not`.

#### Return value "retexpr"

JNPath returns a very specific data structure for each node it finds. This is an array representing a 2-tuple:

`[<explicit path>, <node value>]`

where the explicit path includes the node's name (if the parent is an object) or index (if the parent is an array.)
