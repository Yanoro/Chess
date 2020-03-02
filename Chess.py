import pygame, itertools
import sys


class Piece(pygame.sprite.Sprite):
    def __init__(self, Name, image, Tile, Color):
        pygame.sprite.DirtySprite.__init__(self, SpriteGroup)
        self.SpriteImage = pygame.image.load(image)
        self.Tile = Tile
        self.Color = Color
        self.add(WhitePieces) if Color is White else self.add(BlackPieces)
        self.PieceName = Name
        temp = self.SpriteImage.get_rect()
        self.Hitbox = pygame.rect.Rect(((Tiles[self.Tile]), (temp.width, temp.height)))
        pygame.draw.rect(screen, (255, 0, 0), self.Hitbox, 2)
        self.Draw()
        self.Hitbox.move(0, 50)

    def Draw(self):
        screen.fill(Dark)
        screen.blit(Board, BoardRect)
        self.Hitbox.center = Tiles[self.Tile]
        DrawAllPieces()
        self.Hitbox.left = Tiles[self.Tile][0]
        self.Hitbox.top = Tiles[self.Tile][1]
        pygame.draw.rect(screen, (255, 0, 0), self.Hitbox, 2)
        pygame.display.update()

    def Kill(self):
        pygame.sprite.Sprite.kill(self)


class Pawn(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Pawn", "Pieces/{}_Pawn.png".format(Color), StartingTile, Color)
        self.StartingPosition = True
        self.AllowedMovement = 2 if self.Color is White else -2

    def IsMovementDiagonal(self):
        ValidMovement = 1 if self.Color is White else -1
        return ((self.Horizontal_Movement == 1 and self.Vertical_Movement == ValidMovement) or (self.Horizontal_Movement == -1 and self.Vertical_Movement == ValidMovement))

    def ValidVerticalMovement(self):
        if self.Color is White:
            if not (self.Vertical_Movement <= self.AllowedMovement and self.Vertical_Movement > 0):
                return False
        else:
            if not (self.Vertical_Movement >= self.AllowedMovement and self.Vertical_Movement < 0):
                return False
        return True

    def ValidMove(self, Tiles):
        self.Horizontal_Movement, self.Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not self.ValidVerticalMovement():
            return False

        DestinyTile = Tiles[-1]
        Kill = (self.IsMovementDiagonal() and IsEnemyInside(DestinyTile, self.Color))

        if Kill or (self.Horizontal_Movement == 0 and not Kill and not OcuppiedTile(DestinyTile)):
            if self.StartingPosition:
                self.StartingPosition = False
                self.AllowedMovement = 1 if self.Color is White else -1
            return True

class Horse(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Horse", "Pieces/{}_Horse.png".format(Color), StartingTile, Color)

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not (abs(Horizontal_Movement) == 1 and abs(Vertical_Movement) == 2 or abs(Horizontal_Movement) == 2 and abs(Vertical_Movement) == 1):
            return False
        Ocuppied = OcuppiedTile(Tiles[-1])
        LastTile = Tiles[-1]
        return not Ocuppied or IsEnemyInside(LastTile, self.Color)

class Bishop(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Bishop", "Pieces/{}_Bishop.png".format(Color), StartingTile, Color)

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not (abs(Horizontal_Movement) == abs(Vertical_Movement)):
            return False
        return CheckPath(self, Tiles)

class Tower(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Tower", "Pieces/{}_Tower.png".format(Color), StartingTile, Color)

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not ((abs(Horizontal_Movement) != 0) != (abs(Vertical_Movement) != 0)):
            return False
        return CheckPath(self, Tiles)

class Queen(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Queen", "Pieces/{}_Queen.png".format(Color), StartingTile, Color)

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not ((abs(Horizontal_Movement) == abs(Vertical_Movement)) or ((abs(Horizontal_Movement) != 0) != (abs(Vertical_Movement) != 0))):
            return False
        return CheckPath(self, Tiles)

class King(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("King", "Pieces/{}_King.png".format(Color), StartingTile, Color)
        self.Check = False

    def GetSurroundingTiles(self):
        UpperRow = str(int(self.Tile[1]) + 1)
        CurrentRow = self.Tile[1]
        LowerRow = str(int(self.Tile[1]) - 1)
        LeftColumn = chr(ord(self.Tile[0]) - 1)
        CurrentColumn = self.Tile[0]
        RightColumn = chr(ord(self.Tile[0]) + 1)
        Movement = []
        UpperTiles = LeftColumn + UpperRow, CurrentColumn + UpperRow, RightColumn + UpperRow
        HorizontalTiles = LeftColumn + CurrentRow, RightColumn + CurrentRow
        LowerTiles = LeftColumn + LowerRow, CurrentColumn + LowerRow, RightColumn + LowerRow
        return UpperTiles + HorizontalTiles + LowerTiles

    def GetAllPossibleMoves(self):
        SurroundingTiles = self.GetSurroundingTiles()
        PossibleTiles = []
        for Tile in SurroundingTiles:
            Column = Tile[0]
            Row = int(Tile[1])
            if ord(Column) >= ord("A") and ord(Column) <= ord("H") and Row >= 1 and Row <= 8 and not OcuppiedTile(Tile):
                PossibleTiles.append(Tile)
        return PossibleTiles

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not ((abs(Horizontal_Movement) <= 1 and abs(Vertical_Movement) <= 1)):
            return False
        return CheckPath(self, Tiles)

def DrawAllPieces(Skip = "Optional Skip Argument"):
    for Sprite in SpriteGroup:
        if Sprite == Skip:
            continue
        else:
            screen.blit(Sprite.SpriteImage, Tiles[Sprite.Tile])

def OcuppiedTile(Tile):
    for Sprite in SpriteGroup:
        if Sprite.Tile == Tile:
            return True
    return False

def CheckTrajectory(Tiles):
    TileLength = len(Tiles) - 1
    LastTileIsOcuppied = False
    for Tile in Tiles:
        if OcuppiedTile(Tile):
            return False
    return True

def CreateTile(Piece, Horizontal_Movement, Vertical_Movement):
    Column = chr(ord(Piece.Tile[0]) + Horizontal_Movement)
    Row = str(int(Piece.Tile[1]) + Vertical_Movement)
    Tile = Column + Row
    return Tile

def CheckPath(Piece, Tiles):
    PathResults = CheckTrajectory(Tiles[:-1])
    return PathResults

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

def IsEnemyInside(Tile, MovingPieceColor):
    return True if OcuppiedTile(Tile) and GetPieceInsideTile(Tile).Color != MovingPieceColor else False

def KillIfPossible(EnemyTile):
    if EnemyTile and IsKillLegal(EnemyTile):
        EnemyTile.Kill()

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

def MakeTiles():
    global Tiles
    Tiles = {}
    index = 0
    for Columns in range(1 , 9):
        for Rows, Rowname in zip(range(1 , 9), range(8 , 0, -1)):
            Tiles[Column_Letters[Columns - 1] + str(Rowname)] = [Columns * 88, Rows * 87]

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

def GetMovementHelper(Current, Destiny):
    Counter = 0
    Movement = 1 if Current < Destiny else -1
    while Current != Destiny:
        Counter += Movement
        Current += Movement
    return Counter

def GetMovement(OriginalTile, DestinyTile):
    Horizontal_Movement = 0
    Vertical_Movement = 0
    Horizontal_Movement = GetMovementHelper(ord(OriginalTile[0]), ord(DestinyTile[0]))
    Vertical_Movement = GetMovementHelper(int(OriginalTile[1]), int(DestinyTile[1]))
    return Horizontal_Movement, Vertical_Movement

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

def CanKingEscape(King, PossibleMoves):
    CurrentPosition = King.Tile
    Escape = False
    for Move in PossibleMoves:
        King.Tile = Move
        if not Check():
            Escape = True
            break
    King.Tile = CurrentPosition
    return Escape

def CheckMate():
    CheckedKing = GetCheckedKing()
    EnemyPieces = BlackPieces if CheckedKing.Color is White else WhitePieces
    PossibleTiles = CheckedKing.GetAllPossibleMoves()
    if CanKingEscape(CheckedKing, PossibleTiles):
        return False
    Group = WhitePieces if EnemyPieces is BlackPieces else BlackPieces
    IsCheckMate = True
    for Piece in Group:
        TilePath = CreateTilePath(Piece, *GetMovement(Piece.Tile, Threat.Tile))
        PreviousTile = Piece.Tile
        if TilePath and Piece.ValidMove(TilePath) and IsKillLegal(Threat):
            Piece.Tile = Threat.Tile
            InCheck = Check()
            Piece.Tile = PreviousTile
            if not InCheck:
                IsCheckMate = False
                break
    return IsCheckMate

def IsKillLegal(EnemyPiece):
    Group = WhitePieces if EnemyPiece.Color is White else BlackPieces               #Rework
    EnemyPiece.remove(Group)
    if GetCheckedKing() is Turn:
        if Check():
            EnemyPiece.add(Group)
            return False
    return True

def GetCheckedKing():
    return WhiteKing if WhiteKing.Check else BlackKing                 #Best Practice would be returning an exception if there wasn't a checked King

def CurrentlyInCheck():
    return True if WhiteKing.Check or BlackKing.Check else False

def BothKingsInCheck():
    return True if WhiteKing.Check and BlackKing.Check else False

def IsCheckValid():
    if BothKingsInCheck():
        WhiteKing.Check = False
        BlackKing.Check = False
        return False
    CheckedKingColor = GetCheckedKing().Color
    print(CheckedKingColor)
    if CheckedKingColor is Turn:                                      #Rework 
        if LastTileIsOcuppied and IsEnemyInside(LastTile, CheckedKingColor):
            if not IsKillLegal(LastTileIsOcuppied):
                return False
        else:
            if Check():
                return False
    return True

def HandleLastTile(LastTile, MovingPieceColor):
    LastTileIsOcuppied = OcuppiedTile(LastTile) if LastTile else None
    EnemyTile = GetPieceInsideTile(LastTile) if IsEnemyInside(LastTile, MovingPieceColor) else False
    return LastTileIsOcuppied, EnemyTile

def Check_Helper(Pieces, King):
    global Threat                     #Rework
    for Piece in Pieces:
        TilePath = CreateTilePath(Piece, *GetMovement(Piece.Tile, King.Tile)) #Rework
        if TilePath and Piece.ValidMove(TilePath) and IsKillLegal(King):
            Threat = Piece
            King.Check = True
            return True

def Check():
    return (Check_Helper(BlackPieces, WhiteKing) or Check_Helper(WhitePieces, BlackKing))

def GetPieceInsideTile(Tile):
    for Sprite in SpriteGroup:
        if Sprite.Tile == Tile:
            return Sprite
    raise ValueError("GetPieceInsideTile: Couldn't find the Enemy")

def StartGame():
    pygame.init()
    screen.blit(Board, BoardRect)
    InitializeBoard([[King, ["D4"], ["H8"]], [Tower, ["B7", "C6"], []]])
    GetKings()

def WaitUntilInput():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

def Testing():
    Position1 = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G5", "H7"]], [Horse, ["B1", "G1"], ["B8", "G4"]], [Tower, ["A1", "G8"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]

    Position2 = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]], [Horse, ["B1", "G1"], ["B8", "G8"]], [Tower, ["A1", "H1"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8", "F8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]

    Position3 = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G5", "H7"]], [Horse, ["B1", "G1"], ["B8", "G4"]], [Tower, ["A1", "G8"], ["A8", "H6"]], [Bishop, ["C1", "F1"], ["C8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]

    Position4 = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E5", "F7", "G5", "H7"]], [Horse, ["B1", "G1"], ["B8", "G4"]], [Tower, ["A1", "G8"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8"]], [King, ["E1"], ["E8"]], [Queen, ["H5"], ["D8"]]]

    Position5 = [[King, ["D4"], ["H8"]], [Tower, ["B7", "B8"], []]]

    AllCheckMates = [Position1, Position2, Position3, Position4, Position5]
    CorrectResults = [False, False, True, True, True]
    Index = 0
    AllPassed = True
    Show = False
    for CheckMateSetup in AllCheckMates:
        #pygame.init()
        screen.blit(Board, BoardRect)
        InitializeBoard(CheckMateSetup)
        GetKings()
        Check()
        if CheckMate() == CorrectResults[Index]:
            print("[+] Success With CheckMateSetup {}".format(Index))
        else:
            print("[-] Error With CheckMateSetup {}".format(Index))
            AllPassed = False
        Index += 1
        if Show:
            WaitUntilInput()
        ResetPieces()

    return AllPassed

def Main():
    if Debug:
        if Testing():
            print("[+] All Tests Passed")
        else:
            print("[-] One or More Tests Failed")
        return True

    StartGame()
    Dragged = None
    global LastTileIsOcuppied

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
            if event.type == pygame.MOUSEBUTTONDOWN:
                for Sprite in SpriteGroup:
                    if Sprite.Hitbox.collidepoint(event.pos) and Sprite.Color == Turn:
                        Dragged = Sprite
                        break;
            elif event.type == pygame.MOUSEBUTTONUP:
                if Dragged is not None:
                    OriginalTile = Dragged.Tile
                    DestinyTile = GetTile((event.pos[0] - 20, event.pos[1] - 40))
                    TilePath = CreateTilePath(Dragged, *GetMovement(Dragged.Tile, DestinyTile))
                    LastTile = TilePath[-1] if TilePath else None
                    LastTileIsOcuppied, EnemyTile = HandleLastTile(LastTile, Dragged.Color)
                    if TilePath and Dragged.ValidMove(TilePath) and (not LastTileIsOcuppied or EnemyTile):
                        Dragged.Tile = DestinyTile
                        Dragged.Draw()                                                    #Pawn when in starting Tile can jump over other pieces
                        if Check():
                            if not IsCheckValid():    #Improve this bit
                                InvalidMove()
                                Dragged.Tile = OriginalTile
                                Dragged.Draw()                  #Can Probaly do this way better
                                Dragged = None
                                continue
                            elif CheckMate():
                                FinishGame()
                            else:
                                print("Check")
                        else:
                            if CurrentlyInCheck():
                                GetCheckedKing().Check = False
                        KillIfPossible(EnemyTile)
                        Dragged.Draw()
                        ChangeTurn()
                        PrintMovement(Dragged.PieceName, OriginalTile, DestinyTile, Turn)
                    else:
                        InvalidMove()
                    Dragged.Draw()
                Dragged = None
        Update(Dragged)
        pygame.display.update()

SpriteGroup = pygame.sprite.Group()
WhitePieces = pygame.sprite.Group()
BlackPieces = pygame.sprite.Group()
size = [864, 866]
screen = pygame.display.set_mode(size)
Dark = 0,0,0
Board = pygame.image.load("Board.png").convert()
BoardRect = Board.get_rect();
Column_Letters = "ABCDEFGH"
White = "White"
Black = "Black"
Turn = White

Debug = False
LastTileIsOcuppied = None
Threat = None
IsCheckMate = False

MakeTiles()

if __name__ == "__main__":
    Main()
