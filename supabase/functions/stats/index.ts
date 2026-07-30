// Public readership figures for alaskaaihq.com.
//
// Open on purpose, so nothing needs a key to read these numbers: not the daily
// routine, not a script, not a reader. This publication already publishes its
// source archive and its correction log, so publishing its own traffic is the
// consistent choice rather than a brave one.
//
// Returns ONLY aggregates, computed by public.readership_stats in the database.
// No row ever leaves here, and the underlying table holds nothing personal to
// begin with (no cookie, no visitor id, no IP, no user agent, see /privacy/).
//
// verify_jwt is false because the whole point is that a caller needs nothing.
// The service-role key stays server side and is the only thing that can reach
// the aggregate function, so this endpoint is the single door.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const CORS = {
  // Genuinely public data, so any origin may read it.
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Max-Age": "86400",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  if (req.method !== "GET") {
    return new Response(JSON.stringify({ error: "use GET" }), {
      status: 405,
      headers: { ...CORS, "content-type": "application/json" },
    });
  }

  const url = new URL(req.url);
  // The database clamps this to 1..90 as well; parsing defensively here only
  // keeps a junk value from reaching it.
  const raw = parseInt(url.searchParams.get("days") || "7", 10);
  const days = Number.isFinite(raw) ? Math.min(Math.max(raw, 1), 90) : 7;

  const base = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!base || !key) {
    return new Response(JSON.stringify({ error: "not configured" }), {
      status: 503,
      headers: { ...CORS, "content-type": "application/json" },
    });
  }

  try {
    const r = await fetch(`${base}/rest/v1/rpc/readership_stats`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        apikey: key,
        authorization: `Bearer ${key}`,
      },
      body: JSON.stringify({ p_days: days }),
    });
    if (!r.ok) throw new Error(`rpc ${r.status}`);
    const data = await r.json();
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: {
        ...CORS,
        "content-type": "application/json",
        // Cheap to recompute but pointless to recompute per request. Five
        // minutes keeps the figures current without hammering the database.
        "cache-control": "public, max-age=300",
      },
    });
  } catch (_e) {
    // Never leak an internal error shape to a public endpoint.
    return new Response(JSON.stringify({ error: "unavailable" }), {
      status: 502,
      headers: { ...CORS, "content-type": "application/json" },
    });
  }
});
