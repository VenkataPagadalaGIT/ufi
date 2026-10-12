"""Executing competency questions against a graph, and reporting a pass rate.

A competency question apparatus with no pass rate is prose. This module turns
each question into a SPARQL query and reports two numbers that answer two
different objections:

**Schema support.** Can the ontology express the question at all? A question
whose relation is absent from the model is a declared gap, not a failure to be
averaged away. `run()` reports it as unsupported and names the missing relation,
because an ontology that silently cannot answer a question it lists is worse
than one that says so.

**Instance coverage.** For what share of the subject individuals does the graph
actually return an answer? This is the number that degrades as a population
grows, and it is the one a resource reviewer asks for.

The two are kept apart because they fail for different reasons and are fixed by
different work: schema support by modelling, instance coverage by extraction.

A question may traverse a property chain. `chain: ["^withinAreaCode",
"assignedTo", "isRoleOf"]` reads as a SPARQL property path
`^withinAreaCode/assignedTo/isRoleOf`: from an area code, back to the central
office codes within it, to the carrier roles they are assigned to, to the
organizations holding those roles. `validate_chain()` threads the declared
domains and ranges through the path and reports a step that does not compose,
which is the check that catches a question pointed at a property saying nothing
about what the question asks.
"""
from __future__ import annotations

from dataclasses import dataclass

from .types import CompetencyQuestion


@dataclass(frozen=True)
class CQResult:
    """One competency question's outcome against one graph."""

    id: str
    template: str
    supported: bool
    reason: str = ""          # why unsupported, when it is
    n_subjects: int = 0       # individuals of the subject class in the graph
    n_answered: int = 0       # of those, how many the query answers
    n_answers: int = 0        # total bindings, so fan-out is visible
    sparql: str = ""

    @property
    def coverage(self) -> float:
        """Share of subject individuals for which the graph answers.

        Zero subjects gives zero, not one. An empty population is not full
        coverage, and reporting it as 1.0 is how a vacuous pass rate gets into
        a resource paper.
        """
        return self.n_answered / self.n_subjects if self.n_subjects else 0.0


def steps(cq: CompetencyQuestion) -> tuple[str, ...]:
    """The property path this question traverses, as declared.

    A question with an explicit `chain` uses it. Otherwise the path is the
    single `relation`, inverted when the pattern is `inverse`, which is what
    makes "which codes are in Georgia" a traversal of locatedIn backwards
    rather than a different property.
    """
    if cq.chain:
        return tuple(cq.chain)
    if not cq.relation:
        return ()
    return (f"^{cq.relation}" if cq.pattern == "inverse" else cq.relation,)


def _split(step: str) -> tuple[str, bool]:
    return (step[1:], True) if step.startswith("^") else (step, False)


def validate_chain(cq: CompetencyQuestion, onto) -> list[str]:
    """Thread the declared domains and ranges through the path.

    Returns a problem per step that does not compose. Classes outside the
    ontology (an `ext:` or `xsd:` range) end the thread rather than failing it,
    because the model does not claim to know their subclass structure.
    """
    path = steps(cq)
    if not path:
        return []
    here = cq.subject_class(onto.properties)
    if not here:
        return [f"{cq.id}: cannot determine the class the question is asked of"]
    problems: list[str] = []
    for i, step in enumerate(path, start=1):
        name, inverse = _split(step)
        p = onto.properties.get(name)
        if p is None:
            problems.append(
                f"{cq.id} step {i}: property {name!r} is not defined")
            return problems
        entry, exit_ = (p.range, p.domain) if inverse else (p.domain, p.range)
        if here in onto.classes and entry in onto.classes:
            if not (onto.is_a(here, entry) or onto.is_a(entry, here)):
                problems.append(
                    f"{cq.id} step {i}: {step} enters at {entry} but the path "
                    f"has reached {here}, and neither is a subclass of the "
                    f"other, so the step does not compose")
                return problems
        here = exit_
    if cq.answer_class and here:
        want, got = cq.answer_class, here
        known = (want in onto.classes or want.startswith(("ext:", "xsd:"))) \
            and (got in onto.classes or got.startswith(("ext:", "xsd:")))
        if known and want != got:
            if want in onto.classes and got in onto.classes:
                if not (onto.is_a(got, want) or onto.is_a(want, got)):
                    problems.append(
                        f"{cq.id}: the path ends at {got}, but the question asks "
                        f"for {want}. A path can compose and still answer a "
                        f"different question than the one asked.")
            else:
                problems.append(
                    f"{cq.id}: the path ends at {got}, but the question asks "
                    f"for {want}.")
    return problems


def sparql_for(cq: CompetencyQuestion, onto, base: str) -> str:
    """A SELECT binding one subject and one answer per row.

    An explicit `sparql` on the question wins, so a question needing a filter,
    an aggregate or a negation can carry its own query. Otherwise the query is
    generated from the path, which keeps the common case honest: the query and
    the declared relation cannot drift apart.
    """
    if cq.sparql:
        return cq.sparql
    subject = cq.subject_class(onto.properties)
    path = steps(cq)
    if not path or not subject:
        return ""
    rendered = "/".join(
        f"^<{base}#{n}>" if inv else f"<{base}#{n}>"
        for n, inv in (_split(s) for s in path))
    return (f"SELECT ?s ?a WHERE {{\n"
            f"  ?s a <{base}#{subject}> .\n"
            f"  ?s {rendered} ?a .\n"
            f"}}")


def run(onto, kg=None, graph=None, base: str = "") -> list[CQResult]:
    """Execute every competency question and report per-question results.

    Pass either a `KnowledgeGraph` (converted here) or an rdflib `Graph`. The
    graph should be the materialized one where entailment matters: a question
    asked of GeographicAreaCode answers nothing over a graph that only asserts
    AreaCode, and reporting that as a coverage failure would blame extraction
    for a reasoning step that was never run.
    """
    from . import rdf as _rdf

    if graph is None:
        if kg is None:
            raise ValueError("run() needs a KnowledgeGraph or an rdflib Graph")
        graph = _rdf.to_rdf(onto, kg, base=base or None)
    base = base or f"http://w3id.org/ufi/{onto.name}"

    out: list[CQResult] = []
    for cq in onto.questions:
        if cq.unsupported:
            out.append(CQResult(cq.id, cq.template, False, cq.unsupported))
            continue
        problems = validate_chain(cq, onto)
        if problems:
            out.append(CQResult(cq.id, cq.template, False, problems[0]))
            continue
        subject = cq.subject_class(onto.properties)
        q = sparql_for(cq, onto, base)
        if not q:
            out.append(CQResult(cq.id, cq.template, False,
                                "no relation, chain or sparql declared"))
            continue
        subj_q = f"SELECT ?s WHERE {{ ?s a <{base}#{subject}> }}"
        subjects = {r[0] for r in graph.query(subj_q)}
        pairs = {(r[0], r[1]) for r in graph.query(q)}
        answered = {s for s, _ in pairs} & subjects
        out.append(CQResult(cq.id, cq.template, True, "",
                            len(subjects), len(answered), len(pairs), q))
    return out


def report(results: list[CQResult]) -> str:
    """A text block fit to paste into a paper's evaluation section."""
    if not results:
        return "no competency questions declared"
    lines = [f"{'CQ':5} {'supported':10} {'subjects':>9} {'answered':>9} "
             f"{'coverage':>9}  question"]
    for r in results:
        lines.append(
            f"{r.id:5} {'yes' if r.supported else 'NO':10} "
            f"{r.n_subjects:>9} {r.n_answered:>9} {r.coverage:>8.1%}  "
            f"{r.template}")
        if not r.supported:
            lines.append(f"{'':5} unsupported: {r.reason}")
    sup = [r for r in results if r.supported]
    lines.append("")
    lines.append(f"schema pass rate:   {len(sup)}/{len(results)} "
                 f"({len(sup) / len(results):.0%}) of declared questions the "
                 f"ontology can express")
    if sup:
        mean = sum(r.coverage for r in sup) / len(sup)
        full = sum(1 for r in sup if r.coverage >= 1.0)
        lines.append(f"instance coverage:  {mean:.1%} mean over supported "
                     f"questions; {full}/{len(sup)} answered for every subject")
    return "\n".join(lines)
