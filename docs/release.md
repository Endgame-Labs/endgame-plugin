# Packaging And Release

Git is the canonical plugin package. The self-hosted marketplace resolves the
plugin from the repository root, and the release ZIP is a deterministic
rendering of the same tracked runtime files.

## Build And Verify Locally

Run from the repository root:

```bash
make check
claude plugin validate . --strict
make package
make smoke-package
```

The package command writes:

```text
dist/endgame-plugin-<manifest-version>.zip
```

The builder includes the plugin manifest, license, MCP configuration, and every
tracked file under the seven approved public skill directories. It uses sorted
paths and fixed ZIP timestamps, rejects unsafe paths, untracked skill resources,
and non-file Git entries, and reads packaged bytes and modes directly from
`HEAD`. It verifies that the ZIP file list exactly matches the committed Git
runtime payload, so uncommitted working-tree changes cannot alter the archive.

## Prepare A Release

1. Merge reviewed runtime changes with a corresponding version bump in
   `.claude-plugin/plugin.json`.
2. Confirm `main` passes every required check.
3. Create an annotated `vMAJOR.MINOR.PATCH` tag whose version exactly matches
   the plugin manifest.
4. Push the tag.

For example:

```bash
git switch main
git pull --ff-only
git tag -s v0.1.7 -m "Endgame plugin v0.1.7"
git push origin v0.1.7
```

The `release` workflow checks out the fully qualified tag, verifies that its
peeled commit is both `HEAD` and part of `main`, reruns repository and official
Claude validation, builds the deterministic ZIP, generates its SHA-256 file,
and attaches both files to the matching GitHub Release. A manual rerun succeeds
for an existing release only when both published assets byte-for-byte match the
new deterministic build; it never replaces published assets.

## Version And Marketplace Behavior

`.claude-plugin/plugin.json` is the sole plugin version source. Claude uses that
version as its cache key, so every runtime change requires a version bump. Pull
request CI enforces this rule and requires the new semantic version to be
greater than the version on the current `main` branch. The `main` ruleset uses
strict required checks so a stale pull request must revalidate after another
runtime release merges.

The Endgame-hosted marketplace uses `"source": "./"`, so Git installations and
tagged archives derive from the same repository content. After Anthropic accepts
the plugin into its directory, Anthropic mirrors future public-repository
updates and owns the external marketplace pin.

## Release Automation Boundary

Release Please is intentionally deferred. The repository currently restricts
all branch and tag creation to an explicit maintainer bypass, while Release
Please needs an automation identity that can create release branches and tags.
Add it only after defining a dedicated release identity and a narrowly reviewed
ruleset bypass. Do not grant every GitHub Actions workflow unrestricted ref
write access merely to enable automated tagging.
