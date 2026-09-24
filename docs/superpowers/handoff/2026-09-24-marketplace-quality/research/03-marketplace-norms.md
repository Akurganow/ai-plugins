# 03 — Marketplace and plugin-ecosystem quality norms (clean-room)

Research run: 2026-09-24, fetches between 18:53Z and 19:01Z. Clean-room: nothing under the
local repository was read; git was not run. Sources were read by `curl` (through the session
proxy, TLS verified against `/root/.ccr/ca-bundle.crt`), by WebFetch, and by WebSearch.

## 0. How the sources were reached (read this first)

Most vendor documentation **sites** are blocked by the session's egress proxy. Every blocked
site gave the same reply:

```
$ curl -sS -o /dev/null https://code.visualstudio.com/api/working-with-extensions/publishing-extension
curl: (56) CONNECT tunnel failed, response 403
```

WebFetch was blocked the same way:
`{"error_type":"EGRESS_BLOCKED","domain":"code.visualstudio.com","message":"Access to code.visualstudio.com is blocked by the network egress proxy."}`
(and identically for `plugins.jetbrains.com`).

Blocked sites (curl `(56) CONNECT tunnel failed, response 403`): code.visualstudio.com,
plugins.jetbrains.com, www.jetbrains.com, docs.obsidian.md, developers.raycast.com,
docs.npmjs.com, docs.brew.sh, slsa.dev, developer.chrome.com, extensionworkshop.com,
docs.sigstore.dev, github.blog, salsa.debian.org, reproducible-builds.org. `github.com` answered
HTTP 403. Directly reachable: keepachangelog.com, semver.org, opensource.guide,
raw.githubusercontent.com.

Route used instead: almost every one of these vendors publishes the same documentation pages
as Markdown in a public GitHub repository, fetched from `raw.githubusercontent.com`. Those
copies are the vendor's own documentation source, not blog posts.

**Pinning limitation.** A commit SHA could not be recorded: git was out of bounds for this run,
and `api.github.com` refused the repositories with
`"GitHub access to this repository is not enabled for this session. Use add_repo to request access..."`.
Each raw source below is therefore cited as `owner/repo@branch:path`, with the fetch time above
and the first 16 hex of the SHA-256 of the bytes fetched, so a later reader can tell whether the
file has changed since.

**Unverified content (JetBrains Marketplace).** The JetBrains Marketplace listing and approval pages
(`plugins.jetbrains.com/docs/marketplace/...`, `jetbrains.com/legal/...`) have no raw mirror that
was found. The only content from them is **search-engine summary text** (WebSearch), marked
**[search-summary, not verified]** wherever it is used. It is not a verbatim quote and must not be
cited as one.

### Source ledger

| # | Canonical page (blocked unless noted) | What was actually read | sha256[:16] |
|---|---|---|---|
| S1 | code.visualstudio.com/api/working-with-extensions/publishing-extension | `microsoft/vscode-docs@main:api/working-with-extensions/publishing-extension.md` (DateApproved 9/16/2026) | 0d052dab00aadd40 |
| S2 | code.visualstudio.com/api/references/extension-manifest | `microsoft/vscode-docs@main:api/references/extension-manifest.md` | b3bbd52fe4990741 |
| S3 | code.visualstudio.com/docs/configure/extensions/extension-runtime-security | `microsoft/vscode-docs@main:docs/configure/extensions/extension-runtime-security.md` | 4905d4f0c1341a4c |
| S4 | (vsce tool source, not docs) | `microsoft/vscode-vsce@main:src/package.ts` | c38a19bf4c3237d0 |
| S5 | plugins.jetbrains.com/docs/intellij/publishing-plugin.html | `JetBrains/intellij-sdk-docs@main:topics/basics/getting_started/publishing_plugin.md` | 19c1cf9e3fbec0ea |
| S6 | plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html | `JetBrains/intellij-sdk-docs@main:topics/basics/plugin_structure/plugin_configuration_file.md` | d5ccd3b9705e4d13 |
| S7 | plugins.jetbrains.com/docs/intellij/plugin-signing.html | `JetBrains/intellij-sdk-docs@main:topics/basics/plugin_signing.md` | 666d4aa2b255dff3 |
| S8 | plugins.jetbrains.com/docs/intellij/plugin-user-experience.html | `JetBrains/intellij-sdk-docs@main:topics/basics/plugin_user_experience.md` | b598aaf35c1d77d2 |
| S9 | plugins.jetbrains.com/docs/marketplace/best-practices-for-listing.html, …/jetbrains-marketplace-approval-guidelines.html | **Blocked, no mirror found.** WebSearch summaries only | — |
| S10 | docs.obsidian.md/Plugins/Releasing/Submit+your+plugin | `obsidianmd/obsidian-developer-docs@main:en/Plugins/Releasing/Submit your plugin.md` | 4e4308b75c293eaa |
| S11 | docs.obsidian.md (Submission requirements for plugins) | `…@main:en/Community directory/Submission requirements for plugins.md` (the old `Plugins/Releasing/` path returns 404; the file now lives here, with an alias to the old path) | 025a5ee9228bbb6a |
| S12 | docs.obsidian.md (Developer policies) | `…@main:en/Community directory/Developer policies.md` | 9c5766b4b55ca729 |
| S13 | docs.obsidian.md/Reference/Manifest | `…@main:en/Reference/Manifest.md` | e0d73638bfaa707d |
| S14 | docs.obsidian.md (Plugin guidelines) | `…@main:en/Plugins/Releasing/Plugin guidelines.md` | 2d7caa6241a6f618 |
| S15 | docs.obsidian.md (Release your plugin with GitHub Actions) | `…@main:en/Plugins/Releasing/Release your plugin with GitHub Actions.md` | d4973bac33b6d18f |
| S16 | (sample plugin README) | `obsidianmd/obsidian-sample-plugin@master:README.md` | 5ffddf920efa0828 |
| S17 | developers.raycast.com/basics/prepare-an-extension-for-store | `raycast/extensions@main:docs/basics/prepare-an-extension-for-store.md` | ebc55aaa545d684f |
| S18 | docs.npmjs.com/cli/configuring-npm/package-json | `npm/cli@latest:docs/lib/content/configuring-npm/package-json.md` | 32833f1e3b910cac |
| S19 | docs.npmjs.com/about-package-readme-files | `npm/documentation@main:content/packages-and-modules/contributing-packages-to-the-registry/about-package-readme-files.mdx` | 474f3f71312c049c |
| S20 | docs.npmjs.com/about-semantic-versioning | `…/about-semantic-versioning.mdx` | ea05a1d42a8073cb |
| S21 | docs.npmjs.com/generating-provenance-statements | `npm/documentation@main:content/packages-and-modules/securing-your-code/generating-provenance-statements.mdx` | 1cb28a3dc004c154 |
| S22 | docs.brew.sh/Acceptable-Formulae | `Homebrew/brew@main:docs/Acceptable-Formulae.md` (last_review_date 2026-07-18) | de1c6167f6b22129 |
| S23 | docs.brew.sh/Package-Acceptance-Policy | `Homebrew/brew@main:docs/Package-Acceptance-Policy.md` (last_review_date 2026-07-18) | fe54d5e52e4df4c5 |
| S24 | docs.brew.sh/Acceptable-Casks, Cask-Cookbook | `Homebrew/brew@main:docs/Acceptable-Casks.md`, `docs/Cask-Cookbook.md` | ea54ee63ca66fe89, 7e9978193d4ae834 |
| S25 | docs.brew.sh/Homebrew-Security-and-Supply-Chain | `Homebrew/brew@main:docs/Homebrew-Security-and-Supply-Chain.md` (last_review_date 2026-09-19) | 2b7134b816e05cf3 |
| S26 | extensionworkshop.com/documentation/publish/add-on-policies/ | `mozilla/extension-workshop@master:src/content/documentation/publish/add-on-policies.md` (date 2026-04-30) | 7dcda3c4e838d2a2 |
| S27 | extensionworkshop.com/documentation/develop/create-an-appealing-listing/ | `mozilla/extension-workshop@master:src/content/documentation/publish/create-an-appealing-listing.md` (date 2019-03-18) | 65a2f5fc87a34ede |
| S28 | developer.chrome.com/docs/webstore/best_practices | `GoogleChrome/developer.chrome.com@main:site/en/docs/webstore/best_practices/index.md` (updated 2023-09-29) | dd8ed09493a11083 |
| S29 | developer.chrome.com/docs/webstore/program-policies/listing-requirements | `…@main:site/en/docs/webstore/program-policies/listing-requirements/index.md` (date 2022-11-01) | 7c9f014824494207 |
| S30 | developer.chrome.com/docs/webstore/troubleshooting | `…@main:site/en/docs/webstore/troubleshooting/index.md` (updated 2023-10-05) | d8f93faf8805d98c |
| S31 | github.com/RichardLitt/standard-readme (spec) | `RichardLitt/standard-readme@main:spec.md` | 611144e44bbb1e71 |
| S32 | https://keepachangelog.com/en/1.1.0/ | **direct**, HTTP 200 | — |
| S33 | https://semver.org/ (Semantic Versioning 2.0.0) | **direct**, HTTP 200 | — |
| S34 | https://opensource.guide/starting-a-project/ | **direct**, HTTP 200 | — |
| S35 | slsa.dev/spec/v1.1/levels, …/distributing-provenance | `slsa-framework/slsa@releases/v1.1:spec/levels.md`, `spec/distributing-provenance.md` | f6bb8073f7f15ec6, 391a7752ce561aae |
| S36 | docs.sigstore.dev (overview) | `sigstore/docs@main:content/en/about/overview.md` | fe39557ab1e05cc0 |
| S37 | OpenSSF Scorecard checks | `ossf/scorecard@main:docs/checks.md` | d1a667647fa408a7 |
| S38 | docs.github.com (artifact attestations concept) | `github/docs@main:content/actions/concepts/security/artifact-attestations.md` | 664b528c604fb5b1 |

**Not reached:**
- *Art of README* (hackergrrl/noffle `art-of-readme`): `raw.githubusercontent.com/hackergrrl/art-of-readme/{master,main,HEAD}/README.md` and `noffle/art-of-readme/master/README.md` all returned HTTP 404, and github.com returned 403. **Not used.**
- *reproducible-builds.org*: blocked (`(56) CONNECT tunnel failed, response 403`). A guessed GitHub mirror path returned 404. **Not used.** Reproducible builds therefore appear below only where another source states the norm (AMO build reproduction, Homebrew).
- *Chrome Web Store live pages*: the GitHub copies are dated 2022–2023 (front matter). Whether the live site has changed since could not be checked. Treat Chrome rows as "as of those dates".
- *Raycast "Extension Guidelines"* (manual.raycast.com), linked from S17: not fetched.

---

## 1. VS Code Marketplace (S1–S4)

**Required manifest fields** (S2 table, `Required = Y`): `name` ("should be all lowercase with no
spaces. The name must be unique to the Marketplace."), `version` ("[SemVer] compatible version."),
`publisher`, `engines` ("An object containing at least the `vscode` key … Cannot be `*`.").
Optional: `license`, `displayName` ("must be unique to the Marketplace"), `description` ("A short
description of what your extension is and does."), `categories` (closed list), `keywords`
("currently limited to 30 keywords"), `icon` ("at least 128x128 pixels (256x256 for Retina
screens)"), `badges` (approved list only), `qna`, `sponsor`, `pricing`.

**Files** (S1, "Marketplace integration"; recommendations, stated as "tips"):
- "Add a `README.md` file to the root of your extension with the content you want to show on the extension's Marketplace page."
- "Add a `LICENSE` file to the root of your extension with the information about the extension's license."
- "Add a `CHANGELOG.md` file to the root of your extension with the information about the history of the changes for your extension."
- "Add a `SUPPORT.md` file to the root of your extension with the information about how to get support for your extension."
- "Set an icon by specifying a relative path to a PNG file of at least 128x128px".

**Links** (S2): "There are several optional links (`bugs`, `homepage`, `repository`) you can set
and these are displayed under the **Resources** section of the Marketplace." The mapping is
Issues→`bugs:url`, Repository→`repository:url`, Homepage→`homepage`, License→`license`.

**Description** (S2): "Provide a good display name and description. This is important for the
Marketplace and in product displays. These strings are also used for text search".
**Categories**: "Only use the values that make sense for your extension."

**Hard rejections by the publishing tool** (S1): "`vsce` will not publish extensions that contain
user-provided SVG images." It checks: "The icon provided in `package.json` may not be an SVG."
"Image URLs in `README.md` and `CHANGELOG.md` need to resolve to `https` URLs." "Images in
`README.md` and `CHANGELOG.md` may not be SVGs unless they are from trusted badge providers."
Badges: "Due to security concerns, we only allow badges from trusted services." Keywords: "does
not allow an extension package to have more than 30 `keywords`".

From the vsce **source** (S4, tool code, not documentation):
- A hard error on template text: `It seems the README.md still contains template text. Make sure to edit the README.md file before you package or publish your extension.`
- A warning when the repository link is missing: `A 'repository' field is missing from the 'package.json' manifest file.`
- A missing licence file gives a warning and a prompt: `${this.expectedLicenseName} not found` then `Do you want to continue? [y/N]`, where the expected name is `LICENSE, LICENSE.md, or LICENSE.txt`.
- Hard errors on a missing `engines` field and on images that are not HTTPS: `Images in ${this.name} must come from an HTTPS source`.

**Versioning** (S1): "We only support `major.minor.patch` for extension versions, `semver`
pre-release tags are **not supported**." Once a version is deleted, "you can't reuse this version
number for a new publish." Removed extension names are "permanently reserved and cannot be reused,
even by the original publisher. This helps protect users from impersonation".
**Compatibility** (S1): "When authoring an extension, you must specify the versions of VS Code your
extension is compatible with."
**Packaging hygiene** (S1): "You should ignore all files not needed at runtime."
**Deprecation** (S1): extensions can be deprecated "in favor of another extension or a setting".

**Trust** (S1, S3):
- Verified publisher: "a publisher must have one or more extensions on the VS Marketplace for a minimum of 6 months, and the registration of the domain must also be at least 6 months old."
- Marketplace protections (S3): "**Malware scanning** … Until the scan is all clear, the extension won't be published". "**Extension Signature Verification**: The Visual Studio Marketplace signs all extensions when they're published." "**Secret Scanning** … If any secrets are detected, publishing is blocked".
- What users are told to check (S3): "**Issues, Repository, and License**: Check if the publisher provided these and if they have the support you expect."
- Publishing credentials (S1): "We recommend that extension publishing use Microsoft Entra ID–based authentication with **workload identity federation and managed identities**. This approach eliminates long-lived secrets such as Personal Access Tokens (PATs)". Global PATs are retired on December 1, 2026.

## 2. JetBrains Marketplace (S5–S9)

**Required descriptor elements** (S6, `plugin.xml`): `name` is "**yes**" required ("The user-visible
plugin display name (Title Case)."). `version` is required: "Plugins uploaded to the JetBrains
Marketplace must follow semantic versioning." `idea-version` (the compatibility range) is
required. `vendor` is required. `description` is required. `change-notes` is optional ("A short
summary of new features, bugfixes, and changes provided with the latest plugin version."). `id` is
"highly recommended", with the warning "Make sure to pick a stable ID, as the value cannot be
changed later after public release."
**Compatibility** (S6): for `until-build`, "It's highly recommended not to set this attribute".
**Versions** (S5): "the JetBrains Marketplace won't accept multiple artifacts with the same version."
**Pre-publish checklist** (S5): the plugin "follows all recommendations from [Plugin User
Experience]" and "follows all requirements from [Plugin Overview page]".
**Signing** (S5, S7): "Before publishing a plugin, make sure it is signed." "The JetBrains
Marketplace signing process is designed to ensure that plugins are not modified over the course of
the publishing and delivery pipeline. If the author does not sign the plugin or has a revoked
certificate, a warning dialog will appear in the IDE during installation." "the file will be
signed twice – first by the plugin author, then by JetBrains Marketplace."
**Support** (S8): "it is recommended to set up an issue tracker where users can report errors."
Distribution size: "Make sure no unneeded or multiple versions of the same dependencies are packaged".

**Listing and approval rules — [search-summary, not verified]** (S9; the WebSearch summaries of
plugins.jetbrains.com and jetbrains.com/legal pages, not verbatim):
- "The first 40 characters of the plugin description must be in English and contain a short summary, which will be used for the plugin's preview card".
- Plugin name: "original and unique", "must include keywords or concepts that accurately describe the Plugin", "must not use famous or trademarked names of third parties without their authorization". Best practice: "1-4 words long (max 20 characters)", with a hard limit of 60 characters.
- Logo "must be different from the default logo for the IntelliJ Platform Plugin Template"; "40 px by 40 px", SVG.
- "Plugin functions 'as described' on the Plugin page … and its name and description clearly identify what it is designed to do."
- Change notes "must not have 'Add change notes here'".
- Screenshots: "minimum recommended size is 1200 × 760 pixels".
- Links: "website, issue tracker, forum page, source code, documentation". Also: "Put some inline links to useful resources (issue tracker, forum, etc.) to the description."
- "plugins and plugin updates are manually reviewed one-by-one".

## 3. Obsidian community plugins (S10–S16)

**Required files at the repo root** (S10): "A `README.md` that describes the purpose of the plugin,
and how to use it." "A `LICENSE` that determines how others are allowed to use the plugin and its
source code." "A `manifest.json` that describes your plugin."
**Required manifest fields** (S13): `author`, `minAppVersion`, `name`, `version` ("using Semantic
Versioning in the format `x.y.z`"), and for plugins `description`, `id` ("must contain only
lowercase letters and hyphens, can't end with `plugin`, and can't contain `obsidian`") and
`isDesktopOnly`.
**Name rules** (S13): "Make your name short and descriptive." "Prefer English names and use Basic
Latin characters only. No punctuation (except hyphens, plus sign, and parenthesis), emoji, or
special characters are allowed." "Do not include the word 'Obsidian'". "Every plugin and theme must
have a unique name." "plugins may not contain the word 'Plugin'." A plugin with an invalid new name
is delisted: "If the new name is invalid, the directory delists the plugin until you resolve the
problem."
**Description rules** (S11): "Avoid starting your description with 'This is a plugin'". Also:
"Have 250 characters maximum." "End with a period `.`." "Avoid using emoji or special characters."
"Use correct capitalization for acronyms, proper nouns and trademarks". Good descriptions "often
start with an action statement".
**Compatibility** (S11): "The `minAppVersion` … should be set to the minimum required version of the
Obsidian app that your plugin is compatible with." Node and Electron APIs: "you **must** set
`isDesktopOnly` to `true`".
**Template residue** (S11): "sample code should be removed from your plugin before submission."
Command IDs: "Don't include the plugin ID in the command ID".
**Funding link** (S11): "If you don't accept donations, remove `fundingUrl` from your manifest."
**Releases** (S10, S16):
- "The 'Tag version' of the release must match the version in your `manifest.json`."
- Assets `main.js`, `manifest.json`, `styles.css` are uploaded as release attachments.
- "Use the exact version number, don't include a prefix `v`."
- `versions.json` maps `"new-plugin-version": "minimum-obsidian-version"` "so older versions of Obsidian can download an older version of your plugin that's compatible".
- Review: "your plugin is reviewed automatically". Ownership: "Link your GitHub account to your profile. This lets the directory verify that you own the repository you're submitting."
**Provenance** (S15): the release workflow's "**Generate artifact attestation** step creates a signed
build provenance attestation for your release assets, which is recommended when you submit a
plugin to the community directory."
**Policies** (S12). "Plugins and themes that don't follow these policies will be removed from the directory."
- Not allowed: "Obfuscate code to hide its purpose." "Include client-side telemetry." "Install or update themselves or their dependencies."
- Disclosures: "only allowed if clearly indicated in your README". These cover "Payment is required for full access", "An account is required for full access", "Network use. Clearly explain which remote services are used and why they're needed", "Accessing files outside of Obsidian vaults", and "Server-side telemetry" (which also needs a privacy-policy link).
- Licensing: "Include a LICENSE file and clearly indicate the license of your plugin or theme." "Comply with the original licenses of any code your plugin or theme makes use of, including attribution in the README if required." Trademark: do not use the name "in a way that could confuse users into thinking your plugin or theme is a first-party creation."
- Maintenance: "we may also remove plugins or themes that have become unmaintained or severely broken."
**Code guidelines** (S14): "Avoid unnecessary logging to console", "Rename placeholder class names",
"Avoid `innerHTML`, `outerHTML` and `insertAdjacentHTML`" (Security), "Use sentence case in UI".

## 4. Raycast Store (S17)

This page is the store's review checklist: "requirements and guidelines that you'll need to follow in
order to get through the review".
- Manifest: "use your **Raycast** account username in the `author` field"; "use `MIT` in the `license` field"; use "the latest Raycast API version"; "Ensure the `platforms` field matching the requirement of your extension". Also "include `package-lock.json`". "**run a distribution build** … before submitting".
- Naming: titles follow "Apple Style Guide" conventions. The title should "Make it easy for people to understand what it does" (rejected examples: "`Converter`, `Images`, `Code Review`, `Utils`"). "Avoid generic names for an extension when your extension doesn't provide a lot of commands".
- Description: "In one sentence, what does your extension do? This will be shown in the list of extensions in the Store. Keep it short and descriptive."
- Icon: "512x512px icon in `png` format"; "should look good in both light and dark themes"; "Extensions that use the default Raycast icon will be rejected"; "Make sure to remove unused assets and icons".
- README: "If your extension requires additional setup, such as getting an API access token … please provide a README file at the root folder of your extension."
- Categories: "All extensions should be published with at least one category".
- Screenshots: "maximum of six screenshots. We recommend adding at least three". Specification 2000 x 1250 PNG. "Do not share sensitive data in your screenshots".
- Version history: "add a `CHANGELOG.md` file to the root folder of your extension". Each entry has "a title formatted as an h2 header followed by `{PR_MERGE_DATE}`", and the page points to Keep a Changelog.
- **Binaries**:
  - "If you do end up downloading executable binaries in the background, please make sure it's done from a server that you don't have access to. Otherwise, we cannot guarantee that you won't replace the binary with malicious code after the review."
  - "Add additional integrity checks through hashes."
  - "Don't bundle opaque binaries where sources are unavailable or where it's unclear how they have been built."
  - Rejected: "Any binary with unavailable sources or unclear builds just added to the assets folder".
  - Accepted: "Binary downloaded or installed from a trusted location with additional integrity checking through hashes".
- Security and privacy: "Extensions requesting Keychain Access will be rejected". "It's not allowed to include external analytics in extensions."
- Contribute or new: "If your change is significant, it makes sense to contact the author of the extension before you invest a lot of time into it."

## 5. npm (S18–S21)

- Required to publish: "the *most* important things in your package.json are the name and version fields as they will be required." "Changes to the package should come along with changes to the version." Name: "must be less than or equal to 214 characters"; "New packages must not have uppercase letters in the name"; "Don't put 'js' or 'node' in the name."
- `description`: "Put a description in it. … This helps people discover your package". `keywords`: the same, for `npm search`.
- `bugs`: "The URL to your project's issue tracker and / or the email address to which issues should be reported."
- `repository`: "Specify the place where your code lives." "The URL should be a publicly available (perhaps read-only) URL that can be handed directly to a VCS program without any modification."
- `license`: "You should specify a license for your package so that people know how they are permitted to use it". Use "a current SPDX license identifier"; "Ideally, you should pick one that is OSI approved"; otherwise `"SEE LICENSE IN <filename>"`. "Certain files are always included, regardless of settings": `package.json`, `README`, `LICENSE`/`LICENCE`.
- README (S19): "We highly recommend including a `README.md` file … In most cases `README.md` files include directions for _installing_, _configuring_, and _using_ the code". "An npm package `README.md` file **must** be in the root-level directory of the package."
- SemVer (S20): "we recommend starting your package version at `1.0.0`". "If you introduce a change that breaks a package dependency, we strongly recommend incrementing the version **major number**".
- Provenance (S21): "This allows you to publicly establish where a package was built and who published a package". "When an npm package is published with provenance, it is signed by Sigstore public good servers and logged in a public transparency ledger". Prerequisite: "Ensure your `package.json` is configured with a public `repository` that matches (case-sensitive) where you are publishing with provenance from." Limitation: "it does not guarantee the package has no malicious code. Instead, npm provenance provides a verifiable link to the package's source code and build instructions". With trusted publishing, attestations are "automatically generated … This provides enhanced security and eliminates the need for access tokens".

## 6. Homebrew (S22–S25)

- Presence (S23): "A package must represent software with a public presence independent of Homebrew and a homepage that explains the project." "The software must be actively maintained upstream, have no known unpatched security vulnerabilities".
- Notability (S23): "at least 30 forks, 30 watchers or 75 stars" (90/90/225 for a self-submission); "A code repository less than 30 days old is normally not eligible."
- Discovery (S23): "Homebrew's official repositories are not editorial curation or recommendation services." "Searchability and disambiguation remain in scope because users must be able to identify the correct package for known software."
- Sources (S22): "Sources must use an immutable release archive, tag or revision and downloaded archives must be verified with SHA-256." "An install step must not fetch code from a moving default branch or an unversioned, unchecksummed archive." Stable releases: "Upstream must identify the packaged version as stable and provide an immutable tag or release." Licence: "must be open source under a licence compatible with the Debian Free Software Guidelines". "It must either build from source or install portable, platform-independent output". "Proprietary or platform-specific binary-only software belongs in a cask."
- Self-updating (S22): "Self-update behaviour must be disabled when this can be done without a fragile or invasive patch."
- Casks (S24): the `sha256` stanza is the "SHA-256 checksum of the file downloaded from `url` … or the special value `:no_check`", used "whenever checksumming is impractical". "An installer package that requires certificate verification to be disabled is not eligible."
- Supply chain (S25):
  - "Every change to a Homebrew repository … goes through a pull request that is reviewed and merged by a human maintainer."
  - "A formula pins each download to an explicit `sha256` checksum that lives in the formula file. The checksum is part of the human-reviewed change".
  - "Checksums prove that the downloaded bytes match the reviewed metadata. Bottle provenance attestations add a different check: who built those bytes and from what source."
  - "Homebrew CI also emits bottle attestations with `actions/attest`".
  - Names: "Names in Homebrew's official taps are maintainer-curated, not first-come-first-served."
  - The same page lists "immutable GitHub releases" among the GitHub security features Homebrew enables.

## 7. Firefox AMO (S26–S27)

- "**All add-ons are subject to these policies, regardless of how they are distributed.**" (S26)
- No surprises: "Users should be able to easily discern the functionality of your add-on based on the listing … The listing should include an easy-to-read description of what the add-on does, and what information it transmits."
- "Listings must disclose when payment is required to enable any add-on functionality." A fork: "the name must clearly distinguish it from the original".
- Submission: "Add-ons must function only as described." Source code: "Mozilla needs to review a copy of the source code before any of these steps [transpile/minify] have been applied." The author provides "instructions on how to reproduce the build". "Add-ons are not allowed to contain obfuscated code".
- Development practices: "must only request those permissions that are necessary"; "must be self-contained and not load remote code for execution"; "must use encryption when transporting data remotely"; "should avoid including redundant code or files"; "Only release versions of third-party libraries and/or frameworks may be included".
- Listing guide (S27, dated 2019):
  - Name: "unique and descriptive". The summary "is limited to 250 characters, but do not consider it a challenge to use all the available characters".
  - Screenshots: "make sure each screenshot shows a key feature"; the recommended size is 1280x800px.
  - Categories: "do not include your add-on in a second category if one will do".
  - Support: "you can provide details of its homepage, an email address for support, and the address of a support page … If you can, provide all three of these. However, as a minimum, consider offering an email address for support."
  - Version details: "be crisp and to-the-point".
  - Experimental add-ons: "If your add-on is an experiment, flag this when you submit it".

## 8. Chrome Web Store (S28–S30; the GitHub copies are dated 2022–2023)

- Listing requirements (S29):
  - "If your product has a blank description field or is missing an icon or screenshots, it will be rejected."
  - "We don't allow extensions with misleading, improperly formatted, non-descriptive, irrelevant, excessive, or inappropriate metadata, including but not limited to the extension's description, developer name, title, icon, screenshots, and promotional images."
  - One example of keyword spam: "Unnatural repetition of the same keyword more than 5 times".
  - "We don't allow unattributed or anonymous user testimonials".
- Common rejection reasons (S30):
  - "The extension's title is not meaningful or is misleading."
  - "The extension does not provide the functionality described in the metadata".
  - "The extension performs actions not mentioned in the metadata".
  - The fix: "List all major features the extension provides."
- Best practices (S28): "The purpose of an extension's … store listing is to set the user's expectations. It should explicitly communicate what the extension does." "Include all the required images (icon, tile, marquee, and screenshots)." "The developer console requires you to specify a category".

## 9. README, changelog and versioning conventions (S31–S34)

**standard-readme** (S31), for "A compliant README":
- Structure: "Sections must appear in order". The README "Must not contain broken links."
- Short description: "Must be less than 120 characters." "Must match the description in the packager manager's `description` field."
- Title: "Title must match repository, folder and package manager names - or it may have another, relevant title with the repository, folder, and package manager title next to it". Where these names differ, "there must be a note in the Long Description explaining why".
- Table of contents: "Required; optional for READMEs shorter than 100 lines."
- Install: "Code block illustrating how to install." A `Dependencies` subsection is "Required if there are unusual dependencies or dependencies that must be manually installed."
- Usage: "Code block illustrating common usage."
- Contributing: "Required", and it must "State where users can ask questions" and "State whether PRs are accepted".
- License: "Required", with "State license full name or identifier, as listed on the SPDX license list", "State license owner" and "Must be last section."
- Code examples: "If there are code examples, they should be linted in the same way as the code is linted in the rest of the project."

**Open Source Guides** (S34): "every project should include the following documentation: Open source
license, README, Contributing guidelines, Code of conduct". A README should answer "What does this
project do? Why is this project useful? How do I get started? Where can I get more help, if I need
it?" "If you don't want to accept contributions, or your project is not yet ready for production,
write this information down." Checklist: "The name is easy to remember, gives some idea of what the
project does, and does not conflict with an existing project or infringe on trademarks". Also:
"There are no sensitive materials in the revision history, issues, or pull requests".

**Keep a Changelog 1.1.0** (S32):
- "A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project."
- Guiding principles: "Changelogs are for humans, not machines. There should be an entry for every single version. The same types of changes should be grouped. Versions and sections should be linkable. The latest version comes first. The release date of each version is displayed. Mention whether you follow Semantic Versioning."
- Types of change: Added / Changed / Deprecated / Removed / Fixed / Security. "Keep an Unreleased section at the top".
- "Using commit log diffs as changelogs is a bad idea". "If you do nothing else, list deprecations, removals, and any breaking changes in your changelog." "A changelog which only mentions some of the changes can be as dangerous as not having a changelog." Yanked releases: `## [0.0.5] - 2014-12-13 [YANKED]`. "Call it CHANGELOG.md."

**SemVer 2.0.0** (S33): "Software using Semantic Versioning MUST declare a public API." "Once a
versioned package has been released, the contents of that version MUST NOT be modified. Any
modifications MUST be released as a new version." "Major version zero (0.y.z) is for initial
development. Anything MAY change at any time."

## 10. Supply-chain trust norms (S35–S38, with S1/S7/S21/S25)

- **SLSA v1.1** (S35):
  - Build L1, "Provenance exists": "Package has provenance showing how it was built. Can be used to prevent mistakes but is trivial to bypass or forge." The producer must "Distribute provenance to consumers, preferably using a convention determined by the package ecosystem." "Provenance may be incomplete and/or unsigned at L1."
  - Build L2: "builds run on a hosted platform that generates and signs the provenance."
  - Distribution: "Attestations SHOULD be bound to artifacts, not releases."
- **Sigstore** (S36): unsigned software is at risk from "Typosquatting packages with similar names", "Compromised site where package is hosted", and "Tampering after being published". "Signatures are generated with ephemeral signing keys so there's no need to manage keys. Signing events are recorded in a tamper-resistant public log".
- **GitHub artifact attestations** (S38): "Artifact attestations by itself provides SLSA v1.0 Build Level 2." Verification is the point: "Generating attestations alone doesn't provide any security benefit, the attestations must be verified". What to sign: "Binaries people will run, packages people will download, or manifests that include hashes of detailed contents". What not to sign: "Individual files like source code, documentation files, or embedded images." Warning: "artifact attestations are _not_ a guarantee that an artifact is secure".
- **OpenSSF Scorecard** (S37), as checkable repository-level criteria:
  - Binary-Artifacts: "Risk: `High` (non-reviewable code) … Including generated executables in the source repository increases user risk."
  - Signed-Releases: "This check looks for the following filenames in the project's last five release assets: *.minisig, *.asc (pgp), *.sig, *.sign, *.sigstore, *.sigstore.json, *.intoto.jsonl". A SLSA provenance file gives the maximum score. "Note: The check does not verify the signatures."
  - Security-Policy: looks for "a file named `SECURITY.md`".
  - License, Maintained (at least one commit per week over 90 days for the top score), and Pinned-Dependencies ("explicitly set to a specific hash instead of allowing a mutable version").
  - Token-Permissions: "least privilege".

---

## 11. Synthesis: what every mature ecosystem agrees a quality listing has

Legend: **R** = required or rejected-without, **Rec** = recommended, **—** = not in the pages read
(which is not the same as "not required"). **SS** = JetBrains search-summary, not verified. Source
tags refer to the ledger.

| Criterion | VS Code | JetBrains | Obsidian | Raycast | npm | Homebrew | Firefox AMO | Chrome WS |
|---|---|---|---|---|---|---|---|---|
| Long description / README shown on listing | Rec: README.md at root (S1) | R: `<description>` (S6) | R: README.md (S10) | R only if setup needed (S17) | Rec: "highly recommend"; must be at root if present (S19) | R: upstream homepage "that explains the project" (S23) | R: "easy-to-read description" (S26) | R: blank description rejected (S29) |
| Short one-line summary, length-capped | Rec: `description` (S2) | R: first 40 chars English (SS) | R: ≤250 chars, ends with "." (S11) | R: "In one sentence" (S17) | Rec (S18) | — | R: summary ≤250 (S27) | R (S29) |
| Summary does not restate the obvious | — | — | R: not "This is a plugin" (S11) | Rec: no generic titles (S17) | Rec: no "js"/"node" in name (S18) | — | — | R: no non-descriptive metadata (S29) |
| License declared | Rec: LICENSE file; vsce prompts if absent (S1, S4) | — | R: LICENSE file (S10, S12) | R: `MIT` in `license` (S17) | Rec: SPDX id (S18) | R: DFSG-compatible (S22) | — | — |
| Changelog / release notes | Rec: CHANGELOG.md (S1) | Rec: `change-notes`; template text rejected (S6, SS) | Rec: release description (S10) | Rec: CHANGELOG.md, dated h2 (S17) | — | — | Rec: "version details" (S27) | — |
| SemVer versioning | R: SemVer, x.y.z only (S1, S2) | R: "must follow semantic versioning" (S6) | R: x.y.z (S13) | — | R: node-semver parseable (S18) | R: stable, immutable upstream release (S22) | — | — |
| Version never reused or mutated | R: deleted version can't be reused (S1) | R: same version not accepted (S5) | R: tag == manifest version (S10) | — | Rec: "Changes … should come along with changes to the version" (S18) | R: immutable tag or release (S22) | — | — |
| Host compatibility declared | R: `engines.vscode` (S2) | R: `idea-version` (S6) | R: `minAppVersion`, `isDesktopOnly` (S13) | R: `platforms` checked (S17) | — | R: CI matrix (S22) | Rec: select platforms (S27) | — |
| Icon | Rec: PNG ≥128px, SVG refused (S1) | R: 40px SVG, not the template's (SS) | — | R: 512px PNG; default icon rejected (S17) | — | — | Rec: 32/64 px (S27) | R (S29) |
| Screenshots | via README; HTTPS only (S1) | Rec: ≥1200×760 (SS) | README images (S10) | Rec: ≥3, max 6 (S17) | — | — | Rec: 1280×800 (S27) | R (S29) |
| Category from a fixed list | Rec: closed list (S2) | — | — | R: ≥1 (S17) | — | Explicitly out of scope (S23) | Rec: ≤2 (S27) | R (S28) |
| Keyword limits / anti-spam | R: ≤30 keywords (S1) | — | — | — | Rec: keywords (S18) | — | Rec: "keep their use natural" (S27) | R: keyword spam banned (S29) |
| Repository / source link | Rec; vsce warns if missing (S2, S4) | Rec: source link (SS) | R: source on GitHub (S10) | (monorepo) | Rec; needed for provenance (S18, S21) | R: public upstream (S23) | R: source for review (S26) | — |
| Issue tracker / support channel | Rec: `bugs`, SUPPORT.md, Q&A (S1, S2) | Rec: issue tracker (S8, SS) | Violations go to GitHub issues (S12) | — | Rec: `bugs` (S18) | — | Rec: homepage, email and support page (S27) | — |
| Name unique, descriptive, not misleading or trademark-confusing | R: unique name and displayName (S2) | R: unique, no third-party marks (SS) | R: unique, no "Obsidian"/"Plugin" (S13) | Rec: Apple Style Guide; not generic (S17) | R: ≤214 chars, lowercase (S18) | R: curated names (S25) | R: forks distinguished (S26) | R: misleading title rejected (S30) |
| No template or sample residue | R: README template text is a hard error (S4) | R: template logo and change notes (SS) | R: remove sample code (S11) | R: default icon rejected (S17) | — | — | — | — |
| Functions as described; no undisclosed behaviour | — | R: "as described" (SS) | R: disclosures in README (S12) | — | — | — | R: "No Surprises" (S26) | R: deceptive behaviour (S30) |
| Network, payment and telemetry disclosed | Rec: `pricing` label (S1) | — | R (S12) | R: no external analytics (S17) | — | — | R: payment disclosed (S26) | R: privacy tab (S28) |
| No opaque binaries or obfuscation | — | — | R: no obfuscation (S12) | R: no opaque binaries (S17) | — | R: build from source (S22) | R: reviewable source, no obfuscation (S26) | — |
| Checksums on downloaded artifacts | — | — | — | R: "integrity checks through hashes" (S17) | — | R: SHA-256 pinned (S22, S25) | — | — |
| Signing | R: Marketplace signs all (S3) | R: author and Marketplace sign (S5, S7) | — | — | R with provenance: Sigstore (S21) | R: signed JSON API metadata (S25) | — | — |
| Build provenance / attestation | — | — | Rec: `actions/attest` (S15) | — | Rec: `--provenance`; automatic with trusted publishing (S21) | R in CI: bottle attestations (S25) | R: reproducible build instructions (S26) | — |
| Short-lived CI credentials rather than long-lived tokens | Rec: Entra ID; PATs retired (S1) | — | — | — | Rec: trusted publishing (S21) | — | — | — |
| Human or automated review before listing | Automated scans (S3) | Manual review (SS) | Automated review (S10) | PR review (S17) | None (S25 describes npm as "instant, unreviewed publishing") | Human PR review (S25) | Human and code review (S26) | Review (S30) |
| Publisher identity verified | Rec: verified publisher (S1) | — | R: GitHub account linked (S10) | R: Raycast username as `author` (S17) | via provenance (S21) | Upstream ≠ maintainer (S25) | — | — |
| Maintenance / removal of the unmaintained | Deprecation flow (S1) | — | May remove unmaintained (S12) | — | — | R: actively maintained (S23) | — | — |

**Agreement across all or nearly all ecosystems read:**
1. A human-readable description that says what the thing does, with a separate short summary. Short-summary caps where stated: 250 characters (Obsidian, AMO), 120 (standard-readme), one sentence (Raycast), 40-character English lead (JetBrains, SS).
2. A licence stated in a machine-readable field and/or a LICENSE file.
3. SemVer-shaped versions that are never reused or mutated.
4. A declared compatibility range against the host.
5. Pointers to source, issues and support.
6. The name and metadata must not mislead. Template residue is rejected outright by four ecosystems.

**Agreement among the ecosystems that ship executables** (Homebrew, Raycast, AMO, Obsidian, npm,
VS Code, JetBrains):
- Code must be reviewable: no opaque binaries, no obfuscation.
- Downloads must be integrity-checked by hash.
- The trend is toward signed provenance through Sigstore/SLSA (npm, Homebrew, Obsidian, GitHub).
- Every source that discusses provenance also warns that it is not a safety guarantee (S21, S38).

---

## 12. Transferable quality rubric

Each criterion is checkable with a yes/no or a count. The brackets name the ecosystems or standards
it is drawn from; "SS" marks JetBrains search-summary support that was not verified.

### (a) The marketplace / catalogue as a whole
- **A1. Unique, stable identifiers.** Every entry has a unique id, and removed ids are never reused for another package. [VS Code S1 "permanently reserved"; JetBrains S6 "stable ID"; Obsidian S10/S13; Homebrew S25]
- **A2. The catalogue summary equals the package's own summary.** The one-line description in the catalogue matches, character for character, the package manifest's description and the README's short description. [standard-readme S31 "Must match the description in the packager manager's `description` field"; Obsidian S10: the directory reads the manifest at HEAD]
- **A3. Categories come from a closed, published list.** Each entry has at least one category and uses no more than it needs. [VS Code S2; Raycast S17; AMO S27; Chrome S28]
- **A4. No keyword stuffing.** No keyword is repeated unnaturally and no brand lists are used as filler. Keywords are capped where the host caps them. [Chrome S29; AMO S27; VS Code S1 (30)]
- **A5. Published admission and removal policy.** What is required to be listed, what gets an entry removed (malicious, unmaintained, broken), and how to report a problem are all written down. [Obsidian S12; Homebrew S23; AMO S26; VS Code S3 "Report a concern"]
- **A6. Honest scope of endorsement.** The catalogue says what listing does and does not vouch for. [Homebrew S23 "does not imply Homebrew endorsement or support"; npm S21/GitHub S38: provenance is not a safety guarantee]
- **A7. Deprecation is visible.** Deprecated or withdrawn entries are marked, with the alternative where there is one, and are not silently deleted. [VS Code S1 deprecation; Keep a Changelog S32 `[YANKED]`]

### (b) Each plugin package
- **B1. The manifest is at the package root** and has every host-required field: name, version, description, author/publisher/vendor, and compatibility. [VS Code S2; JetBrains S6; Obsidian S13; npm S18]
- **B2. The licence is declared twice and consistently:** an SPDX identifier (or `SEE LICENSE IN <file>`) in the manifest, and a LICENSE file present. [npm S18; VS Code S1/S2/S4; Obsidian S10/S12; Raycast S17]
- **B3. Compatibility is declared as a minimum host version,** with no arbitrary upper cap. [VS Code S1; JetBrains S6 "highly recommended not to set" `until-build`; Obsidian S11]
- **B4. Platform or runtime restrictions are declared** where they exist (desktop-only, OS, arch). [Obsidian S11 `isDesktopOnly`; Raycast S17 `platforms`; VS Code S1 targets; AMO S27]
- **B5. The name is descriptive and not generic.** It does not contain the host's name or the word "plugin", and does not imply first-party status. [Obsidian S13; Raycast S17; npm S18; AMO S26; Chrome S30; JetBrains SS]
- **B6. No template or sample residue** in the README, change notes, icon, placeholder names or sample code. [vsce S4 hard error; Obsidian S11/S14; Raycast S17; JetBrains SS]
- **B7. Only runtime-needed files ship.** No unused assets, duplicate dependencies or redundant code. [VS Code S1 `.vscodeignore`; AMO S26; Raycast S17; JetBrains S8]
- **B8. Repository, homepage and issue-tracker links exist and resolve.** [npm S18; VS Code S2/S4; AMO S27; JetBrains S8]
- **B9. It does what the listing says, and nothing the listing does not say.** [AMO S26 "No Surprises"; Chrome S30; JetBrains SS]

### (c) Each README
- **C1. The README is at the package root** and is what the listing renders. [npm S19 "must"; VS Code S1; Obsidian S10]
- **C2. It answers what the package does, why it is useful, how to get started, and where to get help.** [Open Source Guides S34]
- **C3. It has an Install section and a Usage section, each with a code block,** plus a Dependencies subsection when manual prerequisites exist. [standard-readme S31; npm S19; Raycast S17 "additional setup"]
- **C4. It discloses** network use (which services and why), required accounts, payment, telemetry, and access outside the host's sandbox. [Obsidian S12; AMO S26; Chrome S28]
- **C5. It has no broken links.** Images are HTTPS or repo-relative and resolve from the rendered location. [standard-readme S31; vsce S1/S4; Obsidian S10]
- **C6. It says where to ask questions and whether contributions are accepted.** [standard-readme S31; Open Source Guides S34]
- **C7. It names the licence (SPDX) and its owner.** [standard-readme S31]
- **C8. The title matches the package, folder and repository name,** or the README explains the difference. [standard-readme S31]
- **C9. Screenshots or media, where present, show real features and contain no sensitive data.** [Raycast S17; AMO S27; Chrome S29]

### (d) Versioning, changelog, releases
- **D1. Versions are SemVer `MAJOR.MINOR.PATCH`,** and a breaking change bumps MAJOR. [SemVer S33; npm S20; VS Code S2; JetBrains S6; Obsidian S13]
- **D2. A released version is immutable and its number is never reused.** [SemVer S33 "MUST NOT be modified"; VS Code S1; JetBrains S5; Homebrew S22]
- **D3. The release tag equals the manifest version exactly,** with no `v` prefix where the host demands that. [Obsidian S10/S16]
- **D4. CHANGELOG.md exists** with one entry per version, newest first, ISO dates, grouped by type (Added/Changed/Deprecated/Removed/Fixed/Security), and an Unreleased section. [Keep a Changelog S32; Raycast S17; VS Code S1]
- **D5. Deprecations, removals and breaking changes are always listed,** and yanked versions are marked `[YANKED]`. [Keep a Changelog S32]
- **D6. Stable and pre-release channels are distinguishable.** [Homebrew S22/S24; VS Code S1]

### (e) Trust and security
- **E1. No committed executables or generated binaries in the source tree.** Any binary is traceable to source and a documented build. [OpenSSF S37 Binary-Artifacts; Raycast S17; AMO S26; Homebrew S22]
- **E2. Every downloaded artifact is pinned by SHA-256** in reviewed metadata, and a mismatch fails the install. [Homebrew S22/S25; Raycast S17]
- **E3. Artifacts come from immutable locations the publisher cannot silently rewrite after review.** [Raycast S17; Homebrew S22/S25]
- **E4. Release artifacts carry a signature or provenance attestation,** and the listing tells users how to verify it. [npm S21; Obsidian S15; Homebrew S25; JetBrains S7; VS Code S3; SLSA S35; GitHub S38; Scorecard S37]
- **E5. Publishing uses short-lived CI identity (OIDC) rather than long-lived tokens.** [VS Code S1; npm S21]
- **E6. There is no obfuscation, no remote code loading and no self-updating.** [Obsidian S12; AMO S26; Homebrew S22]
- **E7. A SECURITY.md or equivalent vulnerability-reporting route exists.** [Scorecard S37; standard-readme S31 Security section]
- **E8. The package contains no secrets.** [VS Code S3 secret scanning; Open Source Guides S34]
- **E9. Build and release workflows pin their dependencies by hash** and use least-privilege tokens. [Scorecard S37 Pinned-Dependencies, Token-Permissions]

That is 40 criteria: A1–A7, B1–B9, C1–C9, D1–D6 and E1–E9.
