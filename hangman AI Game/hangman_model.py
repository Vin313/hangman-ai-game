import json
import re
from collections import Counter
import math

class HangmanAI:
    def __init__(self, word_list=None):
        """
        Initialize the Hangman AI with a word list
        """
        if word_list is None:
            # Default airline-related words if no list provided
            self.word_list = [
                "airplane", "airport", "airline", "boarding", "terminal",
                "cockpit", "flight", "pilot", "steward", "baggage",
                "takeoff", "landing", "turbulence", "emergency", "passenger",
                "security", "departure", "arrival", "luggage", "aircraft",
                "runway", "gate", "crew", "cabin", "jetway",
                "ticket", "boardingpass", "overhead", "lavatory", "oxygen",
                "seatbelt", "traytable", "beverage", "meal", "entertainment",
                "connection", "layover", "destination", "itinerary", "reservation",
                "upgrade", "firstclass", "business", "economy", "premium",
                "checkin", "carryon", "checked", "baggageclaim", "customs",
                "immigration", "visa", "passport", "dutyfree", "shuttle",
                "hangar", "controltower", "radar", "navigation", "autopilot",
                "throttle", "rudder", "elevator", "aileron", "flaps",
                "landinggear", "propeller", "turbine", "engine", "fuselage",
                "wing", "tail", "cockpit", "blackbox", "transponder",
                "altitude", "airspeed", "heading", "course", "waypoint",
                "fuel", "kerosene", "aviation", "aeronautics", "aerodynamics",
                "meteorology", "weather", "turbulence", "clearance", "approach",
                "takeoff", "landing", "taxiing", "deicing", "maintenance"
            ]
        else:
            self.word_list = word_list
        
        self._build_frequency_analysis()
    
    def _build_frequency_analysis(self):
        """
        Build letter frequency analysis from the word list
        """
        # Count letter frequencies
        all_text = ' '.join(self.word_list).lower()
        self.letter_freq = Counter(all_text)
        
        # Remove non-alphabet characters
        for char in list(self.letter_freq.keys()):
            if not char.isalpha():
                del self.letter_freq[char]
        
        # Calculate position-specific frequencies
        max_word_length = max(len(word) for word in self.word_list)
        self.position_freq = [Counter() for _ in range(max_word_length)]
        
        for word in self.word_list:
            word_lower = word.lower()
            for i, char in enumerate(word_lower):
                if char.isalpha() and i < max_word_length:
                    self.position_freq[i][char] += 1
    
    def _get_possible_words(self, pattern, guessed_letters):
        """
        Get all words that match the current pattern and haven't been guessed
        """
        # Convert pattern to regex (e.g., "_ _ e _ a n" -> "^..e.a.n$")
        regex_pattern = pattern.replace(' ', '').replace('_', '.')
        regex_pattern = f"^{regex_pattern}$"
        
        possible_words = []
        guessed_set = set(letter.lower() for letter in guessed_letters)
        
        for word in self.word_list:
            word_lower = word.lower()
            
            # Check if word length matches pattern
            if len(word_lower) != len(regex_pattern) - 2:  # -2 for ^ and $
                continue
            
            # Check if word matches pattern
            if not re.match(regex_pattern, word_lower):
                continue
            
            # Check if word contains any already guessed wrong letters
            contains_wrong_guess = any(
                char in word_lower and char not in pattern.replace(' ', '').replace('_', '')
                for char in guessed_set
            )
            
            if not contains_wrong_guess:
                possible_words.append(word_lower)
        
        return possible_words
    
    def _calculate_letter_scores(self, possible_words, guessed_letters):
        """
        Calculate scores for each letter based on frequency and information gain
        """
        letter_scores = {}
        guessed_set = set(letter.lower() for letter in guessed_letters)
        
        # Count frequency in possible words
        freq_counter = Counter()
        for word in possible_words:
            for char in set(word):  # Count each letter only once per word
                if char not in guessed_set:
                    freq_counter[char] += 1
        
        # Calculate scores with some heuristics
        for char, count in freq_counter.items():
            if char in guessed_set:
                continue
            
            # Base score is frequency in possible words
            score = count
            
            # Add global frequency weight
            global_freq = self.letter_freq.get(char, 0)
            score *= (1 + math.log(global_freq + 1) / 10)
            
            letter_scores[char] = score
        
        return letter_scores
    
    def get_next_guess(self, current_word_state, guessed_letters, guesses_remaining):
        """
        Main method to get the next guess
        """
        # Clean inputs
        pattern = current_word_state.lower().replace(' ', '')
        guessed_letters = [g.lower() for g in guessed_letters]
        
        # Get possible words that match the current pattern
        possible_words = self._get_possible_words(pattern, guessed_letters)
        
        if not possible_words:
            # Fallback: guess by global frequency
            available_letters = [c for c in 'abcdefghijklmnopqrstuvwxyz' 
                               if c not in guessed_letters]
            if not available_letters:
                return 'a'  # Should never happen
            
            # Return most frequent available letter
            return max(available_letters, key=lambda x: self.letter_freq.get(x, 0))
        
        # Calculate letter scores
        letter_scores = self._calculate_letter_scores(possible_words, guessed_letters)
        
        if not letter_scores:
            # No good letters found, use fallback
            available_letters = [c for c in 'abcdefghijklmnopqrstuvwxyz' 
                               if c not in guessed_letters]
            return available_letters[0] if available_letters else 'a'
        
        # Return letter with highest score
        return max(letter_scores.items(), key=lambda x: x[1])[0]
    
    def process_input(self, input_json):
        """
        Process JSON input and return JSON output
        """
        try:
            data = json.loads(input_json) if isinstance(input_json, str) else input_json
            
            current_word_state = data.get('currentWordState', '')
            guessed_letters = data.get('guessedLetters', [])
            guesses_remaining = data.get('guessesRemaining', 6)
            
            next_guess = self.get_next_guess(current_word_state, guessed_letters, guesses_remaining)
            
            return json.dumps({'nextGuess': next_guess})
            
        except Exception as e:
            return json.dumps({'error': str(e), 'nextGuess': 'a'})