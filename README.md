# OWASP ASVS 5.0.0 as a SteerSpec Standard Realm

This repo holds the realm `dev.steerspec.std.owasp.asvs.v5`, a transcription of the
[OWASP Application Security Verification Standard](https://github.com/OWASP/ASVS) 5.0.0.

A project that depends on it can be measured against the **whole** standard, at a chosen level, rather
than only against the clauses it happened to map.

> This is SteerSpec's transcription, not an OWASP publication. The standard's text is OWASP's.
> Report a transcription error here. Report an issue with the standard itself to
> [OWASP/ASVS](https://github.com/OWASP/ASVS).

## Status

Bootstrapping. The realm manifest is in place, with no rules yet. Next:

- [#1](https://github.com/steerspec-hub/strspc-hb-std-owasp-asvs/issues/1): generate the 70 L1
  requirements from OWASP's machine-readable release.
- [#2](https://github.com/steerspec-hub/strspc-hb-std-owasp-asvs/issues/2): the crosswalk from
  4.0.3 to 5.0.0.

## Layout

The realm follows the core Standard Realm rules (STDRLM) of `dev.steerspec.core`:

- `rules/realm.json` declares `"kind": "standard"`, the edition, the licence, the attribution and the
  profiles `L1`, `L2` and `L3`.
- Each chapter is an entity (`V1`) and each section a sub-entity (`V1S1`).
- Each requirement becomes one or more rules, in the standard's order. A requirement with more than one
  sentence becomes one rule per sentence. Every rule carries the standard's number in `clause` (for
  example `V1.1.1`) and its levels in `profiles`.
- The rules are generated from OWASP's JSON with `strspc entity add` and `strspc rule add`. No rule
  JSON is written by hand.
- The rules are Published once checked against the source, and never Implemented: a standard is
  measured against, not evaluated against code.

## Using it

Declare the realm as a dependency in your own `realm.json`, and link a Standard Reference to it:

```json
{
  "realm_id": "dev.steerspec.std.owasp.asvs.v5",
  "version": "<release>",
  "source": "github://steerspec-hub/strspc-hb-std-owasp-asvs@v<release>/rules"
}
```

Then `strspc standards coverage` reports which clauses your rules cover, which are mapped but not yet
enforced, and which nobody mapped, against the clause total of your level.

## Licence

The standard's text is © the OWASP Foundation, licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). This transcription is released under
the same licence; see [LICENSE](LICENSE). Rendering these rules into your own documents may put that
output under CC BY-SA too.
