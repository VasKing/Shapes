import chess
import chess.pgn
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os
import chess.engine


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

themes = {
    "default": {"dark_square": "#436F46", "light_square": "#EAECE7"},#green
    "gray": {"dark_square": "#808080", "light_square": "#D3D3D3"},
    "brown": {"dark_square": "#A78350", "light_square": "#EFDFC7"},
    "blue": {"dark_square": "#517C94", "light_square": "#F1F6F9"}
}

class ChessGameApp:
    def __init__(self, master, game_file):
        self.master = master
        master.title("ChessViewer (V.Aristotelous @ 2024)")

        self.stockfish_path = resource_path(os.path.join('stockfish', 'stockfish.exe'))
        self.stockfish = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
        self.stockfish.configure({"UCI_AnalyseMode": True})

        self.last_evaluation_score = None

        self.board = chess.Board()
        self.moves = []

        self.canvas = tk.Canvas(master, width=470, height=525)
        self.canvas.pack()

        self.load_pgn(game_file)
        self.playback_index = 0
        self.square_size = 55
        self.piece_images = self.load_piece_images()

        self.current_theme = "default"
        self.update_theme()

        self.display_board()

        self.master.bind("<Right>", self.next_move)
        self.master.bind("<Left>", self.prev_move)
        self.master.bind("<Down>", self.start_autoplay)
        self.master.bind("<Up>", self.stop_autoplay)

        self.master.bind("1", lambda event, theme="default": self.switch_theme(event, theme))
        self.master.bind("2", lambda event, theme="gray": self.switch_theme(event, theme))
        self.master.bind("3", lambda event, theme="brown": self.switch_theme(event, theme))
        self.master.bind("4", lambda event, theme="blue": self.switch_theme(event, theme))

        self.autoplay_active = False
        self.autoplay_delay = 500  # milliseconds, adjusted for a slower pace

    def close_application(self):
        try:
            if self.stockfish:
                self.stockfish.quit()
        except Exception as e:
            print(f"Error shutting down Stockfish: {e}")
        finally:
            self.master.destroy()

        self.master.protocol("WM_DELETE_WINDOW", self.close_application)

    def load_pgn(self, file_path):
        try:
            with open(file_path, "r") as file:
                game = chess.pgn.read_game(file)
                self.moves = [move for move in game.mainline_moves()]
                result = game.headers.get("Result", "*")
                self.game_result = result
        except Exception as e:
            messagebox.showerror("Error", f"Error loading PGN: {str(e)}")

    def load_piece_images(self):
        piece_images = {}
        colors = ["w", "b"]
        images_folder = resource_path("Images")  # Use resource_path to adjust the path

        for color in colors:
            for piece_name in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                key = f"{color}_{piece_name}"
                image_path = os.path.join(images_folder, f"{key}.png")
                try:
                    image = Image.open(image_path)
                    size_factor = 0.62 if piece_name == "pawn" else 0.73
                    new_size = int(self.square_size * size_factor)
                    image = image.resize((new_size, new_size))
                    image = ImageTk.PhotoImage(image)
                    piece_images[key] = image
                except Exception as e:
                    print(f"Error loading image: {image_path}, {e}")
        return piece_images

    def get_stockfish_evaluation(self, board, time_limit=0.5):
        result = self.stockfish.analyse(board, chess.engine.Limit(time=time_limit))
        score = result['score'].white()

        if score.is_mate():
            score_str = f"Mate in {score.mate()}"
            current_evaluation = float('inf')  # Represent mate as infinity for comparison
        else:
            cp_score = score.score()
            pawn_score = cp_score / 100.0
            score_str = f"{pawn_score:+.2f}"
            current_evaluation = pawn_score

        # Take action if the evaluation change exceeds a full point
        if self.last_evaluation_score is not None:
            if abs(current_evaluation - self.last_evaluation_score) >= 1:
                self.display_mistake_indicator()

        self.last_evaluation_score = current_evaluation  # Update last evaluation for next move
        return score_str

    def display_mistake_indicator(self):
        canvas_width = 470  # Use the actual width of your canvas
        text_y = 17  # Keep the vertical position as before, near the top
        text_x = canvas_width / 2  # Calculate the center of the canvas width

        self.canvas.create_text(text_x, text_y, text="MISTAKE!", fill="red", font=("Helvetica", 10, "bold"),
                                tags='mistake_indicator')

    def draw_evaluation_bar(self):
        bar_width = 20
        bar_height = self.square_size * 8
        padding_left = 5
        self.bar_x = padding_left
        self.bar_y = self.square_size - 25

        # Draw the evaluation bar
        self.canvas.create_rectangle(self.bar_x, self.bar_y, self.bar_x + bar_width, self.bar_y + bar_height / 2,
                                     fill="grey", tags="eval_bar")
        self.canvas.create_rectangle(self.bar_x, self.bar_y + bar_height / 2, self.bar_x + bar_width,
                                     self.bar_y + bar_height, fill="white", tags="eval_bar")

        marker_x_start = self.bar_x - padding_left  # Adjust this to position the marker within the visible padding area
        marker_x_end = self.bar_x  # Up to the start of the evaluation bar
        middle_y = self.bar_y + (bar_height / 2)

        # Ensure the marker is visible by checking these coordinates
        self.canvas.create_line(marker_x_start, middle_y, marker_x_end, middle_y, fill="blue", width=2,
                                tags="eval_bar_marker")

    def update_evaluation_bar(self, eval_score):
        bar_width = 20  # Width of the evaluation bar
        bar_height = self.square_size * 8  # Total height of the bar
        half_bar_height = bar_height / 2  # Middle point of the bar

        # Normalize the eval_score to fit within the bar's height.
        # Assuming eval_score range is -10 to +10 for simplicity. Adjust based on your expected eval range.
        max_eval = 10
        eval_proportion = eval_score / max_eval

        # Calculate the dynamic height of the white section based on the evaluation score.
        white_height = half_bar_height * (1 + eval_proportion)  # This increases as white advantage increases

        # Ensure the white section never exceeds the total bar height and is never negative
        white_height = max(0, min(white_height, bar_height))

        # Calculate the starting y-coordinate for the white section
        white_start_y = self.bar_y + (bar_height - white_height)

        # The black (or gray) section simply fills the rest of the bar
        black_height = bar_height - white_height

        # Update the bar display
        self.canvas.delete("eval_bar")  # Remove the old bar sections
        # Draw the new black (or gray) section from the top
        self.canvas.create_rectangle(self.bar_x, self.bar_y, self.bar_x + bar_width, self.bar_y + black_height,
                                     fill="grey", tags="eval_bar")
        # Draw the new white section from its dynamic starting point
        self.canvas.create_rectangle(self.bar_x, white_start_y, self.bar_x + bar_width, self.bar_y + bar_height,
                                     fill="white", tags="eval_bar")

    def display_board(self):
        self.canvas.delete("mistake_indicator")
        self.canvas.delete("all")
        self.draw_evaluation_bar()  # Initial draw of the evaluation bar; no need to call it again in this method
        self.draw_chessboard()
        self.draw_pieces()
        self.display_players()

        fen_position = self.board.fen()
        evaluation = self.get_stockfish_evaluation(chess.Board(fen_position))
        # Assuming evaluation is a string like "+0.32", convert it to float
        try:
            eval_score = float(evaluation)
        except ValueError:  # Handle special cases like "Mate in ..."
            # For "Mate in ...", we need a different approach or just set a high/low value
            eval_score = 100 if "Mate in" in evaluation else 0  # Example approach

        # Update the evaluation bar with the current score
        # This is where you dynamically update the evaluation bar
        self.update_evaluation_bar(
            eval_score)  # Ensure this method exists and is implemented to update the bar based on eval_score

        result = self.stockfish.play(chess.Board(fen_position), chess.engine.Limit(time=0.5))
        best_move = result.move
        shortened_algebraic = self.board.san(best_move)
        print(f"BestMove: {shortened_algebraic}", f"   Evaluation: {evaluation}")
        self.canvas.create_text(20, 17, text=f"Evaluation: {evaluation}", font=("Helvetica", 10), anchor="w")
        self.canvas.create_text(395, 17, text=f"Best Move: {shortened_algebraic}", font=("Helvetica", 10), anchor="e")

    def draw_chessboard(self):
        for row in range(8):
            for col in range(8):
                x, y = col * self.square_size + 30, (row + 1) * self.square_size -25  # Add 30 to x-coordinate
                square_color = self.light_square_color if (row + col) % 2 == 0 else self.dark_square_color
                self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, fill=square_color)

    def draw_pieces(self):
        offset_x = 30  # Adjust this value based on the width of your evaluation bar + padding
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                color = "w" if piece.color else "b"
                piece_name = chess.piece_name(piece.piece_type).lower()
                key = f"{color}_{piece_name}"
                image = self.piece_images.get(key, None)
                if image:
                    col, row = chess.square_file(square), 7 - chess.square_rank(square)
                    # Add offset_x to the x coordinate to shift pieces to the right
                    x, y = (col * self.square_size) + offset_x, (row + 0.55) * self.square_size
                    self.canvas.create_image(x + self.square_size / 2, y + self.square_size / 2, image=image)

    def display_players(self):
        with open(game_file, "r", encoding="utf-8") as file:
            lines = [line.lstrip('\ufeff').rstrip() for line in file.readlines()][:2]
        result = "\n".join(lines)
        self.canvas.create_text(220, 500, text=result, font=("Helvetica", 11), justify="center")

    def update_theme(self):
        theme = themes.get(self.current_theme, themes["default"])
        self.dark_square_color = theme["dark_square"]
        self.light_square_color = theme["light_square"]
        self.display_board()

    def switch_theme(self, event, theme_name):
        self.current_theme = theme_name
        self.update_theme()

    def next_move(self, event):
        if self.playback_index < len(self.moves):
            move = self.moves[self.playback_index]
            self.board.push(move)
            self.display_board()
            self.print_fen()  # Print FEN after every move
            self.playback_index += 1
            # Check for the end of the game
            if self.playback_index == len(self.moves):
                self.display_game_result()
        else:
            self.display_game_result()

    def print_fen(self):
        fen = self.board.fen()
        print(f"FEN: {fen}")

    def display_game_result(self):
        text = f"{self.game_result}"
        self.canvas.create_text(200, 200, text=text, font=("Helvetica", 40), fill="red", anchor="center")

    def prev_move(self, event):
        if self.playback_index > 0:
            self.playback_index -= 1
            self.board.pop()
            self.display_board()

    def start_autoplay(self, event):
        if not self.autoplay_active:
            self.autoplay_active = True
            self.autoplay()

    def stop_autoplay(self, event):
        self.autoplay_active = False

    def autoplay(self):
        if self.autoplay_active and self.playback_index < len(self.moves):
            move = self.moves[self.playback_index]
            self.board.push(move)
            self.display_board()
            self.playback_index += 1
            # Check for the end of the game during autoplay
            if self.playback_index == len(self.moves):
                self.display_game_result()
            else:
                self.master.after(self.autoplay_delay, self.autoplay)

    def __del__(self):
        self.stockfish.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game_file = resource_path("PGNgames/Aristotelous_Artemiou.pgn")
    app = ChessGameApp(root, game_file)

    icon_path = resource_path(os.path.join("Images", "PawnIcon.ico"))
    if os.path.exists(icon_path):
        root.iconbitmap(default=icon_path)

    root.mainloop()
