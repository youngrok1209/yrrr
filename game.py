import random
import time
import streamlit as st
from streamlit_keyboard_event import keyboard_event

st.set_page_config(page_title="무한의 계단", page_layout="centered")

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.player_x = 0  # 0: 왼쪽, 1: 오른쪽
    st.session_state.stairs = [random.choice([0, 1]) for _ in range(15)]
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

def reset_game():
    st.session_state.score = 0
    st.session_state.player_x = 0
    st.session_state.stairs = [random.choice([0, 1]) for _ in range(15)]
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

def move(action):
    """
    action: 
      - 'climb': 바라보는 방향으로 올라가기
      - 'turn': 방향을 바꾸고 올라가기
    """
    if st.session_state.game_over:
        return

    # 방향 전환 처리
    if action == "turn":
        st.session_state.player_x = 1 - st.session_state.player_x

    # 현재 계단 위치 판정
    next_stair = st.session_state.stairs[0]

    # 플레이어 위치와 계단 위치가 맞으면 점수 획득
    if st.session_state.player_x == next_stair:
        st.session_state.score += 1
        st.session_state.stairs.pop(0)
        st.session_state.stairs.append(random.choice([0, 1]))
    else:
        st.session_state.game_over = True

# UI 헤더
st.title("🧗‍♂️ 무한의 계단 (Infinite Stairs)")
st.caption("키보드 또는 화면의 버튼을 눌러 계단을 올라가세요!")

# 점수 및 상태 표시
col1, col2 = st.columns(2)
with col1:
    st.metric("현재 점수", st.session_state.score)
with col2:
    if st.session_state.game_over:
        st.error("게임 오버!")
    else:
        st.success("게임 진행 중")

# 계단 시각화 (간단한 텍스트 그리드)
st.markdown("---")
grid_html = "<div style='font-family: monospace; font-size: 20px; line-height: 1.2; text-align: center;'>"

if st.session_state.game_over:
    grid_html += "❌ <b>FAILED!</b><br><br>"
else:
    # 플레이어와 계단 표시 (상단에서 하단으로 출력)
    stairs_view = list(reversed(st.session_state.stairs[:8]))
    for idx, stair in enumerate(stairs_view):
        line_idx = len(stairs_view) - 1 - idx
        left_char = "🟩" if stair == 0 else "⬜"
        right_char = "🟩" if stair == 1 else "⬜"

        # 맨 아래 줄에 플레이어 위치 표시
        if line_idx == 0:
            if st.session_state.player_x == 0:
                left_char = "🏃"
            else:
                right_char = "🏃"

        grid_html += f"{left_char} {right_char}<br>"

grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)
st.markdown("---")

# 컨트롤 버튼 (화면 클릭용)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn1:
    if st.button("🔄 방향 전환 (Turn)", use_container_width=True):
        move("turn")
        st.rerun()

with col_btn2:
    if st.button("⬆️ 올라가기 (Climb)", use_container_width=True):
        move("climb")
        st.rerun()

with col_btn3:
    if st.button("🎮 다시 시작", use_container_width=True):
        reset_game()
        st.rerun()

# 키보드 이벤트 감지 (Spacebar = Climb, ArrowRight = Turn)
key = keyboard_event(key_list=["Space", "ArrowRight"])

if key == "Space":
    move("climb")
    st.rerun()
elif key == "ArrowRight":
    move("turn")
    st.rerun()
