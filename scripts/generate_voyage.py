import os,json,datetime,urllib.request
from pathlib import Path
U=os.getenv("GITHUB_USER","estkayon"); T=os.getenv("GH_TOKEN",""); R=Path(__file__).resolve().parents[1]; A=R/"assets"
now=datetime.datetime.now(datetime.timezone.utc).date()
months=[]
for k in range(7,-1,-1):
 n=now.month-1-k; y=now.year+n//12; m=n%12+1; st=datetime.date(y,m,1); en=datetime.date(y+(m==12),1 if m==12 else m+1,1)-datetime.timedelta(days=1); months.append((st,min(en,now)))
def get(url,method="GET",data=None,headers=None):
 h={"User-Agent":"profile-analytics"}
 if headers:h.update(headers)
 q=urllib.request.Request(url,data=data,headers=h,method=method)
 with urllib.request.urlopen(q,timeout=30) as z:return z.read()
def text(x,y,v,c="#E8F1FF",sz=14,weight="400",anchor="start"):
 v=str(v).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
 return f'<text x="{x}" y="{y}" fill="{c}" font-family="ui-monospace,Consolas,monospace" font-size="{sz}" font-weight="{weight}" text-anchor="{anchor}">{v}</text>'
daily={}; vals=[0]*8; best={"date":str(now),"count":0}
if T:
 q="query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"
 try:
  body=json.dumps({"query":q,"variables":{"login":U,"from":months[0][0].isoformat()+"T00:00:00Z","to":(now+datetime.timedelta(days=1)).isoformat()+"T00:00:00Z"}}).encode()
  out=json.loads(get("https://api.github.com/graphql","POST",body,{"Authorization":"Bearer "+T,"Content-Type":"application/json"}))
  for wk in out.get("data",{}).get("user",{}).get("contributionsCollection",{}).get("contributionCalendar",{}).get("weeks",[]):
   for day in wk.get("contributionDays",[]):
    d=datetime.date.fromisoformat(day["date"]); c=int(day["contributionCount"])
    if months[0][0]<=d<=now:daily[d]=c
  vals=[sum(c for d,c in daily.items() if st<=d<=en) for st,en in months]
  if daily:
   d,c=max(daily.items(),key=lambda x:x[1]);best={"date":d.isoformat(),"count":c}
 except Exception as e:print("GraphQL contribution data unavailable:",e)
mx=max(vals) or 1
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330"><defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#35D6C5"/><stop offset="1" stop-color="#176B87"/></linearGradient></defs><rect width="1200" height="330" rx="18" fill="#071525" stroke="#21415A"/>']
for g in range(5):
 y=245-g*48;p.append(f'<path d="M75 {y}H1140" stroke="#20384D" stroke-dasharray="4 7"/>');p.append(text(60,y+5,round(mx*g/4),"#8DA5BA",12,"400","end"))
for i,(lab,v) in enumerate(zip([st.strftime("%b %Y") for st,en in months],vals)):
 x=110+i*135;h=int(170*v/mx);p.append(f'<rect x="{x}" y="{245-h}" width="66" height="{max(2,h)}" rx="8" fill="url(#b)"/>');p.append(text(x+33,max(25,235-h),v,"#FFF1C1",14,"700","middle"));p.append(text(x+33,278,lab,"#C9D8E8",13,"500","middle"))
p += [text(38,35,"LAST 8 MONTHS / MONTHLY CONTRIBUTIONS","#F4C542",17,"700"),text(1160,35,"AUTO-UPDATED","#35D6C5",12,"700","end"),"</svg>"]
(A/"voyage-monthly.svg").write_text("".join(p))
# Public repository language bytes
langs={}
try:
 h={"Accept":"application/vnd.github+json"}
 if T:h["Authorization"]="Bearer "+T
 repos=json.loads(get(f"https://api.github.com/users/{U}/repos?per_page=100&type=owner&sort=updated",headers=h))
 for repo in repos:
  if repo.get("fork"):continue
  try:
   for n,v in json.loads(get(repo["languages_url"],headers=h)).items():langs[n]=langs.get(n,0)+int(v)
  except Exception:pass
except Exception as e:print("Language data unavailable:",e)
total=sum(langs.values()) or 1; top=sorted(langs.items(),key=lambda x:x[1],reverse=True)[:8] or [("No data",1)]
colors=["#35D6C5","#F4C542","#D62828","#60A5FA","#C084FC","#FB923C","#A3E635","#CBD5E1"]
z=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280"><rect width="1200" height="280" rx="18" fill="#071525" stroke="#21415A"/>',text(32,38,"PUBLIC REPOSITORY LANGUAGE SHARE","#F4C542",17,"700")]
for i,(n,v) in enumerate(top):
 col=i%2;row=i//2;x=35+col*585;y=80+row*47;pc=v*100/total
 z.extend([text(x,y,n,"#E8F1FF",14,"600"),f'<rect x="{x+145}" y="{y-13}" width="300" height="12" rx="6" fill="#152A3C"/>',f'<rect x="{x+145}" y="{y-13}" width="{3*pc:.1f}" height="12" rx="6" fill="{colors[i%8]}"/>',text(x+470,y,f"{pc:.1f}%","#FFF1C1",13,"700")])
z += [text(1160,258,"Language-byte share, not skill rating","#8DA5BA",11,"400","end"),"</svg>"];(A/"tech-stack-usage.svg").write_text("".join(z))
# Night city: each day with contributions creates a lit building; height reflects count.
c=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470"><defs><linearGradient id="n" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#08172C"/><stop offset="1" stop-color="#10152E"/></linearGradient></defs><rect width="1200" height="470" rx="18" fill="url(#n)" stroke="#21415A"/>']
for i in range(100):c.append(f'<circle cx="{(i*97+41)%1190+5}" cy="{(i*53+23)%250+8}" r="{1+i%3*.3}" fill="#DCEBFF" opacity=".6"/>')
c += [text(30,35,"COMMIT CITY / LAST 8 MONTHS","#F4C542",16,"700"),text(1170,35,"BUILDINGS = CONTRIBUTING DAYS","#35D6C5",11,"600","end")]
days=[];d=months[0][0]
while d<=now:
 if daily.get(d,0)>0:days.append((d,daily[d]))
 d+=datetime.timedelta(days=1)
if len(days)>100:days=[days[int(i*len(days)/100)] for i in range(100)]
if not days:c.append(text(600,235,"Run workflow to load GitHub contribution data","#FFF1C1",15,"600","middle"))
else:
 maxc=max(v for d,v in days) or 1;bw=max(4,min(10,1060/len(days)));gap=2;startx=(1200-len(days)*(bw+gap))/2
 for i,(day,v) in enumerate(days):
  h=50+150*v/maxc;x=startx+i*(bw+gap);y=385-h;c.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="1.5" fill="#1C6D8C" stroke="#35D6C5" stroke-opacity=".4"/>')
  for j in range(max(1,min(5,round(v/maxc*5)))):
   wy=y+12+j*16
   if wy<380:c.append(f'<rect x="{x+bw*.25:.1f}" y="{wy:.1f}" width="{max(1,bw*.35):.1f}" height="4" fill="#F4C542"/>')
 c.append('<path d="M35 386H1165" stroke="#F4C542" stroke-opacity=".6"/>')
 for i,(st,en) in enumerate(months):c.append(text(35+i*145,420,st.strftime("%b %Y"),"#D7E4F2",12,"500"))
 c.extend([text(35,448,f"Best day: {best['date']} · {best['count']} contributions","#FFF1C1",13,"700"),text(1165,448,f"{sum(vals)} contributions in window","#35D6C5",12,"600","end")])
c.append("</svg>");(A/"commit-skyline.svg").write_text("".join(c))
# Best-day spotlight, with a pulsing beam and a simple floating Gear-5-inspired silhouette.
b=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250" viewBox="0 0 1200 250"><defs><linearGradient id="bg"><stop stop-color="#08172C"/><stop offset="1" stop-color="#20234C"/></linearGradient><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#FFF1C1" stop-opacity=".95"/><stop offset="1" stop-color="#F4C542" stop-opacity="0"/></linearGradient></defs><rect width="1200" height="250" rx="18" fill="url(#bg)" stroke="#21415A"/>']
for i in range(55):b.append(f'<circle cx="{(i*67+31)%1180+10}" cy="{(i*31+13)%230+8}" r="{1+i%2}" fill="#E8F1FF" opacity=".65"/>')
b.extend([text(35,42,"☀ BEST CONTRIBUTION DAY","#F4C542",18,"700"),text(35,88,best["date"],"#FFF1C1",23,"700"),text(35,125,f'{best["count"]} contributions',"#35D6C5",18,"700"),text(35,180,"The spotlight moves when a new record appears.","#CBD5E1",14)])
b.append('<path d="M910 15L790 250H1120L1000 15Z" fill="url(#beam)" opacity=".7"><animate attributeName="opacity" values=".35;.9;.35" dur="3s" repeatCount="indefinite"/></path>')
b.append('<g transform="translate(955 94)"><ellipse cy="4" rx="39" ry="9" fill="#FFF1C1" opacity=".45"/><circle cy="-27" r="15" fill="#FFF1C1"/><path d="M-14 -36Q0 -52 17 -34L13 -29L-15 -29Z" fill="#D62828" stroke="#F4C542" stroke-width="2"/><path d="M-8 -10L-28 19L-11 31L5 4L19 31L34 18L12 -11Z" fill="#FFF1C1" stroke="#35D6C5" stroke-width="2"/><path d="M-12 -6L-44 -19L-52 -7L-26 8M12 -6L42 -24L52 -13L25 8" fill="none" stroke="#FFF1C1" stroke-width="8" stroke-linecap="round"/><path d="M-8 27L-23 61L-8 66L7 36M12 28L28 60L42 55L28 23" fill="none" stroke="#FFF1C1" stroke-width="9" stroke-linecap="round"/><animateTransform attributeName="transform" type="translate" values="955 94;955 80;955 94" dur="2.4s" repeatCount="indefinite"/></g>')
b += [text(1160,224,"LIVE DATA · AUTO-UPDATED","#35D6C5",11,"700","end"),"</svg>"];(A/"best-day.svg").write_text("".join(b))
