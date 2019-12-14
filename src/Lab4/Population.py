from numpy import random

from src.Lab4.Regulator import GeneticPIDRegulatorBody


class PopulationBody:
    """
    Класс популяции
    """

    def __init__(self, quantity=20):
        self.quantity = quantity
        self.pop_list = [GeneticPIDRegulatorBody() for i in range(quantity)]

    def set_pop_list(self, new_pop_list):
        """
        ввод нового готового списка популяции
        :param new_pop_list:
        :return:
        """
        self.pop_list = new_pop_list

    def create_new_population(self):
        """
        создание новой популяции
        :return: будет возвращаться массив сгенерированных особей
        """
        self.pop_list = [GeneticPIDRegulatorBody() for i in range(self.quantity)]
        for i in range(len(self.pop_list)):
            self.pop_list[i].set_random_regs()

    def sort_and_take_best(self, degree):
        """
        сортирует особи в порядке возрастания их оценок
        :param degree: лист с оценками
        :return: отсортированный лист и лучшая особь
        """

        # сортировка методом пузырька
        for i in range(len(self.pop_list) - 1):
            for j in range(len(self.pop_list) - i - 1):
                if degree[j] < degree[j + 1]:
                    self.pop_list[j + 1], self.pop_list[j] = self.pop_list[j], self.pop_list[j + 1]
                    degree[j], degree[j + 1] = degree[j + 1], degree[j]

        return self.pop_list[0], degree

    def pop_selection(self):
        """
        класс выполняет отбор лучших 30% особей
        :return: возвращает список лучших 30%
        """
        return self.pop_list[0:len(self.pop_list) // 3]

    def pop_mutation(self):
        """
        класс выполняет мутацию 35% худших особей
        :return: мутировавшую популяцию
        """

        mut_group = list(self.pop_list[
                         int(len(self.pop_list) // 2):len(self.pop_list)])

        for i in range(len(mut_group)):
            # А - список коэффициентов Кп, Кд и Ки для данного регулятора
            A = list(mut_group[i].get_regulator_coefficients())
            for j in range(3):
                A[random.randint(0, 2)] = random.uniform(0.01, 5)
            mut_group[i].set_regulator_coefficients(k=A[0], Td=A[1], Tu=A[2])

        return mut_group

    def pop_breeding(self):
        """
        класс выполняет скрещивание 35% особей средней оценки
        :return: новую дочернюю популяцию
        """
        breed_group = list(self.pop_list[
                           len(self.pop_list) // 3:int(len(self.pop_list) // 2)])

        for i in range(len(breed_group)):

            # из случайного регулятора популяции в список A_get записываются коэффициенты
            A_get = (breed_group[random.randint(0, len(breed_group))]
                     .get_regulator_coefficients())

            # А - список коэффициентов Кп, Кд и Ки для данного регулятора
            A = list(breed_group[i].get_regulator_coefficients())

            for j in range(len(A_get)):
                num = random.randint(0, 2)
                # перемешиваются случайным образом
                A[num] = A_get[num]

            breed_group[i].set_regulator_coefficients(k=A[0], Td=A[1], Tu=A[2])

        return breed_group
