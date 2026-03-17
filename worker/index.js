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

    const url = new URL(request.url);

    if (url.pathname === '/events') {
      if (request.method === 'GET') {
        const data = await env.EVENTS.get('events', 'text');
        return new Response(data || '[]', {
          headers: { ...cors, 'Content-Type': 'application/json' }
        });
      }

      if (request.method === 'PUT') {
        const body = await request.text();
        // Validate it's valid JSON array
        try {
          const parsed = JSON.parse(body);
          if (!Array.isArray(parsed)) throw new Error('Not an array');
        } catch (e) {
          return new Response(JSON.stringify({ error: 'Invalid JSON array' }), {
            status: 400,
            headers: { ...cors, 'Content-Type': 'application/json' }
          });
        }
        await env.EVENTS.put('events', body);
        return new Response(JSON.stringify({ ok: true }), {
          headers: { ...cors, 'Content-Type': 'application/json' }
        });
      }
    }

    return new Response('Not found', { status: 404, headers: cors });
  }
};
