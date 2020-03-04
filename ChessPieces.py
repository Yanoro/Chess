import pygame

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

def GetSurroundingTiles(Tile):
        UpperRow = str(int(Tile[1]) + 1)
        CurrentRow = Tile[1]
        LowerRow = str(int(Tile[1]) - 1)
        LeftColumn = chr(ord(Tile[0]) - 1)
        CurrentColumn = Tile[0]
        RightColumn = chr(ord(Tile[0]) + 1)
        Movement = []
        UpperTiles = LeftColumn + UpperRow, CurrentColumn + UpperRow, RightColumn + UpperRow
        HorizontalTiles = LeftColumn + CurrentRow, RightColumn + CurrentRow
        LowerTiles = LeftColumn + LowerRow, CurrentColumn + LowerRow, RightColumn + LowerRow
        return UpperTiles + HorizontalTiles + LowerTiles


def GetAllPossibleDirections(List):
    FirstItem = List[0]
    SecondItem = List[1]
    return [[FirstItem, SecondItem], [-FirstItem, SecondItem], [FirstItem, -SecondItem], [-FirstItem, -SecondItem]]

def GetPieceInsideTile(Tile):
    for Sprite in SpriteGroup:
        if Sprite.Tile == Tile:
            return Sprite
    raise ValueError("GetPieceInsideTile: Couldn't find the Enemy")

def IsEnemyInside(Tile, MovingPieceColor):
    return True if OcuppiedTile(Tile) and GetPieceInsideTile(Tile).Color != MovingPieceColor else False

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

def CheckPath(Piece, Tiles):
    PathResults = CheckTrajectory(Tiles[:-1])
    return PathResults

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

def MakeTiles():
    global Tiles
    Tiles = {}
    index = 0
    for Columns in range(1 , 9):
        for Rows, Rowname in zip(range(1 , 9), range(8 , 0, -1)):
            Tiles[Column_Letters[Columns - 1] + str(Rowname)] = [Columns * 88, Rows * 87]

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

    def NextTile(self, CurrentTile, Horizontal_Direction, Vertical_Direction):
        NewColumn = chr(ord(CurrentTile[0]) + Horizontal_Direction)
        NewRow = str(int(CurrentTile[1]) + Vertical_Direction)
        return NewColumn + NewRow

    def GetTilesInDirection(self, Horizontal_Direction, Vertical_Direction):
        Movements = []
        CurrentTile = self.NextTile(self.Tile, Horizontal_Direction, Vertical_Direction)
        LastTile = False
        while self.IsTileStillValid(CurrentTile) and not LastTile:
            if OcuppiedTile(CurrentTile):
                if not IsEnemyInside(CurrentTile, self.Color):
                    break
                LastTile = True
            Movements.append(CurrentTile)
            CurrentTile = self.NextTile(CurrentTile, Horizontal_Direction, Vertical_Direction)
        return Movements

    def GetTilesInAllDirections(self, Directions):
        Tiles = []
        for Direction in Directions:
            TilesInDirection = self.GetTilesInDirection(Direction[0], Direction[1])
            if TilesInDirection:
                Tiles += TilesInDirection
        return Tiles

    def GetAllDiagonalPossibleMovements(self):
        PossibleMovements = []
        Directions = GetAllPossibleDirections([1, 1])
        return self.GetTilesInAllDirections(Directions)

    def GetAllVerticalAndHorizontalPossibleMovements(self):
        Directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        AllMovements = self.GetTilesInAllDirections(Directions)
        if AllMovements:
            return AllMovements
        else:
            return None

    def IsTileStillValid(self, Tile):
        try:
            Column = Tile[0]
            Row = int(Tile[1])
        except:                                      #RemoveThisTryBlock
            return False                                            #Doesn't take into account situations where the tile is ocuppied by an enemy
        return ord(Column) >= ord("A") and ord(Column) <= ord("H") and Row >= 1 and Row <= 8

    def Move(self, DestinyTile):
        self.Tile = DestinyTile

    def GetCurrentColumnAndRow(self):
        return self.Tile[0], self.Tile[1]

    def Kill(self):
        pygame.sprite.Sprite.kill(self)

class Pawn(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Pawn", "Pieces/{}_Pawn.png".format(Color), StartingTile, Color)
        self.StartingTile = "2" if self.Color is White else "7"
        self.GetAllowedMovement()

    def IsInitialMovement(self):
        return self.Tile[1] == self.StartingTile

    def IsMovementDiagonal(self):
        ValidMovement = 1 if self.Color is White else -1
        return ((self.Horizontal_Movement == 1 and self.Vertical_Movement == ValidMovement) or (self.Horizontal_Movement == -1 and self.Vertical_Movement == ValidMovement))

    def GetDiagonalTiles(self):
        CurrentColumn, CurrentRow = self.GetCurrentColumnAndRow()
        OneTileMove = 1 if self.Color is White else  - 1
        OneTileMove = str(int(self.Tile[1]) + OneTileMove)
        DiagonalLeftTile = chr(ord(CurrentColumn) - 1) + OneTileMove
        DiagonalRightTile = chr(ord(CurrentColumn) + 1) + OneTileMove
        return DiagonalLeftTile, DiagonalRightTile

    def GetPossibleMoves(self):
        PossibleMovements = []
        CurrentColumn, CurrentRow = self.GetCurrentColumnAndRow()
        OneTileMove = 1 if self.Color is White else -1
        CurrentRow = int(CurrentRow)
        PossibleMovements = [CurrentColumn + str(CurrentRow + OneTileMove)]
        if self.IsInitialMovement():
            PossibleMovements.append(CurrentColumn + str(CurrentRow + self.AllowedMovement))

        DiagonalLeftTile, DiagonalRightTile = self.GetDiagonalTiles()

        if IsEnemyInside(DiagonalLeftTile, self.Color):
            PossibleMovements.append(DiagonalLeftTile)

        if IsEnemyInside(DiagonalRightTile, self.Color):
            PossibleMovements.append(DiagonalRightTile)

        return PossibleMovements

    def GetAllowedMovement(self):
        if self.IsInitialMovement():
            self.AllowedMovement = 2 if self.Color is White else -2
        else:
            self.AllowedMovement = 1 if self.Color is White else -1

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
        self.GetAllowedMovement()
        if not self.ValidVerticalMovement():
            return False

        DestinyTile = Tiles[-1]
        Kill = (self.IsMovementDiagonal() and IsEnemyInside(DestinyTile, self.Color))

        if Kill or (self.Horizontal_Movement == 0 and not Kill and not OcuppiedTile(DestinyTile)):
            if abs(self.AllowedMovement) == 2:
                return CheckPath(self, Tiles)
            return True

class Horse(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Horse", "Pieces/{}_Horse.png".format(Color), StartingTile, Color)

    def GetPossibleMoves(self):
        PossibleMovements = []
        CurrentColumn, CurrentRow = self.GetCurrentColumnAndRow()
        AllMoves = GetAllPossibleDirections([1, 2])
        AllMoves += GetAllPossibleDirections([2, 1])
        for Movement in AllMoves:
            Column = chr(ord(CurrentColumn) + Movement[0])
            Row =  str(int(CurrentRow) + Movement[1])
            Tile = Column + Row
            if self.IsTileStillValid(Tile) and (not OcuppiedTile(Tile) or IsEnemyInside(Tile, self.Color)):
                PossibleMovements.append(Tile)
        return PossibleMovements

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

    def GetPossibleMoves(self):
        return self.GetAllDiagonalPossibleMovements()

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not (abs(Horizontal_Movement) == abs(Vertical_Movement)):
            return False
        return CheckPath(self, Tiles)

class Tower(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Tower", "Pieces/{}_Tower.png".format(Color), StartingTile, Color)

    def GetPossibleMoves(self):
        return self.GetAllVerticalAndHorizontalPossibleMovements()

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not ((abs(Horizontal_Movement) != 0) != (abs(Vertical_Movement) != 0)):
            return False
        return CheckPath(self, Tiles)

class Queen(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("Queen", "Pieces/{}_Queen.png".format(Color), StartingTile, Color)

    def GetPossibleMoves(self):
        VerticalAndHorizontalMovements = self.GetAllVerticalAndHorizontalPossibleMovements()
        DiagonalMovements = self.GetAllDiagonalPossibleMovements()
        if DiagonalMovements and VerticalAndHorizontalMovements:
            return VerticalAndHorizontalMovements + DiagonalMovements       #IMPROVE
        elif DiagonalMovements:
            return DiagonalMovements
        return VerticalAndHorizontalMovements

    def ValidMove(self, Tiles):
        Horizontal_Movement, Vertical_Movement = GetMovement(self.Tile, Tiles[-1])
        if not ((abs(Horizontal_Movement) == abs(Vertical_Movement)) or ((abs(Horizontal_Movement) != 0) != (abs(Vertical_Movement) != 0))):
            return False
        return CheckPath(self, Tiles)

class King(Piece):
    def __init__(self, Color, StartingTile):
        super().__init__("King", "Pieces/{}_King.png".format(Color), StartingTile, Color)
        self.Check = False

    def GetPossibleMoves(self):
        SurroundingTiles = GetSurroundingTiles(self.Tile)
        PossibleTiles = []
        for Tile in SurroundingTiles:
            if self.IsTileStillValid(Tile) and (not OcuppiedTile(Tile) or IsEnemyInside(Tile, self.Color)):       #The Not OcuppiedTile... Part is used several times changeit Later to A function
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

MakeTiles()
