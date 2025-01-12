class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.board1 = [
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        # set playerWantsToPlayAsBlack = True if you want to flip board and play as black
        self.playerWantsToPlayAsBlack = False
        self.moveLog = []
        # keeping track of king positions to prevent from checks and also it makes castling easier
        if (self.playerWantsToPlayAsBlack):
            self.whiteKinglocation = (0, 4)
            self.blackKinglocation = (7, 4)
        else:
            self.whiteKinglocation = (7, 4)
            self.blackKinglocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.inCheck = False
        self.score = 0
        self.pins = []
        self.checks = []
        # co-ordinates for square where enpassant is possible
        self.enpasantPossible = ()
        self.enpasantPossibleLog = [self.enpasantPossible]
        # castling rights
        self.whiteCastleKingside = True
        self.whiteCastleQueenside = True
        self.blackCastleKingside = True
        self.blackCastleQueenside = True
        self.castleRightsLog = [castleRights(
            self.whiteCastleKingside, self.whiteCastleQueenside, self.blackCastleKingside, self.blackCastleQueenside)]
        
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # save history of the moved played
        self.moveLog.append(move)
        # swap player
        self.whiteToMove = not self.whiteToMove

        # update king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKinglocation = (move.endRow, move.endCol)
            self.whiteCastleKingside = False
            self.whiteCastleQueenside = False
        elif move.pieceMoved == 'bK':
            self.blackKinglocation = (move.endRow, move.endCol)
            self.blackCastleKingside = False
            self.blackCastleQueenside = False

        # pawn promotion
        # if move.isPawnPromotion:
            # self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant move
        if move.isEnpassantMove:
            # capture piece, (same row , end col ) is the location of the opponent pawn from our pawn
            self.board[move.startRow][move.endCol] = '--'

        # update enpassant variable everytime piece is moved
        # only on 2 square pawn advances
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            # valid square will be between (startRow and endRow, endcol or startCol(because opponent's pawn 2 square move is on same col))
            # if we do the average of startRow and endRow it will be valid for both black and white
            self.enpasantPossible = (
                (move.startRow + move.endRow)//2, move.startCol)
        else:
            # if after opponent move its pawn to second square instead of capturing it with enpassant we played different move then enpassant move will not be possible
            self.enpasantPossible = ()

        # update Log which side castle is possible
        self.updateCastleRights(move)
        self.castleRightsLog.append(castleRights(
            self.whiteCastleKingside, self.whiteCastleQueenside, self.blackCastleKingside, self.blackCastleQueenside))

        # update enpasantPossibleLog
        self.enpasantPossibleLog.append(self.enpasantPossible)

        # castle moves
        if move.castle:
            # King Side
            if move.endCol - move.startCol == 2:
                # Rook move
                self.board[move.endRow][move.endCol -
                                        1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            # Queen Side
            else:
                # Rook move
                self.board[move.endRow][move.endCol +
                                        1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"