# w3id.org namespace registration, prepared and not submitted

The exported OWL and SHACL mint terms under `urn:ufi:<ontology>` by default,
because this project never registered a w3id.org namespace and earlier versions
minted under `http://w3id.org/ufi/...` anyway. To publish under a resolvable
persistent identifier:

1. Fork https://github.com/perma-id/w3id.org
2. Create the directory `ufi/` containing the `.htaccess` below
3. Open a pull request; w3id maintainers merge after review
4. Pass `base="https://w3id.org/ufi/nanp"` to `to_owl()`, `to_shacl()`,
   `to_rdf()` and `ufi cq`, and serve the namespace document at the target

The `.htaccess` below redirects the namespace to this repository's GitHub Pages
copy of the ontology documents. It is a proposal; it does nothing until merged.
