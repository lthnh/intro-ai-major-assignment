from copy import deepcopy
from random import randrange, choice
from queue import Queue

n = int()

# consider replace inline check funtion
def q_chck(clm_fst, rw_fst, clm_snd, rw_snd):
    rw_df = abs(rw_fst - rw_snd)
    clm_df = abs(clm_fst - clm_snd)
    if rw_df == 0 or rw_df == clm_df:
        return True
    return False

def cnflcts_cnt(brd, clm, rw, opt):
    match opt:
        case 0:
            nw_brd = deepcopy(brd)
            nw_brd[clm] = rw
            clms_to_chck = range(clm)
            pass
        case 1:
            nw_brd = brd
            clms_to_chck = filter(lambda x: x != clm, range(n))
            pass
    cnt = 0
    for clm_i in clms_to_chck:
        if q_chck(clm_i, nw_brd[clm_i], clm, rw):
            cnt += 1
    return cnt

# does this function have any use?
def cnflcts_clms(brd):
    clms = list()
    for clm_i in range(n):
        for clm_to_cmp in filter(lambda x: x != clm_i, range(n)):
            rw_df = abs(brd[clm_i] - brd[clm_to_cmp])
            clm_df = abs(clm_i - clm_to_cmp)
            if rw_df == 0 or rw_df == clm_df:
                clms.append(clm_i)
                break
    return clms

def grdy_init():
    init_brd = [-1 for i in range(n)]
    init_brd[0] = randrange(n)
    for clm_i in range(1, n):
        cnflcts_cnt_pr_clm = [cnflcts_cnt(init_brd, clm_i, rw_i, 0) for rw_i in range(n)]
        mn_cnflct_cnt = min(cnflcts_cnt_pr_clm)
        slctd_rws = [i for i, cnt in enumerate(cnflcts_cnt_pr_clm) if cnt == mn_cnflct_cnt]
        chsn_rw = choice(slctd_rws)
        init_brd[clm_i] = chsn_rw
    return init_brd

def mn_cnflcts(brd, mx_stps):
    lst_clms = set()
    for i in range(mx_stps):
        cnflcts_clms = list(filter(lambda x: cnflcts_cnt(brd, x, brd[x], 1) > 0, range(n)))
        if len(cnflcts_clms) == 0:
            return brd
        chsn_cnflct_clm = choice(cnflcts_clms) 
        if chsn_cnflct_clm not in lst_clms:
            lst_clms.add(chsn_cnflct_clm)
            rd = False
        else:
            avi_clms = set(range(n))
            avi_clms -= lst_clms
            chsn_cnflct_clm = choice(list(avi_clms))
            rd = True
        if len(lst_clms) > n//2:
            lst_clms.pop()
        if rd:
            chsn_rw = randrange(n)
        else:
            cnflcts_cnt_pr_clm = [cnflcts_cnt(brd, chsn_cnflct_clm, rw_i, 1) for rw_i in range(n)]
            mn_cnflct_cnt = min(cnflcts_cnt_pr_clm)
            slctd_rws = [i for i, cnt in enumerate(cnflcts_cnt_pr_clm) if cnt == mn_cnflct_cnt]
            chsn_rw = choice(slctd_rws)
        brd[chsn_cnflct_clm] = chsn_rw
        # print(brd)
        # print(lst_clms)
        # print(rd, chsn_cnflct_clm, chsn_rw)
    return None

if __name__ == '__main__':
    n = int(input('N: '))
    init_brd = grdy_init()
    print(init_brd)
    slt = mn_cnflcts(init_brd, int(1e4))
    print(slt)