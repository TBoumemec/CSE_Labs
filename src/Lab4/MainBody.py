from src.Lab4.Population import PopulationBody

"""
Главное тело программы
"""


def genetic_method():
    """
    Генетический способ подбора параметров регулятора
    """

    def target_function(population):
        """
        здесь будет происходить оценка каждой особи
        :param population: популяция особей
        :return: лист оценок
        """

        pass

    # создание популяции
    group = PopulationBody()
    group.create_new_population()

    # оценка особей популяции
    grades = target_function(group)

    best_of_the_best = []

    # сортировка и отбор лучшей особи
    group, best_person = group.sort_and_take_best(grades)
    best_of_the_best.append(best_person)

    while min(grades) > 0.1:

        # процесс селекции, мутации и скрещивания
        group.set_pop_list(group.pop_selection()
                 + group.pop_mutation() + group.pop_breeding())

        grades = target_function(group)

        group, best_person = group.sort_and_take_best(grades)
        best_of_the_best.append(best_person)

        if len(best_of_the_best) >= 50:  # неудачный вид
            group.create_new_population()

def ZN_Method():
    """
    Метод подбора параметров регулятора Зиглера-Николса
    :return:
    """
    pass



genetic_method()
ZN_Method()
