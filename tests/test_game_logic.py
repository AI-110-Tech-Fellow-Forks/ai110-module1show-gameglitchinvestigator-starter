import sys
from pathlib import Path

# Add parent directory to path so we can import logic_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# Original tests
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# FIX: Tests for hints accuracy (verifying type mismatch bug is fixed)
def test_hints_consistency_with_integers():
    """Hints should work correctly when comparing integers."""
    # Guess too high
    outcome, message = check_guess(100, 50)
    assert outcome == "Too High"

    # Guess too low
    outcome, message = check_guess(10, 50)
    assert outcome == "Too Low"

    # Exact match
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_hints_edge_cases():
    """Test hints at range boundaries."""
    # Boundary test: guess at edge
    outcome, message = check_guess(1, 50)
    assert outcome == "Too Low"

    outcome, message = check_guess(100, 50)
    assert outcome == "Too High"


# FIX: Tests for out-of-range validation
def test_parse_guess_valid():
    """Valid guesses should parse correctly."""
    ok, guess_int, err = parse_guess("50")
    assert ok is True
    assert guess_int == 50
    assert err is None


def test_parse_guess_invalid_non_number():
    """Non-numeric input should fail."""
    ok, guess_int, err = parse_guess("abc")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_empty():
    """Empty input should fail."""
    ok, guess_int, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."


def test_parse_guess_none():
    """None input should fail."""
    ok, guess_int, err = parse_guess(None)
    assert ok is False
    assert err == "Enter a guess."


def test_parse_guess_float():
    """Float input should be converted to int."""
    ok, guess_int, err = parse_guess("50.7")
    assert ok is True
    assert guess_int == 50


# FIX: Tests for difficulty ranges
def test_range_easy():
    """Easy mode should have range 1-20."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_range_normal():
    """Normal mode should have range 1-100."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_range_hard():
    """Hard mode should have range 1-50."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50


# FIX: Tests for guess validation in range
def test_guess_in_range():
    """Valid guess within range should be accepted by parse_guess."""
    low, high = get_range_for_difficulty("Normal")
    ok, guess_int, err = parse_guess("50")
    assert ok is True
    assert low <= guess_int <= high


def test_guess_out_of_range_too_high():
    """Guess above range should be identified as out of range."""
    low, high = get_range_for_difficulty("Normal")
    ok, guess_int, err = parse_guess("300")
    assert ok is True  # parse_guess only validates format, not range
    assert guess_int > high  # Out of range should be detected by app logic


def test_guess_out_of_range_too_low():
    """Guess below range should be identified as out of range."""
    low, high = get_range_for_difficulty("Normal")
    ok, guess_int, err = parse_guess("-50")
    assert ok is True  # parse_guess only validates format, not range
    assert guess_int < low  # Out of range should be detected by app logic


# FIX: Tests for score updates
def test_score_update_on_win():
    """Score should increase significantly on win."""
    current_score = 0
    new_score = update_score(current_score, "Win", attempt_number=1)
    assert new_score > current_score
    assert new_score >= 80  # First win should be 90-10*2=70, but min is 10


def test_score_update_too_high():
    """Score should decrease on too high guess (odd attempts)."""
    current_score = 100
    new_score = update_score(current_score, "Too High", attempt_number=1)
    assert new_score == 95  # Odd attempt: -5


def test_score_update_too_low():
    """Score should decrease on too low guess."""
    current_score = 100
    new_score = update_score(current_score, "Too Low", attempt_number=1)
    assert new_score == 95  # -5


def test_score_consistency_multiple_attempts():
    """Score updates should be consistent across multiple attempts."""
    score = 0

    # First wrong guess
    score = update_score(score, "Too High", attempt_number=1)
    assert score == -5

    # Second wrong guess
    score = update_score(score, "Too High", attempt_number=2)
    assert score == 0  # Even attempt: +5

    # Win on third attempt
    score = update_score(score, "Win", attempt_number=3)
    assert score > 0
