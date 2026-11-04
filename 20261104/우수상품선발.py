# 온라인 쇼핑몰에서 판매 중인 상품들의 가격 순위와 판매 가능 여부가 주어집니다.

# 다음 조건에 맞게 상품 2개를 선발하는 solution() 함수를 작성하세요.

# 조건
# 1. 상품 순위가 높은 순서대로 탐색합니다.
# 2. 판매 가능한 상품만 선발합니다.
# 3. 단, 상품 가격이 25,000원 이하인 상품만 선발할 수 있습니다.
# 4. 조건을 만족하는 상품 중 상위 2개를 선발합니다.
# 5. 선발된 상품의 번호를 순서대로 리스트에 담아 반환합니다.
# 6. 2개를 선발하면 탐색을 종료합니다.

# 예상 반환값
# [3, 4]

# 이번에도 힌트는 없어!

# 입력 데이터
rank = [4, 2, 5, 1, 3, 6]
attendance = [True, False, True, True, True, False]
price = [30000, 15000, 50000, 10000, 25000, 40000]

# 첫번째 풀이
def solution(rank, attendance, price):
    selected = []
    for r in range(1, len(rank)+1):
        idx = rank.index(r) 
        if attendance[idx] and price[idx] <= 25000:
            selected.append(idx)
        if len(selected) == 2:
            break
    return selected

#두번째 풀이
def solution2(rank, attendance, price):
    rank_dict = {
        r : idx 
        for idx, r in enumerate(rank)
    }
    selected = []
    for r in range(1, len(rank)+1):
        idx = rank_dict[r]
        if attendance[idx] and price[idx] <= 25000:
            selected.append(idx)
        if len(selected) == 2:
            break
    return selected