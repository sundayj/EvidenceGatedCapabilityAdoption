import Koa from 'koa';

function freshStore() {
  return {
    p1: { id: 'p1', ownerId: 'alice', name: 'Alpha', archived: false, labels: [] },
    p2: { id: 'p2', ownerId: 'bob', name: 'Beta', archived: false, labels: [] },
  };
}

function matchProjectMutation(path) {
  const match = /^\/projects\/([^/]+)\/(archive|rename|labels)$/.exec(path);
  return match ? { id: match[1], op: match[2] } : null;
}

export function createApp() {
  const app = new Koa();
  const store = freshStore();

  app.use(async (ctx, next) => {
    const user = ctx.get('x-user');
    ctx.state.user = user === 'alice' || user === 'bob' ? user : null;
    await next();
  });

  app.use(async (ctx, next) => {
    if (ctx.method !== 'POST') return next();
    const match = matchProjectMutation(ctx.path);
    if (!match) return next();

    const project = store[match.id];
    if (!project) {
      ctx.status = 404;
      ctx.body = { error: 'not-found' };
      return;
    }
    if (!ctx.state.user) {
      ctx.status = 401;
      ctx.body = { error: 'sign-in-required' };
      return;
    }
    if (project.ownerId !== ctx.state.user) {
      ctx.status = 403;
      ctx.body = { error: 'forbidden' };
      return;
    }

    ctx.state.projectMutation = { ...match, project };
    await next();
  });

  app.use(async (ctx) => {
    if (ctx.method === 'GET') {
      const match = /^\/projects\/([^/]+)$/.exec(ctx.path);
      if (match) {
        const project = store[match[1]];
        if (!project) {
          ctx.status = 404;
          ctx.body = { error: 'not-found' };
          return;
        }
        ctx.body = project;
        return;
      }
    }

    const mutation = ctx.state.projectMutation;
    if (ctx.method === 'POST' && mutation) {
      const { op, project } = mutation;
      if (op === 'archive') project.archived = true;
      if (op === 'rename') project.name = ctx.query.name || project.name;
      if (op === 'labels') {
        const label = ctx.query.label;
        if (label) project.labels.push(label);
      }
      ctx.body = project;
      return;
    }

    ctx.status = 404;
    ctx.body = { error: 'not-found' };
  });

  return app;
}
