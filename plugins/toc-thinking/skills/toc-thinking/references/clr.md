# Categories of Legitimate Reservation

The rules for scrutinising a sufficiency tree. `sources.md` says where each
source was read. Quotations marked TOCICO are from the *TOCICO Dictionary*,
second edition. Quotations marked Dettmer are from *The Logical Thinking
Process* (2007).

## Seven or eight

TOCICO counts seven, in three levels: "Level I: clarity reservation. Level
II: causality existence and entity existence reservations. Level III: cause
insufficiency, additional cause, predicted effect existence, cause-effect
reversal or tautology reservations." Dettmer counts eight by listing
tautology on its own. This file follows Dettmer's eight and keeps TOCICO's
levels.

Order matters. TOCICO: "Scrutinizers should proceed from level I to level II
to level III reservations". And the reservations are offers, not verdicts:
"the tree builder is free to accept or reject any reservation at any level."

Scope. Dettmer, chapter 2: the categories "were designed to apply primarily
to sufficiency trees, but they do have some applicability to necessity trees
as well." A cloud's arrows and a prerequisite tree's arrows are checked by
questioning their assumptions (`tools.md`, two logics).

## Level I

### 1. Clarity

TOCICO: raised when the scrutiniser "is concerned about the meaning of an
individual word, the complete statement contained in an entity, or a section
of the diagram, or ... does not recognize a reasonable connection between
the stated cause and the stated effect." Dettmer: "Clarity is not, strictly
speaking, a logic-based reservation. Its roots are in communication." A link
that skips several steps is a clarity problem.

Software example. Fails: "The service is slow." Passes: "The API's p95
response time exceeds 2 seconds at 10 requests per second."

## Level II

### 2. Entity existence

TOCICO: "used to challenge the validity of a proposed statement of fact".
The question: "Does this entity really exist in your world as you have
stated it?" Dettmer tests each entity for completeness (a full sentence),
structure (one idea, no *if-then* inside it) and validity (it exists and can
be evidenced).

Software example. Fails: "Tight coupling exists." Passes: "OrderService
imports five internal classes of ShippingService, and both write the same
table."

### 3. Causality existence

TOCICO: "used to question whether or not the proposed causal relationship
between two entities really exists." Causation is separated from
correlation "by the verifiability of a causal relationship." Dettmer: read
the link aloud as "If [cause], then [effect]" and say how the cause produces
the effect.

Software example. Fails: "If we added caching then users see stale data."
Passes: "If the status cache keeps an entry for five minutes and the payment
service writes the database without invalidating the cache, then a status
read within five minutes returns the old value."

## Level III

### 4. Cause insufficiency

TOCICO: "used when the scrutinizer believes the proposed cause alone is
inadequate to explain the effect." The missing cause is a co-cause joined
with *and*. Dettmer uses "cause sufficiency" and "cause insufficiency" for
the same reservation, and advises keeping the co-causes to three, four at
most.

Software example. Fails: "If there are no tests then deployments fail."
Passes: "If there are no tests and no staging environment and deployments
run unattended, then a defect reaches production undetected."

### 5. Additional cause

TOCICO: "used ... to question whether the stated cause(s) is(are) sufficient
to fully account for the stated effect." The addition is a second,
independent cause of the same effect: "eliminating only one of multiple
independent causes will not overcome the effect entirely." The two sources
draw it differently. TOCICO draws the two causes as "a magnitudinal 'and'
connector", each adding to the size of the effect. Dettmer draws them as
alternatives, and his test reads: "If I eliminate the stated cause, is there
any other circumstance under which the same degree of effect would occur?"
Dettmer also sets this reservation aside when scrutinising a Future Reality
Tree, where only the injection's own effect matters.

Software example. "If the connection pool is exhausted then p95 exceeds 2
seconds" may be true and still not the whole story: an N+1 query pattern or
a missing index produces the same effect on its own, and removing the pool
problem alone leaves part of the latency in place.

### 6. Cause-effect reversal

TOCICO: "used to question whether the cause and effect have been switched."
Dettmer: "Is the stated cause really a reason why, or just how we know the
effect exists?" An indicator of the effect is not its cause.

Software example. Fails: "If the error rate dashboard is red then the
service is failing." The red dashboard is how the failure is known, not why
it happens. A loop, where an effect feeds a cause below it, is a different
structure and a legitimate part of a tree (`tools.md`, Current Reality
Tree).

### 7. Predicted effect existence

TOCICO: "used to challenge either an entity's existence or the existence of
a causal relationship on the basis of the absence of an inevitable effect
that would have to exist if the entity or the proposed causal relationship
really existed." Dettmer: "Predicted effect existence means that if a
proposed cause-effect relationship is valid, some other unstated effect
would also be expected." His example is appendicitis offered as the cause
of abdominal pain: a fever and a raised white cell count would also be
expected, and their absence refutes the cause. Name such an effect and
check for it.

Software example. Claimed cause: "a memory leak in the image handler." If
so, heap use must rise with the number of images processed and fall after a
restart. If heap use is flat across a day of image traffic, the claimed
cause is refuted.

### 8. Tautology

Dettmer: "The effect is offered as a rationale for the existence of the
cause." His example statement is "The Dodgers lost the game because they
played poorly", and the tautology is asking how the poor play is known and
answering that they lost. TOCICO treats this as the same reservation as
cause-effect reversal.

Software example. Fails: "Quality is low because the software has defects."
Ask what produces the defects: no review, no tests, unclear requirements.
