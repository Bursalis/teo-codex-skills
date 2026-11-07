### 1. Research and planning

1. Open the Notion task and identify the requested unit.
2. Read the full course description and all unit descriptions needed to situate it. Follow the bibliography link at the top of the Task page, open **Δ&Α Βιβλιογραφία ανά ενότητα**, and locate the corresponding numbered unit.
3. Record the bibliography entry's exact source selection: complete articles/books and the named chapters, subsections and page ranges. This entry defines the material for the production run.
4. Locate `[Πηγές]`, `[Templates]`, `[Παραδοτέα]`, `Summary Template.dotx`, `Outline Template.dotx`, `Essay Template.dotx` and `Rights&Inequality.potx`; verify their paths rather than assuming a working-directory layout. `[Παραδοτέα]` is the only final-output directory. If the PowerPoint template, output folder, or any bibliography-selected material is missing, stop and report the exact missing path or source passage.
5. Resolve the selected works to local files and read only the specified material exhaustively and closely. For a collection, reader or handbook, enter the file and read the individual chapters or articles named by the bibliography entry, not the volume as a whole. Extract their directly relevant arguments, examples, visual material and exact page references. A source may be used in the deliverables only to the scope specified by the corresponding bibliography entry.
6. Record the potential entries for a private evidence map. Treat the selected project material as the sole evidence base for theories, concepts, historical claims, mechanisms and generalisations. Reconcile, complete and use the map only after the critical-summary audit has passed for every reading, then use it to construct the internal argument dossier. When an analytically necessary contemporary Greek example is anticipated, apply the controlled external-source exception above and record only the selected example in the map. Use sources on the Greek case, welfare, work, care, housing, migration, collective bargaining or social rights only when their bibliography-specified, verified passages directly support the unit's argument.

### 2. Deliverable 1 — critical summaries of the selected bibliography

Use [`critical-paper-summary`](C:\Users\tkary\.codex\plugins\cache\theodoros-personal-skills\critical-paper-summary\0.1.0\skills\critical-paper-summary\SKILL.md) for every individual reading selected by the corresponding entry in **Δ&Α Βιβλιογραφία ανά ενότητα**. Read that skill in full before drafting this deliverable.

- Treat every named standalone article and every named chapter/article within a collection, reader or handbook as a separate reading and create one critical summary for it.
- For a collection, reader or handbook, never apply `critical-paper-summary` to the whole volume. Read and summarise only the individual chapter or article that the bibliography entry names. Do not produce an aggregate summary of several chapters as if it were one reading.
- For a single-authored monograph, create a summary only for the chapter or subsection named in the bibliography entry. If the entry explicitly identifies the complete single-authored monograph as the selected reading, a whole-work summary is permitted; this exception never applies to an edited collection, reader or handbook.
- Before constructing the DOCX, draft each individual summary separately with `critical-paper-summary` from its complete selected source material and validate it separately. Each Greek summary body must contain 270–330 words, targeting approximately 300 words, analytically focused, with no citations, links, labels, process notes or text outside the summary itself. The APA heading is not part of that body-word count.
- **Source-bound prose requirement.** Every word and every sentence in a critical summary must serve the accurate transfer, interpretation or critical assessment of the particular original reading. A sentence must state or clarify its argument, concepts, method or evidence where relevant, internal tension, implication, limitation, or direct analytical usefulness for the unit. Do not use generic statements about inequality, institutions, social processes, analysis, theory, contribution or relevance unless the specific reading itself substantiates that statement and the sentence makes its particular connection explicit. Do not add a generic opening, transition, conclusion, evaluative flourish or other prose merely to make the summary sound complete or to increase its word count.
- **No-padding rule.** Never use a filler paragraph, reusable analytical closure, boilerplate wording, template expansion, automated loop, duplicated sentence or any other mechanical means to make an individual summary reach 270 words. If the first draft falls outside 270–330 words, return to that reading's complete selected material and rewrite the analytical synthesis from the source. Do not append, trim or patch the draft solely to meet the range.
- Derive the exact APA reference for every reading from the bibliography entry and the verified local file metadata. Never invent publication details, chapter authors, editors, page ranges or DOI information. If an APA reference cannot be verified from those inputs, stop and report the specific unresolved item.

Create one DOCX in `[Παραδοτέα]` as `ΔΑ - [αριθμός ενότητας] - [τίτλος ενότητας] - Κριτικές περιλήψεις βιβλιογραφίας.docx` from `[Templates]\Summary Template.dotx`. Apply the Windows-safe title token rule to `[τίτλος ενότητας]` in this filename. The title inside the document must be exactly `ΔΑ - [αριθμός ενότητας] - [τίτλος ενότητας] - Κριτικές περιλήψεις βιβλιογραφίας`.

Inside this DOCX:

1. Write the document title once at the top using **Heading 1**.
2. For each individual selected reading, use its complete verified APA reference as the section title, using **Heading 3**.
3. Place only that reading's critical summary immediately below its APA heading in the appropriate body style.

Do not add a general bibliography, source list, preface, methodology note, table, numbering, or any material other than the document title, the APA-reference headings and their corresponding critical summaries. The number of Heading 3 sections must equal the number of individual readings selected for that unit.

Render and visually inspect this DOCX before beginning the evidence-map and argument-dossier stages. Check that every selected reading appears exactly once, that no edited collection, handbook or reader has been summarised as a whole, and that every APA heading is complete and verified.

After generating the DOCX, run a deterministic per-reading integrity audit. For each Heading 3 reading, extract only the body paragraphs until the next Heading 3 (or document end), exclude its APA heading, and count words using the same word-tokenisation method for every reading. Detect repeated substantive paragraphs and repeated substantive sentences both within a single summary and across the complete set of summaries. A repeated sentence is substantive when it contains at least 12 words after normalisation; do not permit it in two places unless it is a direct quotation explicitly required by the user, which these summaries ordinarily do not contain. Record internally, for every selected reading, its reading identifier, complete APA heading, body-word count, duplicate-paragraph result, duplicate-sentence result and pass/fail status against the 270–330 range and the no-repetition rule.

Then perform a manual source-fidelity audit of every individual summary against the complete selected reading before starting the argument dossier. Read it sentence by sentence and confirm that each sentence has a determinate function in reconstructing or critically assessing that particular source: argument, concept, evidence or method where relevant, mechanism, dispute, implication, limit, or analytical use for the unit. Remove or rewrite every sentence that could be attached unchanged to a different reading, merely praises or generalises, repeats an earlier sentence, or exists only to increase length. This audit is a hard gate. Do not begin the argument dossier, lecture script, outline, slide plan or PPTX until every individual reading passes both the deterministic integrity audit and the manual source-fidelity audit. If any summary fails, return to that reading's complete selected source material, use `critical-paper-summary` again to redo its analytical synthesis, rebuild the DOCX as needed, and rerun the audit for all readings.

### 3. Internal stage — evidence map and argument dossier

After every critical summary passes the per-reading audit, complete the private evidence map and create a mandatory **Argument dossier**. The dossier is an internal analytical plan: do not export it to `[Παραδοτέα]` or present it as a fifth deliverable. Base it exclusively on the evidence map and verified project sources.

The argument dossier must include:

1. the unit's central thesis or core argument in one or two precise sentences;
2. the organising question of the lecture and, where needed, its subsidiary questions;
3. what the unit takes up from earlier sessions and what it prepares for later sessions;
4. the concepts that require definition, their relevant distinctions and the likely misunderstandings the lecture must prevent;
5. a sequence of analytical moves. For each move, specify the sub-claim; exact evidence with author, year and pages; the interpretation or mechanism connecting evidence to claim; the example or pedagogical function; and the transition to the next analytical move. When the example is a permitted contemporary Greek case, record the completed three-candidate comparison and the selected organisation, document, date, stable URL and exact page(s) or unpaginated article/section heading;
6. the substantive theoretical disagreements, objections or tensions in the literature. Organise sources around real stakes rather than as a list of authors;
7. source allocation: which source grounds which claim and where it will be used in the final script; and
8. the points that require return to the primary local project sources for verification or completion before drafting.

Before drafting the lecture, check that every basic analytical move in the dossier is supported by a verified source and exact page reference. Return to the source and evidence map for any unverified, incomplete or weakly connected move. The dossier is an analytical and evidentiary basis, not a rigid mould: it must allow the final script to develop a critical point further where the dossier anticipates it or the verified sources support it.

### 3a. Internal stage — pedagogical design of the lecture

After completing the evidence map and argument dossier, and before drafting the final lecture script, turn the evidenced argument into a coherent teaching design. This is an internal planning stage, not a fifth deliverable; do not export it to `[Παραδοτέα]`.

The pedagogical design must specify:

1. the central learning problem or organising question;
2. two or three learning purposes in accessible language;
3. the principal argumentative structure, and the explicit relationship between structures when more than one is necessary;
4. for each major analytical move, the concept requiring explanation, the evidenced example, the likely misunderstanding and its teaching function;
5. where a diagram, map, image, quotation or dataset could support understanding; and
6. the synthesis needed near the end to consolidate the central argument.

The pedagogical design shapes organisation and explanation only. It must not introduce an unsupported claim, example or source: every substantive element must derive from the evidence map and argument dossier and remain within the skill's evidence boundary. Do not create, include or plan interactive activities, exercises, discussion prompts, student tasks or participation formats in this skill's deliverables.

### 4. Full lecture script (Deliverable 2) in DOCX

- Use `teo-writing-academic` as the governing writing authority for this script and all associated written material. Read its required guidance before drafting.
- Write 3,600–4,400 words in Greek, targeting 4,000, as a spoken academic lecture rather than an essay summary. Realise the approved pedagogical design through clear explanation, examples and transitions, without interactive activities, exercises, discussion prompts or student tasks.
- Preserve the argument dossier's basic structure and scope. Use the additional length for greater analytical depth: explain theories, perspectives, schools of thought, mechanisms, disputes and implications with more precision and development. Do not add new topics, a wider catalogue of material, repetitive exposition or examples merely to increase length. Include an example only where it is analytically necessary and materially improves explanation, comparison or application.
- Write the lecture from the argument dossier and renewed source verification, never by simply expanding outline bullets, notes or short descriptions into paragraphs. It must sustain a self-contained argument, with clear conceptual disputes, mechanisms, documented examples, transitions and analytical development.
- Begin the lecture prose with one natural, spoken introductory paragraph. It must tell students what they will examine today, connect the unit to the relevant preceding sessions where applicable (for the first unit, establish the course-level connection without inventing a prior session), explain why the question matters now, and briefly orient them to the lecture's sections and how those sections build on, contrast with or extend one another. Integrate this orientation into the substantive introduction; do not add a technical contents note, abstract or detached preface. The paragraph is part of the lecture-prose word count. After it, begin the lecture's first substantive section and develop its central question, concepts, mechanisms and examples.
- At the end of every major lecture section, include a brief, low-key transition in natural spoken Greek that says what the next section turns to and why that move follows from the current one. Make the argumentative relation clear (for example, the next section may qualify, contrast with, deepen or apply the preceding analysis), but avoid repetitive signposting formulas or conspicuous roadmap language. The transitions must help listeners follow the text without interrupting its flow.
- End with a synthesis that opens the next unit. Every basic section must have a clear analytical function: posing a problem, defining a concept, developing a mechanism, examining a controversy, introducing an example, synthesising consequences or preparing the next step.
- The document body contains **only** the lecture title, its substantive headings and the lecture prose. At the end, add a `Βιβλιογραφία` section with complete verified APA references for every work cited in the lecture and no uncited works. Do not include a subtitle, module label, learning objective, target audience, abstract, metadata or other prefatory/following matter.
- Use parenthetical citations with author, year and exact page number(s) for every source-dependent claim, concept, example or interpretation in the lecture prose, for example `(Martínez, 2024, σσ. 4–6)`. For a permitted unpaginated Greek-example web source, cite the responsible organisation and date in the prose and provide its full APA reference with stable URL in the final bibliography; do not invent a page number. Do not mechanically insert author names into the verbal flow.
- Before assigning a page number, reopen the relevant project file and verify that the cited page(s) support the precise claim made in the sentence or paragraph. If the relationship cannot be confirmed exactly, revise, narrow or remove the claim; never retain an approximate, inherited or guessed page reference.
- Maintain the same page-specific citation standard in the outline. PowerPoint footers contain the complete APA reference only, without page numbers. Do not create speaker notes. For a permitted unpaginated Greek-example web source, use the exact article title or section heading, publication date and stable URL rather than a fabricated page number. The fact that a claim appeared in a previous draft, slide deck or memory does not count as verification.
- Use varied sentence length and paragraph rhythm. Avoid generic AI phrasing, uniform bullets, unsupported intensification and excessive theoretical name-checking.
- Create the final document in `[Παραδοτέα]` as `ΔΑ - [αριθμός ενότητας] - [τίτλος ενότητας].docx` from `[Templates]\Essay Template.dotx` and preserve its layout, styles and visual identity. The title inside the document must be exactly `ΔΑ - [αριθμός ενότητας] - [τίτλος ενότητας]`. Treat the file as a Word template, not as a generic document. If the authoring library requires a DOCX container, make an internal format-equivalent copy of the DOTX while preserving its OOXML styles, then build the final DOCX from that copy. Use the `documents` skill and render and visually inspect the DOCX before delivery.
- Before proceeding to the outline, measure the lecture-prose word count only. Exclude the final `Βιβλιογραφία` section from this count. Treat 3,600–4,400 words as the acceptable range, targeting 4,000. If it falls outside that range, revise and recheck the script before any downstream work begins.
- **Never pad a script to meet its word range.** Do not repeat a paragraph, sentence, transition, definition, example or generic formulation; do not use a loop, template expansion, automated filler or any comparable method that adds prose solely to increase the count. Every paragraph must make a distinct, source-grounded analytical contribution to the argument dossier.

Before proceeding to the outline, verify that the script falls within 3,600–4,400 words excluding the bibliography, that all citations include exact pages (or, for a permitted unpaginated Greek-example web source, the responsible organisation, exact article title or section heading, publication date and stable URL), that every cited work appears in the final APA bibliography, that its argument has a complete sequence of distinct analytical functions, that added length deepens rather than broadens the lecture, and that it follows the argument dossier. Run the duplicate-prose audit specified below and reject the script if any substantive paragraph is repeated exactly or near-exactly.

#### Mandatory script-integrity gate

Before creating the final lecture DOCX, inspect the complete script as a sequence of sections and paragraphs. Confirm that every substantive paragraph has a distinct claim, evidentiary basis, interpretation or transition, and that it advances the section's stated analytical function. A word-count-compliant draft fails this gate if it obtains length by restating a prior point without a new source-supported development.

Run a deterministic duplicate-prose audit on the lecture prose, excluding the title and the final bibliography. Normalise paragraph text by lowercasing it, collapsing whitespace and removing non-semantic punctuation. Reject any repeated substantive paragraph and any near-exact duplicate that retains the same sequence of sentences with only trivial formatting or connective changes. Record internally the paragraph locations, the matched text and pass/fail status. This audit is a hard gate: do not continue to the outline, DOCX finalisation or delivery until it passes.

Then perform a manual semantic-structure audit against the argument dossier. For every major section, record internally its distinct analytical function, the dossier move it realises, the verified sources it uses and its transition to the next section. Reject the draft if any section consists principally of recycled explanation, if a transition substitutes for analysis, or if any added passage lacks a distinct role in the argument.

#### Mandatory redesign gate for an out-of-range script

Word count is a planning criterion, not a technical target to be reached by padding or trimming a finished draft. The target is 4,000 words, with an acceptable range of 3,600–4,400 words, excluding the bibliography. If the first script falls outside that range, stop before slide planning, PPTX creation or final DOCX delivery. Do not enlarge an existing draft through repetitive explanation, generic theory, retroactive examples, a new unplanned subsection, unnecessary additional topics or an inflated summary. Do not shorten it by randomly removing sentences or paragraphs.

Never use automated repetition, a paragraph-generation loop, duplicated prose, boilerplate filler or any other mechanical extension to make a draft fall within range. Such a draft is invalid even if its deterministic word count passes.

Instead, return to the argument dossier and diagnose the substantive cause: whether its existing analytical moves need fuller explanation of theories, perspectives, schools of thought, mechanisms, disputes or implications; whether they overlap; and whether a single analytically necessary example would clarify a difficulty. Preserve the dossier's basic structure and scope. Revise the dossier first for depth, not breadth. Add, merge or reframe analytical moves only where this improves the lecture's logic and pedagogical function.

Update the dossier with the revised claim, mechanism, transition and source allocation. Then discard the out-of-range script as a drafting basis and write a new, complete lecture script from the revised dossier, targeting 4,000 words within the 3,600–4,400-word range. Do not mechanically extend, compress or patch the prior script.

Recheck the new script for a 3,600–4,400-word count excluding its bibliography, coherence, balance across sections, examples, citations and spoken rhythm. Proceed to the outline only when all of the following are true:

- the script falls within 3,600–4,400 words;
- every substantive final-script section corresponds to the revised argument dossier;
- every substantive addition is supported by a current, page-verified project source;
- the conclusion synthesises the lecture rather than serving as a reservoir for word-count expansion.

The outline must derive only from this final, fully redesigned script. Slide planning and PPTX production are prohibited until the user explicitly requests the second phase after reviewing the three written deliverables.

### 5. Lecture outline (Deliverable 3)

Only after the final lecture script passes its argument, citation, bibliography and word-count checks, draft an outline with discrete sections. It is an exact, concise and structurally organised mapping of the completed lecture, following the writing, syntax and revision rules of `teo-writing-academic`, not a prior plan to be elaborated.

For every section include:

- a concise title;
- a short, coherent account in natural prose of what the section contributes and what it covers, including the key claims, concepts, mechanisms, evidence and exact parenthetical citations with author, year and page number(s), for example `(Επώνυμο, 2024, σσ. 12–15)`; for a permitted unpaginated Greek-example web source, the responsible organisation, date, exact article title or section heading and stable URL instead of a fabricated page number;
- a concrete example, activity or question where it adds teaching value; and
- a brief explanation of how the section fits the lecture's wider structure: where it develops, specifies, contrasts with, qualifies or offers an alternative perspective to another section, and why the next section follows from it.

Write the outline as a readable map of the lecture's argument, not as a production worksheet. Do not use a field labelled «Λειτουργία» or a mechanical statement that a section «αντιστοιχεί στην τάδε παράγραφο» of the script. Do not map paragraph numbers or require one-to-one paragraph correspondence. The outline must make each section's subject, contribution and relationship to the whole lecture clear in a few concise sentences. Do not create an even, mechanical sequence; let more demanding conceptual or empirical material take the space it needs. The outline must not introduce a claim, example or bibliographic reference absent from the final script. If this check shows that substantive development is needed, return to the argument dossier and script, revise them from verified sources, and only then rebuild the outline; never add the material fragmentarily to the outline.

Create this deliverable in `[Παραδοτέα]` as `ΔΑ - [αριθμός ενότητας] - Προσχέδιο.docx` from `[Templates]\Outline Template.dotx`. Preserve that template's styles and visual identity. The title inside the document must be exactly `ΔΑ - [αριθμός ενότητας] - Προσχέδιο`.

Inside the outline DOCX, use this mandatory heading hierarchy from the Word template:

1. At the top, write `Δικαιώματα και ανισότητες [αριθμός ενότητας] - προσχέδιο` using **Heading 1**.
2. Immediately below it, write the complete, exact unit title using the **Title** style.
3. Write every discrete outline section with consecutive numbering and its section title using **Heading 3**. Below each heading, place the concise prose description of its content and contribution, its exact evidence and citations, any useful activity/example, and its relationship to the wider lecture and transition to the next section, in the appropriate body style.

Do not replace these internal headings with the filename, do not add other prefatory metadata, and do not use Heading 1 or Title again elsewhere in the outline.

Before delivering the first three files, review the outline DOCX against the required heading hierarchy, page-specific citations, structural explanations and template formatting. Confirm that it is an accurate, readable, concise condensation of the final lecture script, that no section is reduced to a «function» label or paragraph cross-reference, and that transitions between sections are intelligible. If it has a substantive or formatting defect, repair the earliest responsible stage. Then deliver the three written files and stop for user review; do not proceed to a slide plan.

