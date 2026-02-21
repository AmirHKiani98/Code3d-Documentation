import {slugify} from './slugify.mjs';

function dedupe(values) {
  return [...new Set(values)];
}

function defaultDescription(value, fallback, notes, noteText) {
  if (typeof value === 'string' && value.trim().length > 0) {
    return value.trim();
  }

  if (noteText) {
    notes.push(noteText);
  }

  return fallback;
}

function normalizeParameter(parameter, index, notes) {
  const description = defaultDescription(
    parameter.description,
    'No description provided.',
    notes,
    `Parameter \`${parameter.name}\` is missing a description in source; defaulted to "No description provided."`,
  );

  return {
    name: parameter.name || `param${index + 1}`,
    type: Array.isArray(parameter.type) && parameter.type.length > 0 ? parameter.type : ['unknown'],
    description,
  };
}

function normalizeMethodLike(definition) {
  const notes = [];

  const description = defaultDescription(
    definition.description,
    'No description provided.',
    notes,
    'Description is missing in source; defaulted to "No description provided."',
  );

  const outputType = defaultDescription(
    definition.outputType,
    'unknown',
    notes,
    'Output type is missing in source; defaulted to `unknown`.',
  );

  const parameters = (definition.parameters || []).map((parameter, index) =>
    normalizeParameter(parameter, index, notes),
  );

  return {
    description,
    outputType,
    parameters,
    notes,
  };
}

function signatureKey(functionName, overload) {
  const parameters = overload.parameters
    .map((parameter) => `${parameter.name}:${parameter.type.join('|')}`)
    .join(',');

  return `${functionName}(${parameters}):${overload.outputType}`;
}

function normalizeObjects(rawObjects) {
  const objectNames = Object.keys(rawObjects).sort((a, b) => a.localeCompare(b));

  return objectNames.map((objectName) => {
    const objectDef = rawObjects[objectName];
    const objectNotes = [];

    const description = defaultDescription(
      objectDef.description,
      'No description provided.',
      objectNotes,
      'Description is missing in source; defaulted to "No description provided."',
    );

    const propertyNames = Object.keys(objectDef.properties || {}).sort((a, b) => a.localeCompare(b));
    const properties = propertyNames.map((propertyName) => {
      const propertyDef = objectDef.properties[propertyName];
      const propertyNotes = [];
      const propertyDescription = defaultDescription(
        propertyDef.description,
        'No description provided.',
        propertyNotes,
        `Property \`${propertyName}\` is missing a description in source; defaulted to "No description provided."`,
      );

      return {
        name: propertyName,
        typeNode: propertyDef,
        description: propertyDescription,
        notes: propertyNotes,
      };
    });

    const methodNames = Object.keys(objectDef.methods || {}).sort((a, b) => a.localeCompare(b));
    const methods = methodNames.map((methodName) => {
      const methodDef = objectDef.methods[methodName];
      const normalized = normalizeMethodLike(methodDef);
      return {
        name: methodName,
        ...normalized,
      };
    });

    return {
      name: objectName,
      slug: slugify(objectName),
      description,
      notes: objectNotes,
      properties,
      methods,
    };
  });
}

function normalizeFunctions(rawFunctions) {
  const functionNames = Object.keys(rawFunctions).sort((a, b) => a.localeCompare(b));

  return functionNames.map((functionName) => {
    const overloads = rawFunctions[functionName];
    const seenBySignature = new Map();
    const normalizedOverloads = [];

    overloads.forEach((sourceOverload, sourceIndex) => {
      const normalized = normalizeMethodLike(sourceOverload);
      const key = signatureKey(functionName, normalized);
      const sourceEntry = {
        sourceIndex: sourceIndex + 1,
        description: normalized.description,
      };

      const existing = seenBySignature.get(key);
      if (!existing) {
        const overload = {
          index: normalizedOverloads.length + 1,
          signature: key,
          description: normalized.description,
          outputType: normalized.outputType,
          parameters: normalized.parameters,
          notes: [...normalized.notes],
          sourceVariants: [sourceEntry],
        };
        seenBySignature.set(key, overload);
        normalizedOverloads.push(overload);
        return;
      }

      existing.sourceVariants.push(sourceEntry);

      const isDescriptionVariant =
        normalized.description.trim().toLowerCase() !== existing.description.trim().toLowerCase();
      if (isDescriptionVariant) {
        existing.notes.push(
          `Source variant description: "${normalized.description.replace(/"/g, '\\"')}"`,
        );
      }
    });

    const functionNotes = [];
    if (normalizedOverloads.length < overloads.length) {
      functionNotes.push(
        `Normalized ${overloads.length} source overload entries into ${normalizedOverloads.length} unique signature(s).`,
      );
    }

    for (const overload of normalizedOverloads) {
      if (overload.sourceVariants.length > 1) {
        overload.notes.push(
          `Merged ${overload.sourceVariants.length} source variants with the same signature.`,
        );

        const variantDescriptions = dedupe(overload.sourceVariants.map((entry) => entry.description)).filter(
          (description) => description !== overload.description,
        );

        if (variantDescriptions.length > 0) {
          overload.notes.push(
            `Additional source descriptions: ${variantDescriptions
              .map((description) => `"${description.replace(/"/g, '\\"')}"`)
              .join('; ')}`,
          );
        }
      }

      overload.notes = dedupe(overload.notes);
    }

    const functionDescription =
      normalizedOverloads.length > 0
        ? normalizedOverloads[0].description
        : 'No description provided.';

    return {
      name: functionName,
      slug: slugify(functionName),
      description: functionDescription,
      notes: functionNotes,
      overloads: normalizedOverloads,
    };
  });
}

export function normalizeSchema(schema) {
  const objects = normalizeObjects(schema.objects);
  const functions = normalizeFunctions(schema.functions);

  const objectTypeSlugs = {};
  for (const objectDef of objects) {
    objectTypeSlugs[objectDef.name] = objectDef.slug;
  }

  return {
    objects,
    functions,
    objectTypeSlugs,
  };
}
