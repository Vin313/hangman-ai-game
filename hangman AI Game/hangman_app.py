import streamlit as st
import json
import random
from hangman_model import HangmanAI
from word_list import AIRLINE_WORDS

# Initialize the AI
ai = HangmanAI(AIRLINE_WORDS)

# Set page configuration
st.set_page_config(
    page_title="Hangman Game with AI",
    page_icon="🎮",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #4682B4;
        margin-bottom: 1rem;
    }
    .game-container {
        background-color: #F0F8FF;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .word-display {
        font-size: 2.5rem;
        letter-spacing: 0.5rem;
        text-align: center;
        margin: 2rem 0;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    .hangman-drawing {
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        line-height: 1.4;
        white-space: pre;
        text-align: center;
        margin: 1rem 0;
    }
    .guess-button {
        width: 3rem;
        height: 3rem;
        margin: 0.3rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .message {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    .success {
        background-color: #90EE90;
        color: #006400;
    }
    .warning {
        background-color: #FFD700;
        color: #8B4513;
    }
    .error {
        background-color: #FFB6C1;
        color: #8B0000;
    }
    .info {
        background-color: #ADD8E6;
        color: #000080;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Hangman drawings for different stages
HANGMAN_PICS = [
    """
     -----
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """
]

def initialize_game():
    """Initialize or reset the game state"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = {
            'word': random.choice(AIRLINE_WORDS).upper(),
            'guessed_letters': [],
            'incorrect_guesses': 0,
            'game_over': False,
            'game_won': False,
            'mode': 'player',  # 'player' or 'ai'
            'ai_thinking': False
        }

def get_word_display():
    """Get the current word display with blanks for unguessed letters"""
    word = st.session_state.game_state['word']
    guessed = st.session_state.game_state['guessed_letters']
    
    display = []
    for letter in word:
        if letter in guessed:
            display.append(letter)
        else:
            display.append('_')
    
    return ' '.join(display)

def make_guess(letter):
    """Process a letter guess"""
    if st.session_state.game_state['game_over']:
        return
    
    # Add the letter to guessed letters
    if letter not in st.session_state.game_state['guessed_letters']:
        st.session_state.game_state['guessed_letters'].append(letter)
        
        # Check if the guess is incorrect
        if letter not in st.session_state.game_state['word']:
            st.session_state.game_state['incorrect_guesses'] += 1
            
            # Check if game is lost
            if st.session_state.game_state['incorrect_guesses'] >= 6:
                st.session_state.game_state['game_over'] = True
        
        # Check if game is won
        word = st.session_state.game_state['word']
        guessed = st.session_state.game_state['guessed_letters']
        if all(letter in guessed for letter in word):
            st.session_state.game_state['game_over'] = True
            st.session_state.game_state['game_won'] = True

def get_ai_guess():
    """Get a guess from the AI"""
    current_state = get_word_display()
    guessed_letters = st.session_state.game_state['guessed_letters']
    guesses_remaining = 6 - st.session_state.game_state['incorrect_guesses']
    
    input_data = {
        "currentWordState": current_state,
        "guessedLetters": guessed_letters,
        "guessesRemaining": guesses_remaining
    }
    
    result = ai.process_input(input_data)
    guess = json.loads(result)['nextGuess'].upper()
    
    return guess

def main():
    # Initialize game state
    initialize_game()
    
    # Header
    st.markdown('<h1 class="main-header">🎮 Hangman Game with AI Assistant</h1>', unsafe_allow_html=True)
    
    # Game mode selection
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sub-header">Game Mode</div>', unsafe_allow_html=True)
        mode = st.radio(
            "Select game mode:",
            ["Player vs Computer", "Watch AI Play"],
            horizontal=True,
            key="mode_selector"
        )
        
        # Update game mode
        if mode == "Player vs Computer":
            st.session_state.game_state['mode'] = 'player'
        else:
            st.session_state.game_state['mode'] = 'ai'
    
    with col2:
        # Reset button
        if st.button("🔄 New Game", use_container_width=True):
            initialize_game()
            st.rerun()
    
    # Game container
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    
    # Display hangman drawing
    incorrect_guesses = st.session_state.game_state['incorrect_guesses']
    st.markdown(f'<div class="hangman-drawing">{HANGMAN_PICS[incorrect_guesses]}</div>', unsafe_allow_html=True)
    
    # Display word with blanks
    word_display = get_word_display()
    st.markdown(f'<div class="word-display">{word_display}</div>', unsafe_allow_html=True)
    
    # Display game status
    if st.session_state.game_state['game_over']:
        if st.session_state.game_state['game_won']:
            st.markdown(f'<div class="message success">Congratulations! You won! The word was: {st.session_state.game_state["word"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message error">Game over! The word was: {st.session_state.game_state["word"]}</div>', unsafe_allow_html=True)
    else:
        remaining_guesses = 6 - st.session_state.game_state['incorrect_guesses']
        st.markdown(f'<div class="message info">Remaining guesses: {remaining_guesses}</div>', unsafe_allow_html=True)
    
    # AI thinking and guessing
    if st.session_state.game_state['mode'] == 'ai' and not st.session_state.game_state['game_over']:
        if st.button("🤖 AI Guess", key="ai_guess_button"):
            st.session_state.game_state['ai_thinking'] = True
            ai_guess = get_ai_guess()
            make_guess(ai_guess)
            st.rerun()
    
    # Letter buttons for player input
    if st.session_state.game_state['mode'] == 'player' and not st.session_state.game_state['game_over']:
        st.markdown('<div class="sub-header">Make a Guess</div>', unsafe_allow_html=True)
        
        # Create 4 rows of letter buttons
        for row in range(4):
            cols = st.columns(7)
            for col_idx in range(7):
                letter_index = row * 7 + col_idx
                if letter_index < 26:
                    letter = chr(65 + letter_index)  # A to Z
                    disabled = letter in st.session_state.game_state['guessed_letters'] or st.session_state.game_state['game_over']
                    
                    if cols[col_idx].button(letter, key=f"btn_{letter}", disabled=disabled, use_container_width=True):
                        make_guess(letter)
                        st.rerun()
    
    # Display guessed letters
    guessed_letters = st.session_state.game_state['guessed_letters']
    if guessed_letters:
        st.markdown(f'<div class="message info">Guessed letters: {", ".join(sorted(guessed_letters))}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close game container
    
    # Instructions and information
    with st.expander("ℹ️ How to Play & About the AI"):
        st.markdown("""
        ### How to Play Hangman
        1. Guess letters one at a time to reveal the hidden word
        2. You have 6 incorrect guesses before the game is over
        3. Guess all letters correctly to win!
        
        ### Game Modes
        - **Player vs Computer**: You guess the letters to find the hidden word
        - **Watch AI Play**: The AI assistant makes guesses to solve the puzzle
        
        ### About the AI Assistant
        The AI uses several strategies to make intelligent guesses:
        - **Pattern Matching**: Finds words that match the current revealed letters
        - **Frequency Analysis**: Prioritizes commonly used letters in the English language
        - **Position Analysis**: Considers which letters are most likely in each position
        - **Information Gain**: Chooses letters that will provide the most information
        
        The AI is trained on a vocabulary of airline-related terms.
        """)
    
    # Debug information (optional)
    if st.checkbox("Show debug info"):
        st.write("Game state:", st.session_state.game_state)

if __name__ == "__main__":
    main()