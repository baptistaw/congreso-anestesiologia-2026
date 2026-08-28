export default {
  async fetch(request, env) {
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: cors });
    }

    // no-store: el programa se edita en vivo, y sin esta cabecera el navegador
    // servía datos viejos aunque KV ya estuviera actualizado.
    const json = (obj, status = 200) => new Response(
      typeof obj === 'string' ? obj : JSON.stringify(obj),
      {
        status,
        headers: {
          ...cors,
          'Content-Type': 'application/json',
          'Cache-Control': 'no-store, must-revalidate',
        },
      }
    );

    const url = new URL(request.url);

    // ── Programa: key fija "events", validada como array ──────────────
    if (url.pathname === '/events') {
      if (request.method === 'GET') {
        const data = await env.EVENTS.get('events', 'text');
        return json(data || '[]');
      }
      if (request.method === 'PUT') {
        const body = await request.text();
        try {
          if (!Array.isArray(JSON.parse(body))) throw new Error('Not an array');
        } catch (e) {
          return json({ error: 'Invalid JSON array' }, 400);
        }
        await env.EVENTS.put('events', body);
        return json({ ok: true });
      }
    }

    // ── KV genérico: /kv/<key> — GET/PUT de cualquier JSON válido ──────
    // Habilita formularios (key "forms" y "resp_<formId>") y reutilización
    // futura de la plataforma. Key restringida a [A-Za-z0-9_-].
    const m = url.pathname.match(/^\/kv\/([A-Za-z0-9_-]{1,120})$/);
    if (m) {
      const key = 'kv_' + m[1];
      if (request.method === 'GET') {
        const data = await env.EVENTS.get(key, 'text');
        return json(data || 'null');
      }
      if (request.method === 'PUT') {
        const body = await request.text();
        try {
          JSON.parse(body);
        } catch (e) {
          return json({ error: 'Invalid JSON' }, 400);
        }
        if (body.length > 900000) return json({ error: 'Too large' }, 413);
        await env.EVENTS.put(key, body);
        return json({ ok: true });
      }
    }

    return new Response('Not found', { status: 404, headers: cors });
  }
};
