
import streamlit as st
import random
import math

st.set_page_config(
    page_title="Tic-Tac-Toe AI",
    page_icon="⭕",
    layout="centered"
)

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #202c45);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
div.stButton > button {
    width: 100%;
    min-height: 65px;
    font-size: 27px;
    font-weight: bold;
    border-radius: 12px;
    border: 1px solid #536783;
    background-color: #263750;
    color: white;
    transition: 0.2s;
}
div.stButton > button:hover {
    background-color: #3b5275;
    border-color: #8bb9ff;
}
</style>
""", unsafe_allow_html=True)

# ---------- Game Logic ----------
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def get_winner(board):
    for a, b, c in WINNING_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell is not None for cell in board):
        return "Draw"
    return None

def minimax(board, is_maximizing, depth=0):
    result = get_winner(board)

    if result == "O":
        return 10 - depth
    if result == "X":
        return depth - 10
    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] is None:
                board[i] = "O"
                score = minimax(board, False, depth + 1)
                board[i] = None
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] is None:
                board[i] = "X"
                score = minimax(board, True, depth + 1)
                board[i] = None
                best_score = min(best_score, score)
        return best_score

def ai_move(board, difficulty):
    available = [i for i, cell in enumerate(board) if cell is None]
    if not available:
        return None

    if difficulty == "Easy":
        return random.choice(available)

    if difficulty == "Medium" and random.random() < 0.5:
        return random.choice(available)

    best_score = -math.inf
    best_moves = []

    for i in available:
        board[i] = "O"
        score = minimax(board, False)
        board[i] = None

        if score > best_score:
            best_score = score
            best_moves = [i]
        elif score == best_score:
            best_moves.append(i)

    return random.choice(best_moves)

def new_game():
    st.session_state.board = [None] * 9
    st.session_state.game_over = False
    st.session_state.message = "Your turn — you play X!"

def finish_if_needed():
    result = get_winner(st.session_state.board)

    if result:
        st.session_state.game_over = True

        if result == "X":
            st.session_state.message = "🎉 You win!"
            st.session_state.scores["Player"] += 1
        elif result == "O":
            st.session_state.message = "🤖 AI wins! Try again."
            st.session_state.scores["AI"] += 1
        else:
            st.session_state.message = "🤝 It's a draw!"
            st.session_state.scores["Draws"] += 1

def play_turn(index):
    if st.session_state.game_over or st.session_state.board[index] is not None:
        return

    st.session_state.board[index] = "X"
    finish_if_needed()

    if not st.session_state.game_over:
        move = ai_move(st.session_state.board, st.session_state.difficulty)
        if move is not None:
            st.session_state.board[move] = "O"
        finish_if_needed()

        if not st.session_state.game_over:
            st.session_state.message = "Your turn — you play X!"

# ---------- Session State ----------
if "board" not in st.session_state:
    st.session_state.board = [None] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "message" not in st.session_state:
    st.session_state.message = "Your turn — you play X!"
if "scores" not in st.session_state:
    st.session_state.scores = {"Player": 0, "AI": 0, "Draws": 0}
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Hard"

# ---------- Interface ----------
st.title("⭕ Tic-Tac-Toe AI")
st.markdown("### Challenge the computer. Can you beat the AI?")
st.caption("You are ✕ (X)  •  Computer is ○ (O)")

difficulty = st.selectbox(
    "Choose difficulty",
    ["Easy", "Medium", "Hard"],
    index=["Easy", "Medium", "Hard"].index(st.session_state.difficulty)
)

if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty

st.info(st.session_state.message)

# Scoreboard
c1, c2, c3 = st.columns(3)
c1.metric("👤 Player", st.session_state.scores["Player"])
c2.metric("🤖 AI", st.session_state.scores["AI"])
c3.metric("🤝 Draws", st.session_state.scores["Draws"])

st.markdown("---")
st.markdown("### Game Board")

symbols = {"X": "✕", "O": "○"}

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        value = st.session_state.board[index]
        label = symbols.get(value, "·")

        cols[col].button(
            label,
            key=f"cell_{index}",
            disabled=st.session_state.game_over or value is not None,
            on_click=play_turn,
            args=(index,)
        )

st.markdown("")

left, right = st.columns(2)

with left:
    if st.button("🔄 New Game", use_container_width=True):
        new_game()
        st.rerun()

with right:
    if st.button("🧹 Reset Score", use_container_width=True):
        st.session_state.scores = {"Player": 0, "AI": 0, "Draws": 0}
        new_game()
        st.rerun()

st.markdown("---")
st.caption("Built with Python, Streamlit & the Minimax algorithm.")


