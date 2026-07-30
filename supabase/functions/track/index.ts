// Readership collector for alaskaaihq.com.
//
// Records that a page was read. Records NOTHING about who read it: no cookie is
// set or read, no visitor id is minted, and the IP and user agent are used only
// in memory (to bucket a device class and drop bots) and are never written
// anywhere. That is what lets the site run without a consent banner and say so
// publicly on /privacy/.
//
// Every response is 204, deliberately: the collector never tells a caller whether
// it recorded. That also meant it never told the OWNER, so a silently dropped
// beacon was indistinguishable from a stored one, and three real visits arrived,
// answered 204, and wrote nothing with no way to see which guard ate them.
// console.log does not surface in the queryable log stream, so every drop now
// writes a REASON to page_view_drops. Reason and timestamp only, nothing about
// the reader.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const ALLOWED_ORIGINS = [
  "https://alaskaaihq.com",
  "https://www.alaskaaihq.com",
];

// Obvious automation. A JS beacon already excludes most crawlers (they do not
// run scripts), so this is a second line rather than the only one. Anchored on
// purpose: an unanchored /bot/ or /preview/ can fire on an ordinary browser
// token, and a bot filter that eats real readers is worse than none.
const BOT = /(bot\b|bot\/|crawler|crawling|spider|slurp|headless|\bcurl\/|wget|python-requests|node-fetch|go-http|okhttp|libwww|scrapy|lighthouse|pingdom|uptime|facebookexternalhit|embedly|slackbot|discordbot|whatsapp|telegrambot)/i;

function cors(origin: string | null) {
  const allow = origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Max-Age": "86400",
  };
}

function deviceClass(ua: string): string {
  const s = ua.toLowerCase();
  if (/ipad|tablet|kindle|playbook|silk/.test(s)) return "tablet";
  if (/mobi|android|iphone|ipod|phone/.test(s)) return "mobile";
  if (/mozilla|chrome|safari|firefox|edge|opera/.test(s)) return "desktop";
  return "other";
}

function cleanPath(raw: unknown): string | null {
  if (typeof raw !== "string" || !raw) return null;
  let p = raw.split("#")[0].split("?")[0].trim();
  if (!p.startsWith("/")) return null;
  if (p.length > 300) p = p.slice(0, 300);
  if (p.includes("..") || p.startsWith("//")) return null;
  return p;
}

function refHost(raw: unknown): string | null {
  if (typeof raw !== "string" || !raw) return null;
  try {
    const h = new URL(raw).hostname.toLowerCase().replace(/^www\./, "");
    if (!h || h.length > 120) return null;
    if (h === "alaskaaihq.com") return null;
    return h;
  } catch {
    return null;
  }
}

function campaign(raw: unknown): string | null {
  if (typeof raw !== "string" || !raw) return null;
  const c = raw.trim().slice(0, 60);
  return /^[a-z0-9_.-]+$/i.test(c) ? c : null;
}

const SB_URL = Deno.env.get("SUPABASE_URL");
const SB_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");

async function insert(table: string, row: unknown): Promise<boolean> {
  if (!SB_URL || !SB_KEY) return false;
  try {
    const r = await fetch(`${SB_URL}/rest/v1/${table}`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        apikey: SB_KEY,
        authorization: `Bearer ${SB_KEY}`,
        prefer: "return=minimal",
      },
      body: JSON.stringify(row),
    });
    return r.ok;
  } catch {
    return false;
  }
}

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("origin");
  const headers = cors(origin);
  const reply = () => new Response(null, { status: 204, headers });
  const drop = async (reason: string) => {
    await insert("page_view_drops", { reason });
    return reply();
  };

  if (req.method === "OPTIONS") return reply();
  if (req.method !== "POST") return new Response(null, { status: 405, headers });

  // Browser-level opt-outs, honoured server side too. A browser may send these
  // headers WITHOUT exposing them to JavaScript, so this is the path that
  // actually catches a privacy-minded reader whose client-side check passed.
  if (req.headers.get("dnt") === "1") return await drop("dnt-header");
  if (req.headers.get("sec-gpc") === "1") return await drop("gpc-header");

  const ua = req.headers.get("user-agent") || "";
  if (!ua) return await drop("no-user-agent");
  if (BOT.test(ua)) return await drop("bot-user-agent");

  let body: Record<string, unknown> = {};
  try {
    body = await req.json();
  } catch {
    return await drop("unparseable-body");
  }

  const path = cleanPath(body.p);
  if (!path) return await drop("bad-path");

  if (!SB_URL || !SB_KEY) return reply();

  const ok = await insert("page_views", {
    path,
    ref_host: refHost(body.r),
    campaign: campaign(body.c),
    device: deviceClass(ua),
    country: (req.headers.get("cf-ipcountry") || req.headers.get("x-country-code") || "")
      .slice(0, 2).toUpperCase() || null,
  });
  // A failed insert used to be swallowed entirely, which is how a working beacon
  // and an empty table could coexist with nothing to explain it.
  if (!ok) await insert("page_view_drops", { reason: "insert-failed" });
  return reply();
});
