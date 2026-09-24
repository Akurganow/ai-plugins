# 01 — What the published standards say a high-quality, conformant plugin and skill look like

Clean-room research, 2026-09-24 (UTC). No local repository was read. Everything below was fetched over HTTPS
through the session proxy with `curl` (CA bundle `/root/.ccr/ca-bundle.crt`), WebSearch or WebFetch. Quotes are
verbatim from the fetched text. Where a GitHub raw file was read, it was read from branch `main`; **no commit SHA
could be pinned** because every `github.com` / `api.github.com` request for these repos answered
`HTTP 403 {"message":"GitHub access to this repository is not enabled for this session. ..."}` (only
`raw.githubusercontent.com` was open). Treat every "raw @ main" citation as dated 2026-09-24, not as a permalink.

---

## 0. Sources and reachability

| # | Source | URL actually read | Reachable? | Notes |
|---|---|---|---|---|
| A1 | Agent Plugins Specification 1.0.0 (HTML) | https://agent-plugins.org/specification | Yes, HTTP 200 (425 591 bytes) | "Spec Version: 1.0.0 / Status: Published" |
| A2 | Same, Markdown copy | https://agent-plugins.org/specification.md | Yes, 200 | Normative MUST/SHOULD lines identical to A3 (diffed: no difference) |
| A3 | Spec source in its GitHub repo | https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md | Yes, 200 | raw @ main; SHA not obtainable (github.com 403, see above) |
| A4 | Plugin manifest JSON Schema | https://agent-plugins.org/schemas/1.0.0/plugin.schema.json | Yes, 200 (1 805 bytes) | sha256 `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`; byte-identical to raw @ main `schemas/1.0.0/plugin.schema.json` |
| A5 | MCP config schema | https://agent-plugins.org/schemas/1.0.0/mcp.schema.json | Yes, 200 | required `["$schema","mcpServers"]`, `additionalProperties: false` |
| A6 | Author guides | https://agent-plugins.org/plugin-authors/{build-an-agent-plugin,manifest,skills,mcp-servers,client-extensions}.md | Yes, 200 | Non-normative guides |
| A7 | Client implementer guide | https://agent-plugins.org/llms.txt (full-site dump incl. "Implement an Agent Plugins client") | Yes, 200 | |
| A8 | Spec repo README / 1.1.0 draft / FUTURE_CONSIDERATIONS | raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/{README.md,spec/1.1.0.md,FUTURE_CONSIDERATIONS.md} | Yes, 200 | 1.1.0 is "Working Draft"; diff vs 1.0.0 is version strings + two wording changes only |
| A9 | Official example package | raw.githubusercontent.com/agentplugins/agent-plugins-example/main/{README.md,plugin.json,skills/migrate-agent-plugin/references/validation-checklist.md} | Yes, 200 | "reference example, not a substitute for the normative specification" |
| S1 | Agent Skills Specification | https://agentskills.io/specification.md | **Flaky**: first `curl https://agentskills.io/specification` → `curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to agentskills.io:443`; `specification.md` → `curl: (35) Recv failure: Connection reset by peer`; succeeded on retry (`--retry 4 --retry-all-errors`) | Read in full |
| S2 | agentskills.io best practices | https://agentskills.io/skill-creation/best-practices.md | Yes (with retry) | |
| S3 | agentskills.io optimizing descriptions | https://agentskills.io/skill-creation/optimizing-descriptions.md | Yes (with retry) | |
| S4 | agentskills.io evaluating skills | https://agentskills.io/skill-creation/evaluating-skills.md | Yes (with retry) | |
| S5 | agentskills.io using scripts | https://agentskills.io/skill-creation/using-scripts.md | Yes (with retry) | |
| S6 | agentskills.io client implementation | https://agentskills.io/client-implementation/adding-skills-support.md | Yes (with retry) | grep only (lenient-validation section) |
| S7 | skills-ref reference validator | raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/{README.md,src/skills_ref/validator.py,src/skills_ref/parser.py} | Yes, 200 | raw @ main; "intended for demonstration purposes only" |
| C1 | Anthropic "Skill authoring best practices" | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md | Yes, 200 | Read in full |
| C2 | anthropics/skills skill-creator | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md and `.../scripts/quick_validate.py` | Yes, 200 | raw @ main |
| C3 | anthropics/skills README + template | raw.githubusercontent.com/anthropics/skills/main/{README.md,template/SKILL.md} | Yes, 200 | |
| C4 | Claude Code skills doc | https://code.claude.com/docs/en/skills.md | Yes, 200 | Vendor (client) doc, not a standard |
| C5 | Claude Code plugin evals / plugins reference | https://code.claude.com/docs/en/plugin-evals.md, https://code.claude.com/docs/en/plugins-reference.md | Yes, 200 | Vendor (client) doc, not a standard |
| C6 | "The Complete Guide to Building Skills for Claude" (PDF) | https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf | **BLOCKED**: curl `(56) CONNECT tunnel failed, response 403`; proxy: `resources.anthropic.com:443 — connect_rejected`; WebFetch: `EGRESS_BLOCKED ... Access to resources.anthropic.com is blocked by the network egress proxy.` | Third-party gist copy (gist.github.com/joyrexus/ff71917b4fc0a2cbc84974212da34a4a) also blocked: `CONNECT tunnel failed, response 403`. No vendor copy found. **Not read.** See §6. |

---

## 1. Agent Plugins 1.0.0 — checklist (package-author-relevant first, then client)

Source for every row: A1/A3 (identical). "§" = section of the 1.0.0 spec. Keyword as it appears in the text.

### 1.1 Conformance scope and language
| § | Keyword | Exact sentence |
|---|---|---|
| §1 | MUST | "Clients and plugin packages claiming conformance to Agent Plugins v1 MUST implement or follow the requirements in this document." |
| §2 | — | "the key words MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals." |
| §2 | — | "Appendix A and Design Decisions are non-normative. All other sections are normative." |

### 1.2 Directory layout and package model
| § | Keyword | Exact sentence |
|---|---|---|
| §3 | (def.) | Plugin: "A self-contained directory with a manifest and optional components." Plugin root: "The top-level directory of a plugin package." Manifest: "A `plugin.json` file at the plugin root." |
| §4.1 | — | "A plugin is a directory rooted at a single filesystem location." |
| §4.1 | MUST | "A plugin MUST include a manifest at `plugin.json` in the plugin root." |
| §4.2 | (example) | Standard layout shows `plugin.json`, `skills/<name>/SKILL.md` (+ `scripts/`, `references/`), `mcp.json`, `com.example.client/`, `LICENSE`, `CHANGELOG.md` — "A plugin that has skills, MCP servers, and a client extension can have the following layout". `LICENSE`/`CHANGELOG.md` appear only in this example; no rule requires them. |
| §6.1 | MUST | "Clients MUST discover each supported component type from its fixed location. `plugin.json` cannot override these locations or contain inline component configuration." Fixed locations: Skills → `skills/` ("Subdirectories containing `SKILL.md`"); MCP servers → `mcp.json`. |
| §6.2 | MUST NOT | "If a fixed component location is absent, the client MUST NOT treat that as an error." |
| §6.2 | MUST | "If a fixed component location is present but does not resolve to the expected filesystem kind — for example, `skills` does not resolve to a directory or `mcp.json` does not resolve to a regular file — the client MUST treat that component type as invalid and continue loading other supported component types." |
| §7 | — | "Agent Plugins v1 defines exactly two component types: skills and MCP servers. Other component types are outside the v1 format and do not affect conformance." |
| §7 | MUST | "Clients MUST ignore component types they do not support." |
| A6 build guide | (non-normative) | "Every plugin has a root `plugin.json`; skills and MCP configuration are optional." / "Client-managed installation, distribution, enablement, updates, and user interface are outside the portable specification." |
| A9 example README | (non-normative) | "The directory name and manifest name do not have to match under the portable specification, but keeping them identical is strongly recommended for predictable packaging and discovery." |

### 1.3 Symlinks and containment
| § | Keyword | Exact sentence |
|---|---|---|
| §4.1 | MUST / MAY | "When a client discovers, reads, or executes a file or directory supplied by the plugin package, the filesystem-resolved path MUST remain within the filesystem-resolved plugin root. Symlinks, junctions, reparse points, and equivalent filesystem mechanisms MAY resolve to targets within the plugin root, but clients MUST reject package paths that resolve outside it." |
| §4.1 | MUST | "A configuration field defined by this specification as a plugin-relative path MUST begin with `./`, be resolved against the plugin root, and remain within the filesystem-resolved plugin root after resolution." |
| §4.1 | MUST NOT | "Configuration values not defined as paths, including command arguments and environment variable values, are opaque strings. Clients MUST NOT interpret them as package paths for the purpose of enforcing this section." |
| §4.1 | MUST | "When a path fails a containment requirement, the client MUST apply the narrowest applicable failure boundary:" — "If `plugin.json` does not resolve within the plugin root, the client MUST reject the plugin." / "If a fixed component location does not resolve within the plugin root, the client MUST treat that component type as invalid under §6.2." / "If a discovered `SKILL.md` does not resolve within the plugin root, the client MUST skip that skill under §7.1." / "If an MCP server `command` or `cwd` fails containment, the client MUST treat that server entry as invalid under §7.2.2." / "For any other package path that resolves outside the plugin root, the client MUST deny access to that path." |
| §4.1 | — | "These containment rules govern access to files supplied by the plugin package. They do not sandbox a plugin subprocess or restrict paths supplied at runtime." |

### 1.4 `plugin.json` — object, closed field set, `$schema`
| § | Keyword | Exact sentence |
|---|---|---|
| §5.1 | MUST | "Clients MUST check for a manifest at `plugin.json` in the plugin root." |
| §5.1 | — | "The Agent Plugins core specification defines exactly one portable manifest per plugin. No other file can replace, supplement, or override the core fields in root `plugin.json`." |
| §5.1 | — | "A client loads and validates root `plugin.json` before discovering components or applying client-specific behavior." |
| §5.2 | MUST | "The manifest MUST be JSON and MUST contain a top-level object. Its schema is closed: the only permitted top-level fields are `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and `extensions`." |
| §5.2 | MUST / MUST NOT | "If `plugin.json` contains any other top-level field, it does not conform to the schema. Clients MUST report and ignore each unknown field and MUST continue loading the plugin if the manifest otherwise satisfies this section. Clients MUST NOT assign semantics to unknown fields. Client-specific manifest data belongs under `extensions` as defined in §8." |
| §5.2 | MUST | "Every permitted field otherwise MUST match the type and constraints defined below. Any schema violation other than an unknown top-level field or a non-object `extensions` field is fatal: the client MUST reject the plugin and MUST NOT discover or execute any of its components." |
| §5.2 | — | "The official machine-readable schema is `schemas/1.0.0/plugin.schema.json`. The specification text is authoritative if it conflicts with the schema." |
| §5.2 | MUST | "The required `$schema` field identifies the Agent Plugins specification version targeted by the plugin and its corresponding manifest schema. For Agent Plugins 1.0.0, its value MUST be the canonical identifier `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`." |
| §5.2 | MUST / MAY / MUST NOT / SHOULD | "Clients MUST use a recognized `$schema` value to select locally supported manifest validation and interpretation rules. A client MAY map multiple canonical identifiers to the same implementation only when it explicitly recognizes those Agent Plugins versions as compatible. Clients MUST NOT retrieve a schema while loading a plugin. If a client does not support the declared Agent Plugins version or an explicitly recognized compatible version, it MUST reject the plugin and SHOULD report the unsupported version." |
| A4 schema | (machine) | `"required": ["$schema", "name"]`, `"additionalProperties": false`, `$schema` is `"const": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"`. |

### 1.5 `plugin.json` — required fields (`$schema`, `name`) and name rules
| § | Keyword | Exact sentence |
|---|---|---|
| §5.3 | MUST / MUST NOT / SHOULD | "If a required field is missing, has the wrong type, is empty, or otherwise violates its requirements, the manifest is invalid. Clients MUST reject the plugin and MUST NOT discover or execute any of its components. Clients SHOULD report which required field is invalid." |
| §5.3 | — | `name`: "Human-readable plugin name." (A6 manifest guide: "Human-readable plugin name and package identifier.") |
| §5.5 | MUST | "The manifest `name` value MUST satisfy all of the following:" Length "The name MUST be between 1 and 64 characters inclusive."; Character set "Lowercase alphanumeric characters, hyphens, and periods only."; Start and end "The first and last characters MUST be alphanumeric."; Repetition "Consecutive hyphens and consecutive periods are not allowed." |
| §5.5 | — | "Periods are allowed in plugin names." Valid: `my-plugin`, `acme.tools`, `lint3r`, `a`. Invalid: `My-Plugin`, `-start`, `has--double`, `too.many..dots`, empty. |
| A4 schema | (machine) | `"minLength": 1, "maxLength": 64, "pattern": "^(?!.*(?:--|\\.\\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"` |

### 1.6 `plugin.json` — optional metadata fields
| § | Keyword | Exact sentence / table row |
|---|---|---|
| §5.4 | RECOMMENDED | `version` string — "Version string (Semantic Versioning RECOMMENDED). Used for update checks and cache freshness." |
| §5.4 | — | `description` string — "Short description of plugin purpose." |
| §5.4 | MAY | `author` object — "Author object with optional `name`, `email`, and `url` string fields." / "The `author` object MAY contain only the `name`, `email`, and `url` fields, each with a string value. Any other field or value type makes the manifest invalid." |
| §5.4 | — | `homepage` string — "Documentation or homepage URL." |
| §5.4 | — | `repository` string — "Source repository URL." (a **string**, not an object; schema `"repository": {"type": "string"}`) |
| §5.4 | RECOMMENDED | `license` string — "License identifier (SPDX identifier RECOMMENDED)." |
| §5.4 | — | `keywords` string[] — "Search and discovery tags." |
| §5.4 | MUST NOT | "Except where this specification states an explicit constraint, metadata fields are validated only by their JSON types. Clients MUST NOT reject a manifest solely because `version` is not valid Semantic Versioning; `homepage`, `repository`, or `author.url` is not a recognized URL; `author.email` is not a recognized email address; or `license` is not an SPDX identifier." |
| §5.6 / §8.1 | MUST | "The optional `extensions` field in `plugin.json` MUST be an object whose member names are client extension namespaces and whose member values are objects." |
| §8.1 | MUST | "If `extensions` is not an object, the client MUST report and ignore the field and continue loading components. A client MUST ignore manifest entries for namespaces it does not implement without validating the contents of their values." |

No field in the spec is named `displayName`, `skills`, `mcpServers`, `hooks`, `agents`, `commands`, `category`, `tags`, etc.; A9 example README: "Do not add `hooks`, `agents`, `commands`, `mcpServers`, `lspServers`, or arbitrary client fields at its top level."

### 1.7 Client extensions
| § | Keyword | Exact sentence |
|---|---|---|
| §8 | MUST / MAY | "Client-specific manifest data MUST be represented under a reverse-domain namespace in `extensions`. Client-specific files MUST be represented under a top-level directory named for that namespace. A client MAY use either representation or both." |
| §8 | SHOULD | "A client SHOULD base its namespace on a domain name it controls and SHOULD keep the namespace stable." |
| §8 | — | "Agent Plugins assigns no portable discovery, validation, loading, or failure semantics to client extension data or files." |
| §8.2 | MUST | "A client that implements file-based behavior for a namespace MUST look for it in the corresponding top-level directory." |

### 1.8 Skills inside a plugin
| § | Keyword | Exact sentence |
|---|---|---|
| §7.1 | MUST | "Agent Skills MUST conform to the Agent Skills specification. That specification is the source of truth for the `SKILL.md` format, frontmatter fields, and directory layout (`scripts/`, `references/`, `assets/`)." |
| §7.1 | — | "This specification defines how Agent Skills are discovered within a plugin, not the skill format itself or how clients expose skills to users or models." |
| §7.1 | MUST NOT | "The fixed discovery location is `skills/`. Each immediate child directory containing a path named exactly `SKILL.md` that resolves to a regular file is treated as one skill. Clients MUST NOT recursively search deeper descendants for additional skills." |
| §7.1 | MUST / SHOULD | "If a discovered skill does not conform to the Agent Skills specification, the client MUST skip that skill and continue loading other skills and component types. The client SHOULD report the invalid skill." |
| A6 skills guide | (non-normative) | "`scripts/`, `references/`, and `assets/` are common conventions described by Agent Skills, not an exhaustive allowlist." Example layout also shows `examples/`. |

### 1.9 `mcp.json` (only if the package ships MCP servers)
| § | Keyword | Exact sentence |
|---|---|---|
| §7.2.1 | MUST NOT | "The MCP configuration path is `mcp.json` at the plugin root. MCP configuration MUST NOT be declared inline in `plugin.json` or loaded from any alternative core path." |
| §7.2.1 | MUST | "`mcp.json` MUST be a JSON object containing the required `$schema` and `mcpServers` fields, with no other top-level fields. `mcpServers` MUST be an object whose member names identify servers and whose member values are server configuration objects. An empty `mcpServers` object is valid." |
| §7.2.1 | MUST | "For Agent Plugins 1.0.0, its value MUST be the canonical identifier `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`." |
| §7.2.1 | MUST | "Each server configuration MUST contain a `type` field and match exactly one of the closed variants below. An unknown field, an unknown `type` value, or a field belonging to another variant makes that server entry invalid." (stdio: `type`,`command` req.; `args`,`env`,`cwd` opt. — streamable-http/sse: `type`,`url` req.; `headers` opt.) |
| §7.2.1 | MUST | "The `command` field MUST contain a single executable token, not a shell command string. It MUST be either a bare executable name or a plugin-relative path beginning with `./`." |
| §7.2.1 | MUST NOT / MUST | "Plugins claiming conformance MUST NOT depend on that behavior [configured PATH]. A plugin that bundles an executable in the package MUST use a plugin-relative `command`." |
| §7.2.1 | MUST | `cwd` "MUST have one of these forms: A plugin-relative path beginning with `./`. Exactly `${PLUGIN_ROOT}` or a path beginning with `${PLUGIN_ROOT}/`. Exactly `${PLUGIN_DATA}` or a path beginning with `${PLUGIN_DATA}/`." |
| §7.2.1 | MUST / MUST NOT | "The `url` value MUST be an absolute HTTP or HTTPS URL and MUST NOT contain user information or a fragment. Non-loopback endpoints MUST use HTTPS." |
| §7.2.1 | MUST NOT | "Header values are visible package data, not a portable secret mechanism. Plugins MUST NOT embed credentials or other secrets in `headers`." |
| §9.1 | MUST NOT | "Except for the platform executable search used to resolve a bare `command`, plugins claiming conformance MUST NOT depend on a base-environment variable unless this specification requires that variable or the server configuration supplies it explicitly." |
| §9.2 | MUST NOT | "Plugins MUST NOT embed credentials or other secrets in `env`." / "An MCP server's `env` object MUST NOT contain entries named `PLUGIN_ROOT` or `PLUGIN_DATA`." |
| §10.1 | MUST | "When `mcp.json` is present, the version in its `$schema` value MUST match the version declared by `plugin.json`. A mismatch makes the MCP configuration invalid under §7.2.2 but does not invalidate other component types." |
| §9.1 | (guidance) | "Use `PLUGIN_DATA` for: installed dependencies (node_modules, virtual environments), generated code, caches, and other plugin state that should persist across updates. Use `PLUGIN_ROOT` for referencing bundled scripts, binaries, and config files that ship with the plugin." |

### 1.10 Versioning
| § | Keyword | Exact sentence |
|---|---|---|
| §10.1 | MUST | "Every specification release MUST publish both schemas with the same version as the specification, even when a schema's validation rules are unchanged from the previous release." |
| §10.1 | MUST NOT / MAY | "Published canonical schema identifiers MUST NOT be reassigned to different schema contents. Existing plugins MAY continue targeting an older Agent Plugins version; clients determine support using the declared canonical identifiers and any explicit compatibility mappings." |
| §10.2 | SHOULD | "Plugins SHOULD use Semantic Versioning for `version`." (Major = "Incompatible behavior or schema change."; Minor = "New behavior without breaking existing clients or users."; Patch = "Corrective change without intended behavioral break.") |
| §10.2 | MAY | "Clients MAY use `version` to determine whether updates are available and whether caches are stale." |
| A8 | (status) | README: "Agent Plugins Specification 1.0.0 is the current published release. Agent Plugins Specification 1.1.0 is a working draft." |

### 1.11 Marketplaces / repositories of plugins — what the standard says
- The 1.0.0 spec text contains **no** normative statement about marketplaces, catalogues, registries or multi-plugin repositories. The word "marketplace" does not occur in A1; "registry" occurs only in Design Decisions ("rather than archive formats (`.zip`, `.tar.gz`) or registry-fetched bundles") and ("without requiring a central client-name registry").
- A7 "Implement an Agent Plugins client" — "Agent Plugins defines package structure, validation, discovery, MCP configuration, plugin variables, and failure isolation. It does not prescribe: installation sources, registries, or marketplaces; enablement, update, or cache user experience; permission prompts, trust policy, or sandboxing; how skills are shown to users or models; internal client-extension behavior".
- A6 build guide: "Client-managed installation, distribution, enablement, updates, and user interface are outside the portable specification."
- Landing page (A7 dump): "distribution, installation, permissions, user experience, and client-specific capabilities remain under each client's control."
- A9 example README (non-normative, migration advice): "Keep hooks, agents, commands, LSP, UI, and marketplace metadata in a client extension or a separate compatibility package required by that platform." A9 checklist: "Hooks, agents, commands, LSP, UI, and marketplace metadata are not presented as portable v1 components." / "Portable and legacy manifests are generated from one metadata source where practical."
- FUTURE_CONSIDERATIONS (non-normative): "Organization-scoped plugin registries with approval workflows" listed under possible future "Enterprise controls"; also "No test harness or validation tool is specified. A future version may define: ... A standard plugin linter or validator command".
- Consequence for a reviewer: a marketplace index file (e.g. a vendor's `marketplace.json`) is judged by that vendor's docs, never by Agent Plugins 1.0.0.

### 1.12 What a conformant client does (§11)
| § | Keyword | Exact sentence |
|---|---|---|
| §11.1 | MUST | "A conformant client MUST satisfy all applicable requirements in sections 1–10. At minimum, it:" — "Can load a plugin from a directory path." / "Selects a locally supported plugin manifest schema from `$schema`, then parses and validates the closed `plugin.json` schema using the non-fatal exceptions in §5.2 and §8.1." / "Ignores unimplemented members of `extensions` without validating the contents of their values." / "For each component type it supports, discovers components in its fixed location." / "If it supports MCP servers, selects a locally supported MCP configuration schema from `$schema` and supports at least one of the `stdio` or `streamable-http` variants in `mcp.json`." / "If the client launches plugin subprocesses (i.e., stdio MCP servers), provides `PLUGIN_ROOT` and `PLUGIN_DATA` and expands both variables in runtime configuration values (`args`, `env`, `cwd`)." / "For stdio MCP servers, resolves `command` as a single executable token and uses the plugin root as the default subprocess working directory." / "Supports at least one component type (skills or MCP servers)." |
| §11.2 | — | "A client is not required to support every component type. For example, a skills-only client can conform without supporting MCP servers, provided it satisfies all applicable requirements." |
| §11.3 | MUST / MUST NOT | "Clients MUST ignore unsupported component types." / "Any other `plugin.json` schema violation is fatal to the plugin: the client MUST reject the plugin and MUST NOT discover or execute any of its components." / "A failure isolated to a component type, component entry, or component process MUST NOT prevent the client from loading independently valid components." |
| §11.3 | SHOULD / MAY | "Clients SHOULD report invalid configuration and component failures. Clients MAY report partially unsupported plugins, but lack of support for a component type, MCP transport, or client extension is not itself an error." |
| §7.2.1 | MUST / SHOULD / OPTIONAL | "A client that supports Agent Plugins MCP servers MUST support at least one of `stdio` or `streamable-http` and SHOULD support both. Support for `sse` is OPTIONAL." |

---

## 2. Agent Skills specification — checklist (S1, https://agentskills.io/specification.md)

The spec uses lowercase "must/should/recommend" (it has no RFC 2119 clause). Quoted as written.

### 2.1 Directory and file
- "A skill is a directory containing, at minimum, a `SKILL.md` file" (layout: `SKILL.md` "Required: metadata + instructions"; `scripts/` "Optional: executable code"; `references/` "Optional: documentation"; `assets/` "Optional: templates, resources"; "Any additional files or directories").
- "The `SKILL.md` file must contain YAML frontmatter followed by Markdown content."

### 2.2 Front-matter fields (complete list in the spec)
| Field | Required | Constraint as stated |
|---|---|---|
| `name` | Yes | "Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen." |
| `description` | Yes | "Max 1024 characters. Non-empty. Describes what the skill does and when to use it." |
| `license` | No | "License name or reference to a bundled license file." — "We recommend keeping it short (either the name of a license or the name of a bundled license file)" |
| `compatibility` | No | "Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.)." — "Must be 1-500 characters if provided"; "Should only be included if your skill has specific environment requirements"; note: "Most skills do not need the `compatibility` field." |
| `metadata` | No | "Arbitrary key-value mapping for additional metadata (a map from string keys to string values)." — "We recommend making your key names reasonably unique to avoid accidental conflicts" |
| `allowed-tools` | No | "Space-separated string of pre-approved tools the skill may use. (Experimental)" — "Support for this field may vary between agent implementations" |

**`name` rules (verbatim bullets):** "Must be 1-64 characters" / "May only contain unicode lowercase alphanumeric characters (`a-z`, `0-9`) and hyphens (`-`)" / "Must not start or end with a hyphen (`-`)" / "Must not contain consecutive hyphens (`--`)" / "Must match the parent directory name". Note: **periods are NOT allowed** in a skill name (they are in a plugin name, §1.5).

**`description` rules (verbatim bullets):** "Must be 1-1024 characters" / "Should describe both what the skill does and when to use it" / "Should include specific keywords that help agents identify relevant tasks". Good example: "Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction." Poor example: "Helps with PDFs."

**Unknown front-matter keys:** the spec text does not say in words that other keys are forbidden, but its reference validator (S7 `validator.py`) defines `ALLOWED_FIELDS = {"name","description","license","allowed-tools","metadata","compatibility"}` and errors with "Unexpected fields in frontmatter: ...". Anthropic's `quick_validate.py` (C2) does the same, and C4 says upload/packaging "fails with a hard error instead of ignoring the field".

### 2.3 Body
- "The Markdown body after the frontmatter contains the skill instructions. There are no format restrictions. Write whatever helps agents perform the task effectively."
- "Recommended sections: Step-by-step instructions / Examples of inputs and outputs / Common edge cases"
- "Note that the agent will load this entire file once it's decided to activate a skill. Consider splitting longer `SKILL.md` content into referenced files."

### 2.4 Progressive disclosure and size
- "1. **Metadata** (~100 tokens): The `name` and `description` fields are loaded at startup for all skills 2. **Instructions** (< 5000 tokens recommended): The full `SKILL.md` body is loaded when the skill is activated 3. **Resources** (as needed)"
- "Keep your main `SKILL.md` under 500 lines. Move detailed reference material to separate files."

### 2.5 Optional directories
- "A skill directory may contain any files and directories beyond the required `SKILL.md`. The conventions below are recommendations for organizing common types of content."
- `scripts/`: "Scripts should: Be self-contained or clearly document dependencies / Include helpful error messages / Handle edge cases gracefully"
- `references/`: "Keep individual reference files focused. Agents load these on demand, so smaller files mean less use of context."
- `assets/`: "Templates ... Images ... Data files"

### 2.6 File references
- "When referencing other files in your skill, use relative paths from the skill root"
- "Keep file references one level deep from `SKILL.md`. Avoid deeply nested reference chains."

### 2.7 Validation tooling
- "Use the skills-ref reference library to validate your skills: `skills-ref validate ./my-skill` — This checks that your `SKILL.md` frontmatter is valid and follows all naming conventions."
- S7 README caveat: "This library is intended for demonstration purposes only. It is not meant to be used in production."
- S7 behaviour (source, raw @ main): NFKC-normalises the name; checks lowercase, no leading/trailing hyphen, no `--`, chars `isalnum() or '-'` (so accepts Unicode letters — looser than the spec's "`a-z`, `0-9`" wording); requires directory name == name; description non-empty and ≤1024; compatibility ≤500; closed key set; `find_skill_md` "Prefers SKILL.md (uppercase) but accepts skill.md (lowercase)" (Agent Plugins §7.1 requires "a path named exactly `SKILL.md`"); parses with `strictyaml`.

### 2.8 Client leniency (why authors cannot rely on the client to catch errors) — S6
- "Warn on issues but still load the skill when possible: Name doesn't match the parent directory name → warn, load anyway / Name exceeds 64 characters → warn, load anyway / Description is missing or empty → skip the skill ... / YAML is completely unparseable → skip the skill, log the error"
- "The specification defines strict constraints on the `name` field ... The lenient approach above deliberately relaxes these to improve compatibility with skills authored for other clients."

---

## 3. agentskills.io authoring guidance (open-standard site, non-normative)

### 3.1 Best practices — S2 https://agentskills.io/skill-creation/best-practices.md
- Ground in real expertise: "A common pitfall in skill creation is asking an LLM to generate a skill without providing domain-specific context ... The result is vague, generic procedures ("handle errors appropriately," "follow best practices for authentication")".
- "Run the skill against real tasks, then feed the results — all of them, not just failures — back into the creation process."
- "Focus on what the agent *wouldn't* know without your skill" / "Ask yourself about each piece of content: "Would the agent get this wrong without this instruction?" If the answer is no, cut it."
- Scope: "Skills scoped too narrowly force multiple skills to load for a single task ... Skills scoped too broadly become hard to activate precisely."
- "Concise, stepwise guidance with a working example tends to outperform exhaustive documentation."
- "The specification recommends keeping `SKILL.md` under 500 lines and 5,000 tokens"; "The key is telling the agent *when* to load each file. "Read `references/api-errors.md` if the API returns a non-200 status code" is more useful than a generic "see references/ for details.""
- "Match the specificity of your instructions to the fragility of the task." / "Provide defaults, not menus" / "Favor procedures over declarations".
- Gotchas: "The highest-value content in many skills is a list of gotchas — environment-specific facts that defy reasonable assumptions." / "Keep gotchas in `SKILL.md` where the agent reads them before encountering the situation."
- Templates: "When you need the agent to produce output in a specific format, provide a template."; long templates → `assets/`.
- Checklists, validation loops, plan-validate-execute; "Bundling reusable scripts" when "the agent independently reinventing the same logic each run".

### 3.2 Optimizing descriptions — S3
- "The `description` field in your `SKILL.md` frontmatter is the primary mechanism agents use to decide whether to load a skill" / "the description carries the entire burden of triggering."
- "**Use imperative phrasing.** Frame the description as an instruction to the agent: "Use this skill when..." rather than "This skill does...""
- "**Focus on user intent, not implementation.**"
- "**Err on the side of being pushy.** Explicitly list contexts where the skill applies, including cases where the user doesn't name the domain directly"
- "**Keep it concise.** A few sentences to a short paragraph is usually right ... The specification enforces a hard limit of 1024 characters."
- Trigger evals: "Aim for about 20 queries: 8-10 that should trigger and 8-10 that shouldn't." / near-miss negatives are "the most valuable" / run each "3" times, threshold "0.5 is a reasonable default" / train ~60%, validation ~40% / "Avoid adding specific keywords from failed queries — that's overfitting." / "Five iterations is usually enough."
- If false-triggering: "Add specificity about what the skill does *not* do, or clarify the boundary between this skill and adjacent capabilities."

### 3.3 Evaluating output quality — S4
- "Store test cases in `evals/evals.json` inside your skill directory"; "Start with 2-3 test cases."; "Cover edge cases."
- "run each test case twice: once **with the skill** and once **without it** (or with a previous version)".
- "Each eval run should start with a clean context".
- Assertions: good = "programmatically verifiable", "specific and observable", "countable"; weak = "too vague" or "too brittle".
- "**Require concrete evidence for a PASS.**"; "Remove or replace assertions that always pass in both configurations."
- Iteration guidance: "**Generalize from feedback.**" / "**Keep the skill lean.**" / "**Explain the why.** Reasoning-based instructions ("Do X because Y tends to cause Z") work better than rigid directives ("ALWAYS do X, NEVER do Y")." / "**Bundle repeated work.**"

### 3.4 Scripts — S5
- One-off commands: "**Pin versions**" / "**State prerequisites** in your `SKILL.md` ... For runtime-level requirements, use the `compatibility` frontmatter field." / "**Move complex commands into scripts.**"
- "Use **relative paths from the skill directory root** to reference bundled files." / "List available scripts in your `SKILL.md` so the agent knows they exist".
- "Avoid interactive prompts — This is a hard requirement of the agent execution environment."
- "`--help` output is the primary way an agent learns your script's interface."; "Write helpful error messages"; "Use structured output"; "send structured data to stdout and ... diagnostics to stderr"; idempotency, dry-run, meaningful exit codes, safe defaults, "Predictable output size".

---

## 4. Anthropic's skill-authoring guidance (vendor docs)

### 4.1 "Skill authoring best practices" — C1 https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
Concise
- "The context window is a public good." / "**Default assumption:** Claude is already very smart — Only add context Claude doesn't already have." / "Does this paragraph justify its token cost?"

Degrees of freedom
- "Match the level of specificity to the task's fragility and variability." High freedom (text) / Medium (pseudocode or parameterised scripts) / Low ("specific scripts, few or no parameters") — "Narrow bridge with cliffs on both sides ... Open field with no hazards".

Models
- "Test your Skill with all the models you plan to use it with."

Front matter (Anthropic surface constraints)
- `name`: "Maximum 64 characters / Must contain only lowercase letters, numbers, and hyphens / Cannot contain XML tags / Cannot contain reserved words: "anthropic", "claude""
- `description`: "Must be non-empty / Maximum 1,024 characters / Cannot contain XML tags / Should describe what the Skill does and when to use it"

Naming
- "Consider using **gerund form** (verb + -ing) for Skill names"; acceptable: noun phrases, action-oriented; "**Avoid:** Vague names: `helper`, `utils`, `tools` / Overly generic: `documents`, `data`, `files` / Reserved words ... / Inconsistent patterns within your skill collection".

Description
- "**Always write in third person**. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems. Good: "Processes Excel files and generates reports" Avoid: "I can help you process Excel files" Avoid: "You can use this to process Excel files""
- "**Be specific and include key terms**. Include both what the Skill does and specific triggers/contexts for when to use it."
- "Claude uses it to choose the right Skill from potentially 100+ available Skills."
- Avoid: "Helps with documents", "Processes data", "Does stuff with files".

Progressive disclosure / structure
- "SKILL.md serves as an overview that points Claude to detailed materials as needed, like a table of contents"
- "Keep SKILL.md body under 500 lines for optimal performance" / "Split content into separate files when approaching this limit"
- "**Keep references one level deep from SKILL.md**. All reference files should link directly from SKILL.md to ensure Claude reads complete files when needed."
- "For reference files longer than 100 lines, include a table of contents at the top."

Workflows / feedback
- "Break complex operations into clear, sequential steps. For particularly complex workflows, provide a checklist that Claude can copy into its response"
- "**Common pattern:** Run validator → fix errors → repeat"

Content
- "Avoid time-sensitive information" (use an "Old patterns" section).
- "Use consistent terminology — Choose one term and use it throughout the Skill".
- Template pattern ("Match the level of strictness to your needs"); Examples pattern ("provide input/output pairs"); Conditional workflow pattern.

Evaluation
- "**Create evaluations BEFORE writing extensive documentation.**" / "Build three scenarios that test these gaps" / "Establish baseline" / "Write minimal instructions".
- "There is not currently a built-in way to run these evaluations." (C1's note; C4/C5 now document `claude plugin eval` for Claude Code — the two statements are about different surfaces/dates.)
- Claude A / Claude B iteration; observe "Unexpected exploration paths", "Missed connections", "Overreliance on certain sections", "Ignored content: If Claude never accesses a bundled file, it might be unnecessary or poorly signaled".

Anti-patterns
- "Always use forward slashes in file paths, even on Windows"; "Avoid offering too many options".

Code
- "Solve, don't defer" — handle errors in scripts; no "voodoo constants" ("Configuration parameters should also be justified and documented").
- "Make clear in your instructions whether Claude should: **Execute the script** ... **Read it as reference**".
- "Name files descriptively: Use names that indicate content: `form_validation_rules.md`, not `doc2.md`"; "Organize for discovery: Structure directories by domain or feature".
- "If your Skill uses MCP ... tools, always use fully qualified tool names" (`ServerName:tool_name`).
- "Avoid assuming tools are installed"; "List required packages in your SKILL.md".

Checklist (verbatim headings): **Core quality** — "Description is specific and includes key terms / Description includes both what the Skill does and when to use it / SKILL.md body is under 500 lines / Additional details are in separate files (if needed) / No time-sensitive information (or in "old patterns" section) / Consistent terminology throughout / Examples are concrete, not abstract / File references are one level deep / Progressive disclosure used appropriately / Workflows have clear steps". **Code and scripts** — "Scripts solve problems rather than defer to Claude / Error handling is explicit and helpful / No "voodoo constants" (all values justified) / Required packages listed in instructions and verified as available / Scripts have clear documentation / No Windows-style paths (all forward slashes) / Validation/verification steps for critical operations / Feedback loops included for quality-critical tasks". **Testing** — "At least three evaluations created / Tested with Haiku, Sonnet, and Opus / Tested with real usage scenarios / Team feedback incorporated (if applicable)".

### 4.2 skill-creator (anthropics/skills, raw @ main) — C2
- description: "This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body." / "Claude has a tendency to "undertrigger" skills ... please make the skill descriptions a little bit "pushy"."
- Progressive disclosure: "Metadata (name + description) - Always in context (~100 words)"; "SKILL.md body ... (<500 lines ideal)"; "Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers"; "Reference files clearly from SKILL.md with guidance on when to read them"; "For large reference files (>300 lines), include a table of contents" (C1 says >100 lines — see §5).
- "Principle of Lack of Surprise: ... A skill's contents should not surprise the user in their intent if described."
- "Prefer using the imperative form in instructions."
- Writing style: "Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs." / "If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag".
- Improvement: "**Generalize from the feedback.**" / "**Keep the prompt lean.** Remove things that aren't pulling their weight." / "**Explain the why.**"
- Tests: "come up with 2-3 realistic test prompts"; "Save test cases to `evals/evals.json`"; run with-skill and baseline in the same turn.
- `scripts/quick_validate.py`: `ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}`; name `^[a-z0-9-]+$`, no leading/trailing/double hyphen, ≤64; description string, "cannot contain angle brackets (< or >)", ≤1024; compatibility ≤500.
- The current `main` SKILL.md contains no rule about README.md inside a skill (grep for `readme|changelog|extraneous|auxiliary` found none).

### 4.3 Claude Code docs (client-specific; cited only for tooling and a hard limit) — C4, C5
- C4: "the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing" and "Put the key use case first".
- C4: "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files."
- C4: "Outside Claude Code, you can use only the fields in the Agent Skills spec" — "If you include any field the spec doesn't allow, packaging or upload fails with a hard error instead of ignoring the field".
- C4: "Run `/skill-doctor` to see what each of your skills costs and how often it gets used" ("requires Claude Code v2.1.252 or later").
- C4/C5: "`claude plugin eval` runs each prompt in an isolated session with and without the plugin, scores it with graders ..., and exits non-zero below a threshold so you can gate CI on it." (C5: "Claude Code v2.1.269 or later"; "each case runs three times by default"; "A case passes when its score meets the `--threshold`, `1.0` by default"; "If a case scores 1.0 both with and without the plugin, the plugin isn't what made it pass.")
- C5 requirements line: "A plugin directory with a `plugin.json` or `.claude-plugin/plugin.json` manifest" (plugin-evals page). The plugins-reference page still documents "The `.claude-plugin/plugin.json` file" as the manifest. Not investigated further — client behaviour, out of scope here.
- C5: `claude plugin validate <path> [--strict] [--json]` — "exits 0 when validation passes, 1 when it fails, and 2 when the validation run itself fails".

---

## 5. Tensions between sources (a reviewer must not flag one side as "wrong")

1. **Description voice.** S3 (agentskills.io): "Use imperative phrasing ... "Use this skill when..." rather than "This skill does..."". C1 (Anthropic): "Always write in third person" with good example "Processes Excel files and generates reports", and its own examples end "Use when ...". Both agree the description must say *what* and *when*; they differ on grammatical voice. The spec (S1) itself only says "Should describe both what the skill does and when to use it".
2. **TOC threshold.** C1: reference files ">100 lines" get a TOC; C2 skill-creator: ">300 lines".
3. **Rigid MUSTs.** C1 lists "using stronger language such as "MUST filter"" as one possible refinement; C2 and S4 say reasoning beats "ALWAYS/NEVER".
4. **Skill-name character set.** S1: "`a-z`, `0-9`" and hyphens; S7 reference validator accepts any Unicode alphanumerics after NFKC. Anthropic surfaces add "no XML tags" and reserved words "anthropic", "claude" (C1); `quick_validate.py` bans `<`/`>` in descriptions.
5. **Plugin name vs skill name.** Agent Plugins `name` allows periods (§5.5); Agent Skills `name` does not.
6. **Budget.** S1: "< 5000 tokens recommended" and "under 500 lines"; C2: metadata "~100 words" vs S1 "~100 tokens"; C4 listing cap 1,536 chars (Claude Code only) vs spec hard limit 1,024 chars for `description`.

---

## 6. Not verified / not read

- **"The Complete Guide to Building Skills for Claude" (Anthropic PDF)** — blocked (resources.anthropic.com CONNECT 403 / EGRESS_BLOCKED), third-party gist copy also blocked. Search-engine snippets attribute to it: kebab-case folder names, `SKILL.md` exact-case ("skill.md ... silently ignored"), and "Don't include README.md inside your skill folder." **These are NOT verified against the primary text and must not be cited as Anthropic rules** until read. No rubric item below rests on them.
- No commit SHAs for any GitHub-hosted source (github.com and api.github.com returned 403 for these repos in this session).
- The platform.claude.com "Skills overview" page (linked from C1 for "complete structure details") was not read; C1's own constraints were used instead.

---

## 7. Quality rubric derived from the standards

Each criterion is checkable by reading the package; the tag names the source (AP = Agent Plugins 1.0.0 §; AS = Agent Skills spec S1; ASx = agentskills.io guides S2–S6; SR = skills-ref S7; AN = Anthropic C1/C2; CC = Claude Code docs C4/C5). "Hard" = conformance failure; "Quality" = recommendation.

**Package / manifest**
1. **Hard** — `plugin.json` is a regular file at the plugin root, is a JSON object, and is the only core manifest (no second copy supplementing it). [AP §4.1, §5.1, §5.2]
2. **Hard** — `$schema` equals exactly `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`. [AP §5.2; A4 `const`]
3. **Hard** — `name` present, 1–64 chars, `[a-z0-9.-]`, alphanumeric first/last, no `--`/`..`. [AP §5.5; A4 pattern]
4. **Hard** — no top-level keys beyond the ten permitted; client data only under `extensions.<reverse-domain>` with object values. (Unknown key = schema non-conformance even though clients merely report it.) [AP §5.2, §8.1]
5. **Hard** — `author` has only `name`/`email`/`url` strings; `repository`, `homepage`, `license`, `version`, `description` are strings; `keywords` is a string array. [AP §5.4; A4]
6. **Quality** — `version` is SemVer; `license` is an SPDX identifier. [AP §5.4 RECOMMENDED, §10.2 SHOULD]
7. **Quality** — `description`, `license`, `repository`/`homepage`, `keywords` present and accurate (optional in the spec, but they are the only portable discovery metadata). [AP §5.4 field purposes; A9 example fills them]
8. **Quality** — plugin directory name equals manifest `name`. [A9 example README: "strongly recommended"] (non-normative)

**Layout / containment**
9. **Hard** — every file and every symlink inside the package resolves inside the plugin root; plugin-relative config paths start with `./`. [AP §4.1]
10. **Hard** — skills live only as immediate children of `skills/`, each with a file named exactly `SKILL.md` resolving to a regular file; nothing relies on deeper nesting. [AP §6.1, §7.1]
11. **Hard** — no component declared inline in `plugin.json`; no non-portable component (hooks/agents/commands/LSP/marketplace metadata) presented as portable — such things live under a reverse-domain extension directory or a separate vendor package. [AP §6.1, §7, §8; A9]
12. **Hard (if present)** — `mcp.json` at root, `$schema` = 1.0.0 MCP id matching `plugin.json`'s version, only `$schema`+`mcpServers`, each server a closed variant; `command` one token (`./` for bundled executables); remote URLs HTTPS; no secrets in `env`/`headers`; no `PLUGIN_ROOT`/`PLUGIN_DATA` keys in `env`. [AP §7.2.1, §9.2, §10.1]

**Skill front matter**
13. **Hard** — front matter is valid YAML delimited by `---`, uses only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. [AS; SR `ALLOWED_FIELDS`; AN `quick_validate.py`; CC hard error on upload]
14. **Hard** — skill `name` 1–64, lowercase `a-z0-9-`, no leading/trailing/double hyphen, **no periods**, equals its directory name. [AS `name` field]
15. **Hard** — `description` non-empty, ≤1024 chars; `compatibility`, if present, 1–500 chars; `metadata` string→string. [AS] (Anthropic surfaces additionally: no `<`/`>`, no "anthropic"/"claude" in name [AN C1, C2].)
16. **Quality** — `description` states both *what* the skill does and *when* to use it, with concrete trigger keywords a user would say; not vague ("Helps with X"). [AS; AN C1; ASx S3]
17. **Quality** — description voice is consistent across the package's skills (either the third-person "Does X. Use when …" of AN C1 or the imperative "Use this skill when …" of ASx S3 — flag inconsistency, not either choice); key use case first. [AN C1; ASx S3; CC 1,536 cap]
18. **Quality** — "when to use" information lives in the description, not only in the body. [AN C2]
19. **Quality** — `compatibility` used only when the skill truly has environment requirements (e.g. a bundled binary, network access), and then used. [AS; ASx S5]

**Skill body**
20. **Quality** — `SKILL.md` body under 500 lines and ~5,000 tokens; longer material moved to `references/`/`assets/`. [AS; AN C1; ASx S2]
21. **Quality** — every bundled file is referenced from `SKILL.md`, one level deep, with a stated *when to read it* ("Read X if …"); no orphan files, no chains of references. [AS; AN C1 "Ignored content"; ASx S2]
22. **Quality** — reference files >100 lines (C1) / >300 lines (C2) start with a table of contents. [AN]
23. **Quality** — body contains only what the agent would not know: no explanations of general concepts, no marketing, no restated description; includes concrete gotchas and at least one concrete example / input–output pair. [ASx S2; AN C1 "Concise is key", "Examples are concrete"]
24. **Quality** — one default per decision, not a menu of tools; specificity matched to fragility (exact commands for fragile ops). [AN C1; ASx S2]
25. **Quality** — consistent terminology within the skill and across README/manifest/skill (one name per thing). [AN C1]
26. **Quality** — no time-sensitive statements ("before August 2025 …") outside an "old patterns" section. [AN C1]
27. **Quality** — forward-slash, skill-root-relative paths; scripts listed in `SKILL.md` with execute-vs-read intent stated. [AS; AN C1; ASx S5]
28. **Quality (if scripts)** — non-interactive, `--help`, helpful errors, structured stdout / diagnostics on stderr, pinned dependency versions, prerequisites stated, no unexplained constants. [AS scripts bullets; ASx S5; AN C1]
29. **Quality** — reasoning given for constraints rather than bare ALWAYS/NEVER; the skill's behaviour would not surprise a user reading its description. [AN C2; ASx S4]

**Validation / evaluation**
30. **Quality** — evidence the package is validated mechanically (e.g. `skills-ref validate` per skill, a manifest schema check) and, ideally, behaviourally: ≥3 eval cases with a no-skill baseline and trigger tests including near-miss negatives. [AS "Validation"; AN C1 "At least three evaluations"; ASx S3/S4; CC `claude plugin eval`] — note: the Agent Plugins spec itself defines no validator (FUTURE_CONSIDERATIONS), so this is a quality signal, not a conformance requirement.
