// Rewrites root-absolute links ("/clinical-safety/start-here") in the built HTML
// into relative ones ("../clinical-safety/start-here.html"), so the site works
// from any folder or domain without extra configuration.
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const dist = new URL('../dist/', import.meta.url).pathname;

function walk(dir) {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}

for (const file of walk(dist).filter((f) => f.endsWith('.html'))) {
  const depth = relative(dist, file).split(sep).length - 1;
  const prefix = depth ? '../'.repeat(depth) : './';
  let html = readFileSync(file, 'utf8');
  html = html.replace(/(href|src)="\/(?!\/)([^"]*)"/g, (_, attr, rest) => {
    let [path, hash = ''] = rest.split('#');
    if (path === '' || path.endsWith('/')) path += 'index.html';
    else if (!/\.[a-z0-9]+$/i.test(path)) path += '.html';
    return `${attr}="${prefix}${path}${hash ? '#' + hash : ''}"`;
  });
  writeFileSync(file, html);
}
console.log('Relative links written.');
