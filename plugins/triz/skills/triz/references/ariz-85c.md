# ARIZ-85C, part by part

The algorithm Altshuller published in 1985, in the order and the wording he
gave it, with a gloss for software work under each step. The Russian text is
quoted where the wording is the instrument: the mini-problem, the two ideal
final results and the physical contradiction are formulas, and their words
carry the method. `sources.md` says which copy the text was read from and
which pages could not be opened.

## The name

ARIZ is the Russian acronym for Algorithm of Inventive Problem Solving.
Versions are named by year. In 1985 three modifications followed each other,
lettered with the first three letters of the Russian alphabet, and the third
is ARIZ-85-В. English texts write the Cyrillic В either by its position, C,
or by its sound, V. "ARIZ-85C" and "ARIZ-85V" are the same text. The C does
not stand for "complete".

The algorithm has nine parts and forty steps. Part 5 names the instruments
it applies: the standard solutions, problems solved before, the table of
typical transformations for a physical contradiction, and the pointer to
physical effects. It does not name the 40 principles or the contradiction
matrix. That is why this skill treats the matrix route and the ARIZ route
as two routes rather than one.

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

> Техническая система для (назначение) включает (основные части).
> ТП-1: ЕСЛИ ..., ТО ..., НО ...
> ТП-2: ЕСЛИ ..., ТО ..., НО ...
> Необходимо при минимальных изменениях в системе (результат).

The system, its purpose, its main parts. Two technical contradictions, each
as *if* a state of the tool *then* a good effect *but* a bad one. The result
that must be reached with minimal change.

Software gloss: the tool is the component whose setting or behaviour is in
question, and the product is what it acts on. "If the cache holds an entry
for an hour, then the database is idle, but readers see old data. If it
holds an entry for a second, then readers see fresh data, but the database
is saturated."

**1.2** Name the conflicting pair: the product and the tool.

**1.3** Draw the schemes of TC-1 and TC-2 using Table 1 of the algorithm,
which lists the typical conflict shapes.

**1.4** Of the two, choose the contradiction whose good effect is the
system's main function.

**1.5** Intensify the conflict: push the tool's state to its extreme. Not
"a long TTL" but "an entry that is never evicted".

**1.6** Write the problem model: the conflicting pair, the intensified
conflict, and what the X-element must do. What it must keep, and what it
must remove, improve or provide.

**1.7** Check whether a standard solution resolves the model. If not, go to
Part 2. If it does, Part 7 may follow, and the algorithm still recommends
going on with Part 2.

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
> устраняет (вредное действие) в течение оперативного времени в пределах
> оперативной зоны, сохраняя способность инструмента совершать (полезное
> действие).

The X-element, without complicating the system and without causing harm,
removes the harmful action during the operative time within the operative
zone, while keeping the tool's useful action.

**3.2** Strengthen IFR-1: no new substances and no new fields may be brought
in. The solution uses the resources listed in 2.3. In software: no new
service, no new store, no new protocol, before the existing ones have been
tried.

**3.3** Write the physical contradiction at the macro level:

> оперативная зона в течение оперативного времени должна (макросостояние),
> чтобы выполнять (одно конфликтующее действие), и не должна
> (противоположное макросостояние), чтобы выполнять (другое).

The operative zone, during the operative time, must be in one state to do
one of the conflicting actions and must not be in it to do the other.

**3.4** Write the physical contradiction at the micro level: the same
requirement stated for the parts of the zone rather than the zone as a
whole.

**3.5** Write IFR-2:

> оперативная зона в течение оперативного времени должна сама обеспечивать
> (противоположные макро- или микросостояния).

The operative zone itself, during the operative time, provides both
opposite states.

**3.6** Check whether a standard solution resolves the physical problem as
IFR-2 states it. If not, go to Part 4.

## Part 4. Mobilising and applying the resources

**4.1** Model the conflict with "little people": draw the zone as a crowd of
agents, redraw it so that they act without conflict, then translate the
drawing back into a technical scheme.

**4.2** When the finished system is known and the problem is how to reach
it, take a step back from the IFR: draw the finished system and make the
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
contradiction, which the algorithm keeps in its Table 2. The four
transformations taught most often are in `SKILL.md`: separation in space,
in time, on condition, and between the parts and the whole.

**5.4** Apply the pointer to physical effects and phenomena. The wording of
this step was not read from the text (`sources.md`).

## Part 6. Changing or replacing the problem

**6.1** If solved, go from the physical answer to a technical one: state the
method and give the scheme of the device that carries it out.

**6.2** If not solved, check whether step 1.1 combined several problems.
Split them and solve the main one.

**6.3** If not solved, choose the other technical contradiction at step 1.4.

**6.4** If not solved, return to 1.1 and restate the mini-problem at the
level of the supersystem. Repeat as needed.

## Part 7. Analysis of the way the physical contradiction was removed

**7.1** Check the solution concept. The wording of this step was not read
from the text (`sources.md`).

**7.2** Assess the solution with four questions. Does it meet the main
requirement of IFR-1, that the element does it itself? Which physical
contradiction did it remove, and did it? Does the system contain at least
one well-controlled element, and how is it controlled? Does a solution
found for one cycle hold under many cycles?

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

**8.3** Use the answer for other problems. State the principle in general
form, apply it directly to other problems, try its inverse, build a
morphological table of its variants, and see how it changes as the
system's size goes to zero and to infinity.

## Part 9. Analysis of the course of the solution

**9.1** Compare the real course of the solution with the theoretical one
and write down the deviations.

**9.2** Compare the answer with the information fund. If the principle is
new, record it. The wording of this step was not read from the text
(`sources.md`).
