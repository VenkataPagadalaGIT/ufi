# User First Intelligence: Ontology-Driven Content Gap Discovery from Multi-Source Industry Knowledge Graphs Beyond Search Volume

**Venkata Pagadala**
KL University (doctoral program), Andhra Pradesh, India
Manuscript version 4.8, 12 October 2026. Preprint, not yet peer reviewed.

Keywords: User First Intelligence; content gap discovery; ontology; knowledge graph; competency questions; search measurement; instrument validity; AI Overviews; generative engine optimization; deployment measurement study; reference content

## Abstract

People say what they want to know in many places that are not a search box: forum threads, question sites, video comments, reviews, support tickets, social groups. Keyword-volume tools see the fraction of that demand that reaches a search engine in a countable form, and AI answer surfaces now stand between the question and the page. User First Intelligence (UFI) is a framework built on that premise: collect what people ask across platforms, beyond the website; classify it and link it to the entities of an industry held under an ontology; keep structure, coverage and demand sources in separate roles in a knowledge graph; express user needs as executable competency questions; and score where the organization does not answer, treating the form of the answer as something to measure. An open implementation reading thirteen demand surfaces is released.

This paper reports one deployment of a gap of the kind the framework targets, identified from one of those surfaces, and what two commercial analytics platforms recorded on it: 381 area-code pages on a large US telecommunications provider's site, observed by both from zero. On estimated monthly visits the two differed by 25.9x, 27.1x, 10.2x and 7.5x in successive months; on ranking keywords by 2.0x; on live referring domains by 11.4x. Across twelve sections of the same domain read on one day, the ratio on estimated visits runs from 0.20x to 7.24x (0.20x to 8.89x territory-matched), with no detectable relationship to section age (Spearman −0.11, 95% interval −0.64 to +0.49) and no fixed correction factor, while the instruments agree on which section is larger in 60 of 66 pairs. Both are sound for direction. On a separate set of 37,193 reviews of 378 telecom retail locations linked to a 42,994-node taxonomy, review demand and search volume agree across top-level branches (Spearman +0.78) but barely across topics (+0.19); 14.0% of one- and two-star reviews name waiting, a complaint the taxonomy records at 12 searches a month. The scoring function is specified, not evaluated, and the full multi-surface and persona studies are registered. No causal claim is made.

## 1 Introduction

A content decision starts with a question someone asked. The place it was asked is increasingly not a search engine: it is a forum thread, a question site, a comment under a video, a product review, a support ticket, a post in a group. Keyword-volume tools observe the part of that demand that reaches a search box in a countable phrasing; Section 6 shows this deployment ranking for question forms, misspellings and non-English phrasings that carry little or no reported volume in those tools, and AI answer surfaces now sit between many questions and any page at all. User First Intelligence is a framework built on that premise: go beyond the website to where the questions are, classify and link them to the entities of an industry held under an ontology, keep the sources that establish structure, coverage and demand in separate roles so that a competitor's coverage cannot pose as user demand, express user needs as competency questions that a knowledge graph can be asked, and score where the organization fails to answer, with the form of the answer measured rather than assumed (Figure 1). The deployment reported here was built from a gap identified through one of those surfaces, competitor keyword exports, before the framework's other surfaces were implemented; it is a case of the kind of gap the framework targets, not a run of the framework. It also exposed the measurement problem the rest of this paper is about.

Almost every empirical claim in applied search research rests on a commercial analytics platform. Papers report that a technique moved visibility, that a competitor holds a share of some keyword space, that AI answers cite one kind of source more than another. The underlying numbers come from Ahrefs, Semrush, Similarweb or a comparable vendor, and they are reported the way measurements are reported: as quantities, sometimes to five significant figures, usually from one vendor, rarely with any statement of uncertainty.

The vendors do not claim otherwise in their documentation, which describes click models over estimated volumes at estimated positions. The practice treats them as counters anyway. This paper puts a number on how far two such estimates of one object can lie apart, so that the practice can state its uncertainty. For a framework whose premise is that volume tools see only part of demand, that number is not incidental: it is the size of the gap the framework's demand layer exists to fill, and it has to be measured before the framework can be evaluated against it.

### 1.1 Why a new section is the right instrument

Comparing two analytics vendors on an established site tells you little. Both have years of accumulated index data, the disagreements are confounded with each vendor's historical coverage, and there is no moment at which the true value is known.

A section that did not exist last week is different. Before launch, both instruments correctly report zero. After launch, both observe the same URL prefix, in the same period, with no prior history. Their disagreement is then attributable to their models and their indexes as applied to that object, and its trajectory over time is observable. Section 5.5 shows that the disagreement is specific to the object as well: the same two instruments disagree by different factors, in different directions, on different sections of the same site.

This paper uses one such section: 381 code pages plus hubs under a single prefix on a top-authority domain, published on 26 July 2026 and observed for 77 days, with ranking positions captured daily and the other quantities at seven checkpoints and monthly.

![Figure 1. The User First Intelligence framework. (a) The thirteen demand surfaces the released implementation reads, grouped by whether they carry a user's own words or a tool's reconstruction of demand; the one surface this deployment collected is marked; Section 5.7 adds a first run on business reviews. (b) The pipeline from observed questions to content, with the two observation layers this paper reports (dashed) and the component it specifies but does not evaluate (shaded). The deployment in this paper ran the lower layer and one surface of the upper; it did not run the pipeline end to end.](fig0_framework.pdf)

### 1.2 What this paper reports

1. **The User First Intelligence framework** (Figure 1): collecting user questions beyond the website across thirteen demand surfaces, classifying and linking them to an industry ontology, holding structure, coverage and demand as separate source roles in a knowledge graph, and scoring unanswered questions with a Content Gap Score and two competency-question metrics (schema pass rate and instance coverage); released as a specification (Appendix B) and an open implementation (Section 12). This deployment collected one of the thirteen surfaces; Section 5.7 runs the framework's demand comparison on a second, business reviews, and the full multi-surface study is registered (Section 11).
2. **A divergence series between two commercial instruments** observing one URL prefix from zero, on estimated visits, ranking keywords, referring domains and AI Overview citation. Section 5.1 to 5.4.
3. **A cross-section of twelve prefixes on one domain, both instruments, one day**, showing that the vendor ratio on estimated visits spans 0.20x to 7.24x within a site (0.20x to 8.89x territory-matched), shows no relationship with section age, and does not follow the keyword-universe ratio, while the vendors agree on the ordering of sections (rank correlation 0.94). Section 5.5. This is the paper's main empirical result, and it retracts the age hypothesis advanced in version 4.0.
4. **A first test of the demand premise** on 37,193 business reviews against a 42,994-node keyword taxonomy: the two signals agree across branches and diverge across topics, most for complaints. Section 5.7.
5. **A methodological consequence**: no domain-level correction converts one vendor's estimate into the other's; the vendors rank sections alike and size them by factors that vary from one fifth to nine times within one site. Section 5.6.
6. **A 77-day deployment series** on four quantities at a primary checkpoint chosen to precede three identified disturbances, with every definition, denominator, instrument and read date stated. Section 6.
7. **An observation about which pages AI answers cite**: enumerating hub pages outrank per-entity pages as cited sources, by a factor of roughly two. Section 7.
8. **The deployment's cost, its six enabling conditions, and six lessons stated as the things it got wrong.** Sections 3.1 and 9.

### 1.3 What this paper does not report

A reader is owed this before the results rather than after them.

**No causal claim.** The design is observational. There is no treatment assignment, no control group, no randomization and no matched comparison. The provider's list of sections launched in the same window is not available, so this study cannot say whether this section outperformed conventionally selected content on the same domain in the same period. Where the deployment series appears, it is a description of what was observed following publication, and "following" is the strongest word the design licenses.

**No separation of the method from the domain.** The deployment ran on a domain with an Ahrefs Domain Rating of 90 and a Semrush Authority Score of 86. Nothing here bounds how much of the outcome that explains, and Section 10 lists it among the confounds. An earlier version of this work claimed a bound from a comparison with two carriers of similar authority; that comparison is computed within a set selected on the provider's own presence and bounds nothing, as Section 7.2 sets out.

**No evaluated scoring function.** The framework's Content Gap Score was not computed when the build decision was taken, nothing here tests it, and no published study has tested whether it predicts anything. It is specified in Appendix B with a reference implementation, and it is kept out of the results so that it cannot be mistaken for one.

**No measured traffic.** No figure in this paper is a counted visit. The provider's internal analytics were not available for this study.

**No independent verification.** No person other than the author has graded, replicated or audited any part of this work. Section 12 states what has and has not been done about that, and it is the paper's largest unremedied weakness.

## 2 Related work

**Search measurement and tool validity.** The validity of vendor traffic estimates has been measured mainly against first-party analytics, site by site. An agency comparison of Similarweb, Ahrefs and Semrush against Google Analytics organic visits for 25 sites found all three differing from the first-party figure in level, with the two keyword-based tools below it on total traffic by 17% and 30% [Langridge 2016]. A vendor study of 1,635 sites against Google Search Console reports a median deviation of 49.5% for Ahrefs and 68.4% for Semrush, and a correlation with the first-party figure of 0.76 and 0.74 [Soulo 2022]; it is the vendor reporting on itself and on a competitor, and is cited for its design rather than its ranking. In academic work, traffic-ranking services have been compared as proxies for organizational performance [Vaughan & Yang 2013], and the major top-site lists were shown to disagree with one another on most of their entries and to churn by up to half of their domains a day [Scheitle et al. 2018], which motivated a ranking built to be stable and hard to manipulate [Le Pochat et al. 2019]. Those studies compare an estimate with a ground truth across many sites, or compare lists across the whole web. This paper does neither: it has no ground truth, and it holds the site fixed. What it adds is a reading of two vendors on an object both observed from zero, and a cross-section of twelve sections of one domain on one day, which separates disagreement about a site from disagreement about a section of it.

**Comparison across non-identical universes.** Comparing two measurements computed over different underlying sets is an old problem in information retrieval evaluation. Pooled relevance judgments are incomplete, and systems that did not contribute to the pool are scored on a universe they did not help define [Zobel 1998]; measures robust to incomplete judgments were proposed for exactly that case [Buckley & Voorhees 2004], and the bias a pooled universe imposes on a new system can be estimated and adjusted [Webber & Park 2009]. Section 5.6 makes the same move on commercial instruments: it decomposes the visits divergence into a keyword-universe term and a per-keyword term, so that a disagreement about how much surface each vendor indexes is not read as a disagreement about traffic. Unlike a test collection, neither vendor's universe is published, so the decomposition can be computed only at the aggregate level reported here.

**AI answer surfaces.** An audit of 55,393 queries found that 29.8% of the domains cited by Google's AI Overviews did not appear on the first page of organic results for the same query [Xu, Iqbal & Montgomery 2026]; vendor measurement across 15,000 prompts reports that only 12% of URLs cited by ChatGPT, Gemini and Copilot rank in Google's top ten for the same prompt, with Perplexity at 28.6% [Linehan & Guan 2025]. Users click less when a summary appears and rarely click its sources: a click on a link inside an AI summary occurred in 1% of visits to pages showing one [Chapekis & Lieb 2025]. A critical survey of 45 generative-engine-optimization studies finds no page-level technique with a stable cross-platform effect on visibility, and identifies topical relevance as the most reproducible lever [Martinez 2026]. Section 5.3 adds a measurement observation those studies need: the two vendor definitions of "cited in an AI Overview" differ by a factor that is itself time-varying, so a GEO result reported on one vendor's definition is not directly comparable to one reported on the other's.

**Personalization and the visibility of demand.** The framework's premise that a search box shows only part of what people ask has one documented component, one observation and one open question. Demand that never reaches a search engine in a countable phrasing is documented by the long-tail literature [Goel et al. 2010]; Section 6 adds the untested observation that the section ranks for question forms, misspellings and non-English phrasings carrying little or no reported volume. Personalization of classic web search has been measured directly: about 11.7% of Google results differed between users in a 2013 audit, with signed-in status and location the drivers and demographic attributes such as gender and age producing no substantial effect [Hannak et al. 2013]. What has not been measured is personalization of AI answer surfaces, where the answer is composed rather than ranked and the user's stated situation enters the prompt; the behavioral evidence so far concerns clicks, not variation in the answer itself [Chapekis & Lieb 2025]. Whether AI answers vary with the persona of the asker is therefore an open question this paper does not answer and Section 11 registers.

**Information needs and query fragmentation.** The gap between the unit a user has in mind and the unit a retrieval system indexes is old ground [Belkin, Oddy & Brooks 1982; Taylor 1968], as is the observation that aggregate demand concentrates differently from individual demand [Goel et al. 2010]. The taxonomy of web search [Broder 2002] distinguishes query intent rather than query granularity. Section 4 describes a deployment in which the operative distinction was granularity: one need expressed as thousands of distinct strings.

**Completeness in knowledge bases.** Appendix B's scoring function draws on the study of completeness in open-world knowledge bases [Razniewski et al. 2016; Galárraga et al. 2017; Balaraman et al. 2018; Luggen et al. 2019; Razniewski et al. 2024], on demand-weighted completeness [Hopkinson et al. 2018], and on gap discovery for encyclopedias [Wulczyn et al. 2016; Piccardi et al. 2018; Redi et al. 2020; Shao et al. 2024], with Ripoll et al. [2025] giving the most recent typology of content gaps for a collaborative knowledge base. Since the function is not evaluated here, that discussion sits with the specification in the appendix.

## 3 Setting

A large US telecommunications provider publishes a reference section covering the North American Numbering Plan. **As verified on 12 October 2026 by fetching every code page linked from the section's 52 state hubs, the section holds 381 code pages**: 374 for geographic codes assigned to US states and the District of Columbia, and 7 for toll-free codes. All 381 return HTTP 200, are canonical, and are full pages. The only geographic codes in the plan with no page are the six assigned to US territories. The section is therefore complete over the class it set out to cover, and **there is no set of uncovered codes within the class to serve as a control**.

Earlier versions of this paper, up to and including version 4.1, stated that 290 code pages had been published and that 88 geographic codes had none, and they registered those 88 as a within-class control arm. **Both figures were wrong.** The 290 was carried from an early draft and never re-counted, and the control it implied was never checked against the pages; fetching every page corrected both figures.

All code pages, the state hubs and the national hub were published together at launch; no pages were added to the section during the observation window. This is the author's statement of the deployment's publishing history. Table 5's series of pages holding a position (210, 365, 391, 414, 440) is therefore the indexing of a fixed set of 434 URLs by one instrument, and not growth in the section itself.

Two page counts remain and are easy to conflate. **381** is the number of code pages the section holds. **441** is the number of URLs under the prefix holding at least one ranking position on 11 October, which is selected on the outcome; it exceeds 381 plus the 53 hub pages by seven, which is within what the instrument attributes to a prefix beyond its canonical pages. Brand Radar's count of 455 distinct cited pages (Section 5.3) exceeds 434 by 21; that instrument does not document how it normalizes URL variants, and the difference is reported rather than reconciled. Every fact on the pages is templated from two public-domain US government sources, the numbering plan administrator's registry and census data. The section went live on 26 July 2026, which is day 0 throughout this paper, dated from the first third-party detection of the pages.

### 3.1 Six conditions that make this deployment unrepresentative

These are stated here, before the results, as the scope of everything that follows. All six held, and most classes in most industries satisfy none of them.

1. **The class is finite and enumerable.** There is a fixed, published list of area codes. Coverage is decidable.
2. **A free authoritative registry supplies every fact.** No research, no writer, no subject-matter review per page.
3. **The facts are uncontested.** Two sources would not disagree about which state a code serves.
4. **The domain is top-decile authority.** Ahrefs Domain Rating 90, Semrush Authority Score 86.
5. **No comparable-authority competitor covered the class page-per-entity.** Two carriers at Domain Rating 87 and 91 had, between them, overlay notices and a single lookup page.
6. **No defender responded.** The incumbent pages were specialist directories and voice vendors at Domain Rating 13 to 83, and none mounted a visible response during the window.

Conditions 1 to 3 make production nearly free. Conditions 4 to 6 describe an undefended position. A reader considering transfer should check all six, and should note that condition 6 in particular reads as a criterion for selecting undefended targets. That is the shape of a data void, a query space with thin or absent authoritative content that whoever arrives first fills [Golebiewski & boyd 2018], and Section 12 treats it as an ethics question rather than a tactic.

## 4 Measurement design

Everything in Sections 5 to 7 is an observation. The language is chosen to keep that visible.

### 4.1 Instruments, definitions and denominators

*Table 1. Instruments, definitions, denominators and read dates for every quantity reported in this paper.*

| Quantity | Definition | Instrument | Read |
|---|---|---|---|
| Ranking positions | URL under the prefix in positions 1–100, counted once per location | Ahrefs Site Explorer, prefix mode, all locations | daily series, 11 Oct 2026 |
| Ranking keywords | distinct keywords on which any URL under the prefix ranks 1–100 | Ahrefs (all locations); Semrush (US database) | 11 Oct; 10 Oct 2026 |
| Pages holding a position | distinct URLs with at least one position | Ahrefs | 11 Oct 2026 |
| Estimated visits | vendor click model applied to estimated position and estimated volume | Ahrefs (worldwide); Semrush (US) | 11 Oct; 10 Oct 2026 |
| AI Overview citation (a) | keywords whose AI Overview lists a URL under the prefix as a source, over all keywords the prefix ranks on whose results show an AI Overview | Ahrefs owned-AI-Overview | 11 Oct 2026 |
| AI Overview citation (b) | US keywords with an AI Overview position | Semrush | 10 Oct 2026 |
| AI answers | stored prompts whose latest answer cites a URL under the prefix, per platform | Ahrefs Brand Radar | 11 Oct 2026 |
| AI visibility (Semrush) | mentions and cited pages in the AI-visibility panel; scoped to the domain whatever subfolder is queried (Section 5.5) | Semrush | 10 Oct; 12 Oct 2026 |
| Referring domains | live linking domains to the prefix | Ahrefs; Semrush Backlink Analytics | 11 Oct 2026 |
| Section age (Table 4) | months since the first month with organic traffic in the all-time series; left-censored at September 2015 | Ahrefs Site Explorer, prefix mode, chart interval all | 12 Oct 2026 |
| US share (Table 4) | United States share of the prefix's estimated visits, from the traffic-by-location table | Ahrefs Site Explorer | 12 Oct 2026 |
| Monthly search volume | vendor-estimated monthly searches for a phrasing, summed over a set of phrasings | Ahrefs organic-keywords export, three carrier domains, US database | exported Oct 2025 |

Two properties of these instruments bear on everything that follows, and the first is the subject of Section 5.

**They are models, not counters.** Estimated visits are a click model over an estimated volume at an estimated position. No figure in this paper is a measured visit.

**The Ahrefs and Semrush visit figures are not the same quantity.** Ahrefs' is worldwide; Semrush's is the US database. The section ranks in 105 countries with 18.5% of Ahrefs' estimated visits from outside the US, so the Semrush figure covers a strict subset of the Ahrefs figure's territory and is nonetheless between 7.5 and 27.1 times larger. Section 5.1 reports both the US-only and worldwide Semrush figures so the comparison does not rest on the territory difference.

### 4.2 The query universe, and what cannot be computed on it

The evaluation query set was not frozen before launch; the section was live before this study was designed. The outcome quantities in Section 6 are therefore measured on universes defined after the fact: every keyword the section ranks for, and every prompt whose answer cites it.

Counts and positions on such a universe are meaningful, because the universe is the vendor's index rather than this paper's selection. **Shares and percentages computed on it are not**, because the denominator was selected on the outcome. Every share in this paper is one of the following, and is labeled at the point of use: a share whose denominator is outcome-selected, flagged as such and drawing no comparative conclusion; or a ratio between two instruments on the same object, which is this paper's primary result and is not affected, because both denominators are the same prefix.

### 4.3 The primary checkpoint

Three disturbances fall in the observation window. The September 2026 spam update began on 24 September, day 60, which is also the day of the estimated-traffic peak. Ahrefs posted a notice on 29 September, day 65, that Google had changed how it serves results and that SERP data might be inconsistent from that date, which covers days 65 to 75. And an automated link network began arriving in the day-37 to day-45 interval.

**Day 37 (1 September 2026) is the primary checkpoint**: the last observation preceding all three. Day 37 carries a cost that is stated rather than worked around: it was not one of the fifteen-day checkpoints at which the full quantity set was captured, so it is reported on four quantities and not nine. The claims this paper makes at day 37 concern ranking positions, top-three positions, estimated visits and the link profile, and nothing else.

## 5 Two instruments on one prefix

This is the paper's primary result. It is reported first because it is the finding that does not rest on the author's judgment: every figure below is one of two vendors' readings of a public URL prefix, and a reader holding both subscriptions can re-read them.

### 5.1 Estimated visits: a divergence of 7.5x to 27.1x on one prefix

*Table 2. Estimated monthly visits for the prefix from two instruments. Semrush worldwide in parentheses. The June to September rows are completed-month totals. **The October row is each instrument's current monthly run-rate as read on 10–11 October, not eleven days of accumulated traffic**, and is marked accordingly. The ratio column uses the US figure. Section 5.6 gives the territory-matched ratios, which are larger.*

| Month | Days live | Ahrefs, worldwide | Semrush, US (worldwide) | Semrush US / Ahrefs |
|---|---|---|---|---|
| June 2026 | 0 | 0 | 0 (0) | n/a |
| July 2026 (total) | 6 | 3,862 | 100,012 (103,045) | 25.9x |
| August 2026 (total) | 31 | 32,281 | 876,153 (963,937) | 27.1x |
| September 2026 (total) | 30 | 150,113 | 1,534,362 (1,765,077) | 10.2x |
| October 2026 (run-rate) | 11 (77 cumulative) | 215,577 | 1,610,284 (1,858,297) | 7.5x |

![Figure 2. Estimated monthly visits for the area-code prefix from two instruments, on a logarithmic axis so that the vertical gap is the ratio. Ahrefs Site Explorer (prefix mode, all locations) and Semrush Domain Overview (subfolder mode, US database and worldwide), read 10 and 11 October 2026. June to September are completed-month totals; October is each instrument's current monthly run-rate. The ratio labels are Semrush US over Ahrefs, as in Table 2.](fig1_divergence.pdf)

Three things about this table and Figure 2.

**The disagreement is larger than the quantity most papers report.** An applied paper reporting a 40% lift from a technique, measured on one of these instruments, is reporting an effect roughly one twentieth the size of the disagreement between instruments about the level.

**It is not a territory artifact.** Semrush's US-only figure exceeds Ahrefs' worldwide figure throughout, and the section draws 18.5% of its Ahrefs-estimated visits from outside the US. Using the Semrush worldwide figure widens the ratio rather than closing it.

**It narrows after the second month on this prefix**, from 27.1x to 10.2x to 7.5x. Section 5.5 tests whether that narrowing is a property of section age across twelve prefixes and finds that it is not; Section 5.6 takes up what the narrowing can and cannot be attributed to.

### 5.2 Ranking keywords: a factor of two, stable

On the count of distinct keywords for which any URL under the prefix ranks in positions 1–100, Ahrefs reports 29,000 for all locations and Semrush 58,586 for the US database, read a day apart: a factor of 2.0, again with the larger figure from the smaller territory. Pages holding at least one position are 441 in Ahrefs. The two instruments agree on rank ordering of pages by traffic and disagree on every level.

### 5.3 AI answers and AI Overviews: two definitions, converging

**A withdrawn comparison.** Earlier versions reported a factor of 9.2 on AI answers, from Ahrefs Brand Radar's 17,206 stored answers citing the section against Semrush's 158,100 mentions, read on 10 October. That ratio is not a divergence about the same object. Semrush's companion figure is 29,600 cited pages, which is 68 times the 434 URLs the section holds (381 code pages and 53 hubs) and 67 times the 441 URLs the other instrument attributes to the prefix, so the Semrush count is scoped to the domain or the brand rather than to this prefix. A scope mismatch of that size is not a measurement disagreement and the figure is removed from the abstract and from the comparison. The claim that the two instruments disagree about platform ordering is also dropped, because the evidence for it was a platform breakdown whose own figures did not sum to its stated total and which is not reproduced here.

What can be compared on this prefix is reported above and below: visits, ranking keywords, referring domains and AI Overview counts, each with an instrument, a definition, a territory and a read date in Section 4.1. The Ahrefs figure of 17,206 stored answers on 455 distinct cited pages is reported in Section 6 as a single-instrument count and is not paired with a second reading.

For AI Overview citation the vendors use different operational definitions, given in Section 4.1. Definition (a) is a ratio over AI Overviews the prefix's keywords actually appear on; definition (b) is a count of US keywords with an AI Overview position. Both are reported as "AI Overview visibility" in their respective products.

*Table 3. AI Overview citation under two vendor definitions, same prefix, same months.*

| Month | (a) Ahrefs: cited / all AIO keywords | (a) as %, 95% Wilson CI | (b) Semrush count | (b) / (a) numerator |
|---|---|---|---|---|
| July 2026 | 47 of 284 | 16.5% [12.7, 21.3] | 138 | 2.94x |
| August 2026 | 851 of 6,749 | 12.6% [11.8, 13.4] | 2,221 | 2.61x |
| September 2026 | 3,380 of 22,665 | 14.9% [14.5, 15.4] | 8,187 | 2.42x |
| October 2026 (run-rate) | 7,455 of 37,238 | 20.0% [19.6, 20.4] | 10,018 | 1.34x |

![Figure 3. AI Overview citation under two vendor definitions, same prefix, same months. (a) Ahrefs definition (a) as a share of all AI Overview keywords the prefix ranks on, with 95% Wilson intervals; the denominators grow from 284 to 37,238. (b) The two vendor counts, Semrush keywords with an AI Overview position against the Ahrefs numerator, on a logarithmic axis, with their ratio labeled. Sources as in Table 3.](fig2_aio.pdf)

The ratio between the two counts falls from 2.94 to 1.34 over four months (Figure 3b). Two cautions on reading it. The comparison is between a count (b) and the numerator of a ratio (a), and the two vendors' territories differ, so what the column measures is partly a territory difference and not purely a definitional one. And the series has three intervals, so "converging" describes the observed sequence and is not a trend estimate. The July row rests on 47 events over six days live, and its interval is correspondingly wide. A study reporting an AI Overview visibility figure on one vendor's definition, for a section of a given age, is not reporting a quantity comparable to the same figure from the other vendor, and on this prefix the size of the incomparability changed over its first four months.

The (a) column's percentage is the one proportion in this paper whose denominator grows by two orders of magnitude across the series, from 284 to 37,238, and it is not monotone. Its denominator is outcome-selected: it counts only AI Overviews on keywords the prefix already ranks on. It is reported because numerator and denominator come from one instrument on one date, and no trend is drawn from it.

### 5.4 Referring domains: 11.4x, and disagreement about composition

Both instruments report live referring domains to the same prefix on the same day, and both are in the Section 4.1 table with a definition and a read date, which makes this the cleanest paired comparison in the study after estimated visits.

Ahrefs reports 913 referring domains to the prefix; Semrush Backlink Analytics indexes 80 for the subfolder: a factor of 11.4. They also disagree about what those domains are. Ahrefs puts 61.9% on .info, 26.4% on .asia and 10.2% on .xyz; Semrush puts 75% on .xyz and 88% at Authority Score 0 to 10. Both descriptions agree the domains are low-quality automated networks and disagree about their composition by a wide margin, which matters for any study classifying link profiles from one vendor's TLD distribution.

![Figure 4. Composition of live referring domains to the prefix by top-level domain, as reported by each instrument on 11 October 2026. Ahrefs: 913 domains; Semrush Backlink Analytics: 80 domains, of which the instrument reports 75% on .xyz and does not break down the remainder.](fig3_refdomains.pdf)

Figure 4 shows the two compositions side by side. A third figure from the first instrument complicates even its own count: its daily series gives 909 at day 75 against 913 on 11 October, and its new-and-lost report for September gives 917 new against 95 lost, which with nineteen at day 37 implies 841. Section 8 sets out why no claim here turns on the exact count.

### 5.5 Twelve prefixes on one domain: the divergence is prefix-specific, with no detectable relationship to age

Sections 5.1 to 5.4 are one prefix. Version 4.0 proposed that the narrowing of the visits ratio reflected section age and index coverage, and Section 11 registered a cross-prefix replication as the test. It was run on 12 October 2026, on both instruments, for twelve sections of the same domain: the area-code section and eleven others chosen to span ages from under two years to the instrument's horizon. Every figure below is a dashboard read on one date. The raw values, the read method, the age proxy and the United States share of each prefix's estimated visits are in the released data files, and **every statistic quoted in this section is printed by the script `analyze.py` released beside them**.

*Table 4. Twelve URL prefixes on one domain, both instruments, read 12 October 2026. Age is months since the first month with organic traffic in the Ahrefs all-time series, read to the nearest month or quarter; the series begins in September 2015, so the oldest age (/es-us/local/) is left-censored at that horizon and the next two lie within four months of it. Ahrefs visits are worldwide and Semrush visits are the US database; the "US share" column is the United States share of Ahrefs' estimate from its traffic-by-location table, and the matched ratio divides Semrush US by Ahrefs US-only. The keyword ratio is Semrush over Ahrefs, like the visits ratios; the referring-domain ratio is Ahrefs over Semrush. Referring-domain and keyword counts are the 12 October reads and differ slightly from Sections 5.2 and 5.4's 10–11 October reads (29,000 and 58,586 keywords; 80 Semrush domains, 11.4x).*

| Prefix | Age (mo) | Ahrefs visits | Semrush visits (US) | Ratio, unmatched | US share | Ratio, matched | Ahrefs kw | Semrush kw | Kw ratio | Ahrefs RD | Semrush RD | RD ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| /local/area-codes/ | 3 | 221,000 | 1,600,000 | **7.24** | 81.4% | **8.89** | 28,900 | 59,000 | 2.0 | 913 | 81 | **11.3** |
| /product-compare/ | 21 | 5,500 | 4,100 | 0.75 | 69.6% | 1.07 | 716 | 2,300 | 3.2 | 187 | 41 | 4.6 |
| /local/bundles/ | 36 | 25,600 | 5,200 | 0.20 | 99.2% | 0.20 | 2,100 | 33,800 | 16.1 | 115 | 194 | 0.6 |
| /device-compare/ | 39 | 26,700 | 26,400 | 0.99 | 82.6% | 1.20 | 2,400 | 12,600 | 5.2 | 47 | 45 | 1.0 |
| /local/cell-phones/ | 57 | 37,300 | 135,100 | 3.62 | 98.8% | 3.67 | 3,600 | 37,500 | 10.4 | 144 | 225 | 0.6 |
| /support/ | 93 | 1,900,000 | 1,957,880 | 1.03 | 98.7% | 1.04 | 38,700 | 351,854 | 9.1 | 10,600 | 7,056 | 1.5 |
| /local/fiber/ | 95 | 102,000 | 47,300 | 0.46 | 99.8% | 0.46 | 5,400 | 31,900 | 5.9 | 258 | 245 | 1.1 |
| /buy/ | 95 | 644,000 | 1,014,124 | 1.57 | 98.5% | 1.60 | 19,800 | 206,365 | 10.4 | 7,400 | 3,246 | 2.3 |
| /local/internet/ | 114 | 243,000 | 220,600 | 0.91 | 93.6% | 0.97 | 13,300 | 79,700 | 6.0 | 1,700 | 516 | 3.3 |
| /stores/ | 129 | 312,000 | 2,051,269 | 6.57 | 99.4% | 6.61 | 14,700 | 306,952 | 20.9 | 4,100 | 3,527 | 1.2 |
| /deals/ | 132 | 214,000 | 219,600 | 1.03 | 99.3% | 1.03 | 5,300 | 32,000 | 6.0 | 1,600 | 2,042 | 0.8 |
| /es-us/local/ | 133 | 8,900 | 2,200 | 0.25 | 42.6% | 0.58 | 1,300 | 4,800 | 3.7 | 284 | 62 | 4.6 |

![Figure 5. Twelve URL prefixes on one domain, both instruments, 12 October 2026. Each marker is one prefix; the filled marker is the area-code section. (a) The Semrush over Ahrefs ratio on estimated visits, unmatched for territory, against section age in months since the first month with organic traffic in the Ahrefs all-time series, both axes logarithmic; the horizontal line is a ratio of one. (b) The same ratio against the Semrush over Ahrefs ratio on ranking keywords. Data in Table 4 and in the released file.](fig4_prefixes.pdf)

Six things follow (Figure 5), and the first retracts a claim this paper made in version 4.0.

**The cross-section shows no detectable relationship between the ratio and section age.** Spearman's rank correlation between age and the unmatched visits ratio is −0.11 over twelve prefixes, with a Fisher 95% interval of −0.64 to +0.49 and a permutation p of 0.73; territory-matched it is −0.28; excluding the area-code section it is +0.15. Twelve prefixes give roughly 38% power to detect a correlation of 0.5, so this is not a demonstration that no age effect exists. What it does establish is narrower and sufficient: the ratio does not converge on a common value as sections mature, because the seven sections aged between seven and eleven years sit anywhere from 0.25x to 6.57x unmatched (0.46x to 6.61x matched). The hypothesis in version 4.0, that each vendor's index fills in at its own rate and the ratio settles as a section ages, is withdrawn, and the narrowing of the area-code ratio from 27.1x to 7.5x over three months is reported as an observation on one section and not attributed. Only one prefix in the cross-section is under twenty-one months old, so the first months of a section's life are not characterized here beyond that one case.

**The ratio is prefix-specific, and not one-directional.** Unmatched for territory, Semrush's estimate runs from one fifth of Ahrefs' (/local/bundles/, 0.20x) to seven times it (/local/area-codes/, 7.24x), a spread of 1.55 orders of magnitude, with a median of 1.01 and six of twelve prefixes below one. Matched for territory the spread is wider (0.20x to 8.89x), the median is 1.06, and four of twelve are below one, because two of the six sub-one prefixes cross one once their non-US traffic is removed (/product-compare/, 69.6% US, from 0.75x to 1.07x; /device-compare/, 82.6% US, from 0.99x to 1.20x); /es-us/local/, at 42.6% US, moves from 0.25x to 0.58x and stays below one. The territory objection therefore changes the count and not the conclusion: on the same domain, on the same day, the vendors' estimates differ by factors from well below one to well above it, and no single correction factor maps one onto the other.

**The vendors agree on the ordering of sections and disagree on their magnitudes.** Across the twelve prefixes, the rank correlation between the two instruments' visit estimates is +0.94 (Kendall's tau +0.82, 60 of 66 pairs concordant). The vendors agree on which section is larger in 60 of 66 pairs; what has unknown sign and magnitude is the **correction factor** between the two instruments, which no domain-level constant captures. The consequence for practice is restated in Section 5.6 in that form.

**Keyword universes diverge consistently; visit estimates do not follow them.** Semrush reports more ranking keywords than Ahrefs on every prefix, by between 2.0x and 20.9x. The rank correlation between the keyword ratio and the visits ratio is +0.17 over all twelve, and +0.52 with the area-code section excluded; the second figure is reported because the first is the one the paper is entitled to use and a reader should see both. /local/bundles/ has the second-largest keyword ratio (16.1x) and the smallest visits ratio (0.20x). The larger part of the disagreement is therefore in what each vendor's click model assigns to a discovered keyword, not in how many keywords it discovered, which is consistent with the decomposition in Section 5.6 and inconsistent with the mechanism version 4.0 proposed.

**The section this paper studied is where the instruments disagree most.** It has the highest visits ratio (7.24x unmatched, 8.89x matched; /stores/ is next at 6.57x) and the highest referring-domain ratio (11.3x) of the twelve. The referring-domain outlier has a visible cause: Ahrefs indexed the automated link network described in Section 8 and Semrush largely did not. The visits outlier does not have a visible cause here, and two candidates are stated as hypotheses only: the section's query distribution is unusually long-tailed (Section 6), which click models over estimated volume may treat very differently; and the section was three months old, which the cross-section cannot characterize.

**A measurement result about one of the instruments, established in passing.** Semrush's AI-visibility panel reported 158.3K mentions and 29.5K cited pages for every one of the twelve subfolders, identically, on 12 October (Section 5.3 quotes the 10 October read of 158,100 and 29,600). Those figures are domain-scoped whatever prefix is queried. Section 5.3's withdrawal of the 9.2x AI-answer comparison, made in version 4.1 by inference from the page count, is confirmed by observation.

**Limits.** Twelve prefixes, one domain, one read date; the age proxy is a chart read, left-censored at September 2015 for one prefix and close to that horizon for two more; one prefix under twenty-one months; the territory match uses each prefix's US share as the instrument reports it. A second domain and a second read date are the next step, and neither needs this provider.

### 5.6 What follows for applied search research

**What divergence licenses, and what it does not.** There is no ground truth here. Neither vendor's figure can be checked against a counted visit, because the provider's analytics were not available for this study. Divergence is therefore not error. What two readings A and B of one quantity with true value T license is a bound on the larger error and nothing more:

max(|A − T|, |B − T|) ≥ |A − B| / 2.

At the August ratio of 27.1x, the two readings cannot both lie within a factor of 5.2, the square root of 27.1, of the true value, so at least one of the two estimates lies a factor of five or more from the quantity both are estimating, and this study cannot say which. In absolute terms the bound is larger: the two readings differ by at least 13 times the smaller one. That is the whole of the inference, and it is a property of the pair, not a finding about either vendor: a reader who compares such estimates across instruments should know that on a two-month-old section they can stand a factor of five or more apart, without the comparison itself showing which is closer.

**What the narrowing does and does not support.** The ratio falls 27.1 → 10.2 → 7.5 over three months on this prefix. Version 4.0 attributed this to section age and proposed index coverage as the mechanism. Section 5.5 tested that across twelve prefixes and found no relationship between age and the ratio. Within this one prefix the narrowing is also confounded: section age is collinear with calendar time, and the window contains the September 2026 spam update, the arrival of several hundred automated referring domains, and a vendor data-reliability notice covering two of the four months. The narrowing is reported as an observation on one section and is not attributed.

The index-coverage hypothesis is also the minority term where it can be checked. On 10–11 October, the only date both the visits and the keyword-universe figures were read, the divergence decomposes as

7.47x = 2.02x (keyword universe) × 3.70x (estimated visits per ranking keyword),

so the keyword universe accounts for about 35% of the divergence in log terms and the click model applied to each discovered keyword accounts for 65%. Whatever drives the narrowing, the larger component at that date is not how much surface each vendor has discovered.

**Why the headline ratios understate the disagreement.** The natural objection to Table 2 is territory: Semrush's figure is US and Ahrefs' is worldwide, so the comparison is unfair to Ahrefs. It is, and in the direction that makes the reported ratios conservative. Matching worldwide to worldwide gives 8.62x for October. Matching US to US, deflating the Ahrefs figure by the 18.5% non-US share of its own estimated visits, gives **9.17x** against the 7.5x in the table. The table reports the conservative pairing; the matched ones are stated here.

**Consequence for practice.** The design this bears on is the standard one in applied content work: publish something, read one dashboard, compare it against the rest of the site or against a competitor. Section 5.5 is the finding that bears on it most directly. Across twelve sections of one domain the vendor ratio on estimated visits spans 0.20x to 7.24x (0.20x to 8.89x territory-matched), so no domain-level calibration factor can convert one vendor's figure into the other's. The vendors agree on which of two sections is larger in 60 of 66 pairs, so a single-vendor ranking of sections is usually right in direction; the magnitude of any difference, and any ratio between a section's figure on one vendor and another section's on the other, can differ by a factor of five below to nearly nine above. An effect of the size applied papers usually report is small against that. Both instruments remain the appropriate tools for ranking sections and for directional comparison; this result concerns the comparability of magnitudes across instruments, not the usefulness of either. It is also the measurement that motivates the framework in Figure 1: a content program that needs the magnitude of demand for a topic cannot read it from one volume tool alone. That the demand which never reaches a search box differs in which topics it names and in what form it takes is the framework's hypothesis, not a consequence of this measurement, and Section 11 registers its test. Reporting both makes the range of estimates visible; reporting one does not.

**The limits of this result.** One domain, one vendor pair, no ground truth; the longitudinal series is one prefix over 77 days and the cross-section is twelve prefixes on one date. What is established is that disagreements of up to an order of magnitude occur in both directions between sections of one site, from a factor of five below to nearly nine above, that no relationship with section age is detectable across twelve sections, only one of them under twenty-one months old, and that keyword-universe size does not predict them. What is not established is which instrument is closer to the truth for any section, or what determines the ratio. Section 11 sets out the next step: a second domain and a second read date.

### 5.7 Two demand signals on one taxonomy: reviews against keyword volume

The framework's premise can be tested wherever a first-party demand surface and a tool-derived one describe the same industry. A separate dataset in the same industry allows a first run. It holds 47,485 Google reviews of 378 retail locations of major US telecom carriers, obtained through DataForSEO under its licence and exported on 8 September 2026, of which 37,193 carry text; and a 42,994-node telecom taxonomy built by the author's clustering engine from 1,898,584 keywords, each node carrying DataForSEO monthly search volume. Reviewer names were discarded before analysis and only per-label counts are reported. Reviews were linked to taxonomy labels with the released exact-match linker (`TokenLinker`), so every attribution is auditable from the label. The taxonomy repeats generic labels under many parents, so a label is one linking unit and its volume is the sum over the nodes that carry it. Of the 37,193 reviews, 20,663 (55.6%) linked to at least one of 27,817 linkable labels, at 2.25 labels per linked review, and 1,008 labels were mentioned at least once.

At the level of the taxonomy's 17 top-level branches the two signals agree: the share of review mentions and the share of search volume have a rank correlation of +0.78 (p < 0.001; Figure 6b). At the level of topics they barely do. Across the 1,008 labels the rank correlation between review mentions and monthly volume is +0.19 (Kendall's tau +0.13), +0.28 among the 213 labels with at least twenty mentions, and +0.16 (p = 0.10) among the 106 labels mentioned at least twenty times in one- and two-star reviews (Figure 6a). Of the 1,008 labels, 367 (36.4%) carry under 1,000 monthly searches and 106 (10.5%) carry none. Reviews concentrate on carriers and the store experience, 73.0% of mentions against 29.4% of search volume; broadband is 18.8% of search volume and 0.7% of mentions.

The complaint the author's practice had identified is the cleanest case. Of 6,620 one- and two-star reviews, 924 (14.0%) mention waiting, against 1.9% of five-star reviews; the taxonomy built from 1.9 million keywords holds one label containing "wait", at 12 searches a month. The pain point most often named by unhappy customers is close to invisible to the volume tool, and what it calls for is a product or service change, such as appointment booking or digital check-in, rather than a page.

![Figure 6. First-party demand against tool-derived demand on one industry taxonomy: 37,193 Google reviews of 378 retail locations of major US telecom carriers, linked to a 42,994-node taxonomy carrying vendor monthly search volume (both sourced through DataForSEO). (a) Each marker is one of the 1,008 taxonomy labels mentioned in at least one review; filled squares carry zero reported volume. (b) Share of review mentions against share of search volume for the nine largest of the 17 top-level branches. Only aggregate counts are shown.](fig9_reviews.pdf)

This is a first run, not the registered study. It uses one first-party surface on one platform in one industry, exact-match linking whose precision has not been hand-checked, relative review dates, and a taxonomy whose labels are themselves search phrasings, which biases the comparison toward agreement. The reviews describe store locations rather than the area-code section of Sections 5.1 to 6, so this result tests the framework's demand premise and not the deployment. Within those limits it establishes the framework's narrowest claim: on one industry, what people write in their own words and what a volume tool counts agree on the broad shape of demand and disagree on its topics, and the disagreement is largest for complaints.

## 6 The deployment series

This section is context for Section 5, not a claim. It describes what two instruments recorded following the publication of 381 code pages and their hubs, on a domain and a topic that satisfy all six conditions in Section 3.1.

*Table 5. Outcomes at each checkpoint. Ahrefs daily series for the prefix, all locations; AI answers from Brand Radar at the nearest stored date; read 11 October 2026. Day 37 is the primary checkpoint. "n/r" means not recorded: the quantity was not captured on that date, the daily series does not retain it, and it is not interpolated here.*

| Metric | Day 0 (26 Jul) | Day 15 (10 Aug) | Day 30 (25 Aug) | **Day 37 (1 Sep)** | Day 45 (9 Sep) | Day 60 (24 Sep) | Day 75 (9 Oct) | Day 77 (11 Oct) |
|---|---|---|---|---|---|---|---|---|
| Pages holding a position | 2 | 210 | 365 | **n/r** | 391 | 414 | 440 | 441 |
| Ranking positions, all | 2 | 3,385 | 14,905 | **15,830** | 20,326 | 37,141 | 43,302 | 43,980 |
| Positions 1–3 | 0 | 727 | 1,801 | **1,874** | 2,649 | 5,822 | 8,753 | 9,239 |
| Positions 4–10 | 1 | 1,494 | 10,151 | **n/r** | 15,104 | 28,733 | 33,203 | 33,560 |
| Positions 11–20 | 0 | 909 | 2,639 | **n/r** | 2,331 | 2,336 | 1,276 | n/r |
| Positions 21–100 (derived) | 1 | 255 | 314 | **n/r** | 242 | 250 | 70 | n/r |
| Estimated visits (Ahrefs) | 2 | 22,016 | 51,517 | **≈51,800** | 92,897 | 244,041 | 221,933 | n/r |
| Live referring domains | 0 | 1 | 19 | **19** | 415 | 828 | 909 | 913 |
| AI answers citing the section | 0 | 1,603 | 3,725 | **n/r** | 6,390 | 10,266 | 14,823 | 17,206 |

The 21–100 row is derived as the total less the three reported bands, because Section 4.1 defines a ranking position as positions 1–100 while the instrument reports only three bands and the total. It is arithmetic on vendor estimates and not a fourth measurement. It closes every full column. Day 77 is the last read of the series and the one the abstract and this section quote; positions 11–20 were not captured that day, so the 21–100 row cannot be derived for it, and the daily visits series was read only to day 75 (the October run-rate in Table 2 is a different construct). Its referring-domain figure is the instrument's overview count, which differs from its daily series (Section 8).

Day 75 falls inside the window the Ahrefs data notice covers, and day 60 is the first day of the spam update. The estimated-visits peak at day 60 coincides with that day, and the subsequent fall is consistent with either a data artifact or a ranking change; this study does not distinguish them.

**At the primary checkpoint**, 37 days after publication, the section held 15,830 ranking positions, 1,874 of them in positions 1 to 3, with an estimated 51,800 monthly visits and nineteen referring domains. By day 77 it held 43,980 positions across 441 URLs holding at least one position, ranked for 29,000 keywords in one instrument and 58,586 in the other, was recorded as a cited source in Google AI Overviews on 7,455 keywords, and appeared in 17,206 stored AI answers.

**Concentration.** Of the 441 URLs holding a position on 11 October, the ten highest-traffic carry 22.8% of estimated visits and the top 50 carry 64.9%, both from one instrument and both on a universe selected by the outcome. Fifty of 441 is 11% of the pages carrying about two thirds of the estimated traffic, which is concentration, not breadth; an earlier claim of breadth is withdrawn (Appendix A).

**Demand the volume tools do not report.** Among the 58,586 US keywords, the lowest-traffic rows are misspellings, non-English forms, numeric fragments and question forms with 40 to 170 reported searches a month or none at all. The section ranks in 105 countries, with 18.5% of Ahrefs-estimated visits from outside the US. This is stated as a distributional observation and not as a test; the per-page threshold test that would make it one requires the full per-page keyword export matched to pre-launch reported volume, which has not been run.

## 7 What the answers cite, and what they do not

### 7.1 Enumerating pages outrank per-entity pages

The pages most cited in AI answers are state hubs that enumerate codes, cities and maps: New York 474 answers, California 337, Texas 322, Florida 304, and the national hub 294. Each exceeds any individual code page: 214 Dallas 238, 786 Miami 228, 404 Atlanta 218 (Figure 7).

![Figure 7. The eight pages under the prefix most often cited in stored AI answers, Ahrefs Brand Radar, 11 October 2026. Enumerating pages (state hubs and the national hub) are solid; per-entity code pages are hatched.](fig5_cited.pdf)

A per-entity content strategy predicts the opposite. The question "where is area code 214" is answered most directly by the 214 page, and that page is cited less than the page listing every Texas code. If this generalizes, enumerating pages are more citable than per-entity pages for this class of question, and the unit a content program should publish is not the unit the question names. This is the framework's form question in miniature: the form in which a question is best answered is an empirical property to be measured, which is why the framework scores unanswered questions and leaves form to be tested, and why the Content Gap Score carries no form term (Appendix B).

It is an observation on one section. It is the finding in this paper most worth testing elsewhere, and testing it needs no access to this deployment: any site with both hub and per-entity pages on an enumerable class can check it.

### 7.2 Who else is cited, and what that does not establish

The queries are held, and the AI answers supplied, by encyclopedic and directory sites. The five domains with the largest keyword overlap with the section are two area-code directories, a time-zone reference and two voice vendors, at Domain Ratings between 13 and 83. Wikipedia, at 97, is co-cited in roughly 11,000 of the answers that cite the section. Two other national carriers of comparable authority are co-cited 9 times (Domain Rating 91) and 240 times (Domain Rating 87), against the section's 17,206. Neither published a page per code.

**This establishes nothing about necessity**, and earlier versions of this work claimed that it did. The counts are co-citations *within the set of answers that cite the provider*, a set selected because the provider is in it. A carrier absent from that set may be present across answers the provider is absent from, and no instrument here is pointed at those answers. The counts bound the carriers' co-presence from below within a selected set and support no statement about what authority alone produces, nor about whether content on the topic was necessary.

The comparison that would establish it is outcome-independent and has not been run: the registry's codes crossed with a fixed set of verbalizations, queried without reference to who is cited, so that each domain's presence is measured on a denominator none of them selected. Section 11 registers it.

## 8 The link profile

The section had zero live referring domains through 31 July, one on 10 August, and nineteen on 25 August and still nineteen on 1 September, by which date it already held 15,830 ranking positions.

The referring-domain count on 11 October is reported by the instrument as 913, while the same instrument's daily series gives 909 at day 75 and its new-and-lost report for September gives 917 new against 95 lost, which with nineteen at day 37 implies 841. Three figures for quantities that should nearly agree. The gap is partly explained by domains gained and lost within the month counting in both columns, and not wholly. No claim here turns on the exact count; the shape is nineteen through day 37, several hundred within three weeks, roughly nine hundred by day 75.

The character of the arrivals is not in doubt. They are automated networks: 61.9% .info, 26.4% .asia, 10.2% .xyz, every linking page at URL Rating below 10, top anchors advertising link sellers. The second instrument indexes 80 referring domains for the subfolder, 88% from domains at Authority Score 0–10 and 75% on .xyz.

### 8.1 What the link profile can and cannot explain

*Table 6. Position growth by interval, with the link status of each.*

| Interval | Referring domains | Domains gained | Positions gained | Rate | Link status |
|---|---|---|---|---|---|
| Day 0 to 15 | 0 to 1 | 1 | 3,383 | 226 / day | clean |
| Day 15 to 30 | 1 to 19 | 18 | 11,520 | 768 / day | clean |
| Day 30 to 37 | 19 to 19 | 0 | 925 | 132 / day | clean |
| Day 37 to 45 | 19 to 415 | 396 | 4,496 | 562 / day | network arriving |
| Day 45 to 60 | 415 to 828 | 413 | 16,815 | 1,121 / day | network present |
| Day 60 to 75 | 828 to 909 | 81 | 6,161 | 411 / day | network present, data notice |

![Figure 8. Ranking positions and the link profile over 77 days. Upper panel: ranking positions in positions 1 to 100 and in positions 1 to 3, Ahrefs daily series for the prefix, all locations, read 11 October 2026; the hatched band is the interval in which the automated link network arrived; the vertical rules mark the primary checkpoint (day 37), the September 2026 spam update (day 60) and the vendor data-reliability notice (day 65); live referring domains at each checkpoint are printed along the top. Lower panel: positions gained per day in each interval of Table 6, shaded by link status. The upper panel also plots two reads from the same daily series that are not checkpoints in Table 5: day 6 (984 positions, 186 in 1–3) and day 67 (38,801 and 6,942).](fig6_positions.pdf)

Of the 43,302 positions held at day 75, 15,830 (36.6%) were held at day 37 and 27,472 (63.4%) were acquired after the network began arriving (Figure 8). Because the arrival is dated only to an eight-day interval, that share is itself bounded rather than exact: 53.1% to 63.4%. For AI answers, day 37 is not recorded, so the corresponding share is bounded 56.9% to 74.9%.

**What survives.** A result of 15,830 ranking positions and 1,874 top-three positions was established with nineteen referring domains, a count unchanged for the preceding week. That result does not depend on link acquisition, and it is this paper's negative result about links, stated at the checkpoint that supports it.

**What does not.** Any claim about the full series. An earlier version concluded that link acquisition plays no part in explaining the outcome; most of the series postdates the network.

**What the table does not show, against the temptation to read it as showing it.** The fastest clean interval, 768 a day across days 15 to 30, is 37% faster than the 562 a day of the arrival interval. Reading the 132-a-day trough immediately before the arrival as a baseline would suggest an acceleration; that baseline sits at the series minimum, and the inference does not survive showing all six intervals. A 441-page section entering an index does not grow linearly. The network is therefore **unbounded as a confound on the continuation**, and nothing here shows that it accelerated anything.

**Disclosure.** The provider has an exposure this paper discloses rather than analyzes: a spam link profile pointed at a live section, which the provider has been asked to review. A manual action before a later checkpoint would confound any continuation of this series. The author did not commission, purchase or solicit any link to the section.

## 9 What the deployment cost, and what it got wrong

### 9.1 Cost

These figures are the author's reconstruction from project records, not an accounting extract, and are stated to the nearest useful unit rather than implied to be precise. They are included because a deployment paper without them gives a reader no basis for deciding whether to attempt the same thing (Table 7).

*Table 7. What the deployment cost, as reconstructed by the author from project records.*

| Item | Figure | Basis |
|---|---|---|
| Analysis and class selection | ≈ 3 person-weeks | taxonomy construction, classifier runs, the re-homing pass and a structured review, Nov 2025 to Jul 2026, part-time alongside other duties |
| Template and generation build | ≈ 2 person-weeks | one page template, the registry-to-page generator, internal linking and structured markup |
| Content production, marginal | ≈ 0 | every fact templated from the public registry; no writer, editor or per-page review |
| Editorial and link acquisition | 0 | no outreach, no placement, no paid promotion |
| Third-party data | ≈ USD 6,000 / year | Ahrefs and Semrush subscriptions already held for other work; no incremental spend attributable to this deployment |
| Engineering to publish the section | within existing platform capacity | generated into an existing CMS and publishing pipeline; no new infrastructure |

Two things follow for a reader considering transfer. The marginal cost per page was near zero *because* conditions 1 to 3 of Section 3.1 held, and they do not hold for most classes. And the dominant cost was analysis rather than production, which inverts the usual content-program cost structure and is the part a reader should expect to pay.

### 9.2 Six lessons, stated as this deployment's failures

Each is something this deployment got wrong, which is why its cost can be stated.

1. **Separate structure sources from coverage sources, or do not claim a method.** This deployment did not, so its demand layer derives from what competitors already rank for. Cost: an evaluated method claim; the framework is specified in Appendix B, and this deployment cannot serve as its validation.
2. **Freeze the evaluation query set before launch.** This deployment did not, so every share in this paper would otherwise be computed on a denominator selected by the outcome. Cost: all comparative claims. The released implementation makes freezing a command so the failure is harder to repeat.
3. **Collect at least one first-party demand surface before claiming anything about users.** This deployment collected no first-party surface: of the thirteen demand surfaces the released implementation reads (Figure 1a), only competitor keyword exports, a tool-derived surface, were linked to any entity; no forum, Q&A, video, social, review or support data was. Cost: the deployment cannot show that the framework's user-question layer did any work; that layer is specified in Appendix B, exercised in the released example on synthetic records flagged as synthetic, and untested on this deployment's data; Section 5.7 runs the comparison on a separate review dataset.
4. **Record the recommendation and its date.** The document that turned analysis into a build decision is not in retrievable form. Cost: the causal chain has no anchor at its most important link.
5. **Get a second grader early.** Grading judgments with agents the author built, and planning independent annotation for later, means the reliability statistic arrives after the claims that depend on it. Cost: Appendix B's inputs are unvalidated.
6. **Expect the class that scores well to have no commercial page to attach to.** Area codes are a reference topic on a commercial domain. The score has no feasibility term and someone must decide how business relevance enters.

## 10 Threats to validity

**Instrumentation**, which is the subject of Section 5 rather than a caveat on it. No outcome is a measured visit. On the area-code prefix the two instruments differ by 7.5x to 27.1x on estimated visits, 2.0x on ranking keywords and 11.4x on referring domains; across twelve prefixes of the same domain the visits ratio runs from 0.20x to 8.89x. A fourth comparison, on AI answers, is withdrawn in Section 5.3 as a scope mismatch rather than a divergence. One instrument posted a data-reliability notice covering days 65 to 75. Internal analytics would resolve much of this and are not available.

**Confounding, with directions.** Domain authority: direction positive, magnitude unknown, **no bound available**. An earlier version named the carrier comparison in Section 7.2 as a bound; that comparison is computed on a set selected on the provider's presence and bounds nothing. Content quality and execution: templating, registry facts, structured markup and internal linking are perfectly confounded with selection; direction positive; no estimate. Topic contest: no defender responded. The automated link network: between 53.1% and 63.4% of day-75 positions postdate its arrival, the range reflecting that the arrival is dated only to an eight-day interval; direction unknown, magnitude unestimated, and confounded with index maturation and with the September spam update. Algorithm updates: one named, dated update falls in the window, on the day of the traffic peak; whether unannounced ones did is not knowable from here.

**Selection.** The query universes were defined after launch. Counts are reported on them; shares are reported only where the denominator is stated and flagged, or where the quantity is a ratio between two instruments on the same prefix, which selection does not affect.

**Construct.** "AI Overview citation" has two operational definitions here and they differ by a factor that falls from 2.94 to 1.34; both are reported. "Visibility" is not value: no revenue, conversion or impression figure appears in this paper and none should be inferred.

**Non-human traffic.** The estimated-visit figures are vendor click models and do not distinguish automated from human requests. A section attracting an automated link network may also attract automated requests. No instrument available here separates them, and the estimated-visit figures should be read with that unresolved.

**External validity.** One organization, one industry, one class, a top-authority domain, 77 days, six stated conditions. For Section 5's divergence result: twelve prefixes on one domain, one of them followed for 77 days; one vendor pair; one read date for the cross-section; no ground truth.

**Author independence.** The author designed the approach, deployed it as an employee of the organization studied, performed every measurement, wrote this paper, holds a commercial interest in tools built on the approach, and is the author of a forthcoming book that uses its name. No part of the evaluation has been performed by anyone else. A reader should treat every judgment here as made by an interested party, and should weight Section 5's instrument readings, which are independently reproducible from two commercial subscriptions, far above anything else in the paper. Section 5 is the primary result partly for that reason.

## 11 What would test what this paper declines to claim

**The within-class control, withdrawn.** Versions 3.1 to 4.1 registered a within-class control: the geographic codes for which no page was published, queried on the same instruments as the published ones. Section 3 records that no such set exists. The section holds a page for every geographic code assigned to a US state or the District of Columbia; the six territory codes without pages are too few and too different in kind to serve. The design is withdrawn, and the paper no longer claims a permission-free test of whether publishing a page did anything. The closest substitute is external: a comparable-authority domain that covers the class partially, which this study has not identified.

**The enumerating-pages test, which needs no access to this deployment.** Section 7.1 reports that state hub pages are cited in AI answers roughly twice as often as the individual code pages they enumerate. Any site holding both hub and per-entity pages over an enumerable class can test whether that ordering holds, on either instrument, with no reference to this provider.

**An outcome-independent query universe.** The registry's geographic codes crossed with a fixed set of question verbalizations yields a query set that is complete with respect to the class, defined without reference to any outcome, and hashable. The released implementation writes it: `ufi freeze` produces the set with its digest. The example ships a 924-query demonstration over the 66 codes in its registry extract, at digest `f05ce279942be5f8`; the set for the full class would be built the same way.

**A prospective study on an ordinary domain.** A second industry, a domain outside the top decile of authority, the ontology and parameters registered before collection, the query set frozen and hashed before launch. Three classes with matched page counts: top class by mean score, top class by volume, and a class in the bottom quartile of the score. Primary outcome: top-ten presence on the frozen set at day 37. The parameters are already locked: **α = 0.5, β = 0.5, damping = 0.85, lock digest `7290a2235d8de05f`, locked 12 October 2026**, which is what would make this a test rather than a fit.

**An annotation study**, two graders independent of the author, on a sample of the coverage and answerability items, reporting weighted kappa with bootstrap intervals. The released implementation caches judgments keyed on the rubric, so a second grader costs one pass.

**The multi-platform demand study, which is the framework's own test.** Section 5.7 is a first run on one surface; the registered study extends it. For one enumerable class, collect user questions from the first-party surfaces in Figure 1a (forum, question site, video comments and transcripts, reviews, social groups, support tickets), link them to entities with the released linker, and compare the resulting demand distribution with the keyword-volume distribution for the same entities. The registered prediction is that the two distributions differ in both which entities carry demand and in what form the demand takes (question, comparison, how-to, video), and that the difference is largest where reported volume is smallest. The released implementation reads every surface and prints which returned rows, so a run that collected nothing cannot be reported as one that did.

**A persona study on AI answer surfaces.** The same frozen query set issued to AI answer surfaces under a small set of stated personas (for example parent, business owner, traveller), with the cited sources and the answer text compared across personas. The question is whether the answer and its citations vary with who is asking, which classic web search audits found only weakly for demographic attributes [Hannak et al. 2013] and which no audit has measured for composed answers.

**A second domain for Section 5.5.** The cross-section was run on one domain. The result that the vendor ratio is prefix-specific, with no detectable relationship to age, needs a second site and a second read date before it is more than an observation about one domain. Anyone with both subscriptions and any multi-section site can do it in a day; the data file released with this paper gives the read method.

## 12 Reproducibility, ethics and conflicts of interest

**What is released.** The `ufi` reference implementation at **https://github.com/VenkataPagadalaGIT/ufi** under Apache 2.0, version 0.2.0: test suite, command line interface, and a worked example that runs offline on public data. The corrected numbering-plan ontology in YAML with OWL and SHACL export, and the area-code dataset the example uses. The demand layer ships adapters for thirteen surfaces and a coverage report that prints which surfaces returned rows. The frozen 924-query set, the parameter lock and the run manifest are committed in the repository at `examples/nanp/out/`, so the digests quoted in Section 11 and Appendix B resolve to released files. It has **no DOI**; a Zenodo deposit is outstanding. The exported OWL and SHACL mint terms under `urn:ufi:<name>` by default, which makes no resolution claim; no persistent namespace has been registered.

**Data released with this version.** The twelve-prefix cross-section (Table 4) is released as two CSV files, one per instrument, each row carrying the prefix, the figures read, the read date and the read method, at `data/instrument_divergence/` in the repository named above.

**What a reader can verify independently.** Every figure in Sections 5 and 6 can be re-read from the same two dashboards for the same prefix, subject to index drift. The exception is the Brand Radar answer count, which moved from 14,823 (9 October) to 17,206 (11 October) and 17,400 (12 October) as stored answers were refreshed; it is reported with its read date and is not claimed to be re-readable. The Ahrefs daily series reproduces the checkpoint rows until it ages out of the six-month window.

**What is not released.** The provider's internal graph database, the crawl of its site, and its analytics. No figure in this paper is drawn from them; the cost figures in Section 9.1 are the author's reconstruction from project records.

**Ethics, data collection and site terms.** No human subjects were involved; no user-level, session, cookie or personally identifying data was collected or analyzed. The deployment published reference pages and ran no experiment on visitors. Outcome figures come from commercial dashboards read through their own interfaces under paid subscriptions, within those vendors' terms; no vendor was scraped and no API was used to assemble the series. This study performed no crawl of any third-party site; the provider's own site crawl is an internal operation on the organization's own property. Page facts derive from the numbering plan administrator's public registry and US Census data, both public-domain US government sources. The review dataset in Section 5.7 was obtained through DataForSEO, a licensed data provider, under its terms; reviewer names were discarded before analysis, no review text is reproduced, and only per-label aggregate counts are reported.

*Competitive effects.* The deployment displaced incumbent pages, mostly specialist directories at Domain Rating 13 to 83, in a public search index. This is a commercial outcome with distributional consequences for smaller publishers, and the informational value added is modest, because the registry had already published the facts. Condition 6 of Section 3.1 can be read as a criterion for selecting undefended targets. That reading is available and this paper does not endorse it; a method whose transferable content is "find a finite factual class that an authoritative free registry already answers and that no one is defending" deserves to be stated in those terms so that the question can be asked.

**Corrections to earlier versions.** Appendix A is the single record of corrections across versions, including those that change how a figure must be read.

**Organizational permission.** The organization that operates the section approved publication of the figures in this paper. Approval date: *[to be completed]*. Approving role and unit: *[to be completed]*. Scope: *[to be completed]*. **These three fields are unfilled, and the manuscript is not submitted anywhere until they are.** The organization is not named in this paper. Not naming it does not make it unidentifiable: the prefixes in Table 4 and the conflict-of-interest statement in Section 10 allow a reader with access to the same instruments to identify it, and that statement is kept because the disclosure is required. The name is withheld; the identity is not claimed to be concealed.

**Conflicts of interest.** As stated in Section 10. The mitigations are weaker than the conflict: the primary result is two vendors' readings of a public prefix that any reader with the same subscriptions can re-read, the implementation is released so the specification can be checked against the description, and the designs in Section 11 are registered before their data exist.

**What has not been done, after seven rounds of internal review.** No independent party has checked any number in this paper. The one check that would change that requires nobody's permission, budget or cooperation: a third-party re-read of the day-37 row of Table 5 and of Table 4 from the same dashboards. It has not been performed. The cross-prefix replication registered in version 4.0 was performed on 12 October 2026 (Section 5.5); the within-class control registered with it was found not to exist (Section 3). A reader is entitled to weigh that the remaining undone check is the only one requiring another person's name.

## 13 Conclusion

User First Intelligence starts from the observation that people ask most of what they want to know somewhere other than a search box, and that the tools which count search demand see only the countable part. The framework goes beyond the website to where the questions are, classifies and links them to an industry held under an ontology, keeps structure, coverage and demand in separate roles in a knowledge graph, asks that graph competency questions, and scores where the organization fails to answer, with the form of the answer treated as a property to measure rather than assume, as Section 7.1 shows in miniature. It is specified in Appendix B and released as an open implementation reading thirteen demand surfaces, with executable competency questions whose schema pass rate and instance coverage are reported separately. On 37,193 business reviews linked to a 42,994-node keyword taxonomy, what customers wrote and what the volume tool counted agreed on the broad shape of demand (+0.78 across branches) and diverged on its topics (+0.19), most for complaints: one in seven unhappy reviews named waiting, which the taxonomy records at 12 searches a month. Its scoring function is not evaluated here, and the deployment itself collected demand from one surface of the thirteen; Section 11 registers the multi-platform demand study and the persona study on AI answers that would test the framework's two central claims, with parameters locked before any data exist.

What the deployment measured is the reason the framework's demand layer exists. Two commercial analytics platforms watched the same section from the day it appeared. Over four months they disagreed about its estimated traffic by factors between 7.5 and 27.1, about its ranking keywords by a factor of two, and about its referring domains by a factor of eleven. Read on the same day across twelve sections of the same domain, their ratio on estimated visits ran from one fifth to seven times, with no detectable relationship to how old each section was or to how many keywords each vendor had found. The disagreement is larger than the effects most applied search papers report, the correction factor between the vendors has no fixed sign or size, and it cannot be applied at the domain level; the vendors rank sections alike and size them differently, so a single-vendor study of magnitudes carries an estimation range it cannot bound from its own data, while a single-vendor ranking of sections is usually right in direction.

The deployment underneath that measurement is reported as context. Following the publication of one page per member of a finite enumerable class, templated from a free registry on a top-decile domain that no comparable competitor covered and no one defended, the section held 15,830 ranking positions with nineteen referring domains at day 37, and by day 77 appeared in 17,206 recorded AI answers having earned no editorial link. The pages most cited were the ones that enumerate rather than the ones that answer. What that conjunction depended on, and in what proportion, is not estimated here, and the within-class comparison that would have begun to estimate it cannot be run on this section, because every code in the class has a page.

## References

Balaraman, V., Razniewski, S., & Nutt, W. (2018). Recoin: Relative completeness in Wikidata. In *Companion Proceedings of The Web Conference 2018* (pp. 1787–1792). ACM.

Belkin, N. J., Oddy, R. N., & Brooks, H. M. (1982). ASK for information retrieval: Part I. Background and theory. *Journal of Documentation, 38*(2), 61–71.

Broder, A. (2002). A taxonomy of web search. *SIGIR Forum, 36*(2), 3–10.

Buckley, C., & Voorhees, E. M. (2004). Retrieval evaluation with incomplete information. In *Proceedings of the 27th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 25–32). ACM.

Chapekis, A., & Lieb, A. (2025, July 22). *Google users are less likely to click on links when an AI summary appears in the results.* Pew Research Center.

Galárraga, L., Razniewski, S., Amarilli, A., & Suchanek, F. M. (2017). Predicting completeness in knowledge bases. In *WSDM '17* (pp. 375–383). ACM.

Goel, S., Broder, A., Gabrilovich, E., & Pang, B. (2010). Anatomy of the long tail: Ordinary people with extraordinary tastes. In *WSDM '10* (pp. 201–210). ACM.

Golebiewski, M., & boyd, d. (2018). *Data voids: Where missing data can easily be exploited.* Data & Society Research Institute.

Hannak, A., Sapiezynski, P., Molavi Kakhki, A., Krishnamurthy, B., Lazer, D., Mislove, A., & Wilson, C. (2013). Measuring personalization of web search. In *Proceedings of the 22nd International Conference on World Wide Web (WWW 2013)* (pp. 527–538). ACM.

Haveliwala, T. H. (2002). Topic-sensitive PageRank. In *WWW '02* (pp. 517–526). ACM.

Hopkinson, A., Gurdasani, A., Palfrey, D., & Mittal, A. (2018). Demand-weighted completeness prediction for a knowledge base. In *NAACL-HLT 2018, Industry Papers* (pp. 200–207). ACL.

Langridge, P. (2016, June 13). *How accurate are website traffic estimators?* Screaming Frog. https://www.screamingfrog.co.uk/how-accurate-are-website-traffic-estimators/ (25 sites, February to April 2016, against Google Analytics; accessed 12 October 2026.)

Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczyński, M., & Joosen, W. (2019). Tranco: A research-oriented top sites ranking hardened against manipulation. In *Proceedings of the Network and Distributed System Security Symposium (NDSS 2019)*. Internet Society.

Linehan, L., & Guan, X. (2025, August 11). *Only 12% of AI cited URLs rank in Google's top 10 for the original prompt.* Ahrefs. https://ahrefs.com/blog/ai-search-overlap/ (15,000 long-tail prompts across ChatGPT, Gemini, Copilot and Perplexity; accessed 12 October 2026.)

Luggen, M., Difallah, D., Sarasua, C., Demartini, G., & Cudré-Mauroux, P. (2019). Non-parametric class completeness estimators for collaborative knowledge graphs: The case of Wikidata. In *ISWC 2019* (pp. 453–469). Springer.

Martinez, O. (2026). *Optimizing visibility in generative engines: A critical survey of generative engine optimization (2023–2026).* arXiv:2607.14035.

Piccardi, T., Catasta, M., Zia, L., & West, R. (2018). Structuring Wikipedia articles with section recommendations. In *SIGIR '18* (pp. 665–674). ACM.

Razniewski, S., Arnaout, H., Ghosh, S., & Suchanek, F. (2024). Completeness, recall, and negation in open-world knowledge bases: A survey. *ACM Computing Surveys, 56*(6), Article 150. https://doi.org/10.1145/3639563

Razniewski, S., Suchanek, F. M., & Nutt, W. (2016). But what do we actually know? In *AKBC 2016* (pp. 40–44). ACL.

Redi, M., Gerlach, M., Johnson, I., Morgan, J., & Zia, L. (2020). *A taxonomy of knowledge gaps for Wikimedia projects.* arXiv:2008.12314.

Ripoll, M., Reeves, N., Kurteva, A., Simperl, E., Meroño Peñuela, A., & Diepold, K. (2025). *Filling in the blanks? A systematic review and theoretical conceptualisation for measuring WikiData content gaps.* arXiv:2505.16383.

Scheitle, Q., Hohlfeld, O., Gamba, J., Jelten, J., Zimmermann, T., Strowes, S. D., & Vallina-Rodriguez, N. (2018). A long way to the top: Significance, structure, and stability of Internet top lists. In *Proceedings of the Internet Measurement Conference 2018 (IMC '18)*. ACM.

Shao, Y., Jiang, Y., Kanell, T. A., Xu, P., Khattab, O., & Lam, M. S. (2024). Assisting in writing Wikipedia-like articles from scratch with large language models. In *NAACL 2024.* ACL.

Soulo, T. (2022, May 3). *How accurate are the search traffic estimations in Ahrefs? (New research).* Ahrefs. https://ahrefs.com/blog/traffic-estimations-accuracy/ (1,635 sites against Google Search Console; accessed 12 October 2026.)

Taylor, R. S. (1968). Question-negotiation and information seeking in libraries. *College & Research Libraries, 29*(3), 178–194.

Vaughan, L., & Yang, R. (2013). Web traffic and organization performance measures: Relationships and data sources examined. *Journal of Informetrics, 7*(3), 699–711.

Webber, W., & Park, L. A. F. (2009). Score adjustment for correction of pooling bias. In *Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 444–451). ACM.

Wulczyn, E., West, R., Zia, L., & Leskovec, J. (2016). Growing Wikipedia across languages via recommendation. In *WWW '16* (pp. 975–985). ACM.

Xu, H., Iqbal, U., & Montgomery, J. M. (2026). *Measuring Google AI Overviews: Activation, source quality, claim fidelity, and publisher impact.* arXiv:2605.14021.

Zobel, J. (1998). How reliable are the results of large-scale information retrieval experiments? In *Proceedings of the 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 307–314). ACM.

## Appendix A: Version history

This manuscript is the fourth structural version and has been through seven rounds of adversarial internal review. The history is recorded here rather than in the body, where in version 3.3 it had grown to 26% of the text and had become larger than the results section. Entries are in version order.

**v1 to v2.2.** Framed as a method paper for a Content Gap Score, with the deployment as its validation. Three statements were false and are corrected: that two independent annotators had graded the audit samples (none had, and no annotation study has been run); that the ontology had been released (nothing had been); and an assertion of organizational permission with the date left blank. The first was the most serious: a past-tense claim of an independent check that did not happen, in a document naming the organization.

**v3.0.** Reframed as a deployment measurement study and retitled. The score was withdrawn as an evaluated contribution. A section on what the paper does not report was placed before the results.

**v3.1 to v3.3.** Three corrections that change how a figure must be read. The October 2025 carrier exports were certified as "the one pre-launch artifact that was not selected on the outcome"; they are ranked-keyword exports, selected on a prior ranking outcome. Day 45 was named the primary checkpoint on the stated ground that it preceded the automated link arrival, which the paper's own table refutes; the checkpoint is day 37. And the conclusion that link acquisition played no part in explaining the outcome does not hold across the series, because most of the series postdates the network; it is now stated at day 37 only.

Two further corrections were to arguments rather than figures. A replacement argument in v3.1 held that the per-keyword and pooled views ran over identical rows so selection was held constant; they run over different row sets and the argument fails. And a draft of the link-interval analysis reported only the intervals that made the confound look largest, inferring an acceleration from a baseline chosen at the series minimum; showing all six intervals withdraws it.

**v4.0.** Restructured and retitled. The instrument divergence, present in the data since v2.2 and never advanced as a result, becomes the primary contribution, because it is the finding that does not rest on the author's judgment. The deployment series is demoted to context. The scoring function moves to Appendix B. Claims the preceding versions had conceded piecemeal are removed rather than carried with a qualification attached.

**v4.1 to v4.3.** Corrections to statements version 4.0 had made. The 9.2x comparison of AI-answer counts was withdrawn as a scope mismatch, because the second instrument's count is scoped to the domain rather than the prefix, and a claim about platform ordering resting on a breakdown that did not sum to its total was dropped. Divergence between instruments had been described as error; it is a bound on the larger error and nothing more (Section 5.6). The October row of Table 2 had been labeled month-to-date; it is a monthly run-rate. The AI Overview ratio in Table 3 had been described as purely definitional; it is partly territorial. The deployment had been described as broad rather than driven by a few pages, alongside figures that contradicted it; the breadth claim was withdrawn and only the internally consistent concentration figures are kept. Adjacent sentences had counted two and three algorithm updates; one named, dated update falls in the window. In v4.2 and v4.3, the page count was corrected. The section's page count was verified by fetching every code page linked from its 52 state hubs. It holds 381 code pages, not 290, and covers every geographic code assigned to a US state or DC. The 88-code within-class control registered since v3.1 therefore does not exist and is withdrawn. The author confirms all pages were published together at launch, so the 290 was a miscount and the section did not grow during the window.

**v4.4.** The five incomplete reference entries and three uncited ones were resolved against primary sources.

**v4.5.** The cross-prefix replication registered in v4.0 was run: twelve sections of the same domain on both instruments, one read date. The age hypothesis is retracted; the vendor ratio on estimated visits spans 0.20x to 7.24x within one site, with no detectable relationship to age. Section 5.5.

**v4.6.** Six figures added and the abstract shortened. No figure in the text changed.

**v4.7 and v4.8.** Section 5.5 was regenerated by the released script `analyze.py`, because the v4.5 text had been written from recollection of the table and miscounted it: six of twelve prefixes, not five, have a ratio below one, and the age correlation is −0.11, not −0.09. Territory-matched ratios, the vendors' agreement on the ordering of sections (60 of 66 pairs) and the power of the test were added, and the earlier statement that a single-vendor comparison between two sections "carries an unknown sign" was withdrawn as an overstatement. Two related-work paragraphs, Table 5's day-77 column, referring-domain ranges in Table 6 and two Table 1 rows were added; stale cross-references were corrected; and the corrections list in Section 12 was replaced by this appendix. Section 5.6's bound was restated: a 27.1x disagreement means at least one of the two estimates lies a factor of 5.2 or more, the square root of 27.1, from the quantity both estimate; the earlier text gave 13x, which is the absolute bound expressed in units of the smaller reading, not a multiplicative factor. The left-censoring of the age proxy was corrected from three prefixes to one, and the prefixes that cross one under territory matching were corrected. In v4.8 the original title, used through v2.2, was restored, and the abstract, Section 1, Section 2, lessons 1 and 3 of Section 9.2, Section 11 and the conclusion were revised to state the framework's thesis, that user demand is observed beyond the website and only partly visible to volume tools, with the instrument comparison as its motivating measurement; Figure 1 was added; a personalization paragraph and the multi-platform demand and persona studies were added; every statement about multi-platform demand and personalization is written as the framework's design or as a registered study, because this deployment collected one demand surface of thirteen. The abstract is longer as a result. Section 5.7 and Figure 6 add a first run of the demand comparison on 37,193 business reviews sourced through DataForSEO, with reviewer names discarded and only aggregate counts reported. The organization that operates the section is no longer named; the author's affiliation is given as KL University only.

## Appendix B: The Content Gap Score, as a specification

This function is not evaluated anywhere in this paper. It was not computed when the build decision was taken, nothing in Sections 5 to 8 tests it, and no published study has tested whether it predicts anything. It appears here because the reference implementation is released and a reader may want the specification it implements.

For an entity *e* with a set of competency questions *q*:

CGS(*e*) = prior(*e*) · (1 − own(*e*)) · [ α(1 − cov_K(*e*)) + (1 − α) · mean_q(1 − ans(*q*,*e*)) ]

where prior(*e*) = β · rel(*e*) + (1 − β) · dem(*e*); rel is a topic-sensitive PageRank over the structure graph [Haveliwala 2002], rank-normalized; dem is normalized demand; own is the organization's own coverage; cov_K is coverage of the entity across the open web; and ans(*q*,*e*) is the graded answerability of question *q* about *e*. Parameters are locked at α = 0.5, β = 0.5, damping = 0.85, digest `7290a2235d8de05f`.

Three properties a reader should know before using it. It takes the best of a question's verbalizations, which biases upward when phrasings differ in difficulty. Its `rel` term correlates with node degree at roughly 0.8 in the released example, so on a hand-authored taxonomy it is close to a centrality ranking. And it has no feasibility or business-relevance term, which Section 9.2 lesson 6 records as a practical failure.

The implementation reports competency-question performance as two separate rates, because they fail for different reasons: a schema rate, whether the model can express the question at all, and an instance coverage rate, whether the graph answers it. On the released example these are 4/5 and 70.4%. A question the ontology cannot express is reported as a declared gap with a reason rather than scored as zero.
