// Builds dist/search-index.json from the built pages: one entry per page section (split at h2s),
// so search results can jump straight to the right part of a page. Runs before relativise.mjs.
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const dist = new URL('../dist/', import.meta.url).pathname;
const walk = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? walk(p) : [p]; });
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;|&#x27;|&rsquo;|&lsquo;/g, '’').replace(/&nbsp;/g, ' ').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n));
const text = (h) => decode(h.replace(/<(script|style|svg|nav|button|sup)[\s\S]*?<\/\1>/gi, ' ').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

const out = [];
for (const file of walk(dist).filter((f) => f.endsWith('.html'))) {
  const url = relative(dist, file).split(sep).join('/');
  if (url === '404.html' || url === 'about.html') continue;
  const zone = { 'clinical-safety': 'Clinical safety', 'information-governance': 'Information governance', 'ai-policy': 'AI policy', explainers: 'Explainers', templates: 'Templates' }[url.split('/')[0]];
  const html = readFileSync(file, 'utf8');
  const title = decode((html.match(/<title>([^<]*)<\/title>/) || [, ''])[1]).split(' | ')[0].trim();
  const lede = text((html.match(/<p class="lede">([\s\S]*?)<\/p>/) || [, ''])[1]);
  let body = (html.match(/<article class="prose">([\s\S]*)<\/article>/) || html.match(/<main[^>]*>([\s\S]*?)<\/main>/) || [, ''])[1];
  body = body.replace(/<ol class="refs"[\s\S]*?<\/ol>/g, '');
  const parts = body.split(/(?=<h2[^>]*>)/);
  parts.forEach((part, i) => {
    const h = part.match(/^<h2[^>]*?(?:id="([^"]*)")?[^>]*>([\s\S]*?)<\/h2>/);
    const heading = h ? text(h[2]) : '';
    const id = h && h[1] ? h[1] : '';
    const t = text(h ? part.slice(h[0].length) : part);
    if (!t && !heading) return;
    out.push({ u: url + (id ? '#' + id : ''), p: (zone && url.includes('/') ? zone + ' › ' : '') + title, h: heading, t: (i === 0 && lede ? lede + ' ' : '') + t.slice(0, 3000) });
  });
}
const { keyterms } = await import(new URL('../src/data/keyterms.js', import.meta.url));
for (const k of keyterms) {
  for (const [label, href] of k.go) out.unshift({ u: href.replace(/^\//, '').replace(/(^|\/)([^/#]+)(#|$)/, (m, a, b, c) => a + b + '.html' + c), p: k.t, h: label, t: k.d, a: k.aka, k: 1 });
}
writeFileSync(join(dist, 'search-index.json'), JSON.stringify(out));
console.log(`Search index: ${out.length} sections.`);
