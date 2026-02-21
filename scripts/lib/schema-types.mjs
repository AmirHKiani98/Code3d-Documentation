function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function assert(condition, path, message) {
  if (!condition) {
    throw new Error(`[schema:${path}] ${message}`);
  }
}

function assertOptionalString(value, path) {
  if (value === undefined) {
    return undefined;
  }
  assert(typeof value === 'string', path, 'Expected a string.');
  return value;
}

function assertString(value, path) {
  assert(typeof value === 'string', path, 'Expected a string.');
  return value;
}

function normalizeTypeUnion(value, path) {
  if (typeof value === 'string') {
    return [value];
  }

  assert(Array.isArray(value), path, 'Expected type to be a string or string array.');
  assert(value.length > 0, path, 'Type array cannot be empty.');

  return value.map((entry, index) => {
    assert(typeof entry === 'string', `${path}[${index}]`, 'Type entries must be strings.');
    return entry;
  });
}

function normalizeTypeNode(value, path) {
  if (typeof value === 'string' || Array.isArray(value)) {
    return {type: normalizeTypeUnion(value, path)};
  }

  assert(isPlainObject(value), path, 'Expected a type node object.');

  const type = normalizeTypeUnion(value.type, `${path}.type`);
  const description = assertOptionalString(value.description, `${path}.description`);
  const items =
    value.items === undefined ? undefined : normalizeTypeNode(value.items, `${path}.items`);

  return {type, description, items};
}

function normalizeParameter(value, path) {
  assert(isPlainObject(value), path, 'Expected a parameter object.');

  const name = assertString(value.name, `${path}.name`);
  const type = normalizeTypeUnion(value.type, `${path}.type`);
  const description = assertOptionalString(value.description, `${path}.description`);

  return {
    name,
    type,
    description,
  };
}

function normalizeMethodLike(value, path) {
  assert(isPlainObject(value), path, 'Expected a method/function object.');

  const kind = assertOptionalString(value.type, `${path}.type`) ?? 'function';
  assert(kind === 'function', `${path}.type`, 'Expected value "function" when provided.');

  const description = assertOptionalString(value.description, `${path}.description`);

  const rawParameters = value.parameters ?? [];
  assert(Array.isArray(rawParameters), `${path}.parameters`, 'Expected an array.');
  const parameters = rawParameters.map((parameter, index) =>
    normalizeParameter(parameter, `${path}.parameters[${index}]`),
  );

  const outputType = assertOptionalString(value.outputType, `${path}.outputType`);

  return {
    type: 'function',
    description,
    parameters,
    outputType,
  };
}

function normalizeProperty(value, path) {
  assert(isPlainObject(value), path, 'Expected a property object.');

  return normalizeTypeNode(value, path);
}

function normalizeObjectDefinition(value, path) {
  assert(isPlainObject(value), path, 'Expected an object definition.');

  const type = assertString(value.type, `${path}.type`);
  const description = assertOptionalString(value.description, `${path}.description`);

  const rawProperties = value.properties ?? {};
  assert(isPlainObject(rawProperties), `${path}.properties`, 'Expected an object map.');
  const properties = {};
  for (const [propertyName, propertyDef] of Object.entries(rawProperties)) {
    properties[propertyName] = normalizeProperty(propertyDef, `${path}.properties.${propertyName}`);
  }

  const rawMethods = value.methods ?? {};
  assert(isPlainObject(rawMethods), `${path}.methods`, 'Expected an object map.');
  const methods = {};
  for (const [methodName, methodDef] of Object.entries(rawMethods)) {
    methods[methodName] = normalizeMethodLike(methodDef, `${path}.methods.${methodName}`);
  }

  return {
    type,
    description,
    properties,
    methods,
  };
}

function normalizeFunctionOverload(value, path) {
  return normalizeMethodLike(value, path);
}

export function validateSchema(rawSchema) {
  assert(isPlainObject(rawSchema), '$', 'Expected top-level JSON object.');

  const rawObjects = rawSchema.objects;
  const rawFunctions = rawSchema.functions;

  assert(isPlainObject(rawObjects), '$.objects', 'Missing or invalid objects map.');
  assert(isPlainObject(rawFunctions), '$.functions', 'Missing or invalid functions map.');

  const objects = {};
  for (const [objectName, objectDefinition] of Object.entries(rawObjects)) {
    objects[objectName] = normalizeObjectDefinition(objectDefinition, `$.objects.${objectName}`);
  }

  const functions = {};
  for (const [functionName, overloads] of Object.entries(rawFunctions)) {
    assert(Array.isArray(overloads), `$.functions.${functionName}`, 'Expected an overload array.');
    assert(overloads.length > 0, `$.functions.${functionName}`, 'Overload array cannot be empty.');

    functions[functionName] = overloads.map((overload, index) =>
      normalizeFunctionOverload(overload, `$.functions.${functionName}[${index}]`),
    );
  }

  return {
    objects,
    functions,
  };
}

export function parseAndValidateSchema(jsonText) {
  let parsed;
  try {
    parsed = JSON.parse(jsonText);
  } catch (error) {
    throw new Error(`Invalid JSON: ${error instanceof Error ? error.message : String(error)}`);
  }

  return validateSchema(parsed);
}
