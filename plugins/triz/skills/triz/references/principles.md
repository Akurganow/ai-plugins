# The 40 inventive principles

Numbered as the matrix numbers them. Each entry gives four things. The
name, in the wording the transcriptions in `sources.md` share. The
variants a reader will meet elsewhere. The sub-items, paraphrased from the
MIT-licensed transcription by Robert Adunka that `sources.md` names, which
follows Altshuller's structure and adds items of its own. A software
reading, which is this skill's own, written for the adaptation step, and
not Altshuller's text. Read a principle as a direction and state what it
would mean in the user's system.

## 1. Segmentation

Divide an object into independent parts. Make it easy to take apart.
Increase the degree of fragmentation, down to the micro level.

Software: split a module, a store or a request by tenant, by time, by
version. Partition a table. Break a batch into records.

## 2. Taking out

Variants: extraction, separation. Extract the disturbing part or property
from an object, or extract the only part that is needed.

Software: pull the slow path out of the hot loop. Move a side effect out of
a pure function. Isolate the one operation that needs a lock.

## 3. Local quality

Go from a uniform structure to a non-uniform one. Let different parts do
different jobs. Give each part its own best conditions.

Software: tiered caching, graded validation by field, a different retry
policy per endpoint, strict types at the boundary and loose ones inside.

## 4. Asymmetry

Replace a symmetric form with an asymmetric one, or increase the asymmetry
that exists.

Software: a discriminated union instead of one shape for all cases. A
read model that differs from the write model. Unequal replicas.

## 5. Merging

Variants: consolidation, combining. Bring like objects together in space or
in time. Form bi- and poly-systems.

Software: batch writes, coalesce events, bundle requests, run similar jobs
in one pass.

## 6. Universality

One object does several functions, so that others become unnecessary. Use
standard interfaces.

Software: one handler for several message types, a plugin interface, a
generic component in place of a family of specific ones.

## 7. Nested doll

Variants: nesting, matryoshka. Put one object inside another, and that
inside a third. Pass one object through a cavity in another.

Software: recursive types, nested transactions, a hierarchy of stores,
middleware that wraps middleware.

## 8. Anti-weight

Variants: counterweight. Compensate the weight of an object by joining it
to something that lifts, or by using the environment.

Software: an index that offsets the cost of a scan, a cache that offsets
latency, a CDN that offsets distance.

## 9. Preliminary anti-action

Variants: prior counter-action. When an action has a harmful effect,
perform the counter-action first. Pre-tension in the opposite direction.

Software: a circuit breaker armed before the call, a rollback plan written
before the migration, a reservation before the write.

## 10. Preliminary action

Variants: prior action. Perform the required change, or part of it, in
advance. Arrange things so they act without delay.

Software: precomputation, prefetching, warm caches, connection pools,
ahead-of-time compilation.

## 11. Beforehand cushioning

Variants: in-advance cushioning, beforehand compensation. Compensate for
low reliability with countermeasures prepared in advance.

Software: rate limits, input validation at the edge, error boundaries,
backups, a dead-letter queue.

## 12. Equipotentiality

Change the conditions so the object need not be raised or lowered. Avoid
changes in potential and peaks in load.

Software: keep data at the level where it is used instead of moving it up
and down layers. Level the load with a queue. Keep latency budgets even.

## 13. The other way round

Variants: inversion, reverse. Do the opposite of what the task prescribes.
Make the fixed part move and the moving part fixed. Turn it upside down.

Software: pull instead of push, lazy instead of eager, let the consumer
call back, invert a dependency.

## 14. Spheroidality and curvature

Variants: spheroidality. Replace straight and flat with curved. Use
rollers and spirals. Replace linear motion with rotation.

Software: exponential backoff instead of a fixed interval, a ring buffer
instead of a list, smoothing instead of thresholds.

## 15. Dynamics

Variants: dynamization, dynamicity. Let the object or its environment
adjust to the best state at each phase. Make a rigid thing movable.

Software: adaptive limits, autoscaling, feature flags, a strategy chosen at
run time from the data's shape.

## 16. Partial or excessive actions

When the whole is hard to reach, do a little less or a little more.

Software: over-fetch and filter, over-provision and trim, validate the
common fields now and the rest later.

## 17. Another dimension

Variants: transition to another dimension. Move from a line to a plane to
a volume. Use several layers. Use the other side.

Software: index by time as well as by key, add a tier, shard along a second
axis, render on the server as well as on the client.

## 18. Mechanical vibration

Set the object oscillating. Raise the frequency. Use resonance.

Software: periodic health checks, jittered retries, a heartbeat, a sampling
rate tuned to the signal.

## 19. Periodic action

Replace continuous action with pulses. Change the frequency. Use the
pauses for something else.

Software: batch jobs, polling on a schedule, debouncing, work done between
frames.

## 20. Continuity of useful action

Keep all parts working at full load without pauses. Remove idle time.

Software: streaming instead of request and reply, background workers,
pipelining, a pool that never drains.

## 21. Skipping

Variants: rushing through. Do a harmful or dangerous step at high speed.

Software: an atomic swap instead of an incremental update, a fast cut-over,
a migration in one short window.

## 22. Blessing in disguise

Variants: convert harm into benefit. Use a harmful factor to get a useful
effect. Remove one harm with another. Amplify a harm until it stops
being one.

Software: treat errors as signal for observability, use load to warm the
cache, turn a duplicate delivery into an idempotency check.

## 23. Feedback

Introduce feedback, or change the feedback that exists.

Software: metrics that drive a controller, backpressure, an adaptive
timeout, user-visible progress.

## 24. Intermediary

Variants: mediator. Use an intermediate object to carry or perform the
action. Attach a temporary object that is easy to remove.

Software: a gateway, a queue, an adapter, a proxy, a facade over a legacy
interface.

## 25. Self-service

The object serves and repairs itself. Use waste and lost energy.

Software: a cache that refreshes itself on write events, self-healing
workers, garbage collection, logs that compact themselves.

## 26. Copying

Use a cheap copy instead of the fragile or expensive original. Replace an
object with its optical or digital image.

Software: a mock, a replica, a snapshot, synthetic data, a shadow deploy.

## 27. Cheap short-living objects

Variants: cheap disposables. Replace an expensive durable object with
several cheap ones, giving up some property.

Software: ephemeral containers, disposable environments, short-lived
tokens, immutable builds thrown away after use.

## 28. Mechanics substitution

Variants: replacement of a mechanical system. Replace a mechanical system
with an optical, acoustic, thermal or chemical one. Use fields. Make a
static field dynamic and structured.

Software: replace polling with events, a manual step with a signal, a
timer with a trigger, a scan with a subscription.

## 29. Pneumatics and hydraulics

Replace solid parts with gas or liquid.

Software: replace a rigid structure with a flow: a stream instead of a
buffer, a pipeline instead of stages that hand off files.

## 30. Flexible shells and thin films

Variants: flexible membranes. Replace a rigid construction with a flexible
shell. Isolate an object with a thin film.

Software: a thin interface layer over a core, a thin client, an
anti-corruption layer.

## 31. Porous materials

Make the object porous, or fill existing pores with something useful.

Software: sparse indexes, probabilistic structures, gaps in a schedule kept
free on purpose, room left in a format for later fields.

## 32. Colour changes

Variants: optical property changes. Change the colour or transparency of
an object or its surroundings. Use marker additives.

Software: feature flags that mark a path, tracing tags, colour in a
dashboard, a visible marker on a record.

## 33. Homogeneity

Make interacting objects of the same material.

Software: one error format everywhere, one serialisation, one language on
both sides of a boundary.

## 34. Discarding and recovering

Variants: rejecting and regenerating parts. Discard a part once it has
done its job. Restore used parts during operation.

Software: purge stale entries, rotate keys, regenerate a derived table,
drop a temporary index after the migration.

## 35. Parameter changes

Variants: changing properties, transformation of properties. Change the
state of aggregation, the density, the flexibility, the temperature, the
pressure.

Software: change the representation: denormalise, serialise, change the
encoding, change the consistency level, change the granularity.

## 36. Phase transitions

Use the effects that occur during a change of state.

Software: use the moment of a state change: on commit, on deploy, on
connection, on rollover.

## 37. Thermal expansion

Use expansion and contraction with temperature. Use materials with
different coefficients.

Software: let a structure grow and shrink with load: elastic pools, dynamic
arrays, adaptive sampling.

## 38. Strong oxidants

Variants: accelerated oxidation. Replace air with enriched air, then
oxygen. Use ionised oxygen and ozone.

Software: enrich the environment: more capable runtime, managed services,
a stronger consistency guarantee where it pays.

## 39. Inert atmosphere

Replace the usual medium with an inert one. Work in a vacuum. Add inert
additives.

Software: a sandbox, an isolated container, a read-only mode, a clean
environment for a test.

## 40. Composite materials

Replace a uniform material with a composite one.

Software: hybrid storage, a cache in front of a log, polyglot persistence,
a component built from parts with different properties.

## Separation principles for a physical contradiction

The skill uses four separations in Step 4: in space, in time, on
condition, and between the parts and the whole. That set comes from later
teaching texts, among them the MATRIZ glossary of 2014 and the TETRIS
handbook of 2009. Altshuller's own lists are different. In 1979, in
ARIZ-77, he gave four:

- in space
- in time
- through transitional states in which the opposite properties coexist or
  alternate
- by restructuring, so that the parts have one property and the whole the
  other

In ARIZ-85C he gave the eleven of its Table 2, which `ariz-85c.md` lists
under step 5.3. "On condition" is in neither of his lists. Authors also
attach lists of the 40 principles to each separation. The lists differ
between authors, so this skill attaches none. `sources.md` names where
each list was read.
