# Guardrails, and what an adversarial review found

The package is built so that the common ways an applied content study fools
itself are hard to do by accident and visible when done on purpose.

## Five things the package makes hard to get wrong

**Structure and coverage stay separate.** `structure_subgraph()` returns only
triples whose provenance is a structure source. If coverage evidence reached
the relatedness graph, an entity competitors cover well would gain edges,
centrality and prior, and the score would rank covered entities above
uncovered ones, the opposite of its purpose.

**A demand term with nothing behind it is visible.** `coverage_report()` lists
every designed surface including the ones that produced nothing.
`first_party_share()` reports how much evidence is in a user's own words
rather than reconstructed by a keyword tool, and excludes synthetic records
from the numerator. A run at 0.0 does not support a claim about users, and the
CLI says so rather than leaving it to the reader.

**A query universe defined after the outcome is marked as such.**
`freeze_queries()` writes the evaluation set with a hash and refuses to
overwrite. A run with no frozen set records `none:query-set-not-frozen`
rather than an empty field.

**Judgments are cached with their context.** Each cached row carries the
subject, the question, the rubric identifier and a digest of the evidence. A
cache of anonymous grades cannot be re-graded by a second annotator or traced
back to a published number. Changing the rubric text misses the cache.

**An empty validation is not a clean one.** `rdf.validate()` reports the
number of focus nodes and refuses to call a run conformant when it had nothing
to check. `rdf.reason()` reports how many class assertions were inferred, so
"a reasoner ran" can be told apart from "a reasoner had something to do".

## What an adversarial review found, and what changed

The package was reviewed by a simulated panel that executed it. These are
invented reviewer personas applying a stated standard, not peer review. The
findings were real and the fixes are in this repository:

- the OWL export dropped every property alignment and emitted a bare name
  where an IRI was required, so the file did not parse;
- data properties were inexpressible, so the class whose identity criterion
  is a code pair could not record the pair;
- the judgment cache stored anonymous grades;
- `kendall_tau` was documented as tau-b and computed tau-a over heavily tied
  input;
- the volume and question-mining baselines were fed the same numbers;
- two referenced files did not exist;
- the demo reported a healthy first-party demand share on wholly synthetic
  data;
- the generated SPARQL for one competency question lacked subclass closure,
  so its coverage was published as 0.0% when it is 81.4%; now pinned by a
  test;
- a question marked `unsupported` was being scored as zero instead of
  reported as a declared gap; now pinned by a test;
- terms were minted under a persistent-identifier namespace the project had
  not registered; the default is now `urn:ufi:`;
- the manifest digest moved between two identical runs because the cache
  fingerprint included each judgment's timestamp;
- tied scores reordered between runs; the sort now breaks ties on entity id.

## Known limitations

- `rel` is strongly correlated with node degree on sparse graphs (about 0.8
  on the worked example). Check the correlation on your own graph.
- The three-level rubric is coarse; half credit covers a wide range.
- `ans` takes the best of several verbalizations, which rewards the easiest.
- The entity linker is longest-match over aliases.
- The NANP ontology is a nine-class sketch with Wikidata alignments only; it
  has no registered namespace and no DOI.
- The example's only chain question (`CQ4`) has 0.0% instance coverage
  because the shipped graph records no carrier assignments; the chain
  machinery is tested but not demonstrated answering on data.
