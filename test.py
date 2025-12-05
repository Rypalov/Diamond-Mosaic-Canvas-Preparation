import cv2
import numpy as np
import os

def show_image_with_transparency(image, alpha):
    """Создает копию изображения с заданным уровнем прозрачности"""
    white_background = np.ones_like(image, dtype=np.uint8) * 255
    return cv2.addWeighted(image, alpha, white_background, 1 - alpha, 0)

def add_text(image, text):
    """Добавляет текст под изображением"""
    height, width = image.shape[:2]
    text_background = np.ones((50, width, 3), dtype=np.uint8) * 255
    cv2.putText(text_background, text, (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return np.vstack((image, text_background))

def combine_images(images):
    """Объединяет список изображений горизонтально с отступами"""
    padded_images = []
    for img in images:
        padded = cv2.copyMakeBorder(
            img, 0, 0, 10, 10,
            cv2.BORDER_CONSTANT, value=(255, 255, 255)
        )
        padded_images.append(padded)
    return np.concatenate(padded_images, axis=1)

def resize_image(image, target_size):
    """Изменяет размер изображения до заданного размера, сохраняя пропорции"""
    h, w = image.shape[:2]
    scale = min(target_size[0]/w, target_size[1]/h, 1.0)
    new_size = (int(w*scale), int(h*scale))
    return cv2.resize(image, new_size)

def main():
    # Проверка существования файла
    image_path = "map_img/block_4_5.jpg"
    if not os.path.exists(image_path):
        print(f"Ошибка: Файл {image_path} не найден!")
        return

    # Загрузка изображения
    img = cv2.imread(image_path)

    if img is None:
        print("Ошибка: Не удалось загрузить изображение!")
        return

    original_size = (img.shape[1], img.shape[0])
    print(f"Исходный размер: {original_size[0]}x{original_size[1]} пикселей")

    # Изменение размера изображения до 1000x1000
    target_size = (1000, 1000)
    resized_img = resize_image(img, target_size)
    print(f"Фактический размер после изменения: {resized_img.shape[1]}x{resized_img.shape[0]} пикселей")

    # Создание окна для отображения
    cv2.namedWindow("Варианты прозрачности", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Варианты прозрачности", 1000, 1000)

    # Варианты прозрачности
    alphas = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9]
    ]

    rows = []
    for row_alphas in alphas:
        row_images = []
        for alpha in row_alphas:
            result = show_image_with_transparency(resized_img, alpha)
            result = add_text(result, f"{alpha:.1f}")
            row_images.append(result)
        row = combine_images(row_images)
        rows.append(row)

    final_image = np.concatenate(rows, axis=0)
    final_image = cv2.copyMakeBorder(
        final_image, 10, 10, 0, 0,
        cv2.BORDER_CONSTANT, value=(255, 255, 255)
    )

    # Отображение результата
    cv2.imshow("Варианты прозрачности", final_image)

    # Добавляем несколько пауз для гарантированного отображения
    for _ in range(5):
        cv2.waitKey(100)

    # Проверка размера итогового изображения
    print(f"Размер итогового изображения: {final_image.shape[1]}x{final_image.shape[0]} пикселей")

    # Получение ввода от пользователя
    print("\nВыберите уровень прозрачности (введите число от 0 до 10):")
    try:
        value = float(input())
        if 0 <= value <= 10:
            final_alpha = value / 10
            final_result = show_image_with_transparency(resized_img, final_alpha)
            final_result = add_text(
                final_result,
                f"{value/10:.1f}"
            )
            cv2.imshow("Финальный результат", final_result)
        else:
            print("Пожалуйста, введите значение между 0 и 10")
    except ValueError:
        print("Ошибка: Пожалуйста, введите корректное числовое значение")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()