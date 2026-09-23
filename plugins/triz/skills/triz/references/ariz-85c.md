# ARIZ-85C, part by part

The algorithm Altshuller published in 1985, in his order of parts and
steps. The steps are paraphrased in English, with a gloss for software
work under each. The text is quoted where the wording is the instrument.
The mini-problem, the two ideal final results and the physical
contradiction are formulas, and their words carry the method. `sources.md`
says which copies the text was read from, one Russian and one English,
and which pages could not be opened.

The English text opens with a warning: "ARIZ is a complicated tool. Do not
apply it to solve new practical problems without at least 80 academic
hours of preliminary study." The walk in this skill is guided, and the
user should know what the author asked of a solver.

## The name

ARIZ is the Russian acronym for Algorithm of Inventive Problem Solving.
Versions are named by year. In 1985 three modifications followed each
other, lettered with the first three letters of the Russian alphabet, and
the third is ARIZ-85-В. English texts write the Cyrillic В either by its
position, C, or by its sound, V. "ARIZ-85C" and "ARIZ-85V" are the same
text. The C does not stand for "complete". `sources.md` says what this
naming rests on.

The algorithm has nine parts and forty steps. Part 5 names the instruments
it applies:

- the standard solutions
- problems solved before
- the table of typical transformations for a physical contradiction
- the pointer to physical effects

It names the 40 principles once, in step 9.2, as a record to compare the
finished solution against. It does not name the contradiction matrix. That
is why this skill treats the matrix route and the ARIZ route as two routes
rather than one.

## Vocabulary

- **Product** (изделие): the element that is acted upon.
- **Tool** (инструмент): the element that acts on the product.
- **Technical contradiction** (ТП): a state of the tool that gives one good
  effect and one bad one. Written as a pair, TC-1 and TC-2, one for each
  state of the tool.
- **X-element** (икс-элемент): a placeholder for the change that is not yet
  known. It enters in step 1.6 and is the subject of the ideal final result.
  It is not required to be a new part.
- **Operative zone** (ОЗ) and **operative time** (ОВ): where and when the
  conflict happens.
- **Substance-field resources** (ВПР): what the system, its environment and
  the product already contain that the solution may use.
- **Physical contradiction** (ФП): the operative zone must be in one state
  for one of the conflicting actions and in the opposite state for the
  other.
- **IFR** (ИКР): the ideal final result. ARIZ writes two.

## Part 1. Analysis of the problem

**1.1** Write the mini-problem without special terms, in this form:

> Техническая система: для (указать назначение) включает (перечислить
> основные части системы).
> Техническое противоречие 1 (ТП-1): ЕСЛИ ..., ТО ... , НО ...
> Техническое противоречие 2 (ТП-2): ЕСЛИ ..., ТО ... , НО ...
> Необходимо при минимальных изменениях в системе (указать результат,
> который должен быть получен).

The English text's pattern: "A technical system for <state the purpose of
the system> includes <list the main parts of the system>. Technical
contradiction 1 (TC-1): (identify). Technical contradiction 2 (TC-2):
(identify). It is necessary, with minimum changes to the system, to <state
the required result>." Each contradiction reads *if* a state of the tool
*then* a good effect *but* a bad one.

Software gloss: the tool is the component whose setting or behaviour is in
question, and the product is what it acts on. "If the cache holds an entry
for an hour, then the database is idle, but readers see old data. If it
holds an entry for a second, then readers see fresh data, but the database
is saturated."

**1.2** Name the conflicting pair: the product and the tool.

**1.3** Draw the schemes of TC-1 and TC-2 using Table 1 of the algorithm,
"Typical Graphic Models of Technical Contradictions". Its nine shapes, in
the English text's names, with A the tool and B the product:

1. Counteraction: A acts usefully on B, and at some stage B acts back on A
   harmfully.
2. Conjugated action: A's useful action on B also harms B.
3. Conjugated action: A's useful action on one part of B harms another
   part of B.
4. Conjugated action: A's useful action on B harms C, a third part of the
   system.
5. Conjugated action: A's useful action on B harms A itself.
6. Incompatible action: A's useful action on B is incompatible with C's
   useful action on B.
7. Incomplete action or inaction: A gives one useful action where two are
   required, or does not act on B at all.
8. "Silence": there is no information about A, B or their interaction.
9. Unregulated action: the action of A on B is uncontrollable where a
   controllable one is required.

Name the shape each contradiction has. In a software problem A and B are
components or data and the actions are calls, writes, reads and events.

**1.4** Of the two, choose the contradiction whose good effect is the
system's main function.

**1.5** Intensify the conflict: push the tool's state to its extreme. Not
"a long TTL" but "an entry that is never evicted".

**1.6** Write the problem model: the conflicting pair, the intensified
conflict, and what the X-element must do. What it must keep, and what it
must remove, improve or provide.

**1.7** Check whether a standard solution resolves the model.

- If not, go to Part 2.
- If it does, Part 7 may follow. The algorithm still recommends Part 2.
- This package does not carry the 76 standard solutions. Say so, and go
  on to Part 2.

## Part 2. Analysis of the problem model

**2.1** Define the operative zone: where the conflict happens.

**2.2** Define the operative time: when it happens, and what precedes it.

**2.3** List the substance-field resources of the system, of its environment
and of the product. In software: data already held, events already emitted,
idle capacity, a clock, a log, a version number, a client that already
polls.

## Part 3. The ideal final result and the physical contradiction

**3.1** Write IFR-1:

> икс-элемент, абсолютно не усложняя систему и не вызывая вредных явлений,
> устраняет (указать вредное действие) в течение оперативного времени
> (ОВ) в пределах оперативной зоны (ОЗ), сохраняя способность инструмента
> совершать (указать полезное действие).

The English text's pattern: "The X-element, without complication of the
system and without harmful side effects, eliminates <indicate the harmful
action> during the <Operational Time> inside the <Operational Zone>,
keeping the ability of the tool to provide <indicate the useful action>."

**3.2** Strengthen IFR-1 with one added requirement. No new substances and
no new fields may be brought in. The solution uses the resources listed in
2.3. In software: no new service, store or protocol before the existing
ones have been tried.

**3.3** Write the physical contradiction at the macro level. The English
text's pattern: "the <Operational zone>, during the <Operational time>,
has to... <indicate physical macro-state, for example 'hot'> in order to
perform <indicate one of the conflicting actions> and has to... <indicate
the opposite physical macro-state, for example 'cold'> to perform
<indicate another conflicting action or requirement>." Both halves are
positive. The zone must be hot for one action and must be cold for the
other. The Russian copy this reference was read from writes the second
half as «и не должна (указать противоположное физическое макросостояние,
например "быть холодной")». Read literally, that states no contradiction.
Use the English form.

**3.4** Write the physical contradiction at the micro level. The English
text's pattern: "There should be particles of a substance <indicate their
physical state or action> in the Operational Zone in order to provide
<indicate the macro-state according to step 3.3> and there should not be
the particles (or particles should have the opposite state or action)" to
provide the opposite macro-state. In software the particles are the
records, requests or cells that make up the zone.

**3.5** Write IFR-2:

> оперативная зона (указать) в течение оперативного времени (указать)
> должна сама обеспечивать (указать противоположные физические макро- или
> микросостояния).

The English text's pattern: "The Operational Zone <indicate> has to
provide <indicate the opposite macro- or micro-states> itself during the
Operational Time <indicate it>."

**3.6** Check whether a standard solution resolves the physical problem as
IFR-2 states it. If not, go to Part 4. As at 1.7, the standard solutions
are not carried here: say so and go on to Part 4.

## Part 4. Mobilising and applying the resources

**4.1** Model the conflict with "little people": draw the zone as a crowd of
agents, redraw it so that they act without conflict, then translate the
drawing back into a technical scheme.

**4.2** Take a step back from the IFR, when the finished system is known
and the problem is how to reach it. Draw the finished system. Make the
smallest change that breaks it.

**4.3** Check whether a mixture of resource substances solves the problem.

**4.4** Check whether replacing a resource with a void, or a mixture with a
void, solves it.

**4.5** Check whether a substance derived from a resource solves it.

**4.6** Check whether an electric field in place of a substance, or two
interacting electric fields, solves it.

**4.7** Check whether a pair of a field and an additive that responds to it
solves it.

Software gloss for 4.3 to 4.7: the substances are data and components, the
fields are the interactions between them. A "void" is an absence used on
purpose: a gap in a schedule, an empty slot, a missing entry that means
something. A "derived substance" is a projection, a hash, a digest or a
version of data already held. A "field with a responsive additive" is a
signal plus a marker that reacts to it: a tag on a record that a sweep
recognises.

## Part 5. Applying the information fund

**5.1** Try the standard solutions on the problem as IFR-2 states it, with
the resources refined in Part 4.

**5.2** Try analogy with non-standard problems solved earlier by ARIZ.

**5.3** Try the typical transformations for removing a physical
contradiction, which the algorithm keeps in its Table 2, "Principles for
Eliminating Physical Contradictions". The eleven, in the English text's
wording:

1. Separation of conflicting properties in space.
2. Separation of conflicting properties in time.
3. System transition 1a: combination of homogeneous or heterogeneous
   systems into a super-system.
4. System transition 1b: transition from a system to an anti-system, or
   combination of a system with an anti-system.
5. System transition 1c: the entire system has a property X while its
   parts have a property opposite to X (anti-X).
6. System transition 2: transition to a system that works on the
   micro-level.
7. Phase transition 1: substitution of the phase state of a system's part
   or external environment.
8. Phase transition 2: dual phase state of a system part (using
   substances capable of converting from one phase to another according
   to the operating conditions).
9. Phase transition 3: using phenomena associated with phase transitions.
10. Phase transition 4: substitution of a mono-phase substance with a
    dual-phase state.
11. Physical-chemical transition: substance appearance-disappearance as
    a result of decomposition-combination, ionization-recombination.

The rule beside this step: "Only solution concepts that completely match
the IFR or come close to it are acceptable." The four separations in
`SKILL.md` Step 4 come from later teaching texts, and `principles.md`
names them.

Software gloss. Items 3 to 6 are the system-level moves: a cluster of
services as one system, a service and its inverse, a rigid whole made of
loose parts, a move to a finer grain. Items 7 to 11 are changes of state: a
representation that switches with the conditions, a resource that exists
only while it is needed.

**5.4** Apply the Pointer to Physical Effects and Phenomena: "Consider the
possibility of resolving the Physical contradiction using the Pointer to
Physical Effects and Phenomena." The pointer is a catalogue of physical
effects indexed by the function wanted. In software the counterpart is a
catalogue of known mechanisms: the algorithms, data structures and
protocols that provide a function.

## Part 6. Changing or replacing the problem

**6.1** If solved, go from the physical answer to a technical one: state the
method and give the scheme of the device that carries it out.

**6.2** If not solved, check whether step 1.1 combined several problems.
Split them and solve the main one.

**6.3** If not solved, choose the other technical contradiction at step 1.4.

**6.4** If not solved, return to 1.1 and restate the mini-problem at the
level of the supersystem. Repeat as needed.

## Part 7. Analysis of the way the physical contradiction was removed

**7.1** Check the solution concept: "Consider each introduced substance and
field. Is it possible to apply available or derived SFRs instead of
introducing the substances/fields? Can self-controlled substances be
applied? Correct obtained technical solution accordingly." In software:
for each component or interaction the solution adds, ask whether a
resource listed in 2.3 does the same job, and whether a part can change
its own state in response to conditions instead of being driven.

**7.2** Assess the solution with four questions.

- Does it meet the main requirement of IFR-1, that the element does it
  itself?
- Which physical contradiction did it remove, and did it?
- Does the system contain at least one well-controlled element, and how
  is it controlled?
- Does a solution found for one cycle hold under many cycles?

**7.3** Check the formal novelty of the solution against patent data. In
software: against the published designs and the libraries that already
exist.

**7.4** Write the sub-problems the idea raises: inventive, design,
calculation and organisational.

## Part 8. Applying the answer

**8.1** Say how the supersystem that contains the changed system must
change.

**8.2** Check whether the changed system, or the supersystem, can be used
in a new way.

**8.3** Use the answer for other problems.

- State the principle in general form.
- Apply it directly to other problems.
- Try its inverse.
- Build a morphological table of its variants.
- See how it changes as the system's size goes to zero and to infinity.

## Part 9. Analysis of the course of the solution

**9.1** Compare the real course of the solution with the theoretical one
and write down the deviations.

**9.2** Compare the solution with the knowledge base: "Compare the
obtained solution concept to the information in the TRIZ knowledge base
(Inventive Principles, Inventive Standards, and Pointer to Physical Effects
and Phenomena). If the knowledge base does not include a principle that
applies to the obtained solution concept, document this principle in the
preliminary knowledge base." This is the one step in the algorithm that
names the inventive principles, and it names them as a record to compare
against, after the solution.
