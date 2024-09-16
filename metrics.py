import numpy as np
import helperFuncs

def mse(originalImage: np.ndarray, encryptedImage: np.ndarray, x:int, y:int) -> float:
    m = originalImage.shape[0]
    n = originalImage.shape[1]

    origBlocks = helperFuncs.getBlocks(originalImage)
    encryptedBlocks = helperFuncs.getBlocks(encryptedImage)

    sum = 0

    for i in range(len(origBlocks)):
        sum += pow(origBlocks[i][x][y] - encryptedBlocks[i][x][y], 2)
    
    return sum / (m * n)

def rmse(mseScore: float) -> float:
    return np.sqrt(mseScore)

def psnr(mseScore: float) -> float:
    return 10 * np.log10((255 * 255) / mseScore)

def ec(message: str, image: np.ndarray) -> float:
    m = image.shape[0]
    n = image.shape[1]

    return len(message) / (m * n)

def ber(inputMessage: str, outputMessage: str) -> float:
    cnt = 0
    for i in range(len(inputMessage)):
        if inputMessage[i] != outputMessage[i]:
            cnt += 1
    
    return cnt / len(inputMessage)