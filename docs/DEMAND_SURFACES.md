# Demand surfaces: where the questions come from

The demand term of the Content Gap Score counts user questions linked to an
entity. The point of an adapter interface rather than a fixed list is that the
set of places where people ask questions keeps growing, and a deployment should
declare which of them it actually read.

## The thirteen surfaces

| Surface id | Group | What it holds |
|---|---|---|
| `forum` | first-party voice | threads and replies on discussion boards |
| `qa_site` | first-party voice | question-and-answer sites |
| `social_group` | first-party voice | posts inside groups and communities |
| `social_post` | first-party voice | public posts and replies |
| `video_short` | first-party voice | short-form video titles, captions, comments |
| `video_long` | first-party voice | long-form video titles, descriptions, transcripts, comments |
| `review_gmb` | first-party voice | business-listing reviews |
| `review_platform` | first-party voice | reviews on dedicated review platforms |
| `review_app_store` | first-party voice | app-store reviews |
| `support_ticket` | first-party voice | the organization's own support and contact records |
| `people_also_ask` | tool-derived | question boxes a search engine shows for a query |
| `autocomplete` | tool-derived | search-box completions |
| `keyword_export` | tool-derived | ranked-keyword exports from an SEO tool |

**First-party voice** surfaces carry a user's own words. **Tool-derived**
surfaces carry a tool's reconstruction of demand from what is already searched
or already ranked. The distinction is load-bearing: a deployment whose demand
evidence is entirely tool-derived has a demand term built from what is already
ranked, which is exactly what the framework claims not to depend on. The run
reports the first-party share so that this can be seen.

## The adapter contract

```python
from ufi.demand import DemandAdapter, DemandRecord

class MyForumAdapter(DemandAdapter):
    surface = "forum"
    requires = ("export.jsonl",)

    def read(self, path):
        for row in my_rows(path):
            yield DemandRecord(text=row["title"], surface=self.surface,
                               source_id="forum:myboard", retrieved=row["date"],
                               weight=row["replies"], locator=row["url"])
```

`read(path)` yields `DemandRecord`s (`text`, `surface`, `source_id`, `retrieved`, optional `weight`, `locator`, `language`, `synthetic`); nothing else is required. Two generic adapters
ship: `JsonLinesAdapter` and `CsvAdapter`. Collection itself (API keys, rate
limits, terms of service, robots.txt) is out of scope for the package and
belongs to the deployment.

## Linking questions to entities

`AliasLinker` is a longest-match linker over entity labels and aliases,
deliberately simple so that a reader can see exactly why a question was
attributed to an entity. A deployment that needs better linking subclasses
`EntityLinker`.

## The coverage report

`DemandIndex.coverage_report()` prints every designed surface, including the
ones that returned nothing:

```
demand surfaces
  forum              first-party  read                 137 records,  66 entities
  qa_site            first-party  not collected          0 records,   0 entities
  ...
  keyword_export     tool-derived declared, no rows      0 records,   0 entities
```

A demand term computed from zero rows is a demand term that does not exist,
and a paper that describes the designed source list without reporting the
built one is making a claim it cannot support. The report is what makes the
difference visible.

## Synthetic records

`DemandRecord.synthetic=True` marks a record generated for demonstration. The
flag propagates: synthetic records are excluded from the first-party share,
and the manifest says in plain words when nothing computed is an observation
about users. The worked example runs entirely on synthetic demand records.
