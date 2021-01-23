# random number and coordinate generators

import random

class NodeGeneratorBase():
    def __init__(self):
        pass

    def generate(self) -> list:
        pass


class RandomCoords(NodeGeneratorBase):
    '''random coordinates inside one big region'''

    def __init__(self, num: int = 2) -> None:
        self.num = num
        self.seed = None

    def setCoordNumber(self, num: int) -> None:
        self.num = num

    def setSeed(self, seed: int) -> None:
        self.seed = seed

    def generate(self, min: tuple, max: tuple) -> list:
        '''
        simple random numbers from the whole region
        min: coordinates of top left corner
        max: coordinates of bottom right corner
        '''
        result = []
        random.seed(self.seed)
        for n in range(self.num):
            x = random.randint(min[0], max[0])
            y = random.randint(min[1], max[1])
            result.append((x,y))
        random.seed(None)

        #print(result)
        return result


class RandomRegionCoords(RandomCoords):
    '''
    extends the random coordinate generator
    regionNum variables sets the number of regions
    the whole area should be divided
    '''

    def __init__(self, num: int = 2, regionNumX: int = 2, regionNumY: int = 2) -> None:
        self.regionNumX = regionNumX
        self.regionNumY = regionNumY
        super().__init__(num)

    def setRegionNumbers(self, regionNumX, regionNumY) -> None:
        self.regionNumX = regionNumX
        self.regionNumY = regionNumY

    def generate(self, min: tuple, max: tuple) -> list:
        '''
        simple random numbers by region
        min: coordinates of top left corner of whole area
        max: coordinates of bottom right corner of whole area
        '''
        offsetX = max[0] // self.regionNumX
        offsetY = max[1] // self.regionNumY

        regionMinX = min[0]
        regionMaxX = regionMinX + offsetX
        regionMinY = min[1]
        regionMaxY = regionMinY + offsetY

        result = []
        self.num = 1
        for rX in range(self.regionNumX):
            for rY in range(self.regionNumY):
                coord = super().generate((regionMinX, regionMinY),
                                          (regionMaxX, regionMaxY))
                result.append(coord[0])
                # shift moving region y coords
                regionMinY += offsetY
                regionMaxY += offsetY
            # reset moving region y coords 
            regionMinY = 0
            regionMaxY = 0 + offsetY
            # shift moving region x coords
            regionMinX += offsetX
            regionMaxX += offsetX
            
        print(result)
        return result
