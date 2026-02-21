import {renderTypeNode, renderTypeUnion} from './type-links.mjs';

function escapeTableCell(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\|/g, '\\|')
    .replace(/\n/g, '<br />');
}

function section(title, content) {
  return `## ${title}\n\n${content}`;
}

function renderFrontmatter(lines = []) {
  if (lines.length === 0) {
    return '';
  }

  return ['---', ...lines, '---', ''].join('\n');
}

function normalizeSignatureUnion(typeInput) {
  if (Array.isArray(typeInput)) {
    return typeInput.join(' | ');
  }

  if (typeof typeInput === 'string') {
    return typeInput
      .split('|')
      .map((part) => part.trim())
      .filter(Boolean)
      .join(' | ');
  }

  return 'unknown';
}

function renderMethodSignature(name, parameters, outputType) {
  const signatureParameters = parameters
    .map((parameter) => `${parameter.name}: ${normalizeSignatureUnion(parameter.type)}`)
    .join(', ');
  const signatureReturn = normalizeSignatureUnion(outputType);
  return `${name}(${signatureParameters}): ${signatureReturn}`;
}

function renderNotes(notes) {
  if (!notes || notes.length === 0) {
    return 'None.';
  }

  return notes.map((note) => `- ${note}`).join('\n');
}

function renderParametersTable(parameters, context) {
  if (!parameters || parameters.length === 0) {
    return 'None.';
  }

  const rows = parameters
    .map((parameter) => {
      const renderedType = renderTypeUnion(parameter.type, context);
      const typeCell = renderedType.markdown.replace(/\|/g, '\\|');
      return `| \`${escapeTableCell(parameter.name)}\` | ${typeCell} | ${escapeTableCell(parameter.description)} |`;
    })
    .join('\n');

  return ['| Name | Type | Description |', '| --- | --- | --- |', rows].join('\n');
}

function collectUnresolvedTypeNotes(unresolvedTypes, prefix) {
  return unresolvedTypes.map((typeName) => `${prefix} unresolved type reference \`${typeName}\`.`);
}

function renderObjectPage(objectDef, normalized) {
  const context = {
    objectTypeSlugs: normalized.objectTypeSlugs,
    linkPrefix: './',
  };

  const objectNotes = [...objectDef.notes];

  const propertiesRows = objectDef.properties
    .map((propertyDef) => {
      const renderedType = renderTypeNode(propertyDef.typeNode, context);
      objectNotes.push(
        ...collectUnresolvedTypeNotes(
          renderedType.unresolvedTypes,
          `Property \`${propertyDef.name}\` contains`,
        ),
      );

      for (const note of propertyDef.notes) {
        objectNotes.push(note);
      }

      const typeCell = renderedType.markdown.replace(/\|/g, '\\|');
      return `| \`${escapeTableCell(propertyDef.name)}\` | ${typeCell} | ${escapeTableCell(propertyDef.description)} |`;
    })
    .join('\n');

  const propertiesSection =
    objectDef.properties.length > 0
      ? ['| Name | Type | Description |', '| --- | --- | --- |', propertiesRows].join('\n')
      : 'None.';

  const methodsSummaryRows = objectDef.methods
    .map((methodDef) => {
      const renderedReturnType = renderTypeUnion(methodDef.outputType, context);
      objectNotes.push(
        ...collectUnresolvedTypeNotes(
          renderedReturnType.unresolvedTypes,
          `Method \`${methodDef.name}\` return type contains`,
        ),
      );
      const returnTypeCell = renderedReturnType.markdown.replace(/\|/g, '\\|');
      return `| \`${escapeTableCell(methodDef.name)}\` | ${returnTypeCell} | ${escapeTableCell(methodDef.description)} |`;
    })
    .join('\n');

  const methodsSummarySection =
    objectDef.methods.length > 0
      ? ['| Method | Returns | Description |', '| --- | --- | --- |', methodsSummaryRows].join('\n')
      : 'None.';

  const methodsDetailSections = objectDef.methods
    .map((methodDef) => {
      const renderedReturnType = renderTypeUnion(methodDef.outputType, context);
      const parameterTypeRenders = methodDef.parameters.map((parameter) =>
        renderTypeUnion(parameter.type, context),
      );

      const methodNotes = [...methodDef.notes];
      methodNotes.push(
        ...collectUnresolvedTypeNotes(
          renderedReturnType.unresolvedTypes,
          `Method \`${methodDef.name}\` return type contains`,
        ),
      );

      methodDef.parameters.forEach((parameter, index) => {
        methodNotes.push(
          ...collectUnresolvedTypeNotes(
            parameterTypeRenders[index].unresolvedTypes,
            `Method \`${methodDef.name}\` parameter \`${parameter.name}\` contains`,
          ),
        );
      });

      return [
        `### ${methodDef.name}`,
        '',
        methodDef.description,
        '',
        '#### Signature',
        '',
        '```ts',
        renderMethodSignature(methodDef.name, methodDef.parameters, methodDef.outputType),
        '```',
        '',
        '#### Parameters',
        '',
        renderParametersTable(methodDef.parameters, context),
        '',
        '#### Returns',
        '',
        renderedReturnType.markdown,
        '',
        '#### Notes',
        '',
        renderNotes([...new Set(methodNotes)]),
      ].join('\n');
    })
    .join('\n\n');

  const notesSection = section('Notes', renderNotes([...new Set(objectNotes)]));

  return [
    renderFrontmatter([`title: ${objectDef.name}`]),
    `# ${objectDef.name}`,
    '',
    section('Description', objectDef.description),
    '',
    section('Properties', propertiesSection),
    '',
    section('Methods Summary', methodsSummarySection),
    '',
    section('Methods', methodsDetailSections || 'None.'),
    '',
    notesSection,
    '',
  ].join('\n');
}

function renderFunctionPage(functionDef, normalized) {
  const context = {
    objectTypeSlugs: normalized.objectTypeSlugs,
    linkPrefix: '../objects/',
  };

  const functionNotes = [...functionDef.notes];

  const overloadSections = functionDef.overloads
    .map((overloadDef, overloadIndex) => {
      const renderedReturnType = renderTypeUnion(overloadDef.outputType, context);
      const overloadNotes = [...overloadDef.notes];

      overloadNotes.push(
        ...collectUnresolvedTypeNotes(
          renderedReturnType.unresolvedTypes,
          `Return type contains`,
        ),
      );

      const parameterTypeRenders = overloadDef.parameters.map((parameter) =>
        renderTypeUnion(parameter.type, context),
      );

      overloadDef.parameters.forEach((parameter, parameterIndex) => {
        overloadNotes.push(
          ...collectUnresolvedTypeNotes(
            parameterTypeRenders[parameterIndex].unresolvedTypes,
            `Parameter \`${parameter.name}\` contains`,
          ),
        );
      });

      functionNotes.push(...overloadNotes);

      return [
        `### Overload ${overloadIndex + 1}`,
        '',
        overloadDef.description,
        '',
        '```ts',
        renderMethodSignature(functionDef.name, overloadDef.parameters, overloadDef.outputType),
        '```',
        '',
        '#### Parameters',
        '',
        renderParametersTable(overloadDef.parameters, context),
        '',
        '#### Returns',
        '',
        renderedReturnType.markdown,
        '',
        '#### Notes',
        '',
        renderNotes([...new Set(overloadNotes)]),
      ].join('\n');
    })
    .join('\n\n');

  return [
    renderFrontmatter([`title: ${functionDef.name}`]),
    `# ${functionDef.name}`,
    '',
    section('Description', functionDef.description),
    '',
    section('Overloads', overloadSections || 'None.'),
    '',
    section('Notes', renderNotes([...new Set(functionNotes)])),
    '',
  ].join('\n');
}

function renderObjectsIndex(objects) {
  const rows = objects
    .map(
      (objectDef) =>
        `| [\`${objectDef.name}\`](./${objectDef.slug}) | ${escapeTableCell(objectDef.description)} | [Open](./${objectDef.slug}) |`,
    )
    .join('\n');

  return [
    renderFrontmatter(['title: Objects', 'sidebar_position: 1']),
    '# Objects',
    '',
    'Reference pages for object types used by the API.',
    '',
    '| Object | Description | Link |',
    '| --- | --- | --- |',
    rows,
    '',
  ].join('\n');
}

function renderFunctionsIndex(functions) {
  const rows = functions
    .map(
      (functionDef) =>
        `| [\`${functionDef.name}\`](./${functionDef.slug}) | ${functionDef.overloads.length} | [Open](./${functionDef.slug}) |`,
    )
    .join('\n');

  return [
    renderFrontmatter(['title: Methods', 'sidebar_position: 1']),
    '# Methods',
    '',
    'Reference pages for callable API functions.',
    '',
    '| Function | Overloads | Link |',
    '| --- | --- | --- |',
    rows,
    '',
  ].join('\n');
}

function renderOverview() {
  return [
    renderFrontmatter(['title: API Overview', 'sidebar_position: 1']),
    '# API Overview',
    '',
    'This reference documents the user-language schema as generated pages.',
    '',
    '## Sections',
    '',
    '- [Objects](./objects)',
    '- [Methods](./functions)',
    '- [Conventions](./conventions)',
    '',
    '## Source of Truth',
    '',
    'All pages in this section are generated from `src/data/user-language.schema.json`.',
    '',
  ].join('\n');
}

function renderConventions() {
  return [
    renderFrontmatter(['title: Conventions', 'sidebar_position: 2']),
    '# Conventions',
    '',
    '## Reference Semantics',
    '',
    '- Parameters typed as `object | string` generally accept an object reference, object id, or variable name.',
    '- Parameters documented as coordinates (`x`, `y`, `z`) are numeric axis-aligned values.',
    '',
    '## Type Notation',
    '',
    '- Union types are shown as `typeA | typeB`.',
    '- `array<...>` indicates an array item type.',
    '- `unknown` indicates missing type data in source and is added by normalization.',
    '',
    '## Units and Coordinates',
    '',
    '- Coordinates are 3D values where applicable.',
    '- Unit behavior is controlled by `setUnit` where supported by the runtime.',
    '',
    '## Overloads',
    '',
    '- Overload sections are ordered by source order after duplicate signatures are merged.',
    '- When duplicates are merged, source variants are listed in Notes.',
    '',
  ].join('\n');
}

export function renderReferenceFiles(normalized) {
  const files = new Map();

  files.set(
    '_category_.json',
    `${JSON.stringify(
      {
        label: 'User-Reference',
        position: 1,
        link: {
          type: 'generated-index',
          description: 'Complete API reference for user language objects and methods.',
        },
      },
      null,
      2,
    )}\n`,
  );

  files.set('overview.md', renderOverview());
  files.set('conventions.md', renderConventions());

  files.set(
    'objects/_category_.json',
    `${JSON.stringify(
      {
        label: 'Objects',
        position: 1,
        link: {
          type: 'generated-index',
          description: 'Object types and instance methods.',
        },
      },
      null,
      2,
    )}\n`,
  );

  files.set('objects/index.md', renderObjectsIndex(normalized.objects));

  for (const objectDef of normalized.objects) {
    files.set(`objects/${objectDef.slug}.md`, renderObjectPage(objectDef, normalized));
  }

  files.set(
    'functions/_category_.json',
    `${JSON.stringify(
      {
        label: 'Methods',
        position: 2,
        link: {
          type: 'generated-index',
          description: 'Global functions and overloads.',
        },
      },
      null,
      2,
    )}\n`,
  );

  files.set('functions/index.md', renderFunctionsIndex(normalized.functions));

  for (const functionDef of normalized.functions) {
    files.set(`functions/${functionDef.slug}.md`, renderFunctionPage(functionDef, normalized));
  }

  return files;
}
