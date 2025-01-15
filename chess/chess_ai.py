import random
from start_positions import OpeningBook

DEPTH = 4
pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 2, 2, 2, 2, 2, 2, 1], [1, 2, 3, 3, 3, 3, 2, 1], [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1], [1, 2, 3, 3, 3, 3, 2, 1], [1, 2, 2, 2, 2, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4], [3, 4, 3, 2, 2, 3, 4, 3], [2, 3, 4, 3, 3, 4, 3, 2], [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1], [2, 3, 4, 3, 3, 4, 3, 2], [3, 4, 3, 2, 2, 3, 4, 3], [4, 3, 2, 1, 1, 2, 3, 4]]
CHECKMATE = 1000
STALEMATE = 0
blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 1], [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1], [2, 3, 3, 5, 5, 3, 3, 2], [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]]
queenScores = [[1, 1, 1, 3, 1, 1, 1, 1], [1, 2, 3, 3, 3, 1, 1, 1], [1, 4, 3, 3, 3, 4, 2, 1], [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1], [1, 4, 3, 3, 3, 4, 2, 1], [1, 1, 2, 3, 3, 1, 1, 1], [1, 1, 1, 3, 1, 1, 1, 1]]
SET_WHITE_AS_BOT = -1
whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2], [1, 2, 3, 4, 4, 3, 2, 1], [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]
rookScores = [[4, 3, 4, 4, 4, 4, 3, 4], [4, 4, 4, 4, 4, 4, 4, 4], [1, 1, 2, 3, 3, 2, 1, 1], [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1], [1, 1, 2, 2, 2, 2, 1, 1], [4, 4, 4, 4, 4, 4, 4, 4], [4, 3, 2, 1, 1, 2, 3, 4]]
piecePositionScores = {"N": knightScores, "B": bishopScores, "Q": queenScores, "R": rookScores, "wp": whitePawnScores,
                       "bp": blackPawnScores}
opening_book = OpeningBook()


def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves, returnQueue):
    global nextMove, whitePawnScores, blackPawnScores
    nextMove = None
    random.shuffle(validMoves)
    if gs.playerWantsToPlayAsBlack: whitePawnScores, blackPawnScores = blackPawnScores, whitePawnScores
    SET_WHITE_AS_BOT = 1 if gs.whiteToMove else -1
    book_move = opening_book.get_book_move([m.getChessNotation() for m in gs.moveLog])
    if book_move:
        for move in validMoves:
            if move.getChessNotation() == book_move: returnQueue.put(move);return
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, SET_WHITE_AS_BOT)
    returnQueue.put(nextMove)
