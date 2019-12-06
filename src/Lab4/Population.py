from src.Lab4.Regulator import GeneticPIDRegulatorBody


class PopulationBody:
    """
    Класс популяции
    """

    def __init__(self, quantity=90):
        self.quantity = quantity
        self.pop_list = [0 for i in range(quantity)]

    def create_new_population(self):
        """
        создание новой популяции
        :return: будет возвращаться массив сгенерированных особей
        """

        self.pop_list = [GeneticPIDRegulatorBody() for i in range(len(self.pop_list))]

        for i in range(len(self.pop_list)):
            self.pop_list[i].set_random_regs()
            print(self.pop_list[i].show_regulator_coefficients())

    def sort_and_take_best(self, degrees):
        """
        сортирует особи в порядке убывания их оценок
        :param degrees:
        :return:
        """

        a = True
        while a:
            a = False
        for i in range(len(self.pop_list)):
            a = a or degrees[i] < degrees[i + 1]
            if degrees[i] < degrees[i + 1]:
                self.pop_list[i + 1], self.pop_list = self.pop_list[i], self.pop_list[i + 1]

        pass

    def pop_selection(self):
        """
        класс выполняет отбор лучших 30% особей
        :return: возвращает список лучших 30%
        """
        a = 0
        pass

    def pop_mutation(self):
        """
        класс выполняет мутацию 35% худших особей
        :return: мутировавшую популяцию
        """
        pass

    def pop_breeding(self):
        """
        класс выполняет скрещивание 35% особей средней оценки
        :return: новую дочернюю популяцию
        """
        pass
