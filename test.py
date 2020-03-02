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
        DestinyOcuppied = OcuppiedTile(Tiles[-1])
        Kill = (self.IsMovementDiagonal() and DestinyOcuppied )

        if not self.ValidVerticalMovement():
            return False

        if Kill or (self.Horizontal_Movement == 0 and not Kill and not DestinyOcuppied):
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
        return not Ocuppied or CanKill(Ocuppied)

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
            return Sprite
    return False

def CheckTrajectory(Tiles):
    TileLength = len(Tiles) - 1
    LastTile = False
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

def IsEnemyInside(Piece, MovingPieceColor):
    return True if Piece.Color != MovingPieceColor else False

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


def InitializeBoard():
    if not Debug:
        Positions = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]], [Horse, ["B1", "G1"], ["B8", "G8"]], [Tower, ["A1", "H1"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8", "F8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]
    else:
        Positions = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G5", "H7"]], [Horse, ["B1", "G1"], ["B8", "G8"]], [Tower, ["A1", "G7"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8", ]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]

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

def CheckMate():
    King = GetCheckedKing()
    EnemyPieces = BlackPieces if King.Color is White else WhitePieces
    PossibleTiles = King.GetAllPossibleMoves()
    for Tile in PossibleTiles:
        if not CheckMate_Helper(EnemyPieces, Tile):
            return False
    Group = WhitePieces if EnemyPieces is Black else BlackPieces
    for Piece in Group:
        TilePath = CreateTilePath(Piece, *GetMovement(Piece.Tile, Threat.Tile))
        if TilePath and Piece.ValidMove(TilePath):
            return False
    return True

def CanKill(EnemyPiece):
    KingInCheck = GetCheckedKing()
    Group = WhitePieces if EnemyPiece.Color is White else BlackPieces
    EnemyPiece.remove(Group)
    if KingInCheck is Turn:
        if Check():
            EnemyPiece.add(Group)
            return False
    return True

def GetCheckedKing():
    return WhiteKing if WhiteKing.Check else BlackKing                 #Best Practice would be returning an exception if there wasn't a checked King

def IsCheckValid():
    KingInCheck = GetCheckedKing().Color
    if KingInCheck is Turn:
        if LastTile and IsEnemyInside(LastTile, KingInCheck):
            if not CanKill(LastTile):
                return False
        else:
            if Check():
                return False
    return True

def CheckMate_Helper(Pieces, King_Tile):
    global Threat
    for Piece in Pieces:
        TilePath = CreateTilePath(Piece, *GetMovement(Piece.Tile, King_Tile))
        if TilePath and Piece.ValidMove(TilePath):
            Threat = Piece
            return True

def Check():
    if CheckMate_Helper(BlackPieces, WhiteKing.Tile):
        WhiteKing.Check = True
        return True
    if CheckMate_Helper(WhitePieces, BlackKing.Tile):
        BlackKing.Check = True
        return True
    KingsInCheck = None
    return False

def StartGame():
    pygame.init()
    screen.blit(Board, BoardRect)
    InitializeBoard()
    GetKings()

def HandleCheck():
    if Check():
        if not IsCheckValid():
            return False
        elif CheckMate():
            FinishGame()
        else:
            print("Check")

    return True

def Main():
    StartGame()
    Dragged = None
    global LastTile

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
                    LastTile = OcuppiedTile(TilePath[-1]) if TilePath else None
                    EnemyTile = LastTile if LastTile and IsEnemyInside(LastTile, Dragged.Color) else False
                    if TilePath and Dragged.ValidMove(TilePath) and (not LastTile or EnemyTile):
                        Dragged.Tile = DestinyTile
                        Dragged.Draw()
                        if not HandleCheck():
                                InvalidMove()
                                Dragged.Tile = OriginalTile
                        else:
                            if EnemyTile and CanKill(LastTile):
                                LastTile.Kill()
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
KingInCheck = None
LastTile = None
Threat = None


Debug = True
MakeTiles()

if __name__ == "__main__":
    Main()
