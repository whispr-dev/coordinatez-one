import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),dir=path.join(root,'dist');
const input=process.argv[2];
let url;try{url=new URL(input);}catch{throw Error('Usage: node scripts/configure-origin.mjs https://your-domain.example');}
if(url.protocol!=='https:'||url.username||url.password||url.search||url.hash||url.pathname!=='/')throw Error('Use a plain HTTPS origin, with no path or credentials.');
const origin=url.origin;
let html=fs.readFileSync(path.join(dir,'index.html'),'utf8').replace(/<link rel="canonical"[^>]*>/g,'').replace(/<meta property="og:url"[^>]*>/g,'').replace(/<meta property="og:image"[^>]*>/,`<meta property="og:image" content="${origin}/og.jpg">`);
html=html.replace('</head>',`<link rel="canonical" href="${origin}/"><meta property="og:url" content="${origin}/"></head>`);
fs.writeFileSync(path.join(dir,'index.html'),html);
fs.writeFileSync(path.join(dir,'robots.txt'),`User-agent: *\nAllow: /\n\nSitemap: ${origin}/sitemap.xml\n`);
fs.writeFileSync(path.join(dir,'sitemap.xml'),`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${['/','/about.html','/privacy.html'].map(p=>`  <url><loc>${origin}${p}</loc></url>`).join('\n')}\n</urlset>\n`);
fs.writeFileSync(path.join(dir,'llms.txt'),`# Coordinates\n\n> Free GPS coordinate converter and interactive world time globe by whispr.dev.\n\n- [Tool](${origin}/): Convert WGS 84 latitude/longitude between decimal and DMS. Explore civil clocks and representative IANA time zone locations on a draggable globe.\n- [About and data](${origin}/about.html)\n- [Privacy](${origin}/privacy.html)\n- [whispr.dev](https://whispr.dev/)\n- [SkeleTrace](https://skeletrace.com/)\n\nTimezone lookup is approximate near boundaries. Globe meridians are solar guides, not political timezone boundaries. Clocks use the device clock and browser timezone rules.\n`);
fs.writeFileSync(path.join(dir,'site.json'),JSON.stringify({title:'Coordinates',type:'website',card:'custom',url:origin+'/',image:origin+'/og.jpg',banner:origin+'/x-banner.jpg',author:'whispr.dev',version:'1.0.0'},null,2)+'\n');
console.log('Metadata configured for '+origin);
