import requests


def so(A, so_idx):
    len_A = len(A)
    if len_A == 1:
        return A
    return mrg(so(A[:len_A // 2], so_idx),
               so(A[len_A // 2:], so_idx),
               so_idx)


def mrg(C, D, so_idx):
    idx_c, idx_d, len_C, len_D, E = 0, 0, len(C), len(D), []
    while idx_c != len_C and idx_d != len_D:
        if C[idx_c][so_idx] > D[idx_d][so_idx]:
            E.append(C[idx_c])
            idx_c += 1
        else:
            E.append(D[idx_d])
            idx_d += 1
    if idx_c != len_C:
        E.extend(C[idx_c:])
    else:
        E.extend(D[idx_d:])
    return E


def get_symbol_name_for_isin(isin):
    url = 'https://query1.finance.yahoo.com/v1/finance/search'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    }

    params = dict(
        q=isin,
        quotesCount=1,
        newsCount=0,
        listsCount=0,
        quotesQueryId='tss_match_phrase_query'
    )

    resp = requests.get(url=url, headers=headers, params=params)
    data = resp.json()
    if 'quotes' in data and len(data['quotes']) > 0:
        return data['quotes'][0]['symbol'], data['quotes'][0].get('longname'), \
            data['quotes'][0].get('shortname')
    else:
        return None, None, None
