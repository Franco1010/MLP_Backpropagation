
UI = {}
numberOfClasses = 3
numberOfInputsPerData = 2

# def isLeft(a, b, c):
#     return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) > 0.0

def mulMatrix(A, B):
    n = len(A)
    m = len(B[0])
    z = len(A[0])
    r = [[0.0 for i in range(m)] for j in range(n)] # n * m matrix
    for i in range(n):
        for j in range(m):
            for k in range(z):
                r[i][j] += A[i][k] * B[k][j]
    return r

def tMatrix(A):
    n = len(A)
    m = len(A[0])
    r = [[0.0 for i in range(n)] for j in range(m)] # m * n matrix
    for i in range(n):
        for j in range(m):
            r[j][i] = A[i][j]
    return r

class Obj:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.click = False
        self.default()
    def mouseOver(self, x, y):
        return self.x < x and x < self.x + self.w and self.y < y and y < self.y + self.h
    def clickAction(self):
        self.click = True
    def default(self):
        None
    def dragAction(self):
        None
    def releaseAction(self):
        self.click = False
        self.default()
    
class Button(Obj):
    def __init__(self, name, x, y, w, h, txtsz):
        self.name = name
        self.txtsz = txtsz
        self.defaultButtonFill = [[255, 255, 255], [0, 0, 0]]
        self.defaultNameFill = [[0, 0, 0], [255, 255, 255]]
        Obj.__init__(self, x, y, w, h)
    def display(self):
        stroke(self.buttonStroke)
        fill(*self.buttonFill)
        rect(self.x, self.y, self.w, self.h)
        self.txtsz = min(self.h - 5, self.txtsz)
        textSize(self.txtsz)
        textAlign(CENTER, CENTER)
        fill(*self.nameFill)
        text(self.name, self.x, self.y, self.w, self.h)
    def default(self):
        self.buttonStroke = 0
        self.buttonFill = self.defaultButtonFill[0] 
        self.nameFill = self.defaultNameFill[0]
    def clickAction(self):
        self.click = True
        self.buttonFill = self.defaultButtonFill[1] 
        self.nameFill = self.defaultNameFill[1]
        
class BlueButtonMode1(Button):
    def __init__(self, name, x, y, w, h, txtsz):
        Button.__init__(self, name, x, y, w, h, txtsz)
        self.defaultButtonFill = [[255, 255, 255], [0, 0, 0]]
        self.defaultNameFill = [[0, 0, 255], [255, 255, 255]]
        self.default()
    def clickAction(self):
        Button.clickAction(self)
        UI["field"].curMode = 1
        
class RedButtonMode2(Button):
    def __init__(self, name, x, y, w, h, txtsz):
        Button.__init__(self, name, x, y, w, h, txtsz)
        self.defaultButtonFill = [[255, 255, 255], [0, 0, 0]]
        self.defaultNameFill = [[255, 0, 0], [255, 255, 255]]
        self.default()
    def clickAction(self):
        Button.clickAction(self)
        UI["field"].curMode = 2
        
class GreenButtonMode3(Button):
    def __init__(self, name, x, y, w, h, txtsz):
        Button.__init__(self, name, x, y, w, h, txtsz)
        self.defaultButtonFill = [[255, 255, 255], [0, 0, 0]]
        self.defaultNameFill = [[0, 161, 53], [255, 255, 255]]
        self.default()
    def clickAction(self):
        Button.clickAction(self)
        UI["field"].curMode = 3
        
class InitializeButton(Button):
    def __init__(self, name, x, y, w, h, txtsz):
        Button.__init__(self, name, x, y, w, h, txtsz)
        self.readyToTrain = False
    def clickAction(self):
        Button.clickAction(self)
        offset = UI["field"].n // 2
        
        #Reading training set
        UI["field"].trainingSet = []
        for i in range(UI["field"].n + 1):
            for j in range(UI["field"].n + 1):
                if UI["field"].grid[i][j] != 0:
                    UI["field"].trainingSet.append([float(i - offset), float(j - offset), UI["field"].grid[i][j] - 1])
        
        #Initializing network
        UI["field"].nHidden = UI["hiddenLayers"].val
        UI["field"].nPerLayer = UI["neuronsPerLayer"].val
        UI["field"].nOutputs = numberOfClasses # harcoded number of classes
        UI["field"].nInputs = numberOfInputsPerData # harcoded number of inputs
        UI["field"].network = []
        UI["field"].network.append([{"weights":[random(0.01, 1) for i in range(UI["field"].nInputs + 1)]} for i in range(UI["field"].nPerLayer)])
        for nn in range(UI["field"].nHidden - 1):
            UI["field"].network.append([{"weights":[random(0.01, 1) for i in range(UI["field"].nPerLayer + 1)]} for i in range(UI["field"].nPerLayer)])
        UI["field"].network.append([{"weights":[random(0.01, 1) for i in range(UI["field"].nPerLayer + 1)]} for i in range(UI["field"].nOutputs)])
        for i in UI["field"].network:
            print(i)
        UI["field"].showLines = False
        UI["field"].train = False
        UI["errorHist"].reset()
        self.readyToTrain = True
        
class TrainButton(Button):
    def __init__(self, name, x, y, w, h, txtsz):
        Button.__init__(self, name, x, y, w, h, txtsz)
    def clickAction(self):
        if UI["initialize"].readyToTrain:
            Button.clickAction(self)
            UI["field"].train = True
            UI["field"].maximumError = UI["maximumError"].val
            UI["field"].epochsLeft = UI["epochs"].val
            UI["field"].learningRate = UI["learningRate"].val
            UI["field"].showLines = True
            UI["field"].iterationsCount = 0
            UI["initialize"].readyToTrain = False
            
class TestResultButton(Button):
    def __init__(self, name, x, y, w, h, txtsz):
        Button.__init__(self, name, x, y, w, h, txtsz)
    def clickAction(self):
        Button.clickAction(self)
        UI["field"].curMode = -1

class LeftArrowButton(Button):
    def __init__(self, x, y, w):
        Button.__init__(self, "", x, y, w, w, 0)
    def display(self):
        Button.display(self)
        triangle(self.x + self.w - self.spaceBetweenSquare, self.y + self.spaceBetweenSquare, self.x + self.w - self.spaceBetweenSquare, self.y + self.w - self.spaceBetweenSquare, self.x + self.spaceBetweenSquare, self.y + (self.w) / 2)
    def default(self):
        Button.default(self)
        self.spaceBetweenSquare = 3
    def clickAction(self):
        Button.clickAction(self)
        UI["errorHist"].curPage -= 1
        UI["errorHist"].curPage = max(UI["errorHist"].curPage, 1)
        
class RightArrowButton(Button):
    def __init__(self, x, y, w):
        Button.__init__(self, "", x, y, w, w, 0)
    def display(self):
        Button.display(self)
        triangle(self.x + self.spaceBetweenSquare, self.y + self.spaceBetweenSquare, self.x +  self.spaceBetweenSquare, self.y + self.w - self.spaceBetweenSquare, self.x + self.w - self.spaceBetweenSquare, self.y + (self.w) / 2)
    def default(self):
        Button.default(self)
        self.spaceBetweenSquare = 3
    def clickAction(self):
        Button.clickAction(self)
        UI["errorHist"].curPage += 1
        UI["errorHist"].curPage = min(UI["errorHist"].curPage, UI["errorHist"].cantPage)
        

class ScrollBar(Obj):
    def __init__(self, x, y, h):
        self.bx = x
        self.by = y
        self.bh = h
        self.bw = h / 10
        self.percent = 0
        diff = h / 40
        Obj.__init__(self, self.bx - diff, self.by + h, float(self.bh) * 0.15, self.bh / 10)
    def display(self):
        fill(self.barFill)
        rect(self.bx, self.by, self.bw, self.bh)
        fill(*self.scrollFill)
        stroke(self.scrollStroke)
        rect(self.x, self.y, self.w, self.h)
    def default(self):
        self.yOffset = 0.0
        self.barFill = 0
        self.scrollFill = [255, 0, 0]
        self.scrollStroke = 255
    def clickAction(self):
        self.click = True
        self.yOffset = mouseY - self.y
    def dragAction(self):
        self.y = mouseY - self.yOffset
        if self.y < self.by:
            self.y = self.by
        if self.y > self.by + self.bh:
            self.y = self.by + self.bh
        self.percent = ((float(self.by + self.bh - self.y) * 100.0) / float(self.bh))

class LearningRate(ScrollBar):
    def __init__(self, x, y, h):
        ScrollBar.__init__(self, x, y, h)
        self.percent = 10.0
        self.y = -(((self.percent * float(self.bh)) / 100.0) - self.by - self.bh)
    def display(self):
        ScrollBar.display(self)
        self.val = self.percent / 100.0
        textSize(self.bh * 0.075)
        textAlign(CENTER, CENTER)
        text(str("{:.2f}".format(self.val)), self.bx - (self.bh / 20), self.by - (self.bh / 8), self.w * 1.5, self.h)
        text("Learning", self.bx - 20, self.by + self.bh + 15, self.w * 2.2, self.h)
        text("rate", self.bx - 20, self.by + self.bh + 28, self.w * 2.2, self.h)
       
class Epochs(ScrollBar):
    def __init__(self, x, y, h):
        ScrollBar.__init__(self, x, y, h)
        self.percent = 50.0
        self.y = -(((self.percent * float(self.bh)) / 100.0) - self.by - self.bh)
    def display(self):
        ScrollBar.display(self)
        self.val = int(round(self.percent * 2.0))
        textSize(self.bh * 0.075)
        textAlign(CENTER, CENTER)
        text(str(self.val), self.bx - (self.bh / 20), self.by - (self.bh / 8), self.w * 1.5, self.h)
        text("Epochs", self.x - 20, self.by + self.bh + 15, self.w * 2.2, self.h)
        text("number", self.x - 20, self.by + self.bh + 28, self.w * 2.2, self.h)
        
class MaximumError(ScrollBar):
    def __init__(self, x, y, h):
        ScrollBar.__init__(self, x, y, h)
    def display(self):
        ScrollBar.display(self)
        self.val = self.percent / 100.0
        textSize(self.bh * 0.075)
        textAlign(CENTER, CENTER)
        text(str("{:.2f}".format(self.val)), self.bx - (self.bh / 20), self.by - (self.bh / 8), self.w * 1.5, self.h)
        text("Maximum", self.bx - 20, self.by + self.bh + 15, self.w * 2.2, self.h)
        text("error", self.bx - 20, self.by + self.bh + 28, self.w * 2.2, self.h)
        
class HiddenLayers(ScrollBar):
    def __init__(self, x, y, h):
        ScrollBar.__init__(self, x, y, h)
        self.percent = 20.0
        self.y = -(((self.percent * float(self.bh)) / 100.0) - self.by - self.bh)
    def display(self):
        ScrollBar.display(self)
        self.val = int(round(self.percent / 10.0))
        textSize(self.bh * 0.075)
        textAlign(CENTER, CENTER)
        text(str("{:.2f}".format(self.val)), self.bx - (self.bh / 20), self.by - (self.bh / 8), self.w * 1.5, self.h)
        text("Hidden", self.bx - 20, self.by + self.bh + 15, self.w * 2.2, self.h)
        text("layers", self.bx - 20, self.by + self.bh + 28, self.w * 2.2, self.h)
        
class NeuronsPerLayer(ScrollBar):
    def __init__(self, x, y, h):
        ScrollBar.__init__(self, x, y, h)
        self.percent = 5.0
        self.y = -(((self.percent * float(self.bh)) / 100.0) - self.by - self.bh)
    def display(self):
        ScrollBar.display(self)
        self.val = int(round(self.percent / 2.0))
        textSize(self.bh * 0.075)
        textAlign(CENTER, CENTER)
        text(str("{:.2f}".format(self.val)), self.bx - (self.bh / 20), self.by - (self.bh / 8), self.w * 1.5, self.h)
        text("Neurons", self.bx - 20, self.by + self.bh + 15, self.w * 2.2, self.h)
        text("per layer", self.bx - 20, self.by + self.bh + 28, self.w * 2.2, self.h)
        
class FieldSize(ScrollBar):
    def __init__(self, x, y, h):
        ScrollBar.__init__(self, x, y, h)
        self.percent = 10.0
        self.y = -(((self.percent * float(self.bh)) / 100.0) - self.by - self.bh)
    def display(self):
        ScrollBar.display(self)
        self.val = int(round(self.percent * 0.5)) * 2 + 3
        textSize(self.bh * 0.075)
        textAlign(CENTER, CENTER)
        text(str(self.val), self.bx - (self.bh / 20), self.by - (self.bh / 8), self.w * 1.5, self.h)
        text("Field", self.x - 20, self.by + self.bh + 15, self.w * 2.2, self.h)
        text("size", self.x - 20, self.by + self.bh + 28, self.w * 2.2, self.h)
    def dragAction(self):
        ScrollBar.dragAction(self)
        xx = UI["field"].x
        yy = UI["field"].y
        ww = UI["field"].w
        UI["field"] = Field(xx, yy, ww, self.val)
        
class Field(Obj):
    def __init__(self, x, y, w, n):
        self.n = n
        Obj.__init__(self, x, y, w, w)
        self.grid = [[0 for i in range(self.n)] for j in range(self.n)] # n * m matrix
        self.n = n - 1
        self.space = float(self.w) / float(self.n)
        self.curMode = 1
        self.train = False
        self.iterationsCount = 0
        self.showLines = False
        self.trainingSet = []
    def display(self):
        fill(self.gridFill)
        stroke(self.gridStroke)
        for i in range(self.n):
            for j in range(self.n):
                rect(self.x + i * self.space, self.y + j * self.space, self.space, self.space)
        strokeWeight(self.axisStrokeWeight)
        stroke(*self.axisStroke)
        line(self.x + self.space * (self.n // 2), self.y, self.x + self.space * (self.n // 2), self.y + self.space * self.n)
        line(self.x, self.y + self.space * (self.n // 2), self.x + self.space * self.n, self.y + self.space * (self.n // 2))
        for i in range(self.n + 1):
            for j in range(self.n + 1):
                if self.grid[i][j] == 1:
                    stroke(*self.pointStrokeMode1)
                    fill(*self.pointFillMode1)
                    circle(self.x + i * self.space, self.x + j * self.space, self.pointSz)
                if self.grid[i][j] == 2:
                    stroke(*self.pointStrokeMode2)
                    fill(*self.pointFillMode2)
                    circle(self.x + i * self.space, self.x + j * self.space, self.pointSz)
                if self.grid[i][j] == 3:
                    stroke(*self.pointStrokeMode3)
                    fill(*self.pointFillMode3)
                    circle(self.x + i * self.space, self.x + j * self.space, self.pointSz)
        if self.train:
            self.nextEpoch()
        # if self.showLines:
        #     # print("here")
        #     a = float(-self.weights[0])
        #     b = float(self.weights[1])
        #     c = float(-self.weights[2])
        #     n2 = float(self.n // 2)
        #     eval0 = (a * (-n2) + c) / b + n2
        #     evaln = (a * (+n2) + c) / b + n2
        #     stroke(0)
        #     if(b != 0): line(float(self.x) + float(self.space) * 0, float(self.y) + float(self.space) * eval0, float(self.x) + float(self.space) * float(self.n), float(self.y) + float(self.space) * evaln)
        
    def testElem(self, elem):
        outputs = self.forwardPropagation(elem)
        return outputs.index(max(outputs))
    
    def activatePerceptron(self, W, I):
        activ = W[-1]
        for i in range(len(W) - 1):
            activ += W[i] * I[i]
        return activ
    
    def sigmoidTransfer(self, activ):
        return 1.0 / (1.0 + exp(-activ))
                  
    def forwardPropagation(self, row):
        inputs = row
        for layer in self.network:
            newInputs = []
            for perceptron in layer:
                activ = self.activatePerceptron(perceptron["weights"], inputs)
                perceptron["output"] = self.sigmoidTransfer(activ)
                newInputs.append(perceptron["output"])
            inputs = newInputs
        return inputs
    
    def transferDerivative(self, output):
        return output * (1.0 - output)
    
    def backPropagation(self, expected):
        for i in reversed(range(len(self.network))):
            layer = self.network[i]
            errors = []
            if i != len(self.network) - 1:
                for j in range(len(layer)):
                    error = 0.0
                    for perceptron in self.network[i + 1]:
                        error += (perceptron["weights"][j] * perceptron["delta"])
                    errors.append(error)
            else:
                for j in range(len(layer)):
                    perceptron = layer[j]
                    errors.append(perceptron["output"] - expected[j])
            for j in range(len(layer)):
                perceptron = layer[j]
                perceptron["delta"] = errors[j] * self.transferDerivative(perceptron["output"])
                
    def updateWeights(self, row):
        for i in range(len(self.network)):
            inputs = row[:-1]
            if i != 0:
                inputs = [perceptron["output"] for perceptron in self.network[i - 1]]
            for perceptron in self.network[i]:
                for j in range(len(inputs)):
                    perceptron["weights"][j] -= self.learningRate * perceptron["delta"] * inputs[j]
                perceptron["weights"][-1] -= self.learningRate * perceptron["delta"]
    
    def nextEpoch(self):
        print(self.epochsLeft)
        if self.epochsLeft:
            self.epochsLeft -= 1
            self.iterationsCount = 0
            sumError = 0
            for row in self.trainingSet:
                outputs = self.forwardPropagation(row)
                expected = [0 for i in range(self.nOutputs)]
                expected[row[-1]] = 1
                sumError += sum([(expected[i] - outputs[i])**2 for i in range(len(expected))])
                self.backPropagation(expected)
                self.updateWeights(row)
            sumError = float(sumError) / float(len(self.trainingSet))
            UI["errorHist"].hist.append(sumError)
            UI["errorHist"].recalc()
            if sumError < self.maximumError:
                self.epochsLeft = 0
        if self.epochsLeft == 0:
            self.epochsLeft = -1
            self.train = False
            offset = self.n // 2
            for i in range(self.n + 1):
                for j in range(self.n + 1):
                    if(self.grid[i][j] == 0):
                        self.grid[i][j] = self.testElem([float(i - offset), float(j - offset), 0.0]) + 1
            print("TERMINADO")

    def default(self):
        self.gridFill = 255
        self.gridStroke = 0
        self.axisStrokeWeight = 1
        self.axisStroke = [255, 0, 0]
        self.pointSz = 6
        self.pointStrokeMode1 = [0, 0, 255]
        self.pointFillMode1 = [0, 0, 255]
        self.pointStrokeMode2 = [255, 0, 0]
        self.pointFillMode2 = [255, 0, 0]
        self.pointStrokeMode3 = [0, 161, 53]
        self.pointFillMode3 = [0, 161, 53]
        self.delay = 10
        self.inf = self.n + 10
    def clickAction(self):
        if UI["field"].train: return
        UI["train"].readyToTrain = False
        self.click = True
        # revisar donde fue el click redondeando coordenadas del mouse
        x = int(round((mouseX - float(self.x)) / float(self.space)))
        y = int(round((mouseY - float(self.y)) / float(self.space)))
        if self.curMode == -1:
            offset = self.n // 2
            R = self.testElem([float(x - offset), float(y - offset), 1.0])
            classPred = 0
            if R[0][0] > 0: classPred = 1
            else: classPred = 0
            self.grid[x][y] = classPred + 1
        else:
            if self.grid[x][y] != 0:
                self.grid[x][y] = 0
            else:
                self.grid[x][y] = self.curMode
    
class ErrorHist(Obj):
    def __init__(self, x, y, w, h, limPerPage):
        self.limPerPage = limPerPage
        Obj.__init__(self, x, y, w, h)
        self.cantPage = 1
        self.curPage = 1
        self.reset()
    def display(self):
        stroke(self.lineStroke)
        line(self.x, self.y + self.h, self.x + self.w, self.y + self.h)
        stroke(self.barStroke)
        st = self.limPerPage * (self.curPage - 1)
        for i in range(self.limPerPage):
            pos = i + st
            if(pos >= len(self.hist)): break
            hh = self.barLimUp * self.hist[pos]
            rect(self.x + (i * self.barSz), self.y + self.h - hh, self.barSz, hh)
            textSize(self.txtSz)
            textAlign(CENTER, CENTER)
            text(str(self.hist[pos]), self.x + (i * self.barSz), self.y + self.h + self.txtSz, self.barSz, self.txtSz + 3)
    def reset(self):
        self.cantPage = 1
        self.curPage = 1
        # self.maxHeight = max(1, int(len(UI["field"].trainingSet)))
        self.maxHeight = 1.0
        self.hist = []
        self.barSz = self.w / self.limPerPage
        self.barLimUp = self.h / self.maxHeight
    def default(self):
        self.lineStroke = 0
        self.barStroke = 255
        self.txtSz = 10
    def recalc(self):
        self.cantPage = max(1, len(self.hist) // self.limPerPage + int((len(self.hist) % self.limPerPage) != 0))
        self.curPage = self.cantPage
        self.maxHeight = max(self.hist)
        self.barLimUp = self.h / self.maxHeight

def setup():
    global UI
    background(255)
    size(1100,600)
    UI["mode1"] = BlueButtonMode1("Blue", 670, 20, 80, 30, 15)
    UI["mode2"] = RedButtonMode2("Red", 750, 20, 80, 30, 15)
    UI["mode3"] = GreenButtonMode3("Green", 830, 20, 80, 30, 15)
    UI["learningRate"] = LearningRate(540, 100, 200)
    UI["epochs"] = Epochs(630, 100, 200)
    UI["maximumError"] = MaximumError(720, 100, 200)
    UI["field"] = Field(20, 20, 450, 11)
    UI["initialize"] = InitializeButton("Initialize", 680, 380, 100, 30, 15)
    UI["train"] = TrainButton("Train", 780, 380, 100, 30, 15)
    UI["testResult"] = TestResultButton("Test",730, 410, 100, 30, 15)
    UI["errorHist"] = ErrorHist(20, 470, 1000, 100, 20)
    UI["leftArrow"] = LeftArrowButton(1000, 450, 20)
    UI["rightArrow"] = RightArrowButton(1025, 450, 20)
    UI["fieldSize"] = FieldSize(810, 100, 200)
    UI["hiddenLayers"] = HiddenLayers(900, 100, 200)
    UI["neuronsPerLayer"] = NeuronsPerLayer(990, 100, 200)

def draw():
    global UI
    background(255)
    for i in UI:
        stroke(0)
        strokeWeight(1)
        fill(0)
        UI[i].display()
    
def mousePressed():
    global UI
    for i in UI:
        if UI[i].mouseOver(mouseX, mouseY):
            UI[i].clickAction()

def mouseReleased():
    global UI
    for i in UI:
        UI[i].releaseAction()
        
def mouseDragged():
    global UI
    for i in UI:
        if UI[i].click:
            UI[i].dragAction()
    
    
    
