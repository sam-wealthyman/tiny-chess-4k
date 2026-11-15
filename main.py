import json,os
from urllib.request import Request,urlopen
E=os.environ.get("MAKEFUN_ENV_URL")
M=9999
L=int(os.environ.get("NODES",40000))
W={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0,'.':0}
D={'N':(-21,-19,-12,-8,8,12,19,21),'B':(-11,-9,9,11),'R':(-10,-1,1,10)}
D['Q']=D['K']=D['B']+D['R']
R={95:'KQ',25:'kq',98:'K',91:'Q',28:'k',21:'q'}
def V(x,i):
    u=x.upper();r,f=divmod(i,10);r-=2;f-=1;a=abs(2*f-7);c=-a-abs(2*r-7)
    if x=='p':r=7-r
    z={'P':(6-r)*6-a*3,'N':c*3,'B':c*3,'Q':c}.get(u,0)
    return(W[u]+z)*(1 if x==u else-1)
def put(b,i,c):return b[:i]+c+b[i+1:]
def gen(p,q):
    b,s,c,e,_=p;w=s<1;o=str.isupper if w else str.islower;k=str.islower if w else str.isupper
    for i,x in enumerate(b):
        if not o(x):continue
        u=x.upper()
        if u=='P':
            d=-10 if w else 10
            for t in(i+d-1,i+d+1):
                if k(b[t])or t==e:yield i,t
            t=i+d
            if b[t]=='.'and(not q or t//10 in(2,9)):
                yield i,t
                if i//10==(8 if w else 3)and b[t+d]=='.'and not q:yield i,t+d
            continue
        if u=='K'and not q and i==(95 if w else 25):
            if x in c and b[i+1]==b[i+2]=='.':yield i,i+2
            if chr(ord(x)+6)in c and b[i-1]==b[i-2]==b[i-3]=='.':yield i,i-2
        for d in D[u]:
            t=i+d
            while 1:
                y=b[t]
                if y=='#'or o(y):break
                if y!='.'or not q:yield i,t
                if y!='.'or u in'NK':break
                t+=d
def mk(p,m):
    b,s,c,e,v=p;i,t=m;x=b[i];y=b[t];z=x;P=x in'Pp'
    if y!='.':v-=V(y,t)
    if P and t//10 in(2,9):z='Q'if x=='P'else'q'
    n=put(b,i,'.')
    if P and t==e:
        o=t+10 if x=='P'else t-10;v-=V(b[o],o);n=put(n,o,'.')
    n=put(n,t,z);v+=V(z,t)-V(x,i)
    if x in'Kk'and abs(t-i)==2:
        a=i+3 if t>i else i-4;n=put(put(n,a,'.'),(i+t)//2,b[a])
    for q in(i,t):
        for r in R.get(q,''):c=c.replace(r,'')
    return n,1-s,c,(i+t)//2 if P and abs(t-i)==20 else 0,v
def S(p,d,a,b):
    global N
    N+=1
    if N>L:raise KeyError
    v=p[4]*(1-2*p[1]);q=d<1;r=v
    if q:
        if v>=b:return v
        a=max(a,v)
    else:r=-M
    g=p[0]
    for m in sorted(gen(p,q),key=lambda m:W[g[m[0]].upper()]-W[g[m[1]].upper()]*10):
        if g[m[1]]in'Kk':return M+d
        r=max(r,-S(mk(p,m),d-1,-b,-a));a=max(a,r)
        if a>=b:break
    if r<-M//2 and not q and not any(g[m[1]]in'Kk'for m in gen((g,1-p[1],'',0,0),1)):return 0
    return r
def U(i):return'abcdefgh'[i%10-1]+str(10-i//10)
def mv(p,m):
    i,t=m
    return U(i)+U(t)+('q'if p[0][i]in'Pp'and t//10 in(2,9)else'')
def FEN(f):
    a=f.split();b='#'*20
    for r in a[0].split('/'):b+='#'+''.join('.'*int(c)if c.isdigit()else c for c in r)+'#'
    p=0 if a[3]=='-'else 10*(10-int(a[3][1]))+ord(a[3][0])-96
    p=(b+'#'*20,int(a[1]=='b'),a[2],p,0)
    return p[:4]+(sum(V(x,i)for i,x in enumerate(p[0])if x not in'.#'),)
def pick(p,leg,seen):
    global N
    N=0;ms=[m for m in gen(p,0)if mv(p,m)in leg]or[None];best=ms[0]
    for d in range(1,30):
        try:
            sc=[]
            for j,m in enumerate(ms):
                n=mk(p,m);s=-S(n,d-1,-M*3,M*3)
                if n[0]in seen:s=0
                sc.append((-s,j,m))
            sc.sort();ms=[x[2]for x in sc];best=ms[0]
            if sc[0][0]<-M//2:break
        except KeyError:break
    return best
def post(a,d):return json.load(urlopen(Request(E+a,json.dumps(d).encode(),{"content-type":"application/json"})))
while E:
    g=post("/game",{});seen=set()
    if g["status"]=="done":break
    while g["status"]=="your_move":
        p=FEN(g["fen"]);seen.add(p[0]);leg=g["legal_moves"];m=pick(p,leg,seen)
        u=mv(p,m)if m else leg[0];seen.add(mk(p,m)[0])if m else 0
        g=post("/move",{"game":g["game"],"move":u})
