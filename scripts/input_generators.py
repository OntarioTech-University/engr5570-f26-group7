"""
Random generators of VALID inputs, one per CodeContests problem in our study.

Each generator takes (rng, size) and returns one input string.
  size is "tiny", "small", "medium" or "large". Limits follow the problem
  statement; "large" stays well under the limits so the original Python
  programs finish inside the 5-second timeout of Part 2.
Problems that "guarantee" something (connected graph, valid permutation,
unique answer, ...) build the input so the guarantee holds.
"""
import string

LOW = string.ascii_lowercase
N = {"tiny": 3, "small": 10, "medium": 200, "large": 3000}  # rough scale


def _ints(xs):
    return " ".join(map(str, xs))


# ----------------------------------------------------------------- Codeforces
def g_101_C(r, s):                       # vectors A, B, C, |coord| <= 1e8
    lim = {"tiny": 2, "small": 10, "medium": 1000, "large": 10**8}[s]
    v = lambda: (r.randint(-lim, lim), r.randint(-lim, lim))
    A, C = v(), v()
    if r.random() < 0.5:                 # build a reachable B half of the time
        x, y = A
        for _ in range(r.randint(0, 3)):
            x, y = y, -x
        k1, k2 = r.randint(-3, 3), r.randint(-3, 3)
        cx, cy = C
        B = (x + k1 * cx + k2 * cy, y + k1 * cy - k2 * cx)
        if max(abs(B[0]), abs(B[1])) > 10**8:
            B = v()
    else:
        B = v()
    if r.random() < 0.1:
        C = (0, 0)
    return f"{A[0]} {A[1]}\n{B[0]} {B[1]}\n{C[0]} {C[1]}\n"


def g_1037_E(r, s):                      # n m k, m distinct new edges
    n = {"tiny": r.randint(2, 4), "small": r.randint(2, 10),
         "medium": r.randint(10, 200), "large": r.randint(500, 2000)}[s]
    maxm = n * (n - 1) // 2
    m = r.randint(1, min(maxm, {"tiny": 6, "small": 30, "medium": 800, "large": 4000}[s]))
    k = r.randint(1, min(n - 1, 4))
    seen, edges = set(), []
    while len(edges) < m:
        x, y = r.sample(range(1, n + 1), 2)
        if (min(x, y), max(x, y)) not in seen:
            seen.add((min(x, y), max(x, y)))
            edges.append((x, y))
    return f"{n} {m} {k}\n" + "".join(f"{x} {y}\n" for x, y in edges)


def g_1107_D(r, s):                      # n divisible by 4, hex rows
    n = {"tiny": 4, "small": r.choice([4, 8, 12]), "medium": r.choice([16, 24, 32, 48, 64]),
         "large": r.choice([200, 400, 600])}[s]
    divs = [d for d in range(1, n + 1) if n % d == 0]
    x = r.choice(divs)                   # plant an x-compressible matrix
    blocks = [[r.randint(0, 1) for _ in range(n // x)] for _ in range(n // x)]
    rows = [[blocks[i // x][j // x] for j in range(n)] for i in range(n)]
    if r.random() < 0.3:                 # sometimes break it in one cell
        i, j = r.randrange(n), r.randrange(n)
        rows[i][j] ^= 1
    out = [str(n)]
    for row in rows:
        out.append("".join("%X" % int("".join(map(str, row[c:c + 4])), 2) for c in range(0, n, 4)))
    return "\n".join(out) + "\n"


def g_1208_D(r, s):                      # build s from a hidden permutation
    n = {"tiny": r.randint(1, 3), "small": r.randint(1, 10), "medium": r.randint(10, 300),
         "large": r.randint(1000, 5000)}[s]
    p = list(range(1, n + 1))
    mode = r.random()
    if mode < 0.15:
        p.sort()
    elif mode < 0.3:
        p.sort(reverse=True)
    else:
        r.shuffle(p)
    # s_i = sum of earlier smaller values, O(n log n) with a Fenwick tree
    tree = [0] * (n + 1)
    res = []
    for v in p:
        i, acc = v - 1, 0
        while i > 0:
            acc += tree[i]
            i -= i & -i
        res.append(acc)
        i = v
        while i <= n:
            tree[i] += v
            i += i & -i
    return f"{n}\n{_ints(res)}\n"


def g_1227_D1(r, s):                     # n, m <= 100
    n = {"tiny": r.randint(1, 3), "small": r.randint(1, 10), "medium": r.randint(10, 60),
         "large": 100}[s]
    hi = r.choice([3, 10, 10**9])        # small ranges give many ties
    a = [r.randint(1, hi) for _ in range(n)]
    m = {"tiny": r.randint(1, 3), "small": r.randint(1, 10), "medium": r.randint(10, 60),
         "large": 100}[s]
    q = []
    for _ in range(m):
        k = r.randint(1, n)
        q.append(f"{k} {r.randint(1, k)}")
    return f"{n}\n{_ints(a)}\n{m}\n" + "\n".join(q) + "\n"


def _connected_simple(r, n, m, wmax):
    edges, seen = [], set()
    nodes = list(range(1, n + 1))
    r.shuffle(nodes)
    for i in range(1, n):                # random spanning tree first
        u, v = nodes[i], nodes[r.randrange(i)]
        seen.add((min(u, v), max(u, v)))
        edges.append((u, v, r.randint(1, wmax)))
    while len(edges) < m:
        u, v = r.sample(range(1, n + 1), 2)
        key = (min(u, v), max(u, v))
        if key not in seen:
            seen.add(key)
            edges.append((u, v, r.randint(1, wmax)))
    r.shuffle(edges)
    return edges


def g_1253_F(r, s):                      # connected simple weighted graph
    n = {"tiny": r.randint(2, 4), "small": r.randint(2, 10), "medium": r.randint(10, 200),
         "large": r.randint(1000, 3000)}[s]
    k = r.randint(2, n)
    maxm = n * (n - 1) // 2
    m = r.randint(n - 1, min(maxm, max(n - 1, {"tiny": 6, "small": 25, "medium": 600, "large": 6000}[s])))
    wmax = r.choice([5, 100, 10**9])
    q = r.randint(1, {"tiny": 3, "small": 10, "medium": 200, "large": 3000}[s])
    out = [f"{n} {m} {k} {q}"] + [f"{u} {v} {w}" for u, v, w in _connected_simple(r, n, m, wmax)]
    for _ in range(q):
        a, b = r.sample(range(1, k + 1), 2)
        out.append(f"{a} {b}")
    return "\n".join(out) + "\n"


def _strong_digraph(r, n, extra):
    """Strongly connected digraph: a random Hamiltonian cycle plus extra arcs."""
    if n == 1:
        return []
    order = list(range(1, n + 1))
    r.shuffle(order)
    arcs = {(order[i], order[(i + 1) % n]) for i in range(n)}
    if n == 2:
        return sorted(arcs)
    tries = 0
    while len(arcs) < n + extra and tries < 10 * (n + extra):
        tries += 1
        u, v = r.sample(range(1, n + 1), 2)
        arcs.add((u, v))
    arcs = list(arcs)
    r.shuffle(arcs)
    return arcs


def g_1361_E(r, s):                      # t strongly connected digraphs
    t = {"tiny": 1, "small": r.randint(1, 4), "medium": r.randint(1, 10), "large": r.randint(5, 20)}[s]
    cap = {"tiny": 4, "small": 8, "medium": 60, "large": 400}[s]
    out = [str(t)]
    for _ in range(t):
        n = r.randint(1, cap)
        extra = r.choice([0, 1, 2, n // 3, n])  # few extra arcs keep many "interesting" cities
        arcs = _strong_digraph(r, n, extra)
        out.append(f"{n} {len(arcs)}")
        out += [f"{u} {v}" for u, v in arcs]
    return "\n".join(out) + "\n"


def g_1374_E1(r, s):                     # n, k, books (t, a, b)
    n = {"tiny": r.randint(1, 3), "small": r.randint(1, 10), "medium": r.randint(10, 500),
         "large": r.randint(5000, 20000)}[s]
    k = r.randint(1, n)
    tmax = r.choice([5, 100, 10**4])
    rows = [f"{r.randint(1, tmax)} {r.randint(0, 1)} {r.randint(0, 1)}" for _ in range(n)]
    return f"{n} {k}\n" + "\n".join(rows) + "\n"


def g_143_A(r, s):                       # six sums, 1..20; half built from a real square
    if r.random() < 0.5:
        a, b, c, d = r.sample(range(1, 10), 4)
        vals = [a + b, c + d, a + c, b + d, a + d, b + c]
        vals = [min(20, v) for v in vals]
    else:
        vals = [r.randint(1, 20) for _ in range(6)]
    return f"{vals[0]} {vals[1]}\n{vals[2]} {vals[3]}\n{vals[4]} {vals[5]}\n"


def _date(r, valid=True):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if valid:
        y = r.choice([2013, 2014, 2015])
        mth = r.randint(1, 12)
        d = r.randint(1, days[mth - 1])
    else:
        y = r.choice([2012, 2016, 2013, 2014])
        mth = r.choice([0, 13, 2, 4, 6])
        d = r.choice([0, 29, 30, 31, 32])
    return f"{d:02d}-{mth:02d}-{y}"


def g_260_B(r, s):                       # prophesy with a unique most frequent valid date
    noise_len = {"tiny": 3, "small": 15, "medium": 300, "large": 5000}[s]
    win = _date(r)
    others = [_date(r) for _ in range(r.randint(0, 4))] + [_date(r, valid=False) for _ in range(r.randint(0, 3))]
    others = [o for o in others if o != win]
    wcount = r.randint(1, 6)
    pieces = [win] * wcount
    for o in others:
        pieces += [o] * r.randint(1, max(1, wcount - 1) if o[3:5] not in ("00", "13") else 8)
    r.shuffle(pieces)
    junk = lambda: "".join(r.choice("0123456789-") for _ in range(r.randint(0, noise_len // max(1, len(pieces)))))
    text = junk() + "".join(p + junk() for p in pieces)
    if len(text) > 10**5:
        text = text[:10**5]
    return text + "\n"


def g_309_B(r, s):                       # n words, r rows, c columns, r*c <= 1e6
    n = {"tiny": r.randint(1, 3), "small": r.randint(1, 15), "medium": r.randint(15, 400),
         "large": r.randint(2000, 8000)}[s]
    wl = r.choice([3, 6, 12])
    words = ["".join(r.choice(LOW) for _ in range(r.randint(1, wl))) for _ in range(n)]
    c = r.randint(1, {"tiny": 6, "small": 15, "medium": 40, "large": 80}[s])
    rows = r.randint(1, max(1, min(10**6 // c, {"tiny": 3, "small": 6, "medium": 50, "large": 500}[s])))
    return f"{n} {rows} {c}\n{' '.join(words)}\n"


def g_634_C(r, s):                       # n k a b q, at least one type-2 query
    n = {"tiny": r.randint(1, 3), "small": r.randint(1, 10), "medium": r.randint(10, 500),
         "large": r.randint(2000, 20000)}[s]
    k = r.randint(1, n)
    a = r.randint(2, r.choice([3, 50, 10**4]))
    b = r.randint(1, a - 1)
    q = r.randint(1, {"tiny": 4, "small": 15, "medium": 500, "large": 5000}[s])
    qs = []
    for _ in range(q):
        if r.random() < 0.5:
            qs.append(f"1 {r.randint(1, n)} {r.randint(1, r.choice([3, 10**4]))}")
        else:
            qs.append(f"2 {r.randint(1, n - k + 1)}")
    if not any(x.startswith("2") for x in qs):
        qs[-1] = f"2 {r.randint(1, n - k + 1)}"
    return f"{n} {k} {a} {b} {q}\n" + "\n".join(qs) + "\n"


def g_663_A(r, s):                       # ? + ? - ? ... = n, <= 100 question marks
    cnt = {"tiny": r.randint(1, 3), "small": r.randint(1, 10), "medium": r.randint(10, 60),
           "large": r.randint(80, 100)}[s]
    nmax = r.choice([1, 5, 100, 10**6])
    n = r.randint(1, nmax)
    parts = ["?"]
    for _ in range(cnt - 1):
        parts += [r.choice("+-"), "?"]
    return " ".join(parts) + f" = {n}\n"


def g_675_E(r, s):                       # n, a_i in [i+1, n]
    n = {"tiny": r.randint(2, 4), "small": r.randint(2, 12), "medium": r.randint(12, 500),
         "large": r.randint(5000, 30000)}[s]
    reach = r.choice([1, 3, n])
    a = [r.randint(i + 1, min(n, i + reach)) for i in range(1, n)]
    return f"{n}\n{_ints(a)}\n"


def g_754_E(r, s):                       # cyclic table n x m, pattern r x c
    cap = {"tiny": 3, "small": 8, "medium": 30, "large": 80}[s]
    n, m = r.randint(1, cap), r.randint(1, cap)
    alpha = LOW[:r.choice([2, 3, 26])]
    tab = ["".join(r.choice(alpha) for _ in range(m)) for _ in range(n)]
    pr, pc = r.randint(1, cap), r.randint(1, cap)
    qmark = r.choice([0.0, 0.5, 0.8, 1.0])
    if r.random() < 0.5:                 # copy a real window so matches exist
        i0, j0 = r.randrange(n), r.randrange(m)
        pat = ["".join("?" if r.random() < qmark else tab[(i0 + x) % n][(j0 + y) % m]
                       for y in range(pc)) for x in range(pr)]
    else:
        pat = ["".join("?" if r.random() < qmark else r.choice(alpha) for _ in range(pc)) for _ in range(pr)]
    return f"{n} {m}\n" + "\n".join(tab) + f"\n{pr} {pc}\n" + "\n".join(pat) + "\n"


def g_7_B(r, s):                         # memory manager, t, m <= 100
    t = {"tiny": r.randint(1, 3), "small": r.randint(1, 12), "medium": r.randint(12, 60),
         "large": 100}[s]
    m = r.randint(1, 100)
    ops, allocs = [], 0
    for _ in range(t):
        x = r.random()
        if x < 0.45:
            ops.append(f"alloc {r.randint(1, min(100, max(1, m // r.choice([1, 2, 5]))))}")
            allocs += 1
        elif x < 0.85:
            tok = r.choice([r.randint(1, max(1, allocs + 1)), r.randint(-2**31, 2**31 - 1), 0, -1])
            ops.append(f"erase {tok}")
        else:
            ops.append("defragment")
    return f"{t} {m}\n" + "\n".join(ops) + "\n"


def g_868_A(r, s):                       # password + n distinct 2-letter words
    alpha = LOW[:r.choice([2, 3, 5, 26])]
    pw = r.choice(alpha) + r.choice(alpha)
    allw = [x + y for x in alpha for y in alpha]
    n = r.randint(1, min(100, len(allw), {"tiny": 2, "small": 6, "medium": 30, "large": 100}[s]))
    words = r.sample(allw, n)
    return f"{pw}\n{n}\n" + "\n".join(words) + "\n"


def g_990_E(r, s):                       # n m k, blocked positions, lamp costs
    n = {"tiny": r.randint(1, 4), "small": r.randint(1, 15), "medium": r.randint(15, 1000),
         "large": r.randint(10000, 100000)}[s]
    k = r.randint(1, n)
    m = r.randint(0, n) if r.random() < 0.3 else r.randint(0, max(0, n // r.choice([2, 5, 20])))
    blocked = sorted(r.sample(range(n), m))
    costs = [r.randint(1, r.choice([5, 10**6])) for _ in range(k)]
    return f"{n} {m} {k}\n{_ints(blocked)}\n{_ints(costs)}\n"


# ------------------------------------------------------- CodeChef / HackerEarth
def g_appu_and_sugarcane_farm(r, s):     # N <= 50 heights, one line
    n = {"tiny": r.randint(1, 2), "small": r.randint(1, 8), "medium": r.randint(8, 30), "large": 50}[s]
    if r.random() < 0.5:                 # same odd part -> YES
        base = r.randint(1, 1000) * 2 + 1
        h = [base * 2 ** r.randint(0, 20) for _ in range(n)]
        h = [min(x, 10**9) for x in h]
    else:
        h = [r.randint(1, r.choice([10, 10**9])) for _ in range(n)]
    return f"{n}\n{_ints(h)}\n"


def g_chandu_and_his_girlfriend_returns(r, s):   # T tests, two non-increasing arrays
    t = {"tiny": 1, "small": r.randint(1, 3), "medium": r.randint(1, 10), "large": r.randint(2, 5)}[s]
    cap = {"tiny": 3, "small": 10, "medium": 200, "large": 20000}[s]
    out = [str(t)]
    for _ in range(t):
        n, m = r.randint(1, cap), r.randint(1, cap)
        hi = r.choice([5, 10**9])
        a = sorted((r.randint(0, hi) for _ in range(n)), reverse=True)
        b = sorted((r.randint(0, hi) for _ in range(m)), reverse=True)
        out += [f"{n} {m}", _ints(a), _ints(b)]
    return "\n".join(out) + "\n"


def g_comm3(r, s):                       # T cases, R <= 1000, |X|,|Y| <= 10000
    t = {"tiny": 1, "small": r.randint(1, 5), "medium": r.randint(5, 50), "large": 100}[s]
    out = [str(t)]
    for _ in range(t):
        R = r.randint(1, r.choice([3, 50, 1000]))
        spread = r.choice([2, R, 3 * R, 10000])
        spread = min(spread, 10000)
        out.append(str(R))
        for _ in range(3):
            out.append(f"{r.randint(-spread, spread)} {r.randint(-spread, spread)}")
    return "\n".join(out) + "\n"


def g_golu_and_coins_1(r, s):            # 2 <= M, N <= 10, 0/1 matrix
    cap = {"tiny": 2, "small": 4, "medium": 7, "large": 10}[s]
    M, Nn = r.randint(2, cap), r.randint(2, cap)
    p = r.choice([0.1, 0.5, 0.9])
    rows = [" ".join("1" if r.random() < p else "0" for _ in range(Nn)) for _ in range(M)]
    return f"{M} {Nn}\n" + "\n".join(rows) + "\n"


def g_luckybal(r, s):                    # T <= 10 strings of 4/7
    t = {"tiny": 1, "small": r.randint(1, 4), "medium": r.randint(1, 10), "large": r.randint(1, 3)}[s]
    cap = {"tiny": 3, "small": 12, "medium": 300, "large": 20000}[s]
    p = r.choice([0.1, 0.5, 0.9])
    lines = ["".join("4" if r.random() < p else "7" for _ in range(r.randint(1, cap))) for _ in range(t)]
    return f"{t}\n" + "\n".join(lines) + "\n"


def g_monks_choice_of_numbers_1(r, s):   # T <= 10, N <= 1000, 0 <= K <= N
    t = {"tiny": 1, "small": r.randint(1, 3), "medium": r.randint(1, 10), "large": 10}[s]
    cap = {"tiny": 3, "small": 10, "medium": 200, "large": 1000}[s]
    out = [str(t)]
    for _ in range(t):
        n = r.randint(1, cap)
        k = r.randint(0, n)
        out += [f"{n} {k}", _ints(r.randint(0, r.choice([7, 10**5])) for _ in range(n))]
    return "\n".join(out) + "\n"


def g_roys_life_cycle(r, s):             # N days, each exactly 1440 chars of E/S/C
    n = {"tiny": 1, "small": r.randint(1, 5), "medium": r.randint(5, 60), "large": r.randint(200, 365)}[s]
    lines = []
    for _ in range(n):
        p = r.choice([0.2, 0.6, 0.95, 1.0])
        lines.append("".join("C" if r.random() < p else r.choice("ES") for _ in range(1440)))
    return f"{n}\n" + "\n".join(lines) + "\n"


GENERATORS = {name[2:]: fn for name, fn in globals().items() if name.startswith("g_")}
