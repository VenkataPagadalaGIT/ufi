# User First Intelligence: Ontology-Driven Content Gap Discovery from Multi-Source Industry Knowledge Graphs Beyond Search Volume

**Venkata Pagadala**
KL University (doctoral programme), Atlanta, GA, USA
Manuscript version 4.8, 12 October 2026. Preprint, not yet peer reviewed.

Keywords: search measurement; instrument validity; AI Overviews; generative engine optimization; deployment measurement study; reference content

## Abstract

Applied search research runs almost entirely on commercial analytics platforms and treats their outputs as measurements. This paper reports what happens when two of them are pointed at the same object.

The object is a newly published reference section on a large US telecommunications provider's site: 381 area-code pages plus hubs, generated from a public numbering-plan registry and live from 26 July 2026. Because it did not exist before that date, two instruments observed one URL prefix from zero with no prior history to disagree about. They disagreed by more than the quantities most applied papers report: on estimated monthly visits by 25.9x, 27.1x, 10.2x and 7.5x in successive months; on ranking keywords by 2.0x; on live referring domains, read the same day, by 11.4x, with one instrument reporting 10% of those domains on .xyz and the other 75%.

A cross-section of twelve sections of the same domain, read on both instruments on one day, shows what a single series cannot. The vendor ratio on estimated visits runs from 0.20x to 7.24x across sections of one site, with a median of 1.01 and six of twelve below one; it shows no detectable relationship with section age (Spearman −0.11, 95% interval −0.64 to +0.49); and it does not follow the keyword-universe ratio, which runs 2x to 21x in one direction throughout. The section followed for 77 days sits near one extreme. The vendors agree on which section is larger in 60 of 66 pairs; the correction factor between them is what has no fixed sign or size, so no domain-level calibration converts one vendor's figure into the other's.

The divergence is the primary result because it does not depend on the author's judgment: every reading is of a public prefix that any subscriber can re-read. The deployment series is reported as context. At day 37, the last observation before an automated link network arrived, the section held 15,830 ranking positions with nineteen referring domains; by day 77 it appeared in 17,206 stored AI answers across six platforms with no editorial link, and the pages most cited were the hubs that enumerate codes rather than the pages that answer. Six enabling conditions, the deployment's cost, and six lessons stated as its failures are given. No causal claim is made.

## 1 Introduction

Almost every empirical claim in applied search research rests on a commercial analytics platform. Papers report that a technique moved visibility, that a competitor holds a share of some keyword space, that AI answers cite one kind of source more than another. The underlying numbers come from Ahrefs, Semrush, Similarweb or a comparable vendor, and they are reported the way measurements are reported: as quantities, sometimes to five significant figures, usually from one vendor, rarely with any statement of error.

The vendors do not claim otherwise in their documentation, which describes click models over estimated volumes at estimated positions. The practice treats them as counters anyway. This paper is an attempt to put a number on what that costs.

### 1.1 Why a new section is the right instrument

Comparing two analytics vendors on an established site tells you little. Both have years of accumulated index data, the disagreements are confounded with each vendor's historical coverage, and there is no moment at which the true value is known.

A section that did not exist last week is different. Before launch, both instruments correctly report zero. After launch, both observe the same URL prefix, in the same period, with no prior history. Their disagreement is then attributable to their models and their indexes as applied to that object, and its trajectory over time is observable. Section 5.5 shows that the disagreement is specific to the object as well: the same two instruments disagree by different factors, in different directions, on different sections of the same site.

This paper uses one such section: 381 code pages plus hubs under a single prefix on a top-authority domain, published on 26 July 2026 and observed daily for 77 days.

### 1.2 What this paper reports

1. **A divergence series between two commercial instruments** observing one URL prefix from zero, on estimated visits, ranking keywords, referring domains and AI Overview citation. Section 5.1 to 5.4.
2. **A cross-section of twelve prefixes on one domain, both instruments, one day**, showing that the vendor ratio on estimated visits spans 0.20x to 7.24x within a site (0.20x to 8.89x territory-matched), shows no relationship with section age, and does not follow the keyword-universe ratio, while the vendors agree on the ordering of sections (rank correlation 0.94). Section 5.5. This is the paper's main result, and it retracts the age hypothesis the preceding version advanced.
3. **A methodological consequence**: no domain-level correction converts one vendor's estimate into the other's; the vendors rank sections alike and size them by factors that vary from one fifth to nine times within one site. Section 5.6.
4. **A 77-day deployment series** on four quantities at a primary checkpoint chosen to precede three identified disturbances, with every definition, denominator, instrument and read date stated. Section 6.
5. **An observation about which pages AI answers cite**: enumerating hub pages outrank per-entity pages as cited sources, by a factor of roughly two. Section 7.
6. **The deployment's cost, its six enabling conditions, and six lessons stated as the things it got wrong.** Sections 3, 8 and 9.

### 1.3 What this paper does not report

A reader is owed this before the results rather than after them.

**No causal claim.** The design is observational. There is no treatment assignment, no control group, no randomization and no matched comparison. The provider's list of sections launched in the same window is not available, so we cannot say whether this section outperformed conventionally selected content on the same domain in the same period. Where the deployment series appears, it is a description of what was observed following publication, and "following" is the strongest word the design licenses.

**No separation of the method from the domain.** The deployment ran on a domain with an Ahrefs Domain Rating of 90 and a Semrush Authority Score of 86. Nothing here bounds how much of the outcome that explains, and Section 10 lists it first among the threats. An earlier version of this work claimed a bound from a comparison with two carriers of similar authority; that comparison is computed within a set selected on the provider's own presence and bounds nothing, as Section 7.2 sets out.

**No evaluated scoring function.** Earlier versions of this work proposed a Content Gap Score and devoted their framing to it. It was never computed when the build decision was taken, nothing here tests it, and no published study has tested whether it predicts anything. It is a specification with a reference implementation, and it has been moved to Appendix B so that it cannot be mistaken for a result of this paper.

**No measured traffic.** No figure in this paper is a counted visit. Internal analytics would be and are not available to us.

**No independent verification.** No person other than the author has graded, replicated or audited any part of this work. Section 12 states what has and has not been done about that, and it is the paper's largest unremedied weakness.

## 2 Related work

**Search measurement and tool validity.** Vendor estimates of search volume and traffic are known to be imprecise, and the practice of treating them as measurements is long-standing. What is less often reported is a direct, longitudinal comparison of two vendors on a single object with a known start date. The nearest analogues are audits of search result composition rather than of the estimation layer. This paper's contribution is narrow and empirical: a divergence series on one prefix, with the raw vendor figures printed so the ratios can be recomputed.

**AI answer surfaces.** An audit of 55,393 queries found that 29.8% of the domains cited by Google's AI Overviews did not appear on the first page of organic results for the same query [Xu, Iqbal & Montgomery 2026]; vendor measurement across 15,000 prompts reports that only 12% of URLs cited by ChatGPT, Gemini and Copilot rank in Google's top ten for the same prompt, with Perplexity at 28.6% [Linehan & Guan 2025]. Users click less when a summary appears and rarely click its sources: a click on a link inside an AI summary occurred in 1% of visits to pages showing one [Chapekis & Lieb 2025]. A critical survey of 45 generative-engine-optimization studies finds no page-level technique with a stable cross-platform effect on visibility, and identifies topical relevance as the most reproducible lever [Martinez 2026]. Section 5.3 adds a measurement observation those studies need: the two vendor definitions of "cited in an AI Overview" differ by a factor that is itself time-varying, so a GEO result reported on one vendor's definition is not directly comparable to one reported on the other's.

**Information needs and query fragmentation.** The gap between the unit a user has in mind and the unit a retrieval system indexes is old ground [Belkin, Oddy & Brooks 1982; Taylor 1968], as is the observation that aggregate demand concentrates differently from individual demand [Goel et al. 2010]. The taxonomy of web search [Broder 2002] distinguishes query intent rather than query granularity. Section 4 describes a deployment in which the operative distinction was granularity: one need expressed as thousands of distinct strings.

**Completeness in knowledge bases.** Appendix B's scoring function draws on the study of completeness in open-world knowledge bases [Razniewski et al. 2016; Galárraga et al. 2017; Balaraman et al. 2018; Luggen et al. 2019; Razniewski et al. 2024], on demand-weighted completeness [Hopkinson et al. 2018], and on gap discovery for encyclopedias [Wulczyn et al. 2016; Piccardi et al. 2018; Redi et al. 2020; Shao et al. 2024], with Ripoll et al. [2025] giving the most recent typology of content gaps for a collaborative knowledge base. Since the function is not evaluated here, that discussion sits with the specification in the appendix.

## 3 Setting

A large US telecommunications provider publishes a reference section covering the North American Numbering Plan. **As verified on 12 October 2026 by fetching every code page linked from the section's 52 state hubs, the section holds 381 code pages**: 374 for geographic codes assigned to US states and the District of Columbia, and 7 for toll-free codes. All 381 return HTTP 200, are canonical, and are full pages. The only geographic codes in the plan with no page are the six assigned to US territories. The section is therefore complete over the class it set out to cover, and **there is no set of uncovered codes within the class to serve as a control**.

Earlier versions of this paper, up to and including version 4.1, stated that 290 code pages had been published and that 88 geographic codes had none, and they registered those 88 as a within-class control arm. **Both figures were wrong.** The 290 was carried from an early draft and never re-counted, and the control it implied was advertised for four review rounds without anyone fetching the pages. The correction came from doing so.

All code pages, the state hubs and the national hub were published together at launch; no pages were added to the section during the observation window. This is the author's statement of the deployment's publishing history. Table 5's series of pages holding a position (210, 365, 391, 414, 440) is therefore the indexing of a fixed set of 434 URLs by one instrument, and not growth in the section itself. The figure of 440 at day 75 against 434 published URLs is within what the instrument attributes to a prefix beyond its canonical pages.

Two page counts remain and are easy to conflate. **381** is the number of code pages the section holds. **441** is the number of URLs under the prefix holding at least one ranking position on 11 October, which is selected on the outcome; it exceeds 381 plus the 53 hub pages by seven, which is within what the instrument attributes to a prefix beyond its canonical pages. Every fact on the pages is templated from two public-domain US government sources, the numbering plan administrator's registry and census data. The section went live on 26 July 2026, which is day 0 throughout this paper, dated from the first third-party detection of the pages.

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
| Referring domains | live linking domains to the prefix | Ahrefs; Semrush Backlink Analytics | 11 Oct 2026 |
| Monthly search volume | vendor-estimated monthly searches for a phrasing, summed over a set of phrasings | Ahrefs organic-keywords export, three carrier domains, US database | exported Oct 2025 |

Two properties of these instruments bear on everything that follows, and the first is this paper's subject.

**They are models, not counters.** Estimated visits are a click model over an estimated volume at an estimated position. No figure in this paper is a measured visit.

**The Ahrefs and Semrush visit figures are not the same quantity.** Ahrefs' is worldwide; Semrush's is the US database. The section ranks in 105 countries with 18.5% of Ahrefs' estimated visits from outside the US, so the Semrush figure covers a strict subset of the Ahrefs figure's territory and is nonetheless between 7.5 and 27.1 times larger. Section 5.1 reports both the US-only and worldwide Semrush figures so the comparison does not rest on the territory difference.

### 4.2 The query universe, and what cannot be computed on it

The evaluation query set was not frozen before launch; the section was live before this study was designed. The outcome quantities in Section 6 are therefore measured on universes defined after the fact: every keyword the section ranks for, and every prompt whose answer cites it.

Counts and positions on such a universe are meaningful, because the universe is the vendor's index rather than this paper's selection. **Shares and percentages computed on it are not**, because the denominator was selected on the outcome. Every share in this paper is one of the following, and is labelled at the point of use: a share whose denominator is outcome-selected, flagged as such and drawing no comparative conclusion; or a ratio between two instruments on the same object, which is this paper's primary result and is not affected, because both denominators are the same prefix.

### 4.3 The primary checkpoint

Three disturbances fall in the observation window. The September 2026 spam update began on 24 September, day 60, which is also the day of the estimated-traffic peak. Ahrefs posted a notice on 29 September that Google had changed how it serves results and that SERP data might be inconsistent from that date, covering days 60 to 75. And an automated link network began arriving in the day-37 to day-45 interval.

**Day 37 (1 September 2026) is the primary checkpoint**: the last observation preceding all three. An earlier version of this work used day 45 and justified it as preceding the link arrival, which its own table refuted. Day 37 carries a cost that is stated rather than worked around: it was not one of the fifteen-day checkpoints at which the full quantity set was captured, so it is reported on four quantities and not nine. The claims this paper makes at day 37 concern ranking positions, top-three positions, estimated visits and the link profile, and nothing else.

## 5 Two instruments on one prefix

This is the paper's primary result. It is reported first because it is the finding that does not rest on the author's judgment: every figure below is one of two vendors' readings of a public URL prefix, and a reader holding both subscriptions can re-read them.

### 5.1 Estimated visits: a divergence of 7.5x to 27.1x on one prefix

*Table 2. Estimated monthly visits for the prefix from two instruments. Semrush worldwide in parentheses. The June to September rows are completed-month totals. **The October row is each instrument's current monthly run-rate as read on 10–11 October, not eleven days of accumulated traffic**, and is marked accordingly; version 4.0 of this manuscript labelled it "month-to-date", which is a different construct and made the last row of the series incomparable with the rest. The ratio column uses the US figure. Section 5.1 gives the territory-matched ratios, which are larger.*

| Month | Days live | Ahrefs, worldwide | Semrush, US (worldwide) | Semrush US / Ahrefs |
|---|---|---|---|---|
| June 2026 | 0 | 0 | 0 (0) | n/a |
| July 2026 (total) | 6 | 3,862 | 100,012 (103,045) | 25.9x |
| August 2026 (total) | 31 | 32,281 | 876,153 (963,937) | 27.1x |
| September 2026 (total) | 30 | 150,113 | 1,534,362 (1,765,077) | 10.2x |
| October 2026 (run-rate) | 77 | 215,577 | 1,610,284 (1,858,297) | 7.5x |

![Figure 1. Estimated monthly visits for the area-code prefix from two instruments, on a logarithmic axis so that the vertical gap is the ratio. Ahrefs Site Explorer (prefix mode, all locations) and Semrush Domain Overview (subfolder mode, US database and worldwide), read 10 and 11 October 2026. June to September are completed-month totals; October is each instrument's current monthly run-rate. The ratio labels are Semrush US over Ahrefs, as in Table 2.](fig1_divergence.pdf)

Three things about this table and Figure 1.

**The disagreement is larger than the quantity most papers report.** An applied paper reporting a 40% lift from a technique, measured on one of these instruments, is reporting an effect roughly one twentieth the size of the disagreement between instruments about the level.

**It is not a territory artifact.** Semrush's US-only figure exceeds Ahrefs' worldwide figure throughout, and the section draws 18.5% of its Ahrefs-estimated visits from outside the US. Using the Semrush worldwide figure widens the ratio rather than closing it.

**It narrows after the second month on this prefix**, from 27.1x to 10.2x to 7.5x. Section 5.5 tests whether that narrowing is a property of section age across twelve prefixes and finds that it is not; Section 5.6 takes up what the narrowing can and cannot be attributed to.

### 5.2 Ranking keywords: a factor of two, stable

On the count of distinct keywords for which any URL under the prefix ranks in positions 1–100, Ahrefs reports 29,000 for all locations and Semrush 58,586 for the US database, read a day apart: a factor of 2.0, again with the larger figure from the smaller territory. Pages holding at least one position are 441 in Ahrefs. The two instruments agree on rank ordering of pages by traffic and disagree on every level.

### 5.3 AI answers and AI Overviews: two definitions, converging

**A comparison we withdraw.** Earlier versions reported a factor of 9.2 on AI answers, from Ahrefs Brand Radar's 17,206 stored answers citing the section against Semrush's 158,100 mentions. That ratio is not a divergence about the same object. Semrush's companion figure is 29,600 cited pages, which is 68 times the 434 URLs the section holds (381 code pages and 53 hubs) and 67 times the 441 URLs the other instrument attributes to the prefix, so the Semrush count is scoped to the domain or the brand rather than to this prefix. A scope mismatch of that size is not a measurement disagreement and the figure is removed from the abstract and from the comparison. We also drop the claim that the two instruments disagree about platform ordering, because the evidence for it was a platform breakdown whose own figures did not sum to its stated total and which is not reproduced here.

What can be compared on this prefix is reported above and below: visits, ranking keywords, referring domains and AI Overview counts, each with an instrument, a definition, a territory and a read date in Section 4.1. The Ahrefs figure of 17,206 stored answers on 455 distinct cited pages is reported in Section 6 as a single-instrument count and is not paired with a second reading.

For AI Overview citation the vendors use different operational definitions, given in Section 4.1. Definition (a) is a ratio over AI Overviews the prefix's keywords actually appear on; definition (b) is a count of US keywords with an AI Overview position. Both are reported as "AI Overview visibility" in their respective products.

*Table 3. AI Overview citation under two vendor definitions, same prefix, same months.*

| Month | (a) Ahrefs: cited / all AIO keywords | (a) as %, 95% Wilson CI | (b) Semrush count | (b) / (a) numerator |
|---|---|---|---|---|
| July 2026 | 47 of 284 | 16.5% [12.7, 21.3] | 138 | 2.94x |
| August 2026 | 851 of 6,749 | 12.6% [11.8, 13.4] | 2,221 | 2.61x |
| September 2026 | 3,380 of 22,665 | 14.9% [14.5, 15.4] | 8,187 | 2.42x |
| October 2026 (run-rate) | 7,455 of 37,238 | 20.0% [19.6, 20.4] | 10,018 | 1.34x |

![Figure 2. AI Overview citation under two vendor definitions, same prefix, same months. (a) Ahrefs definition (a) as a share of all AI Overview keywords the prefix ranks on, with 95% Wilson intervals; the denominators grow from 284 to 37,238. (b) The two vendor counts, Semrush keywords with an AI Overview position against the Ahrefs numerator, on a logarithmic axis, with their ratio labelled. Sources as in Table 3.](fig2_aio.pdf)

The ratio between the two counts falls from 2.94 to 1.34 over four months (Figure 2b). Two cautions on reading it. The comparison is between a count (b) and the numerator of a ratio (a), and the two vendors' territories differ, so what the column measures is partly a territory difference and not purely a definitional one; version 4.0 described it as definitional and that was imprecise. And the series has three intervals, so "converging" describes the observed sequence and is not a trend estimate. The July row rests on 47 events over six days live, and its interval is correspondingly wide. A study reporting an AI Overview visibility figure on one vendor's definition, for a section of a given age, is not reporting a quantity comparable to the same figure from the other vendor, and the incomparability is itself a function of age.

The (a) column's percentage is the one proportion in this paper whose denominator grows by two orders of magnitude across the series, from 284 to 37,238, and it is not monotone. Its denominator is outcome-selected: it counts only AI Overviews on keywords the prefix already ranks on. We report it because numerator and denominator come from one instrument on one date, and we draw no trend from it.

### 5.4 Referring domains: 11.4x, and disagreement about composition

Both instruments report live referring domains to the same prefix on the same day, and both are in the Section 4.1 table with a definition and a read date, which makes this the cleanest paired comparison in the study after estimated visits.

Ahrefs reports 913 referring domains to the prefix; Semrush Backlink Analytics indexes 80 for the subfolder: a factor of 11.4. They also disagree about what those domains are. Ahrefs puts 61.9% on .info, 26.4% on .asia and 10.2% on .xyz; Semrush puts 75% on .xyz and 88% at Authority Score 0 to 10. Both descriptions agree the domains are low-quality automated networks and disagree about their composition by a wide margin, which matters for any study classifying link profiles from one vendor's TLD distribution.

![Figure 3. Composition of live referring domains to the prefix by top-level domain, as reported by each instrument on 11 October 2026. Ahrefs: 913 domains; Semrush Backlink Analytics: 80 domains, of which the instrument reports 75% on .xyz and does not break down the remainder.](fig3_refdomains.pdf)

Figure 3 shows the two compositions side by side. A third figure from the first instrument complicates even its own count: its daily series gives 909 at day 75 against 913 on 11 October, and its new-and-lost report for September gives 917 new against 95 lost, which with nineteen at day 37 implies 841. Section 8 sets out why no claim here turns on the exact count.

### 5.5 Twelve prefixes on one domain: the divergence is prefix-specific and not about age

Sections 5.1 to 5.4 are one prefix. Version 4.0 proposed that the narrowing of the visits ratio reflected section age and index coverage, and Section 11 registered a cross-prefix replication as the test. It was run on 12 October 2026, on both instruments, for twelve sections of the same domain: the area-code section and eleven others chosen to span ages from under two years to the instrument's horizon. Every figure below is a dashboard read on one date. The raw values, the read method, the age proxy and the United States share of each prefix's estimated visits are in the released data files, and **every statistic quoted in this section is printed by the script `analyze.py` released beside them**, because the first draft of this section was written from recollection of the table and miscounted it.

*Table 4. Twelve URL prefixes on one domain, both instruments, read 12 October 2026. Age is months since the first month with organic traffic in the Ahrefs all-time series, read to the nearest month or quarter; the series begins in September 2015, so the three oldest ages are left-censored at that horizon. Ahrefs visits are worldwide and Semrush visits are the US database; the "US share" column is the United States share of Ahrefs' estimate from its traffic-by-location table, and the matched ratio divides Semrush US by Ahrefs US-only. Keyword and referring-domain ratios are as in version 4.6.*

| Prefix | Age (mo) | Ahrefs visits | Semrush visits (US) | Ratio, unmatched | US share | Ratio, matched | Ahrefs kw | Semrush kw | Kw ratio | Ahrefs RD | Semrush RD | RD ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| /local/area-codes/ | 3 | 221,000 | 1,600,000 | **7.24** | 81% | **8.89** | 28,900 | 59,000 | 2.0 | 913 | 81 | **11.3** |
| /product-compare/ | 21 | 5,500 | 4,100 | 0.75 | 70% | 1.07 | 716 | 2,300 | 3.2 | 187 | 41 | 4.6 |
| /local/bundles/ | 36 | 25,600 | 5,200 | 0.20 | 99% | 0.20 | 2,100 | 33,800 | 16.1 | 115 | 194 | 0.6 |
| /device-compare/ | 39 | 26,700 | 26,400 | 0.99 | 83% | 1.20 | 2,400 | 12,600 | 5.2 | 47 | 45 | 1.0 |
| /local/cell-phones/ | 57 | 37,300 | 135,100 | 3.62 | 99% | 3.67 | 3,600 | 37,500 | 10.4 | 144 | 225 | 0.6 |
| /support/ | 93 | 1,900,000 | 1,957,880 | 1.03 | 99% | 1.04 | 38,700 | 351,854 | 9.1 | 10,600 | 7,056 | 1.5 |
| /local/fiber/ | 95 | 102,000 | 47,300 | 0.46 | 100% | 0.46 | 5,400 | 31,900 | 5.9 | 258 | 245 | 1.1 |
| /buy/ | 95 | 644,000 | 1,014,124 | 1.57 | 98% | 1.60 | 19,800 | 206,365 | 10.4 | 7,400 | 3,246 | 2.3 |
| /local/internet/ | 114 | 243,000 | 220,600 | 0.91 | 94% | 0.97 | 13,300 | 79,700 | 6.0 | 1,700 | 516 | 3.3 |
| /stores/ | 129 | 312,000 | 2,051,269 | 6.57 | 99% | 6.61 | 14,700 | 306,952 | 20.9 | 4,100 | 3,527 | 1.2 |
| /deals/ | 132 | 214,000 | 219,600 | 1.03 | 99% | 1.03 | 5,300 | 32,000 | 6.0 | 1,600 | 2,042 | 0.8 |
| /es-us/local/ | 133 | 8,900 | 2,200 | 0.25 | 43% | 0.58 | 1,300 | 4,800 | 3.7 | 284 | 62 | 4.6 |

![Figure 4. Twelve URL prefixes on one domain, both instruments, 12 October 2026. Each marker is one prefix; the filled marker is the area-code section. (a) The Semrush over Ahrefs ratio on estimated visits, unmatched for territory, against section age in months since the first month with organic traffic in the Ahrefs all-time series, both axes logarithmic; the horizontal line is a ratio of one. (b) The same ratio against the Semrush over Ahrefs ratio on ranking keywords. Data in Table 4 and in the released file.](fig4_prefixes.pdf)

Five things follow (Figure 4), and the first retracts a claim this paper made in version 4.0.

**The cross-section shows no relationship between the ratio and section age.** Spearman's rank correlation between age and the unmatched visits ratio is −0.11 over twelve prefixes, with a Fisher 95% interval of −0.64 to +0.49 and a permutation p of 0.73; territory-matched it is −0.28; excluding the area-code section it is +0.15. Twelve prefixes give roughly 38% power to detect a correlation of 0.5, so this is not a demonstration that no age effect exists. What it does establish is narrower and sufficient: the ratio does not converge on a common value as sections mature, because sections aged between seven and eleven years sit anywhere from 0.46x to 6.61x. The hypothesis in version 4.0, that each vendor's index fills in at its own rate and the ratio settles as a section ages, is withdrawn, and the narrowing of the area-code ratio from 27.1x to 7.5x over three months is reported as an observation on one section and not attributed. Only one prefix in the cross-section is under twenty-one months old, so the first months of a section's life are not characterized here beyond that one case.

**The ratio is prefix-specific, and not one-directional.** Unmatched for territory, Semrush's estimate runs from one fifth of Ahrefs' (/local/bundles/, 0.20x) to seven times it (/local/area-codes/, 7.24x), a spread of 1.55 orders of magnitude, with a median of 1.01 and six of twelve prefixes below one. Matched for territory the spread is wider (0.20x to 8.89x), the median is 1.06, and four of twelve are below one, because two of the six sub-one prefixes have large non-US shares (/es-us/local/ at 43% US, /product-compare/ at 70%) that the matching corrects. The territory objection therefore changes the count and not the conclusion: on the same domain, on the same day, the vendors' estimates differ by factors from well below one to well above it, and no single correction factor maps one onto the other.

**The vendors agree on the ordering of sections and disagree on their magnitudes.** Across the twelve prefixes, the rank correlation between the two instruments' visit estimates is +0.94 (Kendall's tau +0.82, 60 of 66 pairs concordant). Version 4.6 concluded from the ratio spread that a single-vendor comparison between two sections "carries an unknown sign". That overstated it. The vendors agree on which section is larger in 60 of 66 pairs; what has unknown sign and magnitude is the **correction factor** between the two instruments, which no domain-level constant captures. The consequence for practice is restated in Section 5.6 in that form.

**Keyword universes diverge consistently; visit estimates do not follow them.** Semrush reports more ranking keywords than Ahrefs on every prefix, by between 2.0x and 20.9x. The rank correlation between the keyword ratio and the visits ratio is +0.17 over all twelve, and +0.52 with the area-code section excluded; the second figure is reported because the first is the one the paper is entitled to use and a reader should see both. /local/bundles/ has the second-largest keyword ratio (16.1x) and the smallest visits ratio (0.20x). The larger part of the disagreement is therefore in what each vendor's click model assigns to a discovered keyword, not in how many keywords it discovered, which is consistent with the decomposition in Section 5.6 and inconsistent with the mechanism version 4.0 proposed.

**The section this paper studied is where the instruments disagree most.** It has the highest visits ratio (7.24x unmatched, 8.89x matched; /stores/ is next at 6.57x) and the highest referring-domain ratio (11.3x) of the twelve. The referring-domain outlier has a visible cause: Ahrefs indexed the automated link network described in Section 8 and Semrush largely did not. The visits outlier does not have a visible cause here, and two candidates are stated as hypotheses only: the section's query distribution is unusually long-tailed (Section 6), which click models over estimated volume may treat very differently; and the section was three months old, which the cross-section cannot characterize.

**A measurement result about one of the instruments, established in passing.** Semrush's AI-visibility panel reported 158.3K mentions and 29.5K cited pages for every one of the twelve subfolders, identically. Those figures are domain-scoped whatever prefix is queried. Section 5.3's withdrawal of the 9.2x AI-answer comparison, made in version 4.1 by inference from the page count, is confirmed by observation.

**Limits.** Twelve prefixes, one domain, one read date; the age proxy is a chart read, left-censored at September 2015 for three prefixes; one prefix under twenty-one months; the territory match uses each prefix's US share as the instrument reports it. A second domain and a second read date are the next step, and neither needs this provider.

### 5.6 What follows for applied search research

**What divergence licenses, and what it does not.** There is no ground truth here. Neither vendor's figure can be checked against a counted visit, because the provider's analytics are not available to us. Divergence is therefore not error, and version 4.0 of this manuscript wrote that it was. What two readings A and B of one quantity with true value T license is a bound on the larger error and nothing more:

max(|A − T|, |B − T|) ≥ |A − B| / 2.

At the August ratio of 27.1x, at least one of the two instruments is wrong about this prefix by more than an order of magnitude, and this study cannot say which. That is the whole of the inference, and it is enough to be worth reporting: a field that treats these outputs as measurements should know that at least one major vendor can be off by 13x on a two-month-old section, without knowing which one.

**What the narrowing does and does not support.** The ratio falls 27.1 → 10.2 → 7.5 over three months on this prefix. Version 4.0 attributed this to section age and proposed index coverage as the mechanism. Section 5.5 tested that across twelve prefixes and found no relationship between age and the ratio. Within this one prefix the narrowing is also confounded: section age is collinear with calendar time, and the window contains the September 2026 spam update, the arrival of several hundred automated referring domains, and a vendor data-reliability notice covering two of the four months. The narrowing is reported as an observation on one section and is not attributed.

The index-coverage hypothesis is also the minority term where it can be checked. On 10–11 October, the only date both the visits and the keyword-universe figures were read, the divergence decomposes as

7.47x = 2.02x (keyword universe) × 3.70x (estimated visits per ranking keyword),

so the keyword universe accounts for about 35% of the divergence in log terms and the click model applied to each discovered keyword accounts for 65%. Whatever drives the narrowing, the larger component at that date is not how much surface each vendor has discovered.

**Why the headline ratios understate the disagreement.** The natural objection to Table 2 is territory: Semrush's figure is US and Ahrefs' is worldwide, so the comparison is unfair to Ahrefs. It is, and in the direction that makes the reported ratios conservative. Matching worldwide to worldwide gives 8.62x for October. Matching US to US, deflating the Ahrefs figure by the 18.5% non-US share of its own estimated visits, gives **9.17x** against the 7.5x in the table. We report the conservative pairing in the table and state the matched ones here.

**Consequence for practice.** The design this bears on is the standard one in applied content work: publish something, read one dashboard, compare it against the rest of the site or against a competitor. Section 5.5 is the finding that bears on it most directly. Across twelve sections of one domain the vendor ratio on estimated visits spans 0.20x to 7.24x (0.20x to 8.89x territory-matched), so no domain-level calibration factor can convert one vendor's figure into the other's. The vendors agree on which of two sections is larger in 60 of 66 pairs, so a single-vendor ranking of sections is usually right in direction; the magnitude of any difference, and any ratio between a section's figure on one vendor and another section's on the other, can be off by an order of magnitude either way. An effect of the size applied papers usually report is small against that. Reporting both vendors does not resolve which is right; it makes the uncertainty visible, and reporting one hides it.

**The limits of this result.** One domain, one vendor pair, no ground truth; the longitudinal series is one prefix over 77 days and the cross-section is twelve prefixes on one date. What is established is that disagreements of an order of magnitude occur in both directions between sections of one site, that they are unrelated to section age, and that keyword-universe size does not predict them. What is not established is which instrument is closer to the truth for any section, or what determines the ratio. Section 11 sets out the next step: a second domain, a second read date, and a per-section territory match.

## 6 The deployment series

This section is context for Section 5, not a claim. It describes what two instruments recorded following the publication of 381 code pages and their hubs, on a domain and a topic that satisfy all six conditions in Section 3.1.

*Table 5. Outcomes at each checkpoint. Ahrefs daily series for the prefix, all locations; AI answers from Brand Radar at the nearest stored date; read 11 October 2026. Day 37 is the primary checkpoint. "n/r" means not recorded: the quantity was not captured on that date, the daily series does not retain it, and it is not interpolated here.*

| Metric | Day 0 (26 Jul) | Day 15 (10 Aug) | Day 30 (25 Aug) | **Day 37 (1 Sep)** | Day 45 (9 Sep) | Day 60 (24 Sep) | Day 75 (9 Oct) |
|---|---|---|---|---|---|---|---|
| Pages holding a position | 2 | 210 | 365 | **n/r** | 391 | 414 | 440 |
| Ranking positions, all | 2 | 3,385 | 14,905 | **15,830** | 20,326 | 37,141 | 43,302 |
| Positions 1–3 | 0 | 727 | 1,801 | **1,874** | 2,649 | 5,822 | 8,753 |
| Positions 4–10 | 1 | 1,494 | 10,151 | **n/r** | 15,104 | 28,733 | 33,203 |
| Positions 11–20 | 0 | 909 | 2,639 | **n/r** | 2,331 | 2,336 | 1,276 |
| Positions 21–100 (derived) | 1 | 255 | 314 | **n/r** | 242 | 250 | 70 |
| Estimated visits (Ahrefs) | 2 | 22,016 | 51,517 | **≈51,800** | 92,897 | 244,041 | 221,933 |
| Live referring domains | 0 | 1 | 19 | **19** | 415 | 828 | 909 |
| AI answers citing the section | 0 | 1,603 | 3,725 | **n/r** | 6,390 | 10,266 | 14,823 |

The 21–100 row is derived as the total less the three reported bands, because Section 4.1 defines a ranking position as positions 1–100 while the instrument reports only three bands and the total. It is arithmetic on vendor estimates and not a fourth measurement. It closes every full column.

Day 60 and day 75 fall inside the window the Ahrefs data notice covers. The estimated-visits peak at day 60 coincides with the first day of the spam update, and the subsequent fall is consistent with either a data artifact or a ranking change. We do not distinguish them.

**At the primary checkpoint**, 37 days after publication, the section held 15,830 ranking positions, 1,874 of them in positions 1 to 3, with an estimated 51,800 monthly visits and nineteen referring domains. By day 77 it held 43,980 positions across 441 URLs holding at least one position, ranked for 29,000 keywords in one instrument and 58,586 in the other, was recorded as a cited source in Google AI Overviews on 7,455 keywords, and appeared in 17,206 stored AI answers.

**Concentration, with a defect in the earlier reporting of it.** Version 4.0 wrote that "the result is broad rather than driven by a few pages" and then gave figures that contradict it and each other. Of the 441 URLs holding a position, the ten highest-traffic carry 22.8% of estimated visits and the top 50 carry 64.9%. Fifty of 441 is 11% of the pages carrying about two thirds of the estimated traffic, which is concentration, not breadth. The paragraph also reported that 88.9% of pages receive 1 to 1,000 estimated visits a month and "together carry 64%", which cannot hold alongside the top-50 figure on the same denominator without a single page carrying roughly 29% of about 222,000 estimated visits, against the same paragraph's claim that none exceeds 10,000. At least one of the three figures is computed on a different denominator than the other two, and the source reads that would establish which have not been repeated.

What is reported here is therefore only what is internally consistent: **the ten highest-traffic URLs carry 22.8% and the top 50 carry 64.9% of estimated visits**, both on the 441 URLs holding a position on 11 October, both from one instrument, and both on a universe selected by the outcome. The breadth claim is withdrawn.

**Demand the volume tools do not report.** Among the 58,586 US keywords, the lowest-traffic rows are misspellings, non-English forms, numeric fragments and question forms with 40 to 170 reported searches a month or none at all. The section ranks in 105 countries, with 18.5% of Ahrefs-estimated visits from outside the US. We state this as a distributional observation and not as a test; the per-page threshold test that would make it one requires the full per-page keyword export matched to pre-launch reported volume, which we have not run.

## 7 What the answers cite, and what they do not

### 7.1 Enumerating pages outrank per-entity pages

The pages most cited in AI answers are state hubs that enumerate codes, cities and maps: New York 474 answers, California 337, Texas 322, Florida 304, and the national hub 294. Each exceeds any individual code page: 214 Dallas 238, 786 Miami 228, 404 Atlanta 218 (Figure 5).

![Figure 5. The eight pages under the prefix most often cited in stored AI answers, Ahrefs Brand Radar, 11 October 2026. Enumerating pages (state hubs and the national hub) are solid; per-entity code pages are hatched.](fig5_cited.pdf)

A per-entity content strategy predicts the opposite. The question "where is area code 214" is answered most directly by the 214 page, and that page is cited less than the page listing every Texas code. If this generalizes, enumerating pages are more citable than per-entity pages for this class of question, and the unit a content programme should publish is not the unit the question names.

We note it as an observation on one section. It is the finding in this paper most worth testing elsewhere, and testing it needs no access to this deployment: any site with both hub and per-entity pages on an enumerable class can check it.

### 7.2 Who else is cited, and what that does not establish

The queries are held, and the AI answers supplied, by encyclopedic and directory sites. The five domains with the largest keyword overlap with the section are two area-code directories, a time-zone reference and two voice vendors, at Domain Ratings between 13 and 83. Wikipedia, at 97, is co-cited in roughly 11,000 of the answers that cite the section. Two carriers of comparable authority are co-cited 9 times (Verizon, DR 91) and 240 times (T-Mobile, DR 87), against the section's 17,206. Neither published a page per code.

**This establishes nothing about necessity**, and earlier versions of this work claimed that it did. The counts are co-citations *within the set of answers that cite the provider*, a set selected because the provider is in it. A carrier absent from that set may be present across answers the provider is absent from, and no instrument here is pointed at those answers. The counts bound the carriers' co-presence from below within a selected set and support no statement about what authority alone produces, nor about whether content on the topic was necessary.

The comparison that would establish it is outcome-independent and has not been run: the registry's codes crossed with a fixed set of verbalizations, queried without reference to who is cited, so that each domain's presence is measured on a denominator none of them selected. Section 11 registers it and Section 12 records that it remains undone.

## 8 The link profile

The section had zero live referring domains through 31 July, one on 10 August, and nineteen on 25 August and still nineteen on 1 September, by which date it already held 15,830 ranking positions.

The referring-domain count on 11 October is reported by the instrument as 913, while the same instrument's daily series gives 909 at day 75 and its new-and-lost report for September gives 917 new against 95 lost, which with nineteen at day 37 implies 841. Three figures for quantities that should nearly agree. The gap is partly explained by domains gained and lost within the month counting in both columns, and not wholly. No claim here turns on the exact count; the shape is nineteen through day 37, several hundred within three weeks, roughly nine hundred by day 75.

The character of the arrivals is not in doubt. They are automated networks: 61.9% .info, 26.4% .asia, 10.2% .xyz, every linking page at URL Rating below 10, top anchors advertising link sellers. The second instrument indexes 80 referring domains for the subfolder, 88% from domains at Authority Score 0–10 and 75% on .xyz.

### 8.1 What the link profile can and cannot explain

*Table 6. Position growth by interval, with the link status of each.*

| Interval | Referring domains | Positions gained | Rate | Link status |
|---|---|---|---|---|
| Day 0 to 15 | 0 to 1 | 3,383 | 226 / day | clean |
| Day 15 to 30 | 1 to 19 | 11,520 | 768 / day | clean |
| Day 30 to 37 | 19 | 925 | 132 / day | clean |
| Day 37 to 45 | 19 to 415 | 4,496 | 562 / day | network arriving |
| Day 45 to 60 | 415 | 16,815 | 1,121 / day | network present |
| Day 60 to 75 | 828 | 6,161 | 411 / day | network present, data notice |

![Figure 6. Ranking positions and the link profile over 77 days. Upper panel: ranking positions in positions 1 to 100 and in positions 1 to 3, Ahrefs daily series for the prefix, all locations, read 11 October 2026; the hatched band is the interval in which the automated link network arrived; the vertical rules mark the primary checkpoint (day 37), the September 2026 spam update (day 60) and the vendor data-reliability notice (day 65); live referring domains at each checkpoint are printed along the top. Lower panel: positions gained per day in each interval of Table 6, shaded by link status.](fig6_positions.pdf)

Of the 43,302 positions held at day 75, 15,830 (36.6%) were held at day 37 and 27,472 (63.4%) were acquired after the network began arriving (Figure 6). Because the arrival is dated only to an eight-day interval, that share is itself bounded rather than exact: 53.1% to 63.4%. For AI answers, day 37 is not recorded, so the corresponding share is bounded 56.9% to 74.9%.

**What survives.** A result of 15,830 ranking positions and 1,874 top-three positions was established with nineteen referring domains, a count unchanged for the preceding week. That result does not depend on link acquisition, and it is this paper's negative result about links, stated at the checkpoint that supports it.

**What does not.** Any claim about the full series. An earlier version concluded that link acquisition plays no part in explaining the outcome; most of the series postdates the network.

**What the table does not show, against the temptation to read it as showing it.** The fastest clean interval, 768 a day across days 15 to 30, is 37% faster than the 562 a day of the arrival interval. A draft of this section reported only the last four intervals and inferred an acceleration from the 132-a-day trough immediately before the arrival; that is a baseline selected at the series minimum, and the inference does not survive showing all six. A 441-page section entering an index does not grow linearly. The network is therefore **unbounded as a confound on the continuation**, and nothing here shows that it accelerated anything.

**Disclosure.** The provider has an exposure this paper discloses rather than analyses: a spam link profile pointed at a live section, which the provider has been asked to review. A manual action before a later checkpoint would confound any continuation of this series. The author did not commission, purchase or solicit any link to the section.

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

Two things follow for a reader considering transfer. The marginal cost per page was near zero *because* conditions 1 to 3 of Section 3.1 held, and they do not hold for most classes. And the dominant cost was analysis rather than production, which inverts the usual content-programme cost structure and is the part a reader should expect to pay.

### 9.2 Six lessons, stated as this deployment's failures

Each is something this deployment got wrong, which is why its cost can be stated.

1. **Separate structure sources from coverage sources, or do not claim a method.** We did not, so the demand layer derives from what competitors already rank for. Cost: the method claim, which is why Appendix B's score is a specification and not a result.
2. **Freeze the evaluation query set before launch.** We did not, so every share in this paper would otherwise be computed on a denominator selected by the outcome. Cost: all comparative claims. The released implementation makes freezing a command so the failure is harder to repeat.
3. **Collect at least one first-party demand surface before claiming anything about users.** We collected none: no forum, Q&A, video, social or review data was linked to any entity. Cost: any user-centred framing, which is why this paper's title does not carry one.
4. **Record the recommendation and its date.** The document that turned analysis into a build decision is not in retrievable form. Cost: the causal chain has no anchor at its most important link.
5. **Get a second grader early.** Grading judgments with agents the author built, and planning independent annotation for later, means the reliability statistic arrives after the claims that depend on it. Cost: Appendix B's inputs are unvalidated.
6. **Expect the class that scores well to have no commercial page to attach to.** Area codes are a reference topic on a commercial domain. The score has no feasibility term and someone must decide how business relevance enters.

## 10 Threats to validity

**Instrumentation**, which is this paper's subject rather than a caveat on it. No outcome is a measured visit. On the area-code prefix the two instruments differ by 7.5x to 27.1x on estimated visits, 2.0x on ranking keywords and 11.4x on referring domains; across twelve prefixes of the same domain the visits ratio runs from 0.20x to 8.89x. A fourth comparison, on AI answers, is withdrawn in Section 5.3 as a scope mismatch rather than a divergence. One instrument posted a data-reliability notice covering days 60 to 75. Internal analytics would resolve much of this and are not available.

**Confounding, with directions.** One bookkeeping correction first: version 4.0 said "two" and "three" algorithm updates in adjacent sentences while Section 4.3 names one. **One** named, dated update falls in the window, the September 2026 spam update beginning 24 September (day 60). Whether others occurred unannounced is not knowable from here, and the text no longer implies a count it cannot support.

Domain authority: direction positive, magnitude unknown, **no bound available**. An earlier version named the carrier comparison in Section 7.2 as a bound; that comparison is computed on a set selected on the provider's presence and bounds nothing. Content quality and execution: templating, registry facts, structured markup and internal linking are perfectly confounded with selection; direction positive; no estimate. Topic contest: no defender responded. The automated link network: between 53.1% and 63.4% of day-75 positions postdate its arrival, the range reflecting that the arrival is dated only to an eight-day interval; direction unknown, magnitude unestimated, and confounded with index maturation and with the September spam update. Algorithm updates: one named, dated update falls in the window, on the day of the traffic peak; whether unannounced ones did is not knowable from here.

**Selection.** The query universes were defined after launch. Counts are reported on them; shares are reported only where the denominator is stated and flagged, or where the quantity is a ratio between two instruments on the same prefix, which selection does not affect.

**Construct.** "AI Overview citation" has two operational definitions here and they differ by a factor that falls from 2.94 to 1.34; both are reported. "Visibility" is not value: no revenue, conversion or impression figure appears in this paper and none should be inferred.

**Non-human traffic.** The estimated-visit figures are vendor click models and do not distinguish automated from human requests. A section attracting an automated link network may also attract automated requests. No instrument available here separates them, and the paper's engagement figures should be read with that unresolved.

**External validity.** One organization, one industry, one class, a top-authority domain, 77 days, six stated conditions. For Section 5's divergence result: one prefix, one vendor pair, no ground truth.

**Author independence.** The author designed the approach, deployed it as an employee of the organization studied, performed every measurement, wrote this paper, holds a commercial interest in tools built on the approach, and is the author of a forthcoming book that uses its name. No part of the evaluation has been performed by anyone else. A reader should treat every judgment here as made by an interested party, and should weight Section 5's instrument readings, which are independently reproducible from two commercial subscriptions, far above anything else in the paper. Section 5 is the primary result partly for that reason.

## 11 What would test what this paper declines to claim

**The within-class control, withdrawn.** Versions 3.1 to 4.1 registered a within-class control: the geographic codes for which no page was published, queried on the same instruments as the published ones. Section 3 records that no such set exists. The section holds a page for every geographic code assigned to a US state or the District of Columbia; the six territory codes without pages are too few and too different in kind to serve. The design is withdrawn, and the paper no longer claims a permission-free test of whether publishing a page did anything. The closest substitute is external: a comparable-authority domain that covers the class partially, which this study has not identified.

**The enumerating-pages test, which needs no access to this deployment.** Section 7.1 reports that state hub pages are cited in AI answers roughly twice as often as the individual code pages they enumerate. Any site holding both hub and per-entity pages over an enumerable class can test whether that ordering holds, on either instrument, with no reference to this provider.

**An outcome-independent query universe.** The registry's geographic codes crossed with a fixed set of question verbalizations yields a query set that is complete with respect to the class, defined without reference to any outcome, and hashable. The released implementation writes it: `ufi freeze` produces the set with its digest. The example ships a 924-query demonstration over the 66 codes in its registry extract, at digest `f05ce279942be5f8`; the set for the full class would be built the same way.

**A prospective study on an ordinary domain.** A second industry, a domain outside the top decile of authority, the ontology and parameters registered before collection, the query set frozen and hashed before launch. Three classes with matched page counts: top class by mean score, top class by volume, and a class in the bottom quartile of the score. Primary outcome: top-ten presence on the frozen set at day 37. The parameters are already locked: **α = 0.5, β = 0.5, damping = 0.85, lock digest `7290a2235d8de05f`, locked 12 October 2026**, which is what would make this a test rather than a fit.

**An annotation study**, two graders independent of the author, on a sample of the coverage and answerability items, reporting weighted kappa with bootstrap intervals. The released implementation caches judgments keyed on the rubric, so a second grader costs one pass.

**A second domain for Section 5.5.** The cross-section was run on one domain. The result that the vendor ratio is prefix-specific and age-independent needs a second site, a second read date, and a per-section territory match before it is more than an observation about one domain. Anyone with both subscriptions and any multi-section site can do it in a day; the data file released with this paper gives the read method.

## 12 Reproducibility, ethics and conflicts of interest

**What is released.** The `ufi` reference implementation at **https://github.com/VenkataPagadalaGIT/ufi** under Apache 2.0, commit `02d7588`: test suite, command line interface, and a worked example that runs offline on public data. The corrected numbering-plan ontology in YAML with OWL and SHACL export, and the area-code dataset the example uses. It has **no DOI**; a Zenodo deposit is outstanding. The exported OWL and SHACL mint terms under `http://w3id.org/ufi/nanp`, which does not resolve, and that is a defect in the released artifact rather than a shorthand.

**Data released with this version.** The twelve-prefix cross-section (Table 4) is released as two CSV files, one per instrument, each row carrying the prefix, the figures read, the read date and the read method, at `data/instrument_divergence/` in the repository below.

**What a reader can verify independently.** Every figure in Sections 5 and 6 can be re-read from the same two dashboards for the same prefix, subject to index drift. The Ahrefs daily series reproduces the checkpoint rows until it ages out of the six-month window.

**What is not released.** The provider's internal graph database, the crawl of its site, and its analytics. Figures drawn from them are labelled internally measured where they appear.

**Ethics, data collection and site terms.** No human subjects were involved; no user-level, session, cookie or personally identifying data was collected or analysed. The deployment published reference pages and ran no experiment on visitors. Outcome figures come from commercial dashboards read through their own interfaces under paid subscriptions, within those vendors' terms; no vendor was scraped and no API was used to assemble the series. This study performed no crawl of any third-party site; the provider's own site crawl is an internal operation on the organization's own property. Page facts derive from the numbering plan administrator's public registry and US Census data, both public-domain US government sources.

*Competitive effects.* The deployment displaced incumbent pages, mostly specialist directories at Domain Rating 13 to 83, in a public search index. This is a commercial outcome with distributional consequences for smaller publishers, and the informational value added is modest, because the registry had already published the facts. Condition 6 of Section 3.1 can be read as a criterion for selecting undefended targets. That reading is available and this paper does not endorse it; a method whose transferable content is "find a finite factual class that an authoritative free registry already answers and that no one is defending" deserves to be stated in those terms so that the question can be asked.

**Corrections to earlier versions.** Appendix A gives the full version history; this list and that appendix now name the same items, which version 4.0 did not. Four corrections change how a figure must be read. The October 2025 carrier exports were described as not selected on the outcome and are ranked-keyword exports, selected on a prior ranking outcome. Day 45 was named the primary checkpoint on the ground that it preceded the link arrival, which the data refute; the checkpoint is day 37. A past-tense claim that two independent annotators had graded the audit samples was false, and no annotation study has been run. And **the section's size was misstated in every version through 4.1**: 441 was called its size when it is the number of URLs holding a ranking position on one date, and separately the section was said to hold 290 code pages with 88 geographic codes uncovered. It holds 381 code pages, 374 geographic and 7 toll-free, with only the six territory codes uncovered; the 88-code control arm those versions registered does not exist, and Section 11 withdraws it.

**Organizational permission.** The organization that operates the section approved publication of the figures in this paper. Approval date: *[to be completed]*. Approving role and unit: *[to be completed]*. Scope: *[to be completed]*. **These three fields are unfilled, and the manuscript is not submitted anywhere until they are.** The organization is not named in this paper.

**Conflicts of interest.** As stated in Section 10. The mitigations are weaker than the conflict: the primary result is two vendors' readings of a public prefix that any reader with the same subscriptions can re-read, the implementation is released so the specification can be checked against the description, and the designs in Section 11 are registered before their data exist.

**What has not been done, after six rounds of internal review.** No independent party has checked any number in this paper. The one check that would change that requires nobody's permission, budget or cooperation: a third-party re-read of the day-37 row of Table 5 and of Table 4 from the same dashboards. It has not been performed. The cross-prefix replication the previous version listed here was performed on 12 October 2026 and is Section 5.5; the within-class control it also listed was found not to exist (Section 3). A reader is entitled to weigh that the remaining undone check is the only one requiring another person's name.

## 13 Conclusion

Two commercial analytics platforms watched the same section from the day it appeared. Over four months they disagreed about its estimated traffic by factors between 7.5 and 27.1, about its ranking keywords by a factor of two, and about its referring domains by a factor of eleven. Read on the same day across twelve sections of the same domain, their ratio on estimated visits ran from one fifth to seven times, unrelated to how old each section was and unrelated to how many keywords each vendor had found. The disagreement is larger than the effects most applied search papers report, the correction factor between the vendors has no fixed sign or size, and it cannot be applied at the domain level; the vendors rank sections alike and size them differently, so a single-vendor study of magnitudes carries an error it cannot bound from its own data.

The deployment underneath that measurement is reported as context. Following the publication of one page per member of a finite enumerable class, templated from a free registry on a top-decile domain that no comparable competitor covered and no one defended, the section held 15,830 ranking positions with nineteen referring domains at day 37, and by day 77 appeared in 17,206 recorded AI answers having earned no editorial link. The pages most cited were the ones that enumerate rather than the ones that answer. What that conjunction depended on, and in what proportion, is not estimated here, and the within-class comparison that would begin to estimate it remains unrun.

## References

Twenty-one entries are listed, every one cited in the text, every one complete. Versions through 4.3 carried five entries marked incomplete and three listed without a citation; all were resolved against the primary sources on 12 October 2026, and the two load-bearing ones for Section 2, the 55,393-query AI Overview audit and the 45-study GEO survey, say what this paper cites them for.

Linehan, L., & Guan, X. (2025, August 11). *Only 12% of AI cited URLs rank in Google's top 10 for the original prompt.* Ahrefs. https://ahrefs.com/blog/ai-search-overlap/ (15,000 long-tail prompts across ChatGPT, Gemini, Copilot and Perplexity; accessed 12 October 2026.)

Balaraman, V., Razniewski, S., & Nutt, W. (2018). Recoin: Relative completeness in Wikidata. In *Companion Proceedings of The Web Conference 2018* (pp. 1787–1792). ACM.

Belkin, N. J., Oddy, R. N., & Brooks, H. M. (1982). ASK for information retrieval: Part I. Background and theory. *Journal of Documentation, 38*(2), 61–71.

Broder, A. (2002). A taxonomy of web search. *SIGIR Forum, 36*(2), 3–10.

Chapekis, A., & Lieb, A. (2025, July 22). *Google users are less likely to click on links when an AI summary appears in the results.* Pew Research Center.

Galárraga, L., Razniewski, S., Amarilli, A., & Suchanek, F. M. (2017). Predicting completeness in knowledge bases. In *WSDM '17* (pp. 375–383). ACM.

Goel, S., Broder, A., Gabrilovich, E., & Pang, B. (2010). Anatomy of the long tail: Ordinary people with extraordinary tastes. In *WSDM '10* (pp. 201–210). ACM.

Golebiewski, M., & boyd, d. (2018). *Data voids: Where missing data can easily be exploited.* Data & Society Research Institute.

Haveliwala, T. H. (2002). Topic-sensitive PageRank. In *WWW '02* (pp. 517–526). ACM.

Hopkinson, A., Gurdasani, A., Palfrey, D., & Mittal, A. (2018). Demand-weighted completeness prediction for a knowledge base. In *NAACL-HLT 2018, Industry Papers* (pp. 200–207). ACL.

Luggen, M., Difallah, D., Sarasua, C., Demartini, G., & Cudré-Mauroux, P. (2019). Non-parametric class completeness estimators for collaborative knowledge graphs: The case of Wikidata. In *ISWC 2019* (pp. 453–469). Springer.

Martinez, O. (2026). *Optimizing visibility in generative engines: A critical survey of generative engine optimization (2023–2026).* arXiv:2607.14035.

Piccardi, T., Catasta, M., Zia, L., & West, R. (2018). Structuring Wikipedia articles with section recommendations. In *SIGIR '18* (pp. 665–674). ACM.

Razniewski, S., Suchanek, F. M., & Nutt, W. (2016). But what do we actually know? In *AKBC 2016* (pp. 40–44). ACL.

Razniewski, S., Arnaout, H., Ghosh, S., & Suchanek, F. (2024). Completeness, recall, and negation in open-world knowledge bases: A survey. *ACM Computing Surveys, 56*(6), Article 150. https://doi.org/10.1145/3639563

Redi, M., Gerlach, M., Johnson, I., Morgan, J., & Zia, L. (2020). *A taxonomy of knowledge gaps for Wikimedia projects.* arXiv:2008.12314.

Ripoll, M., Reeves, N., Kurteva, A., Simperl, E., Meroño Peñuela, A., & Diepold, K. (2025). *Filling in the blanks? A systematic review and theoretical conceptualisation for measuring WikiData content gaps.* arXiv:2505.16383.

Shao, Y., Jiang, Y., Kanell, T. A., Xu, P., Khattab, O., & Lam, M. S. (2024). Assisting in writing Wikipedia-like articles from scratch with large language models. In *NAACL 2024.* ACL.

Taylor, R. S. (1968). Question-negotiation and information seeking in libraries. *College & Research Libraries, 29*(3), 178–194.

Wulczyn, E., West, R., Zia, L., & Leskovec, J. (2016). Growing Wikipedia across languages via recommendation. In *WWW '16* (pp. 975–985). ACM.

Xu, H., Iqbal, U., & Montgomery, J. M. (2026). *Measuring Google AI Overviews: Activation, source quality, claim fidelity, and publisher impact.* arXiv:2605.14021.

## Appendix A: Version history

This manuscript is the fourth structural version and has been through five rounds of adversarial internal review. The history is recorded here rather than in the body, where in version 3.3 it had grown to 26% of the text and had become larger than the results section.

**v1 to v2.2.** Framed as a method paper for a Content Gap Score, with the deployment as its validation. Three statements were false and are corrected: that two independent annotators had graded the audit samples (none had, and no annotation study has been run); that the ontology had been released (nothing had been); and an assertion of organizational permission with the date left blank. The first was the most serious: a past-tense claim of an independent check that did not happen, in a document naming the organization.

**v3.0.** Reframed as a deployment measurement study. The score was withdrawn as an evaluated contribution. A section on what the paper does not report was placed before the results.

**v3.1 to v3.3.** Three corrections that change how a figure must be read. The October 2025 carrier exports were certified as "the one pre-launch artifact that was not selected on the outcome"; they are ranked-keyword exports, selected on a prior ranking outcome. Day 45 was named the primary checkpoint on the stated ground that it preceded the automated link arrival, which the paper's own table refutes; the checkpoint is day 37. And the conclusion that link acquisition played no part in explaining the outcome does not hold across the series, because most of the series postdates the network; it is now stated at day 37 only.

Two further corrections were to arguments rather than figures. A replacement argument in v3.1 held that the per-keyword and pooled views ran over identical rows so selection was held constant; they run over different row sets and the argument fails. And a draft of the link-interval analysis reported only the intervals that made the confound look largest, inferring an acceleration from a baseline chosen at the series minimum; showing all six intervals withdraws it.

**v4.5.** The cross-prefix replication registered in v4.0 was run: twelve sections of the same domain on both instruments, one read date. The age hypothesis is retracted; the vendor ratio on estimated visits spans 0.20x to 7.24x within one site and is unrelated to age. Section 5.5. The five incomplete citations and three uncited references were resolved against primary sources.

**v4.2 and v4.3.** The section's page count was verified by fetching every code page linked from its 52 state hubs. It holds 381 code pages, not 290, and covers every geographic code assigned to a US state or DC. The 88-code within-class control registered since v3.1 therefore does not exist and is withdrawn. The author confirms all pages were published together at launch, so the 290 was a miscount and the section did not grow during the window.

**v4.0.** Restructured. The instrument divergence, present in the data since v2.2 and never advanced as a result, becomes the primary contribution, because it is the finding that does not rest on the author's judgment. The deployment series is demoted to context. The scoring function moves to Appendix B. Claims the preceding versions had conceded piecemeal are removed rather than carried with a qualification attached.

## Appendix B: The Content Gap Score, as a specification

This function is not evaluated anywhere in this paper. It was not computed when the build decision was taken, nothing in Sections 5 to 8 tests it, and no published study has tested whether it predicts anything. It appears here because the reference implementation is released and a reader may want the specification it implements.

For an entity *e* with a set of competency questions *q*:

CGS(*e*) = prior(*e*) · (1 − own(*e*)) · [ α(1 − cov_K(*e*)) + (1 − α) · mean_q(1 − ans(*q*,*e*)) ]

where prior(*e*) = β · rel(*e*) + (1 − β) · dem(*e*); rel is a topic-sensitive PageRank over the structure graph [Haveliwala 2002], rank-normalized; dem is normalized demand; own is the organization's own coverage; cov_K is coverage of the entity across the open web; and ans(*q*,*e*) is the graded answerability of question *q* about *e*. Parameters are locked at α = 0.5, β = 0.5, damping = 0.85, digest `7290a2235d8de05f`.

Three properties a reader should know before using it. It takes the best of a question's verbalizations, which biases upward when phrasings differ in difficulty. Its `rel` term correlates with node degree at roughly 0.8 in the released example, so on a hand-authored taxonomy it is close to a centrality ranking. And it has no feasibility or business-relevance term, which Section 9.2 lesson 6 records as a practical failure.

The implementation reports competency-question performance as two separate rates, because they fail for different reasons: a schema rate, whether the model can express the question at all, and an instance coverage rate, whether the graph answers it. On the released example these are 4/5 and 70.4%. A question the ontology cannot express is reported as a declared gap with a reason rather than scored as zero.
