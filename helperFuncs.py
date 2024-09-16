import numpy as np
import random

def generateKey(n: int) -> str:
     message = ''.join(str(random.randint(0, 1)) for i in range(n))
     return message

def getBlocks(image: np.ndarray) -> np.ndarray:
    m = image.shape[0]
    n = image.shape[1]
    blocks = np.zeros(((m // 8) * (n // 8) , 8, 8))
    ptr = 0

    for i in range(0, m - (m % 8), 8):
        for j in range(0, n - (n % 8), 8):
            block = np.zeros((8,8))
            for a in range(8):
                for b in range(8):
                    block[a][b] = image[i + a][j + b][0] - 128
            blocks[ptr] = block
            ptr += 1
    
    return blocks

def median(block: np.ndarray) -> int:
    buf = [block[0][1], block[0][2], block[0][3], block[1][0], 
           block[1][1], block[1][2], block[2][0], block[2][1], 
           block[3][0]]
    buf.sort()
    return buf[4]

def modifactionPower(block: np.ndarray, Z:int=2) -> float:
    med = median(block)
    if (abs(block[0][0]) > 1000 or abs(block[0][0]) < 1):
            return abs(Z * med)
    return abs(Z * (block[0][0] - med) / block[0][0])