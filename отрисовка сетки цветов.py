import cv2
import numpy as np

def draw_colors(rgb_values):
    # Создаем пустое изображение с белым фоном
    # Высота = количество строк × 15px
    # Ширина = максимальное количество цветов в строке × 15px
    rows = len(rgb_values)
    max_cols = max(len(row) for row in rgb_values)
    height = rows * 15
    width = max_cols * 15
    img = np.full((height, width, 3), 255, dtype=np.uint8)

    # Переводим RGB в BGR формат для OpenCV
    bgr_values = [[(b, g, r) for r, g, b in row] for row in rgb_values]

    # Рисуем каждый цвет
    for row_idx, row in enumerate(bgr_values):
        y_start = row_idx * 15
        for col_idx, color in enumerate(row):
            x_start = col_idx * 15
            cv2.rectangle(img, (x_start, y_start),
                          (x_start + 15, y_start + 15), color, -1)

    return img

# Пример использования с разным количеством цветов в строках
rgb_values = [
    [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)],           # Первая строка: красный, зеленый
    [(0, 255, 255), (0, 0, 255), (255, 255, 0), (255, 0, 255), (255, 0, 0), (0, 255, 0)],  # Вторая строка: синий, желтый, магента
    [(0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)],                        # Третья строка: один цвет
]

result = draw_colors(rgb_values)
cv2.imshow('Colors', result)
cv2.waitKey(0)
cv2.destroyAllWindows()