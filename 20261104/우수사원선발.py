# 회사에서 직원 6명의 업무 평가 순위가 주어졌습니다.

# 다음 조건에 따라 우수 사원 3명을 선발하는 함수를 작성하세요.

# 조건
# 1. 참여 가능한 직원 중 평가 순위가 높은 3명을 선발합니다.
# 2. 선발된 직원의 번호를 순위가 높은 순서대로 리스트에 저장합니다.
# 3. 직원 번호는 0번부터 시작합니다.
# 4. 최종 결과는 리스트로 반환합니다.

# 예상 반환값
# [3, 4, 0]

# 입력 데이터
rank = [5, 2, 6, 1, 4, 3]
attendance = [True, False, True, True, True, False]

def solution(rank, attendance):
    rank_dict = {r: i for i, r in enumerate(rank)}

    selected = []

    for r in range(1, len(rank)+1):
        idx = rank_dict[r]
        if attendance[idx]:
            selected.append(idx)
        if len(selected) == 3:
            break
    return selected
    



