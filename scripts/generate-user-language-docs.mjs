#!/usr/bin/env node
import {promises as fs} from 'node:fs';
import path from 'node:path';
import process from 'node:process';

import {parseAndValidateSchema} from './lib/schema-types.mjs';
import {normalizeSchema} from './lib/normalize-schema.mjs';
import {renderReferenceFiles} from './lib/render-markdown.mjs';

const DEFAULT_INPUT = 'src/data/user-language.schema.json';
const DEFAULT_OUT = 'docs/user-reference';

function parseArgs(argv) {
  const options = {
    input: DEFAULT_INPUT,
    out: DEFAULT_OUT,
    check: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === '--check') {
      options.check = true;
      continue;
    }

    if (arg === '--input') {
      const value = argv[index + 1];
      if (!value) {
        throw new Error('Missing value for --input');
      }
      options.input = value;
      index += 1;
      continue;
    }

    if (arg === '--out') {
      const value = argv[index + 1];
      if (!value) {
        throw new Error('Missing value for --out');
      }
      options.out = value;
      index += 1;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  return options;
}

function normalizeContent(content) {
  const normalized = String(content).replace(/\r\n/g, '\n');
  return normalized.endsWith('\n') ? normalized : `${normalized}\n`;
}

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function listFilesRecursive(rootDirectory) {
  if (!(await pathExists(rootDirectory))) {
    return [];
  }

  const results = [];

  async function walk(currentDirectory) {
    const entries = await fs.readdir(currentDirectory, {withFileTypes: true});
    entries.sort((a, b) => a.name.localeCompare(b.name));

    for (const entry of entries) {
      const absolutePath = path.join(currentDirectory, entry.name);
      if (entry.isDirectory()) {
        await walk(absolutePath);
        continue;
      }

      if (!entry.isFile()) {
        continue;
      }

      const relativePath = path.relative(rootDirectory, absolutePath).split(path.sep).join('/');
      results.push(relativePath);
    }
  }

  await walk(rootDirectory);
  return results.sort((a, b) => a.localeCompare(b));
}

async function writeGeneratedFiles(outDirectory, files) {
  await fs.rm(outDirectory, {recursive: true, force: true});

  for (const [relativePath, content] of files) {
    const absolutePath = path.join(outDirectory, relativePath);
    await fs.mkdir(path.dirname(absolutePath), {recursive: true});
    await fs.writeFile(absolutePath, normalizeContent(content), 'utf8');
  }
}

async function checkGeneratedFiles(outDirectory, files) {
  const expectedRelativePaths = [...files.keys()].sort((a, b) => a.localeCompare(b));
  const expectedSet = new Set(expectedRelativePaths);
  const existingRelativePaths = await listFilesRecursive(outDirectory);

  const missingFiles = expectedRelativePaths.filter((relativePath) => !existingRelativePaths.includes(relativePath));
  const extraFiles = existingRelativePaths.filter((relativePath) => !expectedSet.has(relativePath));
  const changedFiles = [];

  for (const relativePath of expectedRelativePaths) {
    const expected = normalizeContent(files.get(relativePath));
    const absolutePath = path.join(outDirectory, relativePath);

    if (!(await pathExists(absolutePath))) {
      continue;
    }

    const actual = normalizeContent(await fs.readFile(absolutePath, 'utf8'));
    if (actual !== expected) {
      changedFiles.push(relativePath);
    }
  }

  if (missingFiles.length === 0 && extraFiles.length === 0 && changedFiles.length === 0) {
    return {
      ok: true,
      message: 'Generated docs are up-to-date.',
    };
  }

  const messageLines = ['Generated docs are out-of-date.'];

  if (missingFiles.length > 0) {
    messageLines.push('Missing files:');
    for (const relativePath of missingFiles) {
      messageLines.push(`- ${relativePath}`);
    }
  }

  if (changedFiles.length > 0) {
    messageLines.push('Changed files:');
    for (const relativePath of changedFiles) {
      messageLines.push(`- ${relativePath}`);
    }
  }

  if (extraFiles.length > 0) {
    messageLines.push('Extra files:');
    for (const relativePath of extraFiles) {
      messageLines.push(`- ${relativePath}`);
    }
  }

  return {
    ok: false,
    message: messageLines.join('\n'),
  };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));

  const inputPath = path.resolve(process.cwd(), options.input);
  const outPath = path.resolve(process.cwd(), options.out);

  const rawSchemaText = await fs.readFile(inputPath, 'utf8');
  const validatedSchema = parseAndValidateSchema(rawSchemaText);
  const normalizedSchema = normalizeSchema(validatedSchema);
  const renderedFiles = renderReferenceFiles(normalizedSchema);

  if (options.check) {
    const result = await checkGeneratedFiles(outPath, renderedFiles);
    if (!result.ok) {
      console.error(result.message);
      process.exitCode = 1;
      return;
    }

    console.log(result.message);
    return;
  }

  await writeGeneratedFiles(outPath, renderedFiles);
  console.log(`Generated ${renderedFiles.size} files in ${options.out}`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
