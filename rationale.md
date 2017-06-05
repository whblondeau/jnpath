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

----
## how

### "JNPath"
Other projects have used various names for their JSON + XPath adaptations. "JNPath" seems like a simple, adequately salient, adequately representative name whose googlespace isn't much colonized.

### 80% solution
JNPath is defined, from the outset, as a sort of Pareto solution. Its intent is to be realistically completable and pragmatically useful. The subset of possible features is severely restricted, based mainly on balancing concerns of utility vs. complication.

A **ruthless refusal to implement Just This One Other Cool Feature** is a core pronciple of JNPath.

### porn simple
JNPath will, insofar as possible, always strive to be _highly explicit_ and to _require minimum thought_ from users. The (possibly slightly sarcastic) reference to production values of the commercial pornographic industry makes a handy mnemonic.

Snark aside, "porn simple" is a tagline for a very serious matter. **Anybody using JNPath should find it obvious, reasonable, easy, small, and—perhaps most important—_not confusing._**

One very important implication of porn simple is **"flatlogic"**: the principle that JNPath expressions **should not require the programmer to apply extra mental effort to interpret them on the fly.** In other words, the expressions themselves have relatively little logical depth. This makes sight-reading easy to do.

A lot of very promising and useful features have been excluded from the design because they failed the porn simple test. (A good example is regular expressions as wildcards in `jnpattern` steps. Regexes are powerful, fast, expressive, and extensively used in the implementation; and some in fact are exposed as API constants. But, while like maybe 7% of us would be happy to use them, for the rest of the world regexes are an unspeakable horror. Their occurrence creates an immense blast of visual static that derails intuition and shakes the reader/developer out of the zone. As Philip Marlowe said, it "stands out like a tarantula on your slice of angel food cake." So no. No regexes.)

### optimized for readability
This is a straight steal from Python's excellent example; and a reaction to XSLT's terrible counterexample. (XSLT, which is logically excellent, has visually and cognitively forbidding syntax. I personally never had trouble with it, but the verdict is pretty clear: a lot of very capable programmers hit XSLT and bounce off.)

### syntax: familiar and not forbidding
Hopefully, anyway.

Rather than using the XPath syntax, JNPath uses a matching syntax designed explicitly for JSON. The intent is to provide a language that the target audience will naturally understand. `jnpattern` syntax is a superset of the normal notation for extracting values from JSON objects. The path notation is augmented by:

 - the **shortcut** step `[...]`, which skips zero or more steps in a path;

 - **wildcard/multiselect** steps:
 
  - `[.]` which matches any step, whether named or array index
 
  - `[*]` which matches any named step

  - `[-]`, `[m:n]`, `[-n]` for array index steps
  
  - limited glob-style wildcarding (e.g. `["*"]`, `["ab*ve"]`) for named steps
  
 - a **very limited set of boolean conditionals**, with syntactic sugar, that can be injected into path steps.

...and that's it.

### JavaScript and Python as privileged languages
These two languages share a number of characteristics. The pertinent commonality they have is that _JSON serialization is valid JavaScript syntax **and** valid Python syntax._ Building on this, the path syntax for JSON paths uses the full square-bracketed step notation, which is also valid for accessing JSON properties in both languages. **Dot notation: not gonna happen.** Not only is it inconsistent with Python's Dictionary/List representation of JSON, dot notation permits  more ambiguous situations.

JNPath's reference implementation is written in Python, primarily for simplicity and clarity—it is, after all, a _reference_. It needs to be easily understood and debugged; and some of the lower-level implementation code gets a little gnarly. Among the major imperative languages, Python is the best optimized for sight-reading of code. It's the closest thing we have to pseudocode that executes.

Python is also the source of the array index wildcard syntax expressions `[m:n]` (slicing) and `[-n]`(negative indexing). Javascript's equivalent of `[m:n]` would be `array.slice(m, n)`; Javascript's equivalent of `[-n]` is the unforunate `array[(array.length - (n + 1)]`. The Python representations are much simpler and neater. The only problem you're likely to have is based on a couple of unfortunate conventions of almost all programming languages: zero-based indexing (but for positive indexes only), and [include:exclude] slicing. Once you've wrapped your head around those, you'll probably like this notation pretty well.

A conformant JavaScript working implementation is also provided.
