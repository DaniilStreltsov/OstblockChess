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


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            gs.checkmate = False
            return -CHECKMATE
        else:
            gs.checkmate = False
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if SET_WHITE_AS_BOT:
                    if square[0] == "w":
                        score += pieceScore[square[1]] + piecePositionScore * 0.1
                    elif square[0] == "b":
                        score -= pieceScore[square[1]] + piecePositionScore * 0.1
                else:
                    if square[0] == "w":
                        score -= pieceScore[square[1]] + piecePositionScore * 0.1
                    elif square[0] == "b":
                        score += pieceScore[square[1]] + piecePositionScore * 0.1
    return score


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
