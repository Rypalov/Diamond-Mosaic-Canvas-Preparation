import cv2
import numpy as np

def validate_aspect_ratio(ratio_str):
    """Проверяет корректность введенного соотношения сторон."""
    try:
        parts = ratio_str.split(':')
        if len(parts) != 2:
            raise ValueError("Соотношение должно быть в формате 'a:b'")

        width = float(parts[0].strip())
        height = float(parts[1].strip())

        if width <= 0 or height <= 0:
            raise ValueError("Числа должны быть положительными")

        # Проверяем, что числа целые
        if width != int(width) or height != int(height):
            raise ValueError("Числа должны быть целыми")

        return int(width), int(height)

    except ValueError as e:
        raise ValueError(f"Неверный формат соотношения: {str(e)}")

def get_user_input():
    """Получает и валидирует ввод пользователя."""
    while True:
        try:
            ratio_input = input("Введите соотношение сторон (например, 30:40): ")
            width, height = validate_aspect_ratio(ratio_input)
            return width, height

        except ValueError as e:
            print(f"Ошибка: {str(e)}")
            print("Попробуйте снова.")

def find_largest_multiple_less_than(size, divisor):
    """Находит наибольшее кратное число, меньшее или равное заданному размеру."""
    return (size // divisor) * divisor

def remove_excess_pixels(image, width_divisor, height_divisor):
    """Удаляет лишние пиксели для достижения заданного соотношения сторон."""
    try:
        if image is None:
            raise ValueError("Изображение не загружено")

        height, width = image.shape[:2]

        print(f"Исходные размеры: {width}x{height}")

        # Находим оптимальные размеры, кратные делителям
        target_width = find_largest_multiple_less_than(width, width_divisor)
        target_height = find_largest_multiple_less_than(height, height_divisor)

        print(f"Целевые размеры: {target_width}x{target_height}")

        # Определяем, по какой стороне нужно обрезать
        if width > target_width:
            # Удаляем пиксели по ширине
            excess_width = width - target_width
            left_cut = int(excess_width // 2)
            right_cut = int(excess_width - left_cut)
            print(f"Обрезка по ширине: слева {left_cut}, справа {right_cut}")
            image = image[:, left_cut:-right_cut]

        if height > target_height:
            # Удаляем пиксели по высоте
            excess_height = height - target_height
            top_cut = int(excess_height // 2)
            bottom_cut = int(excess_height - top_cut)
            print(f"Обрезка по высоте: сверху {top_cut}, снизу {bottom_cut}")
            image = image[top_cut:-bottom_cut]

        return image

    except Exception as e:
        print(f"Ошибка при обработке пикселей: {str(e)}")
        return None

def process_image():
    """Обрабатывает изображение с фиксированными именами файлов."""
    try:
        # Загружаем изображение
        image = cv2.imread('image_1.jpg')
        if image is None:
            raise ValueError("Ошибка при загрузке изображения 'image_1.jpg'")

        # Проверяем размеры изображения
        height, width = image.shape[:2]
        if height <= 0 or width <= 0:
            raise ValueError("Некорректные размеры изображения")

        print(f"Загружено изображение размером {width}x{height}")

        # Получаем соотношение сторон от пользователя
        width_divisor, height_divisor = get_user_input()
        print(f"Ширина должна делиться на {width_divisor}")
        print(f"Высота должна делиться на {height_divisor}")

        # Удаляем лишние пиксели
        processed = remove_excess_pixels(image, width_divisor, height_divisor)
        if processed is None:
            raise ValueError("Ошибка при обработке изображения")

        # Проверяем размеры результата
        if processed.size == 0:
            raise ValueError("Результат обработки пустой")
        elif processed.shape[0] == 0 or processed.shape[1] == 0:
            raise ValueError("Одна из размерностей результата равна нулю")

        # Проверяем, что размеры делятся на заданные делители
        if processed.shape[1] % width_divisor != 0:
            raise ValueError(f"Ширина {processed.shape[1]} не делится на {width_divisor}")
        if processed.shape[0] % height_divisor != 0:
            raise ValueError(f"Высота {processed.shape[0]} не делится на {height_divisor}")

        # Сохраняем результат
        cv2.imwrite('img.jpg', processed)

        print(f"\nРезультат обработки:")
        print(f"Исходный размер: {processed.shape[:2]}")
        print(f"Ширина делится на {width_divisor}: {processed.shape[1] % width_divisor == 0}")
        print(f"Высота делится на {height_divisor}: {processed.shape[0] % height_divisor == 0}")

        return processed  # Возвращаем результат вместо None

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

def main():
    """Основная функция программы."""
    print("Начало обработки изображения...")
    result = process_image()
    if result is None:
        print("Обработка завершена с ошибкой")
    else:
        print("Обработка завершена успешно")

if __name__ == "__main__":
    main()