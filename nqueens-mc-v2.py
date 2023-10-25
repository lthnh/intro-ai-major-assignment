from random import randrange

n = int()
b = int()
q = list()
n_diag = list()
p_diag = list()

def update_diag(clm, mode):
    if mode == 0:
        n_diag_cnst = q[clm] + clm
        p_diag_cnst = q[clm] - clm
        n_diag[n_diag_cnst] -= 1
        p_diag[b+p_diag_cnst] -= 1
    elif mode == 1:
        n_diag_cnst = q[clm] + clm
        p_diag_cnst = q[clm] - clm
        n_diag[n_diag_cnst] += 1
        p_diag[b+p_diag_cnst] += 1

def swap(clm_i, clm_j):
    q[clm_i], q[clm_j] = q[clm_j], q[clm_i]

def swap_n_update(clm_i, clm_j):
    update_diag(clm_i, 0)
    update_diag(clm_j, 0)
    swap(clm_i, clm_j)
    update_diag(clm_i, 1)
    update_diag(clm_j, 1)

def prtl_collis(clm):
    n_diag_cnst = q[clm] + clm
    p_diag_cnst = b + q[clm] - clm
    return n_diag[n_diag_cnst] + p_diag[p_diag_cnst]

def ttl_collis(clm):
    n_diag_cnst = q[clm] + clm
    p_diag_cnst = b + q[clm] - clm
    return n_diag[n_diag_cnst] + p_diag[p_diag_cnst] - 2

def init_srch():
    clm = 0
    for _ in range(round(3.08 * n)):
        if clm >= n: break
        rd_clm = randrange(clm, n)
        swap(clm, rd_clm)
        if prtl_collis(clm) == 0:
            update_diag(clm, 1)
            clm += 1
        else:
            swap(clm, rd_clm)
    for clm_i in range(clm, n):
        rd_clm = randrange(clm_i, n)
        swap_n_update(clm_i, rd_clm)
    return n - clm + 1

def fnal_srch(k, mx_stps):
    for clm in range(n-k+1, n):
        if ttl_collis(clm) > 0:
            for i in range(mx_stps):
                rd_clm = randrange(1, n)
                swap_n_update(clm, rd_clm)
                conds = ttl_collis(clm) > 0 or ttl_collis(rd_clm) > 0
                if conds: swap_n_update(clm, rd_clm)
                else: break

def is_slt():
    for clm in range(n):
        if ttl_collis(clm) > 0:
            return False
    return True

if __name__ == '__main__':
    n = int(input('N: '))
    b = n - 1
    q = list(range(n))
    mx_stps = int(1e4)
    for i in range(mx_stps):
        if i == 0 or not is_slt():
            n_diag = [0 for _ in range(2 * n - 1)]
            p_diag = [0 for _ in range(2 * n - 1)]
            k = init_srch()
            fnal_srch(k, mx_stps)
        else:
            print(q)
            exit(0)
    print(q)
    print('None')