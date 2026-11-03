rank = [4, 2, 5, 1, 3]
attendance = [True, False, True, True, True]

# 참여 가능한 학생 중 등수가 높은 2명을 선발한다.
# 선발된 학생의 번호를 등수가 높은 순서대로 반환한다.
# 학생 번호는 0번부터 시작한다.

def solution(rank, attendance):
    rank_dict = {r : idx for idx, r in enumerate(rank)}
    selected = []
    for r in range(1, len(rank)+1):
        idx = rank_dict[r]
        if attendance[idx]:
            selected.append(idx)
        if len(selected) == 2:
            break
    return selected