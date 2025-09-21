# NYPC 3번
# N, K = map(int, input().split(' '))

# value = 0
# for i in range(K):
#     k = i + 1
#     value = value + (N-k)*k

# print(value + K)



# NYPC 4번
# N, M = map(int, input().split(' '))
# A = list(map(int, input().split(' ')))
# A.sort()

# S = 0
# for i in range(0,len(A),2):
#     a = A[i]
#     b = A[i+1]
#     if a > b:
#         P = (a+b) - (a-b)
#         m = b
#     else:
#         P = (a+b) - (b-a)
#         m = a
#     C = m//M
#     S = S + P*C
# print(S)

N = int(input())
lst = list(map(int, input().split(' ')))

(lst[0] - 1)
for i in range((lst[0]-1),N):
    print(i)