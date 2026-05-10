import timeit


#Алгоритм Боєра-Мура
def build_shift_table(pattern: str) -> dict:
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text: str, pattern: str) -> int:
    shift_table = build_shift_table(pattern)
    i = len(pattern) - 1

    while i < len(text):
        j = len(pattern) - 1
        current_index = i

        while j >= 0 and text[current_index] == pattern[j]:
            j -= 1
            current_index -= 1
        if j < 0:
            return current_index + 1
        i += shift_table.get(text[i], len(pattern))

    return -1


#Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern: str) -> list:
    lps = [0] * len(pattern)
    length = 0
    k = 1

    while k < len(pattern):
        if pattern[k] == pattern[length]:
            length += 1
            lps[k] = length
            k += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[k] = 0
                k += 1
    return lps


def kmp_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0

    lps = compute_lps(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == m:
            return i - j

    return -1


#Алгоритм Рабіна-Карпа
def rabin_karp_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    base = 256
    mod = 101

    pattern_hash = 0
    text_hash = 0
    h = 1

    for _ in range(m - 1):
        h = (h * base) % mod
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        text_hash = (base * text_hash + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if text_hash < 0:
                text_hash += mod
    return -1


#Бенчмарк
def benchmark(text: str, pattern: str, label: str, repeats: int = 1000) -> dict:
    results = {}

    for name, func in [
        ("Boyer-Moore", boyer_moore_search),
        ("KMP",         kmp_search),
        ("Rabin-Karp",  rabin_karp_search),
    ]:
        t = timeit.timeit(lambda f=func, tx=text, p=pattern: f(tx, p), number=repeats)
        results[name] = t
        print(f"  {name:15s}: {t:.6f} с  (знайдено: {func(text, pattern)})")
    fastest = min(results, key=results.get)
    print(f"  ✓ Найшвидший для '{label}': {fastest}\n")
    return results


def run_all():
    # Завантаження текстів
    with open("../../Downloads/goit-algo-hw-05/article1.txt", encoding="utf-8") as f:
        text1 = f.read()
    with open("../../Downloads/goit-algo-hw-05/article2.txt", encoding="utf-8") as f:
        text2 = f.read()

    # Підрядки: існуючий та вигаданий
    existing1  = "алгоритм сортування"          # є в статті 1
    fictional1 = "квантовий нейромережевий блокчейн"  # немає

    existing2  = "рекомендаційної системи"       # є в статті 2
    fictional2 = "гіперпросторовий індексатор даних"  # немає

    all_results = {}

    print("=" * 60)
    print("СТАТТЯ 1")
    print("=" * 60)

    print(f"\n[Існуючий підрядок] '{existing1}'")
    r = benchmark(text1, existing1, "стаття1-існуючий")
    all_results[("article1", "existing")] = r

    print(f"[Вигаданий підрядок] '{fictional1}'")
    r = benchmark(text1, fictional1, "стаття1-вигаданий")
    all_results[("article1", "fictional")] = r

    print("=" * 60)
    print("СТАТТЯ 2")
    print("=" * 60)

    print(f"\n[Існуючий підрядок] '{existing2}'")
    r = benchmark(text2, existing2, "стаття2-існуючий")
    all_results[("article2", "existing")] = r

    print(f"[Вигаданий підрядок] '{fictional2}'")
    r = benchmark(text2, fictional2, "стаття2-вигаданий")
    all_results[("article2", "fictional")] = r

    # Загальний переможець
    print("=" * 60)
    print("ЗАГАЛЬНІ ПІДСУМКИ")
    print("=" * 60)
    totals = {"Boyer-Moore": 0, "KMP": 0, "Rabin-Karp": 0}
    for v in all_results.values():
        for algo, t in v.items():
            totals[algo] += t

    for algo, t in sorted(totals.items(), key=lambda x: x[1]):
        print(f"  {algo:15s}: {t:.6f} с (сума по всіх тестах)")

    overall_winner = min(totals, key=totals.get)
    print(f"\n  ✓ Найшвидший алгоритм загалом: {overall_winner}")

    return all_results


if __name__ == "__main__":
    run_all()
