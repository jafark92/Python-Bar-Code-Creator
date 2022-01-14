#Mashrul Amin
import math

def Distance (X0, Y0, X1, Y1):
    DeltaX = X1 - X0
    DeltaY = Y1 - Y0
    return math.sqrt(DeltaX*DeltaX + DeltaY*DeltaY)

black = [ 0, 0, 0]
blue = [ 0, 0,255]
green = [ 0,255, 0]
cyan = [ 0,255,255]
red = [255, 0, 0]
magenta = [255, 0,255]
yellow = [255,255, 0]
white = [255,255,255]
gray = [128,128,128]

def getRed (Pixel): return Pixel[0]
def getGreen (Pixel): return Pixel[1]
def getBlue (Pixel): return Pixel[2]

#canvas
def makeEmptyPicture (Width, Height,Color=white) :
    return {"Width":Width, "Height":Height, "Default":Color}

def getWidth (Canvas): return Canvas ["Width"]
def getHeight (Canvas) : return Canvas ["Height"]

#---------------------------------------------------

def PixelIndex (X,Y): return int (round(Y))*100000+int(round(X))

def setPixel (Canvas, X, Y, Color=black):
    if (X < 0): return
    if (Y < 0): return
    if (X >= Canvas["Width"]): return
    if (Y >= Canvas["Height"]): return
    Index = PixelIndex (X,Y)
    if Color == Canvas["Default"]:
        if Index in Canvas: del Canvas[Index]
    else:
        Canvas[Index] = Color
    return
    
def getPixel (Canvas, X, Y):
    Index = PixelIndex(X,Y)
    if Index in Canvas:
        Result = Canvas[Index]
    else:
        Result = Canvas["Default"]
    return Result

def HorizontalLine (Canvas, X1, X2, Y, Color=black):
    for X in range(X1,X2+1): setPixel(Canvas,X,Y,Color)
    return

def VerticalLine (Canvas, X, Y1, Y2, Color=black):
    for Y in range(Y1,Y2+1) : setPixel(Canvas,X,Y,Color)
    return

#------------------------------------------------------

def WriteString(Outfile,S):
    L = [ord(CH) for CH in S]
    Outfile.write(bytes(L))
    return

def WriteBytes (Outfile,N,TotalBytes=1):
    L = []
    for I in range(TotalBytes):
        L = L + [N % 256]               # Little endian
        N = N // 256
    Outfile.write(bytes(L))
    return

#-------------------------------------------------------

def WriteBMP (FileName, Canvas): # FileName will end in bmp format
    Width            = getWidth(Canvas)
    Height           = getHeight(Canvas)
    FileHeaderSize   = 14
    ImageHeaderSize  = 40
    BytesPerPixel    = 3
    BitsPerPixel     = BytesPerPixel * 8
    Pad              = 4 - (Width * BytesPerPixel) % 4
    if Pad == 4: Pad = 0
    BytesPerRaster   = Width * BytesPerPixel + Pad
    ImageSize        = Height * BytesPerRaster
    Offset           = FileHeaderSize + ImageHeaderSize
    FileSize         = ImageSize + Offset
    Outfile          = open(FileName, 'wb') # w write to file b binary not text
    try:
        WriteString(Outfile,'BM')
        WriteBytes(Outfile, FileSize, 4)
        WriteBytes(Outfile, 0, 2)
        WriteBytes(Outfile, 0, 2)
        WriteBytes(Outfile, Offset, 4)
        WriteBytes(Outfile, ImageHeaderSize, 4)
        WriteBytes(Outfile, Width, 4)
        WriteBytes(Outfile, Height, 4)
        WriteBytes(Outfile, 1, 2)
        WriteBytes(Outfile, BitsPerPixel, 2)
        WriteBytes(Outfile, 0, 4)
        WriteBytes(Outfile, ImageSize, 4)
        WriteBytes(Outfile, 0, 4)
        WriteBytes(Outfile, 0, 4)
        WriteBytes(Outfile, 0, 4)
        WriteBytes(Outfile, 0, 4)
        for Y in range(Height-1, -1, -1):
            for X in range(Width):
                Pixel = getPixel(Canvas, X, Y)
                WriteBytes(Outfile, getBlue(Pixel), 1)
                WriteBytes(Outfile, getGreen(Pixel), 1)
                WriteBytes(Outfile, getRed(Pixel), 1)
            if Pad > 0: WriteBytes(Outfile, 0, Pad)
    finally:
        Outfile.close()
    return

# ------------------------------------------------

def addLine (Canvas,X1,Y1,X2,Y2,Color=black):
    D = int(round(Distance(X1,Y1,X2,Y2))) + 1
    Ax = X2 - X1
    Ay = Y2 - Y1
    for I in range(D+1):
        T = I / float(D)
        X = Ax * T + X1
        Y = Ay * T + Y1
        setPixel(Canvas, X, Y, Color)
    return


# ------------------------------------------------

def BresenhamCircle (Canvas, Xc, Yc, R, Color=black):
    X = R
    Y = 0
    E = -R
    while (X >= Y):
        setPixel (Canvas, Xc - X, Yc + Y, Color)
        setPixel (Canvas, Xc + X, Yc + Y, Color)
        setPixel (Canvas, Xc - X, Yc - Y, Color)
        setPixel (Canvas, Xc + X, Yc - Y, Color)
        setPixel (Canvas, Xc - Y, Yc + X, Color)
        setPixel (Canvas, Xc + Y, Yc + X, Color)
        setPixel (Canvas, Xc - Y, Yc - X, Color)
        setPixel (Canvas, Xc + Y, Yc - X, Color)
        E = E + Y + Y + 1
        Y = Y + 1
        if (E > 0):
            E = E - X - X + 2
            X = X - 1
    return

def BresenhamFilledCircle (Canvas, Xc, Yc, R, Color=black):
    X = R
    Y = 0
    E = -R
    while (X >= Y):
        HorizontalLine(Canvas, Xc - X, Xc + X, Yc + Y, Color)
        HorizontalLine(Canvas, Xc - X, Xc + X, Yc - Y, Color)
        HorizontalLine(Canvas, Xc - Y, Xc + Y, Yc + X, Color)
        HorizontalLine(Canvas, Xc - Y, Xc + Y, Yc - X, Color)
        E = E + Y + Y + 1
        Y = Y + 1
        if (E > 0):
            E = E - X - X + 2
            X = X - 1
    return 
