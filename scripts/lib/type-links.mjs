const PRIMITIVE_TYPES = new Set([
  'number',
  'string',
  'boolean',
  'void',
  'object',
  'function',
  'array',
  'unknown',
]);

function dedupe(values) {
  return [...new Set(values)];
}

function splitUnionToken(token) {
  return String(token)
    .split('|')
    .map((part) => part.trim())
    .filter(Boolean);
}

function normalizeUnion(typeInput) {
  if (Array.isArray(typeInput)) {
    return typeInput.flatMap(splitUnionToken);
  }

  if (typeof typeInput === 'string') {
    return splitUnionToken(typeInput);
  }

  return [];
}

function renderAtomicType(typeName, {objectTypeSlugs, linkPrefix}) {
  const slug = objectTypeSlugs[typeName];
  if (slug) {
    return {
      markdown: `[\`${typeName}\`](${linkPrefix}${slug})`,
      unresolvedTypes: [],
    };
  }

  if (PRIMITIVE_TYPES.has(typeName)) {
    return {
      markdown: `\`${typeName}\``,
      unresolvedTypes: [],
    };
  }

  return {
    markdown: `\`${typeName}\``,
    unresolvedTypes: [typeName],
  };
}

export function renderTypeUnion(typeInput, context) {
  const union = normalizeUnion(typeInput);
  const parts = [];
  const unresolved = [];

  for (const typeName of union) {
    const rendered = renderAtomicType(typeName, context);
    parts.push(rendered.markdown);
    unresolved.push(...rendered.unresolvedTypes);
  }

  return {
    markdown: parts.join(' | ') || '`unknown`',
    unresolvedTypes: dedupe(unresolved),
  };
}

export function renderTypeNode(typeNode, context) {
  if (!typeNode || typeof typeNode !== 'object') {
    return {
      markdown: '`unknown`',
      unresolvedTypes: [],
    };
  }

  const union = Array.isArray(typeNode.type) ? typeNode.type : [];
  const unresolved = [];
  const parts = [];

  for (const typeName of union) {
    if (typeName === 'array' && typeNode.items) {
      const renderedItem = renderTypeNode(typeNode.items, context);
      parts.push(`\`array\` of ${renderedItem.markdown}`);
      unresolved.push(...renderedItem.unresolvedTypes);
      continue;
    }

    const rendered = renderAtomicType(typeName, context);
    parts.push(rendered.markdown);
    unresolved.push(...rendered.unresolvedTypes);
  }

  return {
    markdown: parts.join(' | ') || '`unknown`',
    unresolvedTypes: dedupe(unresolved),
  };
}
