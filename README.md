# Hangman Game with AI Assistant

A Streamlit web application that allows users to play the classic Hangman game with an intelligent AI assistant. The AI can either help players by suggesting guesses or play the game autonomously.

## Features

- **Two Game Modes**:
  - Player vs Computer: You guess the letters to find the hidden word
  - Watch AI Play: The AI assistant makes guesses to solve the puzzle

- **Intelligent AI Assistant**:
  - Uses pattern matching to find possible words
  - Employs frequency analysis for optimal guessing
  - Considers letter positions for informed decisions
  - Maximizes information gain with each guess

- **User-Friendly Interface**:
  - Visual hangman display that updates with each wrong guess
  - Interactive letter buttons for easy gameplay
  - Clean, responsive design with custom styling
  - Game status tracking and feedback

- **Airline-Themed Vocabulary**:
  - Specialized dictionary of airline-related terms
  - Challenging and educational word selection

## Installation

1. Clone or download this repository to your local machine.

2. Navigate to the project directory:
   cd hangman-game-ai

3. Install the required dependencies:
    pip install -r requirements.txt

4. Running the Application
    Start the Streamlit application:
    streamlit run hangman_app.py
