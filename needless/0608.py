# k = 0
# list = [0, 1, 5, 8, 10]

# # 최댓값 구하기
# for i in range(len(list)):
#     if k < list[i]:
#         k = list[i]

# # 최솟값 구하기
# min_value = list[0]
# for i in range(len(list)):
#     if min_value > list[i]:
#         min_value = list[i]

# # 평균값 구하기
# sum_value = 0
# for i in range(len(list)):
#     sum_value += list[i]
# avg_value = sum_value / len(list)

# print(f"최댓값: {k}")
# print(f"최솟값: {min_value}")
# print(f"평균값: {avg_value:.2f}")

lst = [[1,2,3],[4,5,2],[7,3,2]]
for i in range(len(lst)):
    for j in range(len(lst[i])):
        if i%j == 0:
            lst[j][i] =2
print(lst)