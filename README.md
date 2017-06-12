# JNPath
_TL;DR:_ 

_A lightweight, ad-hoc toolkit that **unambitiously** provides minimal XPath-like declarative capability for JSON, without attempting to use the XPath syntax._

_A JNPath pattern expression (`jnpattern`) is a match expression. Pattern notation is a superset of JSON path notation, with additional matching syntax based closely on familiar expressions._

_Any notation in JNPath is severely constrained to be **simple**, **unambiguous**, and **cognitively undemanding**._

_The fundamental operation of JNPath is the matching of a JSON instance path to a `jnpattern`._

_JNPath includes reciprocal operations for:_
 - _decomposing a JSON object into a set of instance paths, and_
 - _composing a set of instance paths into a JSON object._
_This provides a straightforward utility for applying `jnpattern` tests to any JSON object, and composing new JSON objects out of any set of generated or selected paths._

----
### Why "JNPath"?
Other projects have used various names for their JSON + XPath adaptations. "JNPath" seems like a simple, adequately salient, adequately representative name whose googlespace isn't much colonized.

### This project is a definitional and development repo.
Its immediate purpose is to serve as a kind of factory for pieces of working code, which will be used in various production scripts and working code.

When the definition is sufficiently stable, a reference implementation will be built and published.

## `jnpattern` examples

`[.]`                                       get all top-level nodes of a JSON object

`[....]`                                    get all nodes of a JSON object

`['stores']['*parrot'][.]`                  get **all child nodes** of any child
                                            of the "stores" top-level node, whose name
                                            ends in "parrot"
                                            
`['stores']['*parrot'][*]`                  get **all named child nodes** of any child
                                            of the "stores" top-level node, whose name
                                            ends in "parrot" (if the "*parrot" node value
                                            is an array, no match occurs)
                                            
`['stores']['*parrot'][-]`                  get **all indexed child nodes** of any child
                                            of the "stores" top-level node, whose name
                                            ends in "parrot" (if the "*parrot" node value
                                            is an object rather than an array, no match occurs)

`['stores'][...]['inventory'][.]`           get any child nodes of any "inventory"   
                                            descendants of the "stores" top-level node

`['student'](['first_name'] == 'Ann')[.]`   get the entire contents of every "student"
                                            record where the record's "first_name"
                                            property has a value of "Ann"

`[0]`                                       get the first top-level element of a JSON
                                            array object

`[-2]`                                      get the next to last top-level element
                                            of a JSON array object

`[...](['herp'] == 'derp')`                 get all nodes in the JSON object for
                                            which the "herp" property has a value
                                            of "derp"

`['books'][-](no ['donor'])`                get any nodes from the "books" top-level
                                            array that have no "donor" property

`['books'][-](yes ['donor'])`               get any nodes from the "books" top-level
                                            array that do have a "donor" property
                                            (irrespective of "donor"'s value or
                                            lack of value)

`['books'][-](falsy ['donor'])`             get any nodes from the "books" top-level
                                            array that have a "donor" property whose
                                            value is falsy `(null`, empty string,
                                            boolean `false`, etc)

`['books'][-](empty ['donor'])`             get any nodes from the "books" top-level
                                            array that have a "donor" property whose
                                            value is an empty object or array

`['album']['tracks'][3][.]`                 get the fourth node from the "tracks" array 
                                            in the "album" top-level object

`['album']['tracks'][-1][.]`                get the last node from the "tracks" array
                                            in the "album" top-level object

`['album']['tracks'][2:7][.]`               get the third through seventh node from the  
                                            "tracks" array in the "album" top-level object

`['album']['tracks'][3, 5, 8][.]`           get the fourth, sixth, and ninth nodes from the  
                                            "tracks" array in the "album" top-level object

`['album']['tracks'][1:-1][.]`              get all nodes _except_ the first and last from
                                            the "tracks" array in the "album" top-level
                                            object

----
(For an expanded discussion of this section, see [the rationale](https://github.com/whblondeau/jnpath/blob/master/rationale.md#why-define-and-build-jnpath]).)
## why
### JSON could really use a set of declarative tools.

Declarative programming, unlike the more familiar imperative style, has two major practical benefits:
- Very low bug rate
- Prior resolution of complicated algorithms

The declarative programming style is best understood through the simple characteristic: _The programmer states **what** is to happen, but does not have to say **how** to do it._ Familiar examples of successful declarative programming include SQL, the linux command line, and the expansive suite of XML technologies defined by the W3C. 

It's that last that provides a working example for JNPath. **XPath, a declarative syntax for selecting nodes from an XML document,** is the fundamental underlying technology for schema validation, transformations, and other hard, potentially expensive problems.

JSON, setting aside notational differences, is a restricted and simplified subset of the XML datamodel. _In principle_, the XPath-based toolsets could be applied to JSON. In practice, this sort of thing only happens under the hood, in libraries and components. Developers working with JSON have not, generally speaking, received the hands-on benefits of XPath.

Why?

Well, it's not a trivial question to answer, but I think the roots lie in the cultural and work norms of the JavaScript developer community: the majority of the people who work with JSON. To boil it down to a drastically oversimplified form:
- JavaScript developers appear to hate all things XML. (They're not alone. XML is, unfortunately, detested in many communities of practice.)

- JavaScript developers are so focused on mastering asynchronous code (expressed in a syntax that, let's face it, is demanding and pretty ugly), and on coping with the various web development frameworks, that they justifiably do not want to learn yet another syntax—let alone another way of thinking about programming.

Given these predispositions, it's understandable that some worthy efforts to apply XPath-style benefits to JSON have seen little uptake.

JNPath is one more whack at the piñata. One that attempts to avoid predictable (and arguably justified) resistance to XPath technologies.

----
(For an extended discussion of this section, see [Design Principles](https://github.com/whblondeau/jnpath/blob/master/design_principles.md).)
## how
JNPath observes several key design and implementation principles:
### scope
- **80% is good enough.** XPath and its children are necessarily 100% solutions, because the W3C was defining general standards. JNPath, by implementing only a carefully-considered **pragmatic subset** of the logical model involved in JSON node selection, remains realistically completable and, hopefully, useful.

- **Discard inapplicable aspects of the XPath datamodel.** XPath is used as a **guiding illustration of capability, rather than a datamodel to be ported.** JNPath defines a logical model of node selection that considers JSON only. XPath is _much_ larger and more complicated than JNPath. Using XPath to select JSON nodes is a textbook example of taking a 5-ton dump truck to the corner store for a banana and a pack of cigarettes.

- **Leaf Path implementation.** JSON carries its data in leaf nodes. The access paths simply represent organization. This is _much simpler than XML's mixed-content datamodel_. This permits a remarkable and powerful design feature: The JNPath API exposes a function for converting JSON objects into leaf-node paths, and another function for assembling a structurally coherent set of leaf paths into a JSON object. Not only does this permit node selection on JSON objects to be implemented via a very simple pattern-matching operation on paths, it provides enormous convenience to any developer who wants to perform custom operations on paths.

### syntax
- **Use familiar JSON syntax**, and expressions derived from it, instead of XML/XPath syntax.

- **Make extended syntax as simple and straightforward as possible.** When moving beyond JSON access syntax in order to define `jnpattern` expressions, use symbols that have familiar meaning (e.g., `*`), that are salient and distinct (e.g., `...`), and that have low visual static (the wildcard symbol for "any array index" was going to be `#`, but was replaced by `-`: for no other reason than to slightly declutter the visual representation.)

- **Optimize syntax for readability.** Code will typically be read many times, during initial construction and subsequent maintenance or modification. It's written once. The more sight-readable the code, the better.

- **Favor direct syntax over object notation.** This may seem a bit odd, but consider a comparison: identifying an array element by counting backwards from the end. Instead of the JavaScript array notation `array[(array.length - (n + 1)]` for selecting the `n`th-to-last element in an array, JNPath follows the Python negative-indexing syntax: `[-n]`. Really, and c'mon: which would you rather sight-read?

These principles, ruthlessly applied, will hopefully ensure that JNPath will benefit the various communities of JSON use.
