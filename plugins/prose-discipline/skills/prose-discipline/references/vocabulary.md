# Vocabulary: Depth

Extends the Vocabulary section of the core rule with the substitution
catalog and the domain-term contract.

## Substitution table

| Instead of | Write | Reason |
| --- | --- | --- |
| leverage, utilize | use | plain verb |
| utilize, make use of | use | plain verb |
| facilitate | help, enable | plain verb |
| in order to | to | shorter |
| prior to | before | shorter |
| due to the fact that | because | shorter |
| in the event that | if | shorter |
| at this point in time | now, currently | shorter |
| a plethora of, a myriad of | many | plain quantifier |
| ensure that, make sure that | verify that, check that | active assertion, where the step checks a condition |
| delve into, dive into | examine, inspect, review | non-cliché |
| establish connectivity | connect | plain verb |
| streamlines, empowers, harnesses | (delete, or state the concrete effect) | marketing |
| serves as a mechanism to | does | plain copula |
| game-changer, transformative | (delete, or state the measurable change) | hype |

`ensure` survives where the instruction requires the actor to *make* a
condition true. Substituting `verify` there turns a required remediation
into an observation, which is a worse defect than the weak verb. The test:
if the reader must change something, keep `ensure` or name the action.

## Weak verbs and split predicates

Use direct action verbs across all languages. Avoid weak verbs coupled with
verbal nouns (such as "perform validation" -> validate, "carry out execution"
-> execute).

## Significance inflation

Delete or quantify: *pivotal*, *crucial*, *vital*, *cornerstone*,
*testament to*, *powerful*, *comprehensive*, *robust* (outside its
term-of-art use below), and non-English equivalents. If the thing matters,
the consequence or number states it.

## Hollow reassurance and filler: delete on sight

"Rest assured", "please be advised", "we understand the importance of",
"it goes without saying", "it is important to note", and their non-English
equivalents. Each carries zero information.
## Domain-term contract

These terms are correct engineering vocabulary and are never flagged:

- *accessible*: UI and API documentation standard term.
- *accept*: protocols and tests accept input. "The server accepts the
  request" is exact.
- *validate*: schemas, parsers, forms.
- *rotate*: credentials, logs, keys.
- *robust*: statistics (robustness checks) and distributed systems (robust
  consensus) use it as a term of art.

The test: if the term names a technical property, keep it. If it decorates a
claim ("a robust solution"), delete it or state the guarantee it implies.

## Audit severity

- Substitution-table and inflation findings: `minor`.
- A hollow phrase that replaces a missing fact ("robust handling" instead of
  naming the failure mode): `major`. The reader cannot act on it.
