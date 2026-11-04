# 문자열 myStr이 주어집니다.

# 문자 "0"과 "1"을 구분자로 사용하여 문자열을 나누고, 나눠진 문자열 중 길이가 2 이상인 문자열만 순서대로 저장한 배열을 반환하세요.

# 단, 결과가 빈 배열이라면 ["EMPTY"]를 반환합니다.
# myStr = "a0bc1d00efg1h"

# 기대 결과:
# ["bc", "efg"]

# 이번에는 replace()를 사용하지 않고, split()의 구분자 기능을 직접 활용해 봐!

import re
def solution(myStr):
    result = [s for s in re.split(r"[01]",myStr) if len(s)>=2]
    return result if result else ["EMPTY"]