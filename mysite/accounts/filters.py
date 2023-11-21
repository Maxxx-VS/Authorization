from PIL import Image
from accounts.views import DarkFilter, BrightFilter, RedFilter, GreenFilter, BlueFilter, Drugs_eye, apply_filter
import os

def main():
    filter_names = [
        "Уменьшить яркость",
        "Увеличить яркость",
        "Красный фильтр",
        "Зеленый фильтр",
        "Синий фильтр",
        "Наркоманские глаза",
    ]

    filters = [
        DarkFilter,
        BrightFilter,
        RedFilter,
        GreenFilter,
        BlueFilter,
        Drugs_eye,
    ]

    print("Добро пожаловать")

    is_finished = False
    while not is_finished:
        path = input("Введите путь к файлу >>> ")

        while not os.path.exists(path):
            path = input("Файл не найден. Попробуйте еще раз >>> ")

        img = Image.open(path).convert('RGB')

        print("Какой фильтр хотите применить >>> ?")

        for i in range(len(filter_names)):
            print(f'{i} - {filter_names[i]}')

        choice = input("Выберите фильтр (введите номер): >>> ")

        while not choice.isdigit() or int(choice) >= len(filters):
            choice = input("Некорректный ввод. Попробуйте еще раз >>> ")

        filt = filters[int(choice)]
        img = apply_filter(img, filt)

        img.show()
        answer = input("Еще раз? (да/нет): ")

        while answer != 'да' and answer != 'нет':
            answer = input("Некорректный ввод. Попробуйте еще раз >>> ")

        is_finished = answer == 'нет'

if __name__ == "__main__":
    main()