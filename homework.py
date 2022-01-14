from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Создание информационного сообщения о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # расстояние преодолеваемое за один шаг
    M_IN_KM: float = 1000  # константа перевода значений из метров в километры
    M_IN_HR = 60  # константа перевода значений из минут в часы

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Вычисление средней скорости"""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод еще не реализован.')

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

    COEFF_CALORIE_1 = 18  # Вынос неименованных значений в переменные
    COEFF_CALORIE_2 = 20  # Вынос неименованных значений в переменные

    def get_spent_calories(self) -> float:
        """Вычисление затраченных калорий"""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight_kg
                / super().M_IN_KM
                * self.duration_h
                * self.M_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # в классе переопределен метод get_spent_calories добавлен атрибут height
    COEFF_CALORIE_3: float = 0.035  # Вынос неименованных значений в переменные
    COEFF_CALORIE_4: float = 0.029  # Вынос неименованных значений в переменные

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
        return ((self.COEFF_CALORIE_3
                * self.weight_kg
                + (self.get_mean_speed()**2 // self.height_cm)
                * self.COEFF_CALORIE_4
                * self.weight_kg)
                * (self.duration_h * self.M_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""

    # в классе переопределены методы get_spent_calories() и get_mean_speed()
    # добавлены атрибуты length_pool,count_pool
    LEN_STEP: float = 1.38  # расстояние преодолеваемое за один гребок
    COEFF_CALORIE_5: float = 1.1
    # Вынос неименованных значений в переменные
    COEFF_CALORIE_6: int = 2
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
        self.length_pool_m = length_pool
        self.count_pool_qn = count_pool

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
        return ((self.get_mean_speed() + self.COEFF_CALORIE_5)
                * self.COEFF_CALORIE_6
                * self.weight_kg)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout:
        raise ValueError('Тренировка отсутствует')
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """ подготовленные тестовые данные для проверки фитнес-трекера"""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
