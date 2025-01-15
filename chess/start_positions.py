class OpeningBook:
    def __init__(self):
        self.openings = {
            "start": {
                "moves": ["e2e4", "d2d4"],
                "names": ["King's Pawn", "Queen's Pawn"]
            },
            "e2e4": {
                "moves": ["e7e5", "c7c5", "e7e6"],
                "names": ["King's Pawn Game", "Sicilian Defense", "French Defense"]
            },
            "d2d4": {
                "moves": ["d7d5", "g8f6"],
                "names": ["Queen's Pawn Game", "Indian Defense"]
            }
        }

    def get_book_move(self, move_history):
        if not move_history:
            return self.openings["start"]["moves"][0]

        last_move = move_history[-1]
        if last_move in self.openings:
            moves = self.openings[last_move]["moves"]
            if moves:
                return moves[0]

        return None