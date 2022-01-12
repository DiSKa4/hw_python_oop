class InfoMessage:

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float
    ) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        info = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        minute = 60
        spent_calories = ((coeff_calorie_1 * super().get_mean_speed()
                          - coeff_calorie_2) * self.weight / super().M_IN_KM
                                             * self.duration * minute)
        return spent_calories


class SportsWalking(Training):
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029
    minute: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = (self.coeff_calorie_3 * self.weight
                    + (super().get_mean_speed()**2 // self.height)
                    * self.coeff_calorie_4 * self.weight) * (self.duration
                                                             * self.minute)
        return calories


class Swimming(Training):
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_5: float = 1.1
        coeff_calorie_6: int = 2
        spent_calories = ((self.get_mean_speed() + coeff_calorie_5)
                          * coeff_calorie_6 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
