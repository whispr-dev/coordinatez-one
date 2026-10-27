import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),d=path.join(root,'dist');
const required=['index.html','style.css','app.js','core.js','data.js','og.jpg','x-banner.jpg','favicon.svg','site.json','robots.txt','sitemap.xml','llms.txt','cookies.txt','README.md','about.html','privacy.html','vendor/d3.min.js','vendor/tz.js'];
for(const file of required){if(!fs.statSync(path.join(d,file)).size)throw Error('Empty asset: '+file);}
const s=JSON.parse(fs.readFileSync(path.join(d,'site.json'))),html=fs.readFileSync(path.join(d,'index.html'),'utf8');
if(s.title!=='Coordinates'||s.type!=='website'||s.card!=='custom')throw Error('Invalid site metadata');
for(const text of ['whispr.dev','© 2026 whispr.dev','https://skeletrace.com/'])if(!html.includes(text))throw Error('Missing brand '+text);
for(const match of html.matchAll(/(?:src|href)="([^"#]+)"/g)){const ref=match[1];if(!ref.includes(':')&&!fs.existsSync(path.join(d,ref)))throw Error('Missing local resource: '+ref);}
if(fs.readdirSync(d).some(f=>f.startsWith('__qa')))throw Error('Remove temporary QA pages before shipping');
console.log('Brand and static asset check: OK');
