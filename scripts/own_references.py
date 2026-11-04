"""
Small reference solutions written by us, used as an extra oracle in
build_new_inputs.py for problems where CodeContests has no Python 3 solution.
Each one follows the problem statement directly and favours clarity over speed.
"""
APPU = r'''
n=int(input()); h=list(map(int,input().split()))
def odd(x):
    while x%2==0: x//=2
    return x
print("YES" if len({odd(x) for x in h})==1 else "NO")
'''
CHANDU = r'''
import sys
d=sys.stdin.read().split(); i=0; t=int(d[i]); i+=1; out=[]
for _ in range(t):
    n,m=int(d[i]),int(d[i+1]); i+=2
    a=list(map(int,d[i:i+n])); i+=n; b=list(map(int,d[i:i+m])); i+=m
    out.append(" ".join(map(str,sorted(a+b,reverse=True))))
print("\n".join(out))
'''
COMM3 = r'''
import sys
d=list(map(int,sys.stdin.read().split())); i=1; out=[]
for _ in range(d[0]):
    R=d[i]; p=[(d[i+1],d[i+2]),(d[i+3],d[i+4]),(d[i+5],d[i+6])]; i+=7
    ok=lambda a,b:(a[0]-b[0])**2+(a[1]-b[1])**2<=R*R
    c=ok(p[0],p[1])+ok(p[0],p[2])+ok(p[1],p[2])
    out.append("yes" if c>=2 else "no")
print("\n".join(out))
'''
LUCKYBAL = r'''
import sys
d=sys.stdin.read().split(); out=[]
for s in d[1:1+int(d[0])]:
    n=len(s); total=n*(n+1)//2; run=0; sevens=0
    for ch in s+"4":
        if ch=="7": run+=1
        else: sevens+=run*(run+1)//2; run=0
    out.append(str(total-sevens))
print("\n".join(out))
'''
MONKS = r'''
import sys
d=sys.stdin.read().split(); i=1; out=[]
for _ in range(int(d[0])):
    n,k=int(d[i]),int(d[i+1]); i+=2
    bits=sorted((bin(int(x)).count("1") for x in d[i:i+n]),reverse=True); i+=n
    out.append(str(sum(bits[:k])))
print("\n".join(out))
'''
ROYS = r'''
import sys
L=sys.stdin.read().split(); n=int(L[0]); days=L[1:1+n]
def longest(s):
    b=c=0
    for ch in s:
        c=c+1 if ch=="C" else 0
        b=max(b,c)
    return b
print(max(longest(x) for x in days), longest("".join(days)))
'''
OWN = {"appu_and_sugarcane_farm": [APPU], "chandu_and_his_girlfriend_returns": [CHANDU],
       "comm3": [COMM3], "luckybal": [LUCKYBAL], "monks_choice_of_numbers_1": [MONKS],
       "roys_life_cycle": [ROYS]}
