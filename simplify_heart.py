import os          # Для работы с файлами и папками
import sys         # Для системных операций
import time        # Для измерения времени выполнения
from pathlib import Path  # Для удобной работы с путями файлов

# Научные библиотеки
import numpy as np  # Для работы с массивами и математикой

# Библиотеки для 3D
import trimesh      # Основная библиотека для работы с 3D-моделями

# Библиотеки для графики
import matplotlib.pyplot as plt  # Для создания графиков
from mpl_toolkits.mplot3d import Axes3D  # Для 3D-графиков

print("=" * 60)
print("     ПРОГРАММА УПРОЩЕНИЯ STL-МОДЕЛИ СЕРДЦА")
print("=" * 60)
print(f"Python версия: {sys.version}")
print(f"NumPy версия: {np.__version__}")
print(f"Trimesh версия: {trimesh.__version__}")
print("=" * 60)

# Создаем папку для результатов, если её нет
if not os.path.exists("results"):
    os.makedirs("results")
    print("✓ Создана папка 'results' для сохранения результатов")