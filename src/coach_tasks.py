from typing import List, Dict

def generate_tasks(goal_type: str, time_budget: str) -> List[Dict[str, str]]:
    """
    goal_type(목표 분야)와 time_budget(가능 시간)에 맞춰
    바로 실행 가능한 초소형 미션(작은 행동)을 리턴한다.
    """
    mappings = {
        ("데이터 분석", "10분만 가능"): [
            {"task_id": "da_gh", "core": "GitHub 계정 만들고 프로필 한 줄 작성하기"},
            {"task_id": "da_kaggle", "core": "Kaggle에서 흥미 있는 데이터셋 1개 북마크하기"},
            {"task_id": "da_vid", "core": "파이썬 기초 강의 10분짜리 한 편 시청하기"},
        ],
        ("데이터 분석", "30분 가능"): [
            {"task_id": "da_nb", "core": "Jupyter Notebook 켜서 print('hello') 실행해보기"},
            {"task_id": "da_pandas", "core": "pandas 튜토리얼 20분 따라하기"},
            {"task_id": "da_plot", "core": "matplotlib으로 막대그래프 1개 그려보기"},
        ],

        ("영어 회화", "10분만 가능"): [
            {"task_id": "eng_greet", "core": "기본 인사 표현 5개 소리 내서 녹음·반복하기"},
            {"task_id": "eng_vocab", "core": "새 표현 5개 적고 직접 말해보기"},
            {"task_id": "eng_listen", "core": "원어민 인터뷰 3분 듣고 기억나는 문장 1개 적기"},
        ],
        ("영어 회화", "30분 가능"): [
            {"task_id": "eng_msg", "core": "친구나 스터디원에게 영어로 메시지 3줄 보내보기"},
            {"task_id": "eng_shadow", "core": "영상/드라마 대사 10분 쉐도잉 따라읽기"},
            {"task_id": "eng_intro", "core": "자기소개 5문장 영어로 쓰고 녹음하기"},
        ],

        ("홈트", "10분만 가능"): [
            {"task_id": "fit_basic", "core": "스쿼트 20회 + 플랭크 30초 유지하기"},
            {"task_id": "fit_walk", "core": "집 근처 10분 걷기 (휴대폰 보지 말고)"},
            {"task_id": "fit_stretch", "core": "전신 스트레칭 루틴 10분 따라하기"},
        ],
        ("홈트", "30분 가능"): [
            {"task_id": "fit_hiit", "core": "HIIT 루틴 20분 따라하기"},
            {"task_id": "fit_yoga", "core": "초보자 요가 세션 30분 따라하기"},
            {"task_id": "fit_body", "core": "맨몸 운동 루틴 30분 진행하기"},
        ],

        ("포트폴리오", "10분만 가능"): [
            {"task_id": "pf_goal", "core": "포트폴리오에서 보여주고 싶은 강점 3줄 적기"},
            {"task_id": "pf_repo", "core": "GitHub 새 리포지토리 만들고 README 시작하기"},
            {"task_id": "pf_template", "core": "좋은 포트폴리오 템플릿 1개 북마크하기"},
        ],
        ("포트폴리오", "30분 가능"): [
            {"task_id": "pf_case", "core": "대표 프로젝트 1개 골라 문제-해결-성과 정리하기"},
            {"task_id": "pf_intro", "core": "자기소개 About Me 섹션 초안 작성하기"},
            {"task_id": "pf_review", "core": "우수 포트폴리오 3개 보고 공통점 뽑기"},
        ],
    }

    return mappings.get((goal_type, time_budget), [])


def render_mission(core_text: str, variant: str) -> str:
    """
    같은 행동을 다른 카피 스타일(A/B)로 보여준다.
    - A: 감정형(자신감, 심리적 장벽 낮추기)
    - B: 실용형(ROI, 바로 쓰이는 결과 강조)
    """
    if variant == "A":
        return (
            f"🔥 자신감 챙기기: {core_text}\n"
            "완벽할 필요 없어. 이거 하면 오늘 이미 성장 중이야."
        )
    elif variant == "B":
        return (
            f"💡 바로 성과로 연결: {core_text}\n"
            "이건 실제로 남는 산출물이라서 나중에 바로 쓸 수 있어."
        )
    else:
        return core_text
