import json,re,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
# Major city coordinates are city centres, rather than IANA's reference stations.
major=[('Greenwich','Europe/London',51.4779,-.0015),('London','Europe/London',51.5074,-.1278),('New York','America/New_York',40.7128,-74.006),('Los Angeles','America/Los_Angeles',34.0522,-118.2437),('Chicago','America/Chicago',41.8781,-87.6298),('Vancouver','America/Vancouver',49.2827,-123.1207),('Mexico City','America/Mexico_City',19.4326,-99.1332),('São Paulo','America/Sao_Paulo',-23.5505,-46.6333),('Buenos Aires','America/Argentina/Buenos_Aires',-34.6037,-58.3816),('Reykjavík','Atlantic/Reykjavik',64.1466,-21.9426),('Paris','Europe/Paris',48.8566,2.3522),('Berlin','Europe/Berlin',52.52,13.405),('Kyiv','Europe/Kyiv',50.4501,30.5234),('Cairo','Africa/Cairo',30.0444,31.2357),('Lagos','Africa/Lagos',6.5244,3.3792),('Johannesburg','Africa/Johannesburg',-26.2041,28.0473),('Nairobi','Africa/Nairobi',-1.2921,36.8219),('Istanbul','Europe/Istanbul',41.0082,28.9784),('Dubai','Asia/Dubai',25.2048,55.2708),('Tehran','Asia/Tehran',35.6892,51.389),('Karachi','Asia/Karachi',24.8607,67.0011),('Delhi','Asia/Kolkata',28.6139,77.209),('Kathmandu','Asia/Kathmandu',27.7172,85.324),('Dhaka','Asia/Dhaka',23.8103,90.4125),('Yangon','Asia/Yangon',16.8409,96.1735),('Bangkok','Asia/Bangkok',13.7563,100.5018),('Singapore','Asia/Singapore',1.3521,103.8198),('Hong Kong','Asia/Hong_Kong',22.3193,114.1694),('Beijing','Asia/Shanghai',39.9042,116.4074),('Tokyo','Asia/Tokyo',35.6762,139.6503),('Seoul','Asia/Seoul',37.5665,126.978),('Perth','Australia/Perth',-31.9523,115.8613),('Adelaide','Australia/Adelaide',-34.9285,138.6007),('Sydney','Australia/Sydney',-33.8688,151.2093),('Auckland','Pacific/Auckland',-36.8485,174.7633),('Chatham Islands','Pacific/Chatham',-43.9535,-176.5597),('Honolulu','Pacific/Honolulu',21.3099,-157.8581),('Anchorage','America/Anchorage',61.2181,-149.9003),('St John’s','America/St_Johns',47.5615,-52.7126),('Kiritimati','Pacific/Kiritimati',1.8721,-157.4278),('Pago Pago','Pacific/Pago_Pago',-14.2756,-170.702)]
priority=['Greenwich','New York','Tokyo','Sydney','London','Delhi','Kathmandu','Los Angeles','São Paulo','Dubai','Auckland','Chatham Islands']
major.sort(key=lambda c: priority.index(c[0]) if c[0] in priority else 100)
cities=[dict(name=n,zone=z,lat=a,lon=b,major=True) for n,z,a,b in major]
seen={c['zone'] for c in cities}
def coord(s):
 m=re.fullmatch(r'([+-])(\d{2})(\d{2})(\d{2})?([+-])(\d{3})(\d{2})(\d{2})?',s)
 if not m: raise ValueError(s)
 a,b,c,d,e,f,g,h=m.groups();return ((int(b)+int(c)/60+int(d or 0)/3600)*(-1 if a=='-' else 1),(int(f)+int(g)/60+int(h or 0)/3600)*(-1 if e=='-' else 1))
for line in (root/'zone.tab').read_text().splitlines():
 if not line or line.startswith('#'):continue
 cells=line.split('\t');zone=cells[2]
 if zone in seen:continue
 a,b=coord(cells[1]);cities.append(dict(name=zone.split('/')[-1].replace('_',' '),zone=zone,lat=round(a,6),lon=round(b,6),major=False));seen.add(zone)
land=json.loads((root/'land.geojson').read_text())
(root/'dist/data.js').write_text('/* Natural Earth public domain; IANA zone.tab — see about.html. */\nwindow.COORD_DATA='+json.dumps(dict(cities=cities,land=land),separators=(',',':'))+';\n')
print(f'{len(cities)} representative locations; {len(seen)} civil time zones')
