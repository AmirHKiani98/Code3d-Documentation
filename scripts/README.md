# API Docs Generator

This project generates modular Docusaurus reference docs from a single schema file.

## Source of Truth

- Schema input: `src/data/user-language.schema.json`
- Generator entrypoint: `scripts/generate-user-language-docs.mjs`
- Helper modules: `scripts/lib/*`

## Commands

- Generate docs: `npm run docs:generate:api`
- Check docs are up to date: `npm run docs:check:api`

Generated files are written to `docs/user-reference`.

## Normalization Rules

- Function overloads are deduplicated by canonical signature:
  - `functionName + ordered params(name+types) + outputType`
- The first matching overload is canonical.
- Duplicate variants are merged and noted in each function page.
- Missing `outputType` is normalized to `unknown` and noted.
- Missing parameter descriptions default to `No description provided.` and are noted.
- Unresolved type references are rendered as code and recorded in Notes sections.

## Resolving Unresolved Types

If generated docs report unresolved types (example: `edge`):

1. Add the missing type to `objects` in `src/data/user-language.schema.json`, or
2. Update schema type values to an existing object type, or
3. Keep as-is if intentionally external and rely on Notes for clarity.

After changing the schema, regenerate docs.
