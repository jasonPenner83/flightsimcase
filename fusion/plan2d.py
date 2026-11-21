# 2D plan-view fold planner for the double-hinge wings (my frame: x right, y toward pilot, mm).
import math, sys
from collections import deque

T, Wc, Ww, g, Fe, Be, clr, pr = 20, 410, 350, 4, 45, 30, 5, 20


def rects_panel(xl, xr, with_bracket_side=None):
    R = [
        ('up', xl, xl + T, -T, pr), ('up', xr - T, xr, -T, pr),
        ('rail', xl + T, xr - T, -T, 0), ('front', xl + T, xr - T, 0, Fe), ('rear', xl + T, xr - T, -T - Be, -T),
    ]
    return R


def poly(r):
    _, x0, x1, y0, y1 = r
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rot_cw(p, th):
    c, s = math.cos(th), math.sin(th)
    return (p[0] * c + p[1] * s, -p[0] * s + p[1] * c)


def sat(P, Q, eps):
    for poly_ in (P, Q):
        n = len(poly_)
        for i in range(n):
            a, b = poly_[i], poly_[(i + 1) % n]
            ax, ay = b[1] - a[1], a[0] - b[0]
            L = math.hypot(ax, ay)
            ax, ay = ax / L, ay / L
            pa = [ax * x + ay * y for x, y in P]
            qa = [ax * x + ay * y for x, y in Q]
            if max(pa) + eps <= min(qa) or max(qa) + eps <= min(pa):
                return False
    return True


def geometry(yp):
    yL = 2 * Fe + clr
    yR = yL + T + Be + Fe + clr
    sL = yL - 2 * yp
    sR = yR - 2 * yp
    AL = ((-(Wc + g) + sL) / 2.0, yp); BL = ((-(Wc + g) - sL) / 2.0, yp)
    AR = (((Wc + g) - sR) / 2.0, yp); BR = (((Wc + g) + sR) / 2.0, yp)
    return AL, BL, AR, BR


def wing_polys(rects, A, B0, a, b, sign):
    # sign=+1 left (cw), -1 right (ccw)
    th1 = math.radians(a) * sign
    th2 = math.radians(a + b) * sign
    v = rot_cw((B0[0] - A[0], B0[1] - A[1]), th1)
    B = (A[0] + v[0], A[1] + v[1])
    out = []
    for r in rects:
        pts = []
        for p in poly(r):
            q = rot_cw((p[0] - B0[0], p[1] - B0[1]), th2)
            pts.append((B[0] + q[0], B[1] + q[1]))
        out.append((r[0], pts))
    return out


def collides(fixed, moving, eps=2.0):
    for _, P in fixed:
        for _, Q in moving:
            if sat(P, Q, eps):
                return True
    return False


def plan(yp, step=3, amin=-30, amax=120, bmin=-120, bmax=180, side='L', left_closed=None):
    AL, BL, AR, BR = geometry(yp)
    center = [(r[0], poly(r)) for r in rects_panel(-Wc / 2, Wc / 2)]
    if side == 'L':
        rects = rects_panel(-Wc / 2 - g - Ww, -Wc / 2 - g); A, B0, sg = AL, BL, 1
        fixed = center
    else:
        rects = rects_panel(Wc / 2 + g, Wc / 2 + g + Ww); A, B0, sg = AR, BR, -1
        lw = wing_polys(rects_panel(-Wc / 2 - g - Ww, -Wc / 2 - g), AL, BL, 90, 90, 1)
        fixed = center + lw
    alphas = list(range(amin, amax + 1, step)); betas = list(range(bmin, bmax + 1, step))
    ok = {}
    for a in alphas:
        for b in betas:
            ok[(a, b)] = not collides(fixed, wing_polys(rects, A, B0, a, b, sg))
    start, goal = (0, 0), (90, 90)
    # start/goal are touching-allowed states; force ok
    ok[start] = True; ok[goal] = True
    prev = {start: None}
    dq = deque([start])
    while dq:
        c = dq.popleft()
        if c == goal:
            break
        for da in (-step, 0, step):
            for db in (-step, 0, step):
                n = (c[0] + da, c[1] + db)
                if n in ok and ok[n] and n not in prev:
                    prev[n] = c
                    dq.append(n)
    if goal not in prev:
        return None, ok
    path = []
    c = goal
    while c:
        path.append(c); c = prev[c]
    return path[::-1], ok


if __name__ == '__main__':
    for yp in [float(v) for v in sys.argv[1:]] or [-10.0]:
        for side in ('L', 'R'):
            path, ok = plan(yp, side=side)
            print('yp', yp, side, 'path' if path else 'NO PATH', len(path) if path else '',
                  'free frac %.2f' % (sum(ok.values()) / len(ok)))
            if path:
                # compress to corner points
                pts = [path[0]]
                for i in range(1, len(path) - 1):
                    d1 = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
                    d2 = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
                    if d1 != d2:
                        pts.append(path[i])
                pts.append(path[-1])
                print('   ', pts)
