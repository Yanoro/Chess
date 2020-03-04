from ChessPieces import *
import itertools
import sys #REMOVE

Debug = True
LastTileIsOcuppied = None
IsCheckMate = False
WhiteKing = None
BlackKing = None

def CreateTile(Piece, Horizontal_Movement, Vertical_Movement):
    Column = chr(ord(Piece.Tile[0]) + Horizontal_Movement)
    Row = str(int(Piece.Tile[1]) + Vertical_Movement)
    Tile = Column + Row
    return Tile

def CreateTilePath(Piece, Horizontal_Movement, Vertical_Movement):
    if Vertical_Movement < 0:
        V_Movement = -1
    else:
        V_Movement = 1
    if Horizontal_Movement < 0:
        H_Movement = -1
    else:
        H_Movement = 1

    Tiles = []
    Current_Column = ord(Piece.Tile[0]) - ord("A")
    Current_Row = int(Piece.Tile[1])
    Last_Column = ord(Piece.Tile[0]) - ord("A")
    Last_Row = Piece.Tile[1]

    for Row, Column in itertools.zip_longest(range(Current_Row + V_Movement, Current_Row + Vertical_Movement + V_Movement, V_Movement), range(Current_Column + H_Movement, Current_Column + Horizontal_Movement + H_Movement, H_Movement)):
        if Column is not None:
            Last_Column = Column
        if Row is not None:
            Last_Row = Row
        Tiles.append(Column_Letters[Last_Column] + str(Last_Row))

    return Tiles

def Update(Dragged):
    if Dragged is not None:
        pos = pygame.mouse.get_pos()
        screen.fill(Dark)
        screen.blit(Board, BoardRect)
        DrawAllPieces(Dragged)
        screen.blit(Dragged.SpriteImage, (pos[0] - 30, pos[1] - 40))

def PrintMovement(PieceName, OriginalTile, DestinyTile, CurrentTurn):
    print("{}: {} to {}".format(PieceName, OriginalTile, DestinyTile))
    print("{} Turn".format(CurrentTurn))

def ClosestToZero(List):
    Closest = 0
    for index, Item in enumerate(List):
        if (abs(Item) < abs(List[Closest])):
            Closest = index
    return Closest

def GetTile(Mouse_Pos):
    Positions = [88.2, 176.4, 264.6, 352.8, 441.0, 529.2, 617.4, 705.6]
    Placeholder_Rows = []
    Placeholder_Columns = []
    for Position in Positions:
        Placeholder_Columns.append(Mouse_Pos[0] - Position)
    Positions.reverse()
    for Position in Positions:
        Placeholder_Rows.append(Mouse_Pos[1] - Position)
    Row = ClosestToZero(Placeholder_Rows) + 1
    Column = Column_Letters[ClosestToZero(Placeholder_Columns)]
    return Column + str(Row)

def InitializeBoard(ChangeBoard = False):            #REMOVE THE OPTIONAL ARGS
    if not ChangeBoard:
        Positions = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]], [Horse, ["B1", "G1"], ["B8", "G8"]], [Tower, ["A1", "H1"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8", "F8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]
    else:
        Positions = ChangeBoard
    for Position in Positions:
        Piece = Position[0]
        for WhiteTiles in Position[1]:
            DirtyPiece = Piece(White, WhiteTiles)
        for BlackTiles in Position[2]:
            DirtyPiece = Piece(Black, BlackTiles)

def InvalidMove():
    print("Invalid Move!")

def ResetPieces():
    for Sprite in SpriteGroup:
        Sprite.Kill()

def ChangeTurn():
    global Turn
    Turn = Black if Turn is White else White

def GetKings():
    global WhiteKing
    global BlackKing

    for Sprite in SpriteGroup:
        if Sprite.PieceName == "King":
            if Sprite.Color == White:
                WhiteKing = Sprite
            else:
                BlackKing = Sprite
    return WhiteKing, BlackKing


def FinishGame():
    print("CheckMate")
    print("{} Wins!".format(Turn))
    print("Press R to start a New Game")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    ResetPieces()
                    Main()

def CheckAllPiecesPossibleMovements(MovingPiece, DestinyTile, Group):
    PreviousTile = MovingPiece.Tile
    MovingPiece.Tile = DestinyTile
    IsCheck = True
    for Piece in Group:
        PossibleMoves = Piece.GetPossibleMoves()
        if PossibleMoves:
            print(PossibleMoves)
            for Move in PossibleMoves:
                TilePath = CreateTilePath(Piece, *GetMovement(Piece.Tile, Move))
                LastTile = TilePath[-1]
                if TilePath and Piece.ValidMove(TilePath) and IsLastTileLegal(LastTile, Piece.Color):
                    if not Check(Piece, Move):
                        print(Move)
                        IsCheck = False
                        break
    MovingPiece.Tile = PreviousTile
    return IsCheck

def CheckMate(MovingPiece, DestinyTile):
    if not CurrentlyInCheck():
        return False
    Group = BlackPieces if Turn is White else WhitePieces #Can be turned into a function
    return CheckAllPiecesPossibleMovements(MovingPiece, DestinyTile, Group)

def IsKillLegal(EnemyPiece):
    if CurrentlyInCheck() and GetCheckedKing().Color is Turn:
        if Check():
            return False
    Group = WhitePieces if EnemyPiece.Color is White else BlackPieces
    return True

def GetCheckedKing():
    if not (WhiteKing.Check or BlackKing.Check):
        raise ValueError("Called GetCheckedKing Without Having a King in Check")
    return WhiteKing if WhiteKing.Check else BlackKing

def CurrentlyInCheck():
    return True if WhiteKing.Check or BlackKing.Check else False

def BothKingsInCheck():
    return True if WhiteKing.Check and BlackKing.Check else False

def IsCheckMovementValid(MovingPiece, DestinyTile):
    if BothKingsInCheck():
        WhiteKing.Check = False
        BlackKing.Check = False
        return False
    if GetCheckedKing().Color == Turn and Check(MovingPiece, DestinyTile): #Can prob remove CheckedKingColor
        return False
    return True

def IsLastTileLegal(LastTile, MovingPieceColor):
    LastTileIsOcuppied = OcuppiedTile(LastTile) if LastTile else None
    if LastTileIsOcuppied:
        if not IsEnemyInside(LastTile, MovingPieceColor):
            return False
    return True

def Check_Helper(Pieces, King):
    for Piece in Pieces:
        TilePath = CreateTilePath(Piece, *GetMovement(Piece.Tile, King.Tile)) #Rework
        if TilePath and Piece.ValidMove(TilePath):
            King.Check = True
            return True
    return False

def Check(MovingPiece, DestinyTile):
    Kill = False
    if IsEnemyInside(DestinyTile, MovingPiece):
        Enemy = GetPieceInsideTile(DestinyTile)
        PreviousGroups = Enemy.groups()
        Enemy.Kill()
        Kill = True
    PreviousTile = MovingPiece.Tile
    MovingPiece.Tile = DestinyTile
    WhiteKingInCheck = Check_Helper(BlackPieces, WhiteKing)
    BlackKingInCheck = Check_Helper(WhitePieces, BlackKing)
    MovingPiece.Tile = PreviousTile
    if Kill:
        Enemy.add(PreviousGroups)
    return WhiteKingInCheck or BlackKingInCheck

def StartGame():
    pygame.init()
    screen.blit(Board, BoardRect)
    InitializeBoard()
    GetKings()

def IsMovementLegal(MovingPiece, OriginalTile, DestinyTile, TilePath):
    LastTile = TilePath[-1] if TilePath else None
    LastTileIsLegal = IsLastTileLegal(LastTile, MovingPiece.Color)
    if TilePath and MovingPiece.ValidMove(TilePath) and LastTileIsLegal:
        if Check(MovingPiece, DestinyTile):
            if not IsCheckMovementValid(MovingPiece, DestinyTile):
                return False
            elif CheckMate(MovingPiece, DestinyTile):
                FinishGame()
            else:
                print("Check")
        else:
            if CurrentlyInCheck():
                GetCheckedKing().Check = False
        return True

def Main():
    StartGame()
    MovingPiece = None
    global LastTileIsOcuppied

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
            if event.type == pygame.MOUSEBUTTONDOWN:
                for Sprite in SpriteGroup:
                    if Sprite.Hitbox.collidepoint(event.pos) and Sprite.Color == Turn:
                        MovingPiece = Sprite
                        break;
            elif event.type == pygame.MOUSEBUTTONUP:
                if MovingPiece is not None:
                    OriginalTile = MovingPiece.Tile
                    DestinyTile = GetTile((event.pos[0] - 20, event.pos[1] - 40))
                    TilePath = CreateTilePath(MovingPiece, *GetMovement(MovingPiece.Tile, DestinyTile))  #Could probably remove the need for the GetMovement Call
                    if IsMovementLegal(MovingPiece, OriginalTile, DestinyTile, TilePath):
                        if IsEnemyInside(DestinyTile, MovingPiece.Color):
                            GetPieceInsideTile(DestinyTile).Kill()
                        ChangeTurn()
                        MovingPiece.Move(DestinyTile)   #Remember to replace other cases of this
                        PrintMovement(MovingPiece.PieceName, OriginalTile, DestinyTile, Turn)
                    else:
                        InvalidMove()
                    MovingPiece.Draw()
                MovingPiece = None
        Update(MovingPiece)
        pygame.display.update()

if __name__ == "__main__":
    Main()
