from typing import ClassVar, List
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    message: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    training_type: str  # имя класса тренировки
    duration: float  # длительность тренировки в часах
    distance: float  # дистанция в киллометрах
    speed: float  # средняя скорость
    calories: float  # количество килокалорий

    def get_message(self):
        """Создание информационного сообщения о тренировке."""

        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # расстояние преодолеваемое за один шаг
    M_IN_KM: float = 1000  # константа перевода значений из метров в километры

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Вычисление дистанции в км."""

        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Вычисление средней скорости"""

        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info = InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    Coeff_calorie_1 = 18  # Вынос неименованных значений в переменные
    Coeff_calorie_2 = 20  # Вынос неименованных значений в переменные
    M_IN_HR = 60  # Вынос неименованных значений в переменные

    def get_spent_calories(self) -> float:
        """Вычисление затраченных калорий"""

        M_IN_HR = 60  # Вынос неименованных значений в переменные
        return ((self.Coeff_calorie_1 * self.get_mean_speed()
                - self.Coeff_calorie_2)
                * self.weight_kg
                / super().M_IN_KM
                * self.duration_h
                * M_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # в классе переопределен метод get_spent_calories добавлен атрибут height
    Coeff_calorie_3: float = 0.035  # Вынос неименованных значений в переменные
    Coeff_calorie_4: float = 0.029  # Вынос неименованных значений в переменные
    M_IN_HR: int = 60  # Вынос неименованных значений в переменные

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        """Вычисление количества калорий"""

        return ((self.Coeff_calorie_3
                * self.weight_kg
                + (self.get_mean_speed()**2 // self.height_cm)
                * self.Coeff_calorie_4
                * self.weight_kg)
                * (self.duration_h * self.M_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""

    # в классе переопределены методы get_spent_calories() и get_mean_speed()
    # добавлены атрибуты length_pool,count_pool
    LEN_STEP: float = 1.38  # расстояние преодолеваемое за один гребок
    M_IN_KM: float = 1000  # константа перевода значений из метров в километры
    Сoeff_calorie_5: float = 1.1
    # Вынос неименованных значений в переменные
    Сoeff_calorie_6: int = 2
    # Вынос неименованных значений в переменные

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool  # длина бассейна в метрах
        self.count_pool_qn = count_pool
        # сколько раз пользователь переплыл бассейн

    def get_distance(self) -> float:
        """Вычисление дистанции"""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Вычисление средней скорости"""

        return (self.length_pool_m
                * self.count_pool_qn
                / self.M_IN_KM
                / self.duration_h)

    def get_spent_calories(self) -> float:
        """Вычисление калорий"""

        return ((self.get_mean_speed() + self.Сoeff_calorie_5)
                * self.Сoeff_calorie_6
                * self.weight_kg)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout: dict[str, list[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout:
        raise NotImplementedError
    else:
        return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    # подготовленные тестовые данные для проверки фитнес-трекера"""

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
