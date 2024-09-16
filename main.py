import encode
import metrics
from PIL import Image
import numpy as np

image = Image.open(r"./input/img.jpeg")
m, h = image.size
image = np.array(image)

n = (m // 8) * (h // 8)
buf = open(r"./input/secret.txt")
message = buf.read()
buf.close()

newImage = encode.encrypt(message, image)
result = Image.fromarray(newImage)
result.save("./output/encrypted.jpeg")

encoded = Image.open(r"img.jpg")
encoded = np.array(encoded)

resp = encode.decrypt(encoded, 4, 4)

mseScore = metrics.mse(image, encoded, 4, 4)

print(f"Среднеквадратичное отклонение(MSE) = {mseScore}")
print(f"Дисперсия(RMSE) = {metrics.rmse(mseScore)}")
print(f"Пиковое отношение сигнал-шум(PSNR) = {metrics.psnr(mseScore)}")
print(f"Количество бит на пиксель(EC) = {metrics.ec(message, image)}")
print(f"Интенсивность битовых ошибок(BER) = {metrics.ber(message, resp)}")
print(f"Длина сообщения = {len(message)}")