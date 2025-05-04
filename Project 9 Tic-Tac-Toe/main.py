import streamlit as st
import random

# --- Game Logic Class ---
class TicTacToe:
    def __init__(self):
        # Initializing the board with 9 empty spots
        self.board = ['' for _ in range(9)]
        # To keep track of the current winner
        self.current_winner = None

    def make_move(self, square, letter):
        # Make a move if the spot is empty, then check for a winner
        if self.board[square] == '':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def available_moves(self):
        # Return a list of indices where the board is empty
        return [i for i, x in enumerate(self.board) if x == '']

    def is_full(self):
        # Check if the board is full
        return '' not in self.board

    def check_winner(self, square, letter):
        # Check if a player has won after making a move
        # Check the row where the move was made
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Check the column where the move was made
        col_ind = square % 3
        col = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in col]):
            return True

        # Check both diagonals if the square is one of the diagonal positions (0, 2, 4, 6, 8)
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0,4,8]]  # Left-to-right diagonal
            diag2 = [self.board[i] for i in [2,4,6]]  # Right-to-left diagonal
            if all([spot == letter for spot in diag1]) or all([spot == letter for spot in diag2]):
                return True

        return False

# --- Initialize session state ---
# Streamlit session_state is used to store the game state across reruns
if 'game' not in st.session_state:
    # Create a new TicTacToe game if it doesn't exist
    st.session_state.game = TicTacToe()
    # Set the initial turn to 'X' (the human player)
    st.session_state.turn = 'X'  
    # Set the initial game status message
    st.session_state.status = "🎮 Your turn!"
    # Keep track of the last clicked cell (for use in computer's move logic)
    st.session_state.last_clicked = None

game = st.session_state.game

# --- Streamlit Interface ---
# Title of the game
st.title("🎲 Tic Tac Toe ")
# Display the current game status (e.g., "Your turn", "You win", etc.)
st.subheader(st.session_state.status)

# --- Game Grid (3x3 board layout) ---
# Use Streamlit columns to create a grid layout for the game board
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        # Check the content of the cell in the game board
        cell = game.board[i]
        # If the cell is empty, allow the human player to make a move
        if cell == '':
            if st.session_state.turn == 'X':
                # Create a button for each cell to handle player input
                if st.button(" ", key=f"cell_{i}"):
                    # Make the move for player 'X'
                    game.make_move(i, 'X')
                    st.session_state.last_clicked = i
                    # Check if player 'X' won after the move
                    if game.current_winner:
                        st.session_state.status = "🏆 You win!"  # Player 'X' wins
                        st.session_state.turn = None  # End the game
                    # Check if the game is a tie (board is full but no winner)
                    elif game.is_full():
                        st.session_state.status = "🤝 It's a tie!"  # Tie
                        st.session_state.turn = None  # End the game
                    else:
                        # Switch turn to player 'O' (the computer)
                        st.session_state.turn = 'O'
                    # Trigger a rerun to update the UI after a move
                    st.rerun()
            else:
                # Show a placeholder if it's the computer's turn
                st.markdown("### ⬜")
        else:
            # Display the current player's move (either 'X' or 'O')
            st.markdown(f"### {cell}")

# --- Computer's Turn ---
# If it's the computer's turn (turn = 'O')
if st.session_state.turn == 'O':
    # Get the list of available moves for the computer
    available = game.available_moves()
    if available:
        # Select a random available move for the computer
        move = random.choice(available)
        # Make the move for the computer
        game.make_move(move, 'O')
        # Check if the computer has won
        if game.current_winner:
            st.session_state.status = "💻 Computer wins!"  # Computer wins
            st.session_state.turn = None  # End the game
        # Check if the game is a tie
        elif game.is_full():
            st.session_state.status = "🤝 It's a tie!"  # Tie
            st.session_state.turn = None  # End the game
        else:
            # Switch turn to player 'X' (human player)
            st.session_state.turn = 'X'
        # Trigger a rerun to update the UI after the computer's move
        st.rerun()

# --- Restart Game ---
# A button to restart the game
st.markdown("---")
if st.button("🔁 Restart Game"):
    # Reset the game state and session variables
    st.session_state.game = TicTacToe()
    st.session_state.turn = 'X'  # Set human player 'X' as the first player
    st.session_state.status = "🎮 Your turn!"  # Set initial status message
    st.session_state.last_clicked = None  # Reset last clicked cell
    # Trigger a rerun to restart the game UI
    st.rerun()
