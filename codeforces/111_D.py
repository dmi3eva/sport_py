# Условие: https://codeforces.com/problemset/problem/1550/D
# Разбор: https://codeforces.com/blog/entry/92864

MOD = 1e9 + 7

def C(m, n):
    if m < 0 or m > n:
        return 0
    result = 1
    for i in range(1, m + 1):
        result = result * (n - i + 1) // i
        result %= MOD
    return int(result)


def extract_abc(l, r, n, k):
    pluses_start = max(l - k, 1)
    pluses_end = min(n, r - k)
    minuses_start = max(1, l + k)
    minuses_end = min(n, r + k)
    if minuses_start > pluses_end:
        a = pluses_end - pluses_start + 1  # Только плюсы
        b = minuses_end - minuses_start + 1  # Только минусы
        c = 0  # Общая часть
    else:
        common_start = minuses_start
        common_ends = pluses_end
        a = common_start - pluses_start  # Только плюсы
        b = minuses_end - common_ends   # Только минусы
        c = common_ends - common_start + 1  # Общая часть
    return a, b, c


def calculate_variants(l, r, n, k, half, holy):
    a, b, c = extract_abc(l, r, n, k)
    variants_amount = 0
    for i in range(0, min(a, half) + 1):
        if holy % 2 == 0:
            variants_amount += C(i, a) * C(half - i, c) * C(half, c + b - half + i) % MOD
        else:
            variants_amount += C(i, a) * C(half - i, c) * C(half + 1, c + b - half + i) % MOD
            variants_amount += C(i, a) * C(half - i + 1, c) * C(half, c + b - half + i - 1) % MOD
    return variants_amount


def partly_solve(k, n, l, r, step):
    partly_answer = 0
    half = n // 2
    pluses = min(n, r - k) - max(1, l - k) + 1
    minuses = min(n, r + k) - max(1, l + k) + 1
    while (pluses >= half) and (minuses >= half) and (k <= n) and (k >= 1):
        partly_answer += calculate_variants(l, r, n, k, half, n)
        partly_answer %= MOD
        k += step
        pluses = min(n, r - k) - max(1, l - k) + 1
        minuses = min(n, r + k) - max(1, l + k) + 1
    return partly_answer


def find_half(minuses_starts_line, minuses_ends_line, pluses_starts_line, pluses_ends_line):
    strat_k = max(minuses_starts_line, pluses_starts_line)
    end_k = min(minuses_ends_line, pluses_ends_line)
    for k in range(strat_k, end_k):
        a, b, c = extract_abc(l, r, n, k)
        half_k = min(max(a, b), min(a, b) + c)
        half = max(half, half_k)
    return half * 2


def find_not_full_solution(n, l, r):
    if l + 1 >= n:
        return 0
    minuses_starts_line = 1
    minuses_ends_line = n - l
    pluses_starts_line = max(1, l - n)
    pluses_ends_line = max(1, r - 1)
    holy = find_half(minuses_starts_line, minuses_ends_line, pluses_starts_line, pluses_ends_line)
    half = holy // 2
    answer = 0
    strat_k = max(minuses_starts_line, pluses_starts_line)
    end_k = min(minuses_ends_line, pluses_ends_line)
    for k in range(strat_k, end_k):
        answer += calculate_variants(l, r, n, k, half, holy)
        answer *= (r - l + 1) ** (n - 2 * half)
        answer %= MOD
    return answer


def solve(n, l, r):
    answer = 0
    half = n // 2
    lower_bound = max(1, n - r, l - 1)
    upper_bound = min(1 - l, r - n)
    if upper_bound >= lower_bound:
        if n % 2 == 0:
            answer += (1 + upper_bound - lower_bound) * C(half, n)
        else:
            answer += (1 + upper_bound - lower_bound) * (C(half, n) + C(half + 1, n))
        answer %= MOD
    answer += partly_solve(upper_bound + 1, n, l, r, 1)
    answer += partly_solve(lower_bound - 1, n, l, r, -1)
    if answer == 0:
        answer = find_not_full_solution(n, l, r)
    return int(answer)


if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        n, l, r = map(int, input().split())
        print(solve(n, l, r))

