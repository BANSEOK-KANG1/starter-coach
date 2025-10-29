import os
import uuid
import random
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

# 로컬 모듈 임포트
from src.coach_tasks import generate_tasks, render_mission
from src.io_log import ensure_dir, append_log, read_logs


# -------------------------------------------------
# 페이지 / 경로 설정
# -------------------------------------------------
st.set_page_config(
    page_title="Starter Coach",
    page_icon="🌱",
    layout="wide",
)

# 현재 파일 기준으로 경로 잡기 (Cloud / 로컬 모두 안정적으로 동작)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in os.sys.path:
    os.sys.path.append(SRC_DIR)

LOG_DIR = os.path.join(BASE_DIR, "data", "logs")
ensure_dir(LOG_DIR)  # logs 디렉터리 없으면 생성


# -------------------------------------------------
# 세션 상태 (익명 사용자 ID, A/B 배정)
# -------------------------------------------------
if "sid" not in st.session_state:
    st.session_state["sid"] = str(uuid.uuid4())  # 익명 유저 세션 id

if "variant" not in st.session_state:
    # A: 감정형 동기부여 / B: 실용형·ROI 강조
    st.session_state["variant"] = random.choice(["A", "B"])

sid = st.session_state["sid"]
variant = st.session_state["variant"]


# -------------------------------------------------
# 로깅 유틸
# -------------------------------------------------
def log_completion(goal_type: str, time_budget: str, task_id: str, done: int):
    """
    과제를 완료했다고 사용자가 표시했을 때
    한 줄 로그를 CSV에 append한다.
    """
    ts_iso = datetime.now(timezone.utc).isoformat()

    row = {
        "sid": sid,                     # 어떤 세션인지
        "ts": ts_iso,                   # 언제 완료했는지 (UTC ISO)
        "goal_type": goal_type,         # 선택한 목표 분야
        "time_budget": time_budget,     # 선택한 시간 예산
        "task_id": task_id,             # 어떤 과제였는지
        "variant": variant,             # A/B 중 어떤 톤을 봤는지
        "done": int(done),              # 완료 여부 (1)
    }

    # 날짜별 로그 파일
    file_path = os.path.join(
        LOG_DIR,
        f"starter_log_{datetime.utcnow().date()}.csv"
    )
    append_log(file_path, row)


# -------------------------------------------------
# UI: 타이틀/설명
# -------------------------------------------------
st.title("🌱 Starter Coach")
st.caption("지금 바로 할 수 있는 '한 걸음'을 추천하고, 어떤 말투가 실제 행동을 더 잘 이끌어내는지 실험합니다.")


# -------------------------------------------------
# 사이드바: 유저 설정 입력
# -------------------------------------------------
with st.sidebar:
    st.header("설정")

    goal_type = st.selectbox(
        "당신의 목표 영역은 무엇인가요?",
        ["데이터 분석", "영어 회화", "홈트", "포트폴리오"],
    )

    time_budget = st.selectbox(
        "오늘 투자 가능한 시간은 어느 정도인가요?",
        ["10분만 가능", "30분 가능"],
    )

    st.markdown("---")
    st.info(
        f"이 세션은 **Variant {variant}** 톤(카피 스타일)을 보고 있습니다.\n\n"
        "A: 감정형(자신감/칭찬)\n"
        "B: 실용형(ROI/성과 강조)\n\n"
        "→ 어느 쪽이 실제로 행동 완료율을 더 높이는지 측정합니다."
    )


# -------------------------------------------------
# 오늘의 추천 미션 생성
# -------------------------------------------------
tasks = generate_tasks(goal_type, time_budget)

st.subheader("오늘의 추천 미션")

if not tasks:
    st.warning("해당 조합에 맞는 미션 템플릿이 아직 없습니다. 다른 옵션을 선택해 주세요.")
else:
    cols = st.columns(len(tasks))

    for idx, task in enumerate(tasks):
        with cols[idx]:
            # variant에 따라 다르게 포장된 설명 문구
            mission_text = render_mission(task["core"], variant)

            # 미션 본문
            st.markdown(f"**{mission_text}**")

            # 완료 버튼
            if st.button("✅ 완료", key=f"done_{task['task_id']}"):
                log_completion(goal_type, time_budget, task["task_id"], done=1)
                st.success("기록되었습니다! 잘하셨어요 🙌")


# -------------------------------------------------
# 로그 분석 섹션
# -------------------------------------------------
st.divider()
st.subheader("📊 오늘의 실험 결과 요약")

log_file = os.path.join(
    LOG_DIR,
    f"starter_log_{datetime.utcnow().date()}.csv"
)

df = read_logs(log_file)

if df is None or df.empty:
    st.write("아직 오늘의 완료 로그가 없습니다. 미션을 완료해보세요!")
else:
    # 전체 수행 현황
    total_actions = len(df)
    total_done = int(df["done"].sum())
    done_rate = (total_done / total_actions * 100.0) if total_actions else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("총 완료 기록 수", f"{total_actions}")
    c2.metric("완료된 미션 수", f"{total_done}")
    c3.metric("완료율", f"{done_rate:.1f}%")

    # variant별 비교 (A vs B)
    by_variant = (
        df.groupby("variant", as_index=False)
        .agg(
            actions=("done", "count"),
            completions=("done", "sum"),
        )
    )
    by_variant["완료율(%)"] = (
        by_variant["completions"] / by_variant["actions"] * 100.0
    ).round(1)

    st.markdown("**A/B 톤별 완료율 (오늘)**")
    st.dataframe(by_variant, use_container_width=True)

    # goal_type + variant 조합별
    by_goal_variant = (
        df.groupby(["goal_type", "variant"], as_index=False)
        .agg(
            actions=("done", "count"),
            completions=("done", "sum"),
        )
    )
    by_goal_variant["완료율(%)"] = (
        by_goal_variant["completions"] / by_goal_variant["actions"] * 100.0
    ).round(1)

    st.markdown("**목표 영역별 A/B 결과 (오늘)**")
    st.dataframe(by_goal_variant, use_container_width=True)
