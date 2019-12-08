# def get_hight(list):
#     hills = 0
#     while True:
#         if max(y3) > 1.05 * last_y:
#             hills += 1
#             get_down(y3[max(y3):])
#         else: break
#     return hills
#
# def get_down(list):
#     if 0.95 * last_y > min(y3):
#         return get_hight(list[min(y3):])


# if actual < ideal:
#     return 5
# elif ideal < actual < 6 / 5 * ideal:
#     return 4
# elif 6 / 5 * ideal < actual < 7 / 5 * ideal:
#     return 3
# elif 7 / 5 * ideal < actual < 8 / 5 * ideal:
#     return 2
# elif 8 / 5 * ideal < actual < 9 / 5 * ideal:
#     return 1
# return 0


# mas = [0, 1, 1.2, 1.4, 1.6, 1.8, 2]
# for i in range(len(mas)-1):
#
#     if mas[i] * ideal < actual < mas[i + 1] * ideal:
#         return len(mas) - 2 - i
#     elif actual>mas[-1]*ideal:
#         return -1