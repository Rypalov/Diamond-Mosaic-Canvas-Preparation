import cv2
import numpy as np
import os

def get_ratio():
    """Получает соотношение сторон от пользователя"""
    while True:
        try:
            ratio = input("Введите соотношение (ширина:высота): ")
            width, height = map(int, ratio.split(':'))

            if width <= 0 or height <= 0:
                print("Значения должны быть положительными числами!")
                continue

            return width, height
        except ValueError:
            print("Ошибка! Используйте формат: ширина:высота (например, 16:9)")

def split_image_into_blocks(img, blocks_x, blocks_y):
    """Разделяет изображение на блоки и сохраняет их"""
    h, w = img.shape[:2]

    # Создаем папку для блоков, если она не существует
    block_dir = "map_img"
    os.makedirs(block_dir, exist_ok=True)

    # Вычисляем размер каждого блока
    block_width = w // blocks_x
    block_height = h // blocks_y

    # Сохраняем каждый блок
    for i in range(blocks_y):
        for j in range(blocks_x):
            block = img[i*block_height:(i+1)*block_height,
                    j*block_width:(j+1)*block_width]

            # Сохраняем блок с названием блока_x_y.jpg
            filename = f"block_{j+1}_{i+1}.jpg"
            cv2.imwrite(os.path.join(block_dir, filename), block)

    return block_width, block_height

# Читаем изображение
img = cv2.imread('img.jpg')

# Проверяем успешность загрузки
if img is None:
    print("Ошибка при чтении изображения!")
else:
    # Получаем соотношение от пользователя
    blocks_y, blocks_x = get_ratio()

    # Отображаем оригинальное изображение
    cv2.imshow('Оригинальное изображение', img)

    # Разделяем изображение на блоки
    block_width, block_height = split_image_into_blocks(img, blocks_x, blocks_y)

    # Выводим информацию
    print(f"\nТекущие размеры изображения: {img.shape[1]}x{img.shape[0]}")
    print(f"Количество блоков: {blocks_x}x{blocks_y}")
    print(f"Размер каждого блока: {block_width}x{block_height}")
    print(f"\nБлоки сохранены в папку 'map_img'")

    # Ждем нажатия клавиши
    cv2.waitKey(0)

    # Закрываем все окна
    cv2.destroyAllWindows()