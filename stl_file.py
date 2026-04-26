# ============================================================================
# ЧАСТЬ 2: ЗАГРУЗКА STL-ФАЙЛА
# ============================================================================

print("\n" + "=" * 60)
print("ШАГ 1: ЗАГРУЗКА STL-ФАЙЛА")
print("=" * 60)
import os
import sys
import time
import numpy as np
import trimesh, pyvista
import matplotlib.pyplot as plt
import fast_simplification
# Укажите путь к вашему STL-файлу
# ВАЖНО: Замените "heart.stl" на путь к вашему файлу!
stl_file = "D://lessons/PhD/aproximation/wolfram/heart_comsol.stl"
# Проверяем, существует ли файл
if not os.path.exists(stl_file):
    print(f"ОШИБКА: Файл '{stl_file}' не найден!")
    print("\nЧто делать?")
    print("1. Убедитесь, что файл heart.stl находится в той же папке, что и скрипт")
    print("2. Или укажите полный путь к файлу, например:")
    print("   ПУТЬ_К_ФАЙЛУ = 'C:/Users/ВашеИмя/Downloads/heart.stl'")
    sys.exit(1)  # Останавливаем программу

# Получаем информацию о файле
size_file = os.path.getsize(stl_file) #размер_файла 
size_file_kb = size_file / 1024 #размер_в_кб
size_file__mb = size_file_kb / 1024 #размер_в_мб

print(f"\nfile найден: {"D://lessons/PhD/aproximation/wolfram/heart_comsol.stl"}")
print(f"Размер файла: {size_file_kb:.2f} КБ ({size_file__mb:.2f} МБ)")
#***************************************************************

# Загружаем STL-файл
print("\nЗагрузка модели...")
start_load = time.time()
print(start_load)

try:
    # trimesh.load() - основная функция для загрузки 3D-моделей
    # Она автоматически определяет формат файла (STL, OBJ, PLY и др.)
    model = trimesh.load(stl_file)
    
    # Проверяем, что загрузилось
    if isinstance(model, trimesh.Scene):
        # Если файл содержит сцену с несколькими объектами
        print("Обнаружена сцена с несколькими объектами. Объединяем...")
        model = model.dump(concatenate=True)
    time_load = time.time() - start_load
    print(f"✓ Модель загружена за {time_load:.2f} секунд")
except Exception as e:
    print(f"ОШИБКА при загрузке: {e}")
    print("\nВозможные причины:")
    print("- Файл поврежден")
    print("- Файл не является STL-форматом")
    print("- Не хватает памяти")
    sys.exit(1)

peaks = model.vertices # Все вершины (точки
edges = model.faces # Все грани (треугольники)
quantity_peaks = len(peaks) # количество_вершин
quantity_edges = len(edges) # количество_граней
print(f"\n=== ХАРАКТЕРИСТИКИ МОДЕЛИ ===")
print(f"Количество вершин (точек): {quantity_peaks:,}")
print(f"Количество граней (треугольников): {quantity_edges:,}")
print("****************************************************************")

# Анализируем размер модели
print(f"\n=== АНАЛИЗ РАЗМЕРА МОДЕЛИ ===")

if quantity_edges < 1000:
    print("Модель: ПРОСТАЯ (менее 1000 треугольников)")
    print("Рекомендация: Упрощение может не потребоваться")
    
elif quantity_edges < 10000:
    print("Модель: СРЕДНЯЯ (1000-10000 треугольников)")
    print("Рекомендация: Упрощение даст хороший результат")
    
elif quantity_edges < 100000:
    print("Модель: ДЕТАЛЬНАЯ (10000-100000 треугольников)")
    print("Рекомендация: Упрощение значительно уменьшит размер")
    
else:
    print("Модель: ОЧЕНЬ ДЕТАЛЬНАЯ (более 100000 треугольников)")
    print("Рекомендация: Упрощение необходимо для комфортной работы")

print("****************************************************************")
# ============================================================================
# ЧАСТЬ 3: ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР
# ============================================================================

print("\n" + "=" * 60)
print("ШАГ 2: ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР МОДЕЛИ")
print("=" * 60)

# Создаем простую визуализацию
# matplotlib позволяет создавать графики и 3D-визуализации

fig = plt.figure(figsize=(12, 8))

# Создаем 3D-график
ax = fig.add_subplot(111, projection='3d')

# Отображаем модель как сетку из треугольников
# Используем только часть граней для скорости (если модель большая)
max_edges_display = min(quantity_peaks, 50000) # макс_граней_для_показа 

# Берем первые N граней для визуализации
display_peaks = edges #вершины_для_показа = вершины
display_edges = edges[:max_edges_display] 

# Отображаем треугольники
for edgess in display_edges:
    # Получаем координаты вершин треугольника
    trois_peaks = display_peaks[edgess]
    
    # Замыкаем треугольник (добавляем первую вершину в конец)
    x = [trois_peaks[0][0], trois_peaks[1][0], trois_peaks[2][0], trois_peaks[0][0]]
    y = [trois_peaks[0][1], trois_peaks[1][1], trois_peaks[2][1], trois_peaks[0][1]]
    z = [trois_peaks[0][2], trois_peaks[1][2], trois_peaks[2][2], trois_peaks[0][2]]
    
    ax.plot(x, y, z, color='red', linewidth=0.1, alpha=0.5)

# Настройки графика
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'Модель сердца ({quantity_edges:,} треугольников)')

# Сохраняем изображение
plt.savefig('results/preview.png', dpi=150)
print("✓ Предварительный просмотр сохранен в 'results/preview.png'")

# Показываем график (закомментировано, чтобы не прерывать выполнение)
#plt.show()

# Объяснение каждого параметра:
# figsize=(12, 8) - размер окна в дюймах
# projection='3d' - создаем 3D-график
# color='red' - красный цвет модели
# linewidth=0.1 - толщина линий
# alpha=0.5 - прозрачность (0 = невидимо, 1 = полностью видимо)
# dpi=150 - качество сохраненного изображения

# ============================================================================
# ЧАСТЬ 4: ИЗУЧЕНИЕ МОДЕЛИ
# ============================================================================

print("\n" + "=" * 60)
print("ШАГ 3: ИЗУЧЕНИЕ МОДЕЛИ")
print("=" * 60)

# 4.1 Границы модели (минимальные и максимальные координаты)
min_axis = peaks.min(axis=0)
max_axis = peaks.max(axis=0)
width = max_axis - min_axis

print("\n--- ГРАНИЦЫ МОДЕЛИ (Bounding Box) ---")
print(f"X: от {min_axis[0]:.2f} до {max_axis[0]:.2f} (ширина: {width[0]:.2f})")
print(f"Y: от {min_axis[1]:.2f} до {max_axis[1]:.2f} (ширина: {width[1]:.2f})")
print(f"Z: от {min_axis[2]:.2f} до {max_axis[2]:.2f} (ширина: {width[2]:.2f})")

# 4.2 Центр модели
centre = model.centroid
print(f"\n--- ЦЕНТР МОДЕЛИ ---")
print(f"Центр: ({centre[0]:.2f}, {centre[1]:.2f}, {centre[2]:.2f})")

# 4.3 Площадь поверхности
surface = model.area
print(f"\n--- ПЛОЩАДЬ ПОВЕРХНОСТИ ---")
print(f"Общая площадь: {surface:.2f} квадратных единиц")

# 4.4 Объем модели (только для замкнутых моделей)
if model.is_volume:
    volume = model.volume
    print(f"\n--- ОБЪЕМ МОДЕЛИ ---")
    print(f"Объем: {volume:.2f} кубических единиц")
else:
    print(f"\n--- ОБЪЕМ МОДЕЛИ ---")
    print("Модель не замкнута (есть отверстия). Объем не может быть вычислен.")

# 4.5 Проверка на водонепроницаемость
watertight = model.is_watertight
print(f"\n--- ПРОВЕРКА ЦЕЛОСТНОСТИ ---")
if watertight:
    print("✓ Модель водонепроницаема (замкнутая, нет дырок)")
else:
    print("✗ Модель НЕ водонепроницаема (есть отверстия или разрывы)")
    print("  Это может повлиять на качество упрощения")

# ============================================================================
# ЧАСТЬ 5: АНАЛИЗ КАЧЕСТВА СЕТКИ
# ============================================================================

print("\n" + "=" * 60)
print("ШАГ 4: АНАЛИЗ КАЧЕСТВА СЕТКИ")
print("=" * 60)

"""
ТЕОРИЯ: Качество треугольника

Идеальный треугольник - равносторонний (все стороны равны)
Плохой треугольник - очень вытянутый (почти линия)

Как измерить: Aspect Ratio (отношение сторон)
- Формула: (периметр) / (6 * √(площадь))
- Для равностороннего треугольника: 1.0
- Для вытянутого треугольника: > 5.0
- Чем ближе к 1, тем лучше качество
"""

def calculate_aspect_ratio(triangle):
    """
    Вычисляет качество треугольника (Aspect Ratio)
    
    Параметры:
    треугольник: массив из 3 точек, каждая точка = [x, y, z]
    
    Возвращает:
    float: Aspect Ratio (1 = идеально, >5 = плохо)
    """
    # Распаковываем вершины треугольника
    v1, v2, v3 = triangle
    
    # Вычисляем длины сторон (Евклидово расстояние)
    a = np.linalg.norm(v2 - v1)  # сторона между v1 и v2
    b = np.linalg.norm(v3 - v2)  # сторона между v2 и v3
    c = np.linalg.norm(v1 - v3)  # сторона между v3 и v1
    
    # Полупериметр
    s = (a + b + c) / 2
    
    # Площадь по формуле Герона
    площадь = np.sqrt(s * (s - a) * (s - b) * (s - c))
    
    # Aspect Ratio
    if surface > 1e-12:  # Защита от деления на ноль
        aspect_ratio = (a + b + c) / (6 * np.sqrt(surface))
        return aspect_ratio
    else:
        return float('inf')  # Вырожденный треугольник

# Вычисляем качество для всех треугольников
print("\nВычисление качества треугольников...")
start_analysis = time.time()

quality_triangle = []
for edge in edges:
    # Получаем координаты вершин треугольника
    triangle = peaks[edge]
    
    # Вычисляем качество
    quality = calculate_aspect_ratio(triangle)
    quality_triangle.append(quality)

time_analysis = time.time() - start_analysis
print(f"Анализ завершен за {time_analysis:.2f} секунд")

# Фильтруем бесконечные значения (вырожденные треугольники)
final_values = [q for q in quality_triangle if np.isfinite(q)]

# Статистика качества
print(f"\n=== СТАТИСТИКА КАЧЕСТВА ТРЕУГОЛЬНИКОВ ===")
print(f"Среднее качество: {np.mean(final_values):.3f}")
print(f"Медианное качество: {np.median(final_values):.3f}")
print(f"Лучшее качество (мин): {np.min(final_values):.3f}")
print(f"Худшее качество (макс): {np.max(final_values):.3f}")

# Количество плохих треугольников
bad = [q for q in final_values if q > 5]
print(f"Плохих треугольников (AR > 5): {len(bad)} ({len(bad)/len(final_values)*100:.1f}%)")

# Количество вырожденных треугольников
degeneration = [q for q in quality_triangle if not np.isfinite(q)]
if degeneration:
    print(f"ВНИМАНИЕ: Найдено {len(degeneration)} вырожденных треугольников (нулевая площадь)")

# ============================================================================
# ЧАСТЬ 6: ВИЗУАЛИЗАЦИЯ КАЧЕСТВА
# ============================================================================

print("\n" + "=" * 60)
print("ШАГ 5: ВИЗУАЛИЗАЦИЯ КАЧЕСТВА СЕТКИ")
print("=" * 60)

# Создаем графики для визуализации распределения качества
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# График 1: Гистограмма Aspect Ratio
ax1 = axes[0, 0]
ax1.hist(final_values, bins=50, color='blue', alpha=0.7, edgecolor='black')
ax1.axvline(x=1, color='green', linestyle='--', linewidth=2, label='Идеально (1)')
ax1.axvline(x=3, color='orange', linestyle='--', linewidth=2, label='Предел (3)')
ax1.axvline(x=5, color='red', linestyle='--', linewidth=2, label='Плохо (5)')
ax1.set_xlabel('Aspect Ratio (ближе к 1 = лучше)')
ax1.set_ylabel('Количество треугольников')
ax1.set_title('Распределение качества треугольников')
ax1.legend()
ax1.grid(True, alpha=0.3)

# График 2: Гистограмма с ограничением (только хорошие)
ax2 = axes[0, 1]
good = [q for q in final_values if q <= 3]
ax2.hist(good, bins=50, color='green', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Aspect Ratio')
ax2.set_ylabel('Количество треугольников')
ax2.set_title('Только хорошие треугольники (AR ≤ 3)')
ax2.grid(True, alpha=0.3)

# График 3: Ящик с усами (boxplot)
ax3 = axes[1, 0]
box_data = [final_values]
bp = ax3.boxplot(box_data, vert=True, patch_artist=True)
bp['boxes'][0].set_facecolor('lightblue')
ax3.set_ylabel('Aspect Ratio')
ax3.set_title('Статистическое распределение качества')
ax3.grid(True, alpha=0.3)

# График 4: Процентное соотношение
ax4 = axes[1, 1]
category = ['Хорошие (AR≤3)', 'Средние (3<AR≤5)', 'Плохие (AR>5)', 'Вырожденные']
good_percent = len([q for q in final_values if q <= 3]) / len(final_values) * 100
average_percent = len([q for q in final_values if 3 < q <= 5]) / len(final_values) * 100
bad__percent = len([q for q in final_values if q > 5]) / len(final_values) * 100
degeneration_percent = len(degeneration) / len(quality_triangle) * 100

percentage = [good_percent, average_percent, bad__percent, degeneration_percent]
color = ['green', 'yellow', 'red', 'gray']
ax4.pie(percentage, labels= category, colors=color, autopct='%1.1f%%', startangle=90)
ax4.set_title('Состав модели по качеству треугольников')

plt.suptitle('Анализ качества 3D сетки', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('results/quality_analysis.png', dpi=150)
print("✓ Графики качества сохранены в 'results/quality_analysis.png'")
#plt.show()  # Раскомментируйте, чтобы увидеть графики

# ============================================================================
# ЧАСТЬ 7: УПРОЩЕНИЕ МОДЕЛИ
# ============================================================================

print("\n" + "=" * 60)
print("ШАГ 6: УПРОЩЕНИЕ МОДЕЛИ")
print("=" * 60)

"""
ТЕОРИЯ: Методы упрощения

1. Quadric Decimation (рекомендуется):
   - Сохраняет форму лучше всего
   - Медленнее, но качественнее
   - Использует алгоритм "коллапса ребер"

2. Fast Simplification:
   - Быстрее, но менее качественно
   - Для очень больших моделей

Как выбрать коэффициент:
   коэффициент = 0.1  → оставить 10% треугольников
   коэффициент = 0.2  → оставить 20% треугольников
   коэффициент = 0.5  → оставить 50% треугольников
"""

# Рекомендации по выбору коэффициента
print("\n--- РЕКОМЕНДАЦИИ ПО ВЫБОРУ КОЭФФИЦИЕНТА ---")
print("Для 3D печати (качественная):     коэффициент = 0.2-0.3")
print("Для 3D печати (черновая):         коэффициент = 0.1-0.15")
print("Для быстрой визуализации:         коэффициент = 0.05-0.1")
print("Для веб-публикации:               коэффициент = 0.02-0.05")
print("Для максимального упрощения:      коэффициент = 0.01-0.02")

# Задаем коэффициент упрощения
# ИЗМЕНИТЕ ЭТО ЗНАЧЕНИЕ В ЗАВИСИМОСТИ ОТ ВАШЕЙ ЦЕЛИ
coeff = 0.1  # Оставить 10% треугольников

target_quantity_edges = int(quantity_edges * coeff)

print(f"\nВыбран коэффициент: {coeff}")
print(f"Целевое количество граней: {target_quantity_edges:,}")
print(f"Сокращение: {(1 - coeff) * 100:.0f}%")

# Выполняем упрощение
print("\nВыполнение упрощения...")
start_simplification = time.time()

try:
    # Метод 1: Quadric decimation (рекомендуемый)
    # Этот алгоритм сохраняет форму лучше всего
    #model_simplify = model.simplify_quadric_decimation(target_quantity_edges)
    
    # Альтернативный метод (если quadric не работает)
    model_simplify = модель.simplify(target_quantity_edges)
    
    time_simplification = time.time() - start_simplification
    print(f"✓ Упрощение завершено за {time_simplification:.2f} секунд")
    
except Exception as e:
    print(f"ОШИБКА при упрощении: {e}")
    print("\nПробуем альтернативный метод...")
    
    try:
        # Альтернативный метод (быстрее, но менее качественно)
        model_simplify = model.simplify(target_quantity_edges)
        time_simplification = time.time() - start_simplification
        print(f"✓ Упрощение (альтернативный метод) завершено за {time_simplification:.2f} секунд")
    except Exception as e2:
        print(f"ОШИБКА: Не удалось упростить модель. {e2}")
        sys.exit(1)

# Получаем характеристики упрощенной модели
new_peaks = model_simplify.vertices
new_edges = model_simplify.faces

new_quantity_peaks = len(new_peaks)
new_quantity_edges = len(new_edges)

print(f"\n=== РЕЗУЛЬТАТ УПРОЩЕНИЯ ===")
print(f"Исходно вершин: {quantity_peaks:,}")
print(f"Стало вершин:   {new_quantity_peaks:,}")
print(f"Сокращение вершин: {(1 - new_quantity_peaks/quantity_peaks)*100:.1f}%")
print(f"\nИсходно граней: {quantity_edges:,}")
print(f"Стало граней:   {new_quantity_edges:,}")
print(f"Сокращение граней: {(1 - new_quantity_edges/quantity_edges)*100:.1f}%")
#end

