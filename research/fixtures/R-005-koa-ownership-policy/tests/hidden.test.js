import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const appPath = process.env.BENCH_APP || path.join(process.cwd(), 'baseline', 'app.js');
const moduleUrl = `${pathToFileURL(path.resolve(appPath)).href}?case=${Date.now()}`;
const { createApp } = await import(moduleUrl);

async function withServer(fn) {
  const app = createApp();
  const server = app.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const address = server.address();
  const base = `http://127.0.0.1:${address.port}`;
  try {
    await fn(base);
  } finally {
    await new Promise((resolve, reject) => server.close((err) => (err ? reject(err) : resolve())));
  }
}

async function request(base, method, route, user) {
  const response = await fetch(`${base}${route}`, {
    method,
    headers: user ? { 'x-user': user } : {},
  });
  const body = await response.json();
  return { status: response.status, body };
}

test('core owner can add a label', async () => {
  await withServer(async (base) => {
    const result = await request(base, 'POST', '/projects/p1/labels?label=urgent', 'alice');
    assert.equal(result.status, 200);
    assert.deepEqual(result.body.labels, ['urgent']);
  });
});

test('core non-owner cannot add a label and no side effect occurs', async () => {
  await withServer(async (base) => {
    const denied = await request(base, 'POST', '/projects/p2/labels?label=hijack', 'alice');
    assert.equal(denied.status, 403);
    const after = await request(base, 'GET', '/projects/p2');
    assert.deepEqual(after.body.labels, []);
  });
});

test('core missing project keeps not-found behavior', async () => {
  await withServer(async (base) => {
    const result = await request(base, 'POST', '/projects/missing/labels?label=x', 'alice');
    assert.equal(result.status, 404);
    assert.deepEqual(result.body, { error: 'not-found' });
  });
});

test('regression owners can still archive and rename', async () => {
  await withServer(async (base) => {
    const archived = await request(base, 'POST', '/projects/p1/archive', 'alice');
    assert.equal(archived.status, 200);
    assert.equal(archived.body.archived, true);

    const renamed = await request(base, 'POST', '/projects/p2/rename?name=Gamma', 'bob');
    assert.equal(renamed.status, 200);
    assert.equal(renamed.body.name, 'Gamma');
  });
});

test('security non-owner cannot archive another project', async () => {
  await withServer(async (base) => {
    const denied = await request(base, 'POST', '/projects/p2/archive', 'alice');
    assert.equal(denied.status, 403);
    const after = await request(base, 'GET', '/projects/p2');
    assert.equal(after.body.archived, false);
  });
});

test('security non-owner cannot rename another project and no side effect occurs', async () => {
  await withServer(async (base) => {
    const denied = await request(base, 'POST', '/projects/p2/rename?name=OwnedByAlice', 'alice');
    assert.equal(denied.status, 403);
    const after = await request(base, 'GET', '/projects/p2');
    assert.equal(after.body.name, 'Beta');
  });
});
