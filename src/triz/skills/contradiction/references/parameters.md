# The 39 engineering parameters

The parameters of the classic contradiction matrix, numbered as the matrix
numbers them. The names are the wording shared by the transcriptions
`sources.md` names. A variant is shown where those transcriptions differ.
The parameters describe physical systems. The software reading beside each
is this skill's own, written for the mapping step, and is not Altshuller's
text. Use it to find the parameter that plays the same role in the system
at hand, not as a definition.

"Moving" and "stationary" in parameters 1 to 8, 15, 16, 19 and 20 are read
here as "while the system runs" and "at rest": source, build output,
stored data and configuration are at rest, and a process, a request or a
session is moving.

| # | Parameter | Software reading |
| --- | --- | --- |
| 1 | Weight of moving object | Resources a running process consumes: memory, CPU, network while it works |
| 2 | Weight of stationary object | Footprint at rest: bundle size, dependency size, disk use, downloaded assets |
| 3 | Length of moving object | Path length at run time: call depth, middleware layers, hops a request makes |
| 4 | Length of stationary object | Size of the code or a module: files, lines, import depth, inheritance depth |
| 5 | Area of moving object | Surface active at once: rendered elements, live connections, concurrent processes |
| 6 | Area of stationary object | Interface width: exports, options, endpoints, parameters a caller can touch |
| 7 | Volume of moving object | Data in flight per unit of time: message rate, event rate, update volume |
| 8 | Volume of stationary object | Data held: cache size, stored state, index size, accumulated logs |
| 9 | Speed | Latency and throughput: response time, render time, operations per second |
| 10 | Force (Intensity) (variant: Force) | Intensity of one action on a resource: the size of one write, the weight of one request, the strength of one lock |
| 11 | Stress or pressure | Load under contention: concurrent requests, simultaneous writes, queue depth |
| 12 | Shape | Structure: module boundaries, component hierarchy, data model layout |
| 13 | Stability of the object's composition (variant: Stability of object composition) | Consistency: state in agreement across parts, invariants kept, contracts preserved |
| 14 | Strength | Strictness of guarantees: type safety, validation rigour, access control |
| 15 | Duration of action of moving object (variant: by moving object) | How long a running process stays healthy: a session, a connection, an uptime |
| 16 | Duration of action by stationary object (variant: of stationary object) | How long stored things stay valid: cache lifetime, token expiry, artifact reuse |
| 17 | Temperature | Rate of change: churn in code, mutation frequency, hot paths |
| 18 | Illumination intensity | Observability: what logs, metrics and traces show of what happens |
| 19 | Use of energy by moving object | Cost per active operation: computation per request, per render, per action |
| 20 | Use of energy by stationary object | Cost while idle: background tasks, polling, subscriptions, memory held by inactive parts |
| 21 | Power | Peak capacity: the largest burst the system handles |
| 22 | Loss of energy | Wasted work: recomputation, redundant operations, discarded results |
| 23 | Loss of substance | Lost data or state: dropped on navigation, lost on disconnect, lost on error |
| 24 | Loss of information | Lost meaning: swallowed errors, unclear logs, missing context for a diagnosis |
| 25 | Loss of time | Wasted time: waiting for builds, manual steps, slow feedback |
| 26 | Quantity of substance (variant: Quantity of substance/the matter) | Number of instances: components, connections, DOM nodes, dependencies |
| 27 | Reliability | Behaviour under failure: errors, edge cases, network faults handled or not |
| 28 | Measurement accuracy | Precision of what is measured or computed: timing, rounding, numeric correctness |
| 29 | Manufacturing precision | Reproducibility of the build: same input, same output, across machines |
| 30 | Object-affected harmful factors (variant: External harm affecting the object) | Harm from outside: attacks, unreliable third parties, platform differences |
| 31 | Object-generated harmful factors | Harm the system does to itself or its neighbours: coupling, side effects, leaks |
| 32 | Ease of manufacture | Effort to build: boilerplate, tooling friction, learning curve |
| 33 | Ease of operation | Ease of use: for the end user of a product, or for the caller of an interface |
| 34 | Ease of repair | Ease of diagnosis and fix: traceability, messages, reloads, source maps |
| 35 | Adaptability or versatility | Flexibility: reuse across contexts, configuration, theming, platforms |
| 36 | Device complexity | Number of parts and concepts a reader must hold: layers, indirections, abstractions |
| 37 | Difficulty of detecting and measuring (variant: Difficulty of detection) | Difficulty of testing and measuring: hard-to-mock dependencies, unobservable behaviour |
| 38 | Extent of automation | What runs without a person: checks, generation, formatting, deployment |
| 39 | Productivity | Useful output per unit of effort: build speed, iteration speed, delivery rate |
