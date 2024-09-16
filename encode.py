import numpy as np
import scipy.fft
import helperFuncs

def encrypt(message: str, image: np.ndarray, T:int=110, K:int=15) -> np.ndarray:
    m = image.shape[0]
    n = image.shape[1]
    newImage = image
    widthBlock = n // 8
    blocks = helperFuncs.getBlocks(image)

    for i in range(len(blocks)):
        blocks[i] = scipy.fft.dct(scipy.fft.dct(blocks[i].T, norm='ortho').T, norm='ortho')
    
    for i in range(min(len(blocks), len(message))):
        x = 4
        y = 4
        modPower = helperFuncs.modifactionPower(blocks[i])

        neighbour = -widthBlock
        if i < widthBlock:
            neighbour = widthBlock         

        delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
        if int(message[i]) == 1:
            if delta > T - K:
                while delta > T - K:
                    blocks[i][x][y] -= modPower
                    delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
            elif K > delta > (-T / 2):
                while delta < K:
                    blocks[i][x][y] += modPower
                    delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
            elif delta < (-T / 2):
                while delta > -T - K:
                    blocks[i][x][y] -= modPower
                    delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
        else:
            if delta > T / 2:
                while delta <= T + K:
                    blocks[i][x][y] += modPower
                    delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
            elif -K < delta < T / 2:
                while delta >= -K:
                    blocks[i][x][y] -= modPower
                    delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
            elif delta < K - T:
                while delta <= K - T:
                    blocks[i][x][y] += modPower
                    delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
            
    for i in range(len(blocks)):
        blocks[i] = scipy.fft.idct(scipy.fft.idct(blocks[i].T, norm='ortho').T, norm='ortho')
        blocks[i] = np.round(blocks[i])
        for j in range(8):
            for k in range(8):
                blocks[i][j][k] += 128

    blocks = blocks.astype("int64")

    idx = 0
    for i in range(0, m - (m % 8), 8):
        for j in range(0, n - (n % 8), 8):
            for a in range(8):
                for b in range(8):
                    newImage[i + a][j + b][0] = blocks[idx][a][b]
            idx += 1

    return newImage

def decrypt(image: np.ndarray, x:int, y:int, T:int=110, K:int=15) -> str:
    blocks = helperFuncs.getBlocks(image)
    res = ""
    n = image.shape[1]
    widthBlock = n // 8

    for i in range(len(blocks)):
        blocks[i] = scipy.fft.dct(scipy.fft.dct(blocks[i].T, norm='ortho').T, norm='ortho')
    
    for i in range(len(blocks)):
        x = 4
        y = 4

        neighbour = -widthBlock
        if i < widthBlock:
            neighbour = widthBlock         

        delta = blocks[i][x][y] - blocks[i + neighbour][x][y]
        if (delta < -T) or ((delta > 0) and (delta < T)):
            res += '1'
        else:
            res += '0'
    
    return res