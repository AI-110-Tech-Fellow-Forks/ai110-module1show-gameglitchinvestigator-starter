import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

# Initialize all session state variables upfront
if "status" not in st.session_state:
    st.session_state.status = "playing"

if "game_difficulty" not in st.session_state:
    st.session_state.game_difficulty = "Normal"

if "secret" not in st.session_state:
    low, high = get_range_for_difficulty(st.session_state.game_difficulty)
    st.session_state.secret = random.randint(low, high)

# FIX: Attempts counter was off by one - identified with Claude Code analysis
# Changed initialization from 1 to 0 for correct display
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

# FIX: Prevent difficulty changes mid-game using Claude Code AI assistance
# Store difficulty in session state and disable selector when playing
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=["Easy", "Normal", "Hard"].index(st.session_state.game_difficulty),
    disabled=st.session_state.status == "playing"
)

if st.session_state.status == "playing":
    difficulty = st.session_state.game_difficulty
else:
    st.session_state.game_difficulty = difficulty

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.subheader("Make a guess")

# FIX: Range display was hardcoded to 1-100 - Claude Code identified and fixed
# Now dynamically displays actual range based on difficulty selection
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game button wasn't resetting game state - Claude Code identified and fixed
# Now properly resets status, score, history, and respects difficulty selection
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: Guesses outside range were being accepted - Claude Code added validation
        if guess_int < low or guess_int > high:
            st.error(f"Please guess a number between {low} and {high}.")
        else:
            # FIX: Hints were incorrect due to type mismatch - Claude Code removed buggy conversion
            # Now always compares guess and secret as same type for accurate feedback
            outcome, message = check_guess(guess_int, st.session_state.secret)

            if show_hint:
                st.warning(message)

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(
                        f"Out of attempts! "
                        f"The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
