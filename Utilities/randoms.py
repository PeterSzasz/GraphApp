# random number and coordinate generators

import random

class RandomInt():
    '''
    generates one random integer between min and max
    '''    
    def __init__(self) -> None:
        self.min = 0
        self.max = 1000
        self.rand_strat = None

    def setMin(self, min: int) -> None:
        self.min = min

    def setMax(self, max: int) -> None:
        self.max = max

    def generate(self) -> int:
        return random.randint(self.min, self.max)


class RandomCoord(RandomInt):
    '''
    extends the random int generator with a Y coordinate
    min2, max2, setMinX, etc are for this extra dimension
    min and max and the other parent methods are for X coord
    '''

    def __init__(self) -> None:
        self.min2 = 0
        self.max2 = 1000
        super().__init__()
    
    def setMinX(self, min: int) -> None:
        self.setMin(min)

    def setMaxX(self, max: int) -> None:
        self.setMax(max)

    def setMinY(self, min: int) -> None:
        self.min2 = min

    def setMaxY(self, max: int) -> None:
        self.max2 = max

    def moveBoundaries(self, offsetX, offsetY):
        '''shifts the min-max regions'''
        self.min += offsetX
        self.max += offsetX
        self.min2 += offsetY
        self.max2 += offsetY

    def generateCoord(self) -> tuple:
        x = self.generate()
        y = random.randint(self.min2, self.max2)
        print(str(x)+" "+str(y))
        return (x, y)