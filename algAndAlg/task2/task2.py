# n = int(input())
# from random import randrange

# n = 1

# def randbinary(n, force_leading_one=False):
#     r = randrange(0, 2**n) | (2**n)
#     r = list(map(int, bin(r)[3:]))
#     if force_leading_one:
#         r[-1] = 1
#     return r

# print(randbinary(n))

#### Более менее рабочий
# n = int(input())
# input_list = list(range(0, 3*n))

# list_of_list = []
# for i in range(0,len(input_list),3):
#     list_of_list.append(input_list[i:i+3])


# out_idx = list(range(2*(n+1)))
# first_line = (out_idx[2*(n+1)//2-1])
# second_line = (out_idx[2*(n+1)//2])
# out_idx = out_idx[:2*(n+1)//2-1] + out_idx[2*(n+1)//2+1 :]

# count = list_of_list[-1][-1] + 1
# for j, (a, b, c) in enumerate(list_of_list):

#     print(f"GATE {count} AND {a} {b}")  # 1
#     bet_4 = count
#     count += 1 
#     print(f"GATE {count} AND {a} {c}") # 2
#     bet_5 = count
#     count += 1 
#     print(f"GATE {count} AND {b} {c}") # 3
#     bet_6 = count
#     count += 1 
#     # bet_5 = count
#     print(f"GATE {count} OR {bet_4} {bet_5}") 
#     bet_7 = count
#     count += 1 
#     print(f"GATE {count} OR {bet_7} {bet_6}") 
#     P = count
#     count += 1 

#     print(f"GATE {count} OR {a} {b}") 
#     s_bet_8 = count
#     count += 1
#     print(f"GATE {count} OR {s_bet_8} {c}") 
#     s_bet_9 = count
#     count += 1
#     print(f"GATE {count} OR {bet_4} {c}") 
#     s_bet_10 = count
#     count += 1
#     print(f"GATE {count} OR {s_bet_9} {s_bet_10}") 
#     s_bet_11 = count
#     count += 1
#     print(f"GATE {count} NOT {P}") 
#     s_bet_not = count
#     count += 1
#     print(f"GATE {count} AND {s_bet_not} {s_bet_11}") 
#     S = count
#     count += 1

#     o1 = f"OUTPUT {out_idx.pop(0)} {P}"
#     o2 = f"OUTPUT {out_idx.pop(0)} {S}"
#     print(o1)
#     print(o2)
    

#     if j == len(list_of_list)-1:
#         print(f"GATE {count} AND {P} {s_bet_not}")
#         zero = count


# print(f"OUTPUT {first_line} {zero}")
# print(f"OUTPUT {second_line} {zero}")


# print(f"OUTPUT {first_line} {zero}")
# print(f"OUTPUT {second_line} {zero}")


n = int(input())
input_list = list(range(0, 3*n))

list_of_list = []
for i in range(0,len(input_list),3):
    list_of_list.append(input_list[i:i+3])


out_idx = list(range(2*(n+1)))
first_line = (out_idx[2*(n+1)//2-1])
second_line = (out_idx[2*(n+1)//2])

out_idx = out_idx[:2*(n+1)//2-1] + out_idx[2*(n+1)//2+1 :]

count = list_of_list[-1][-1] + 1
# count = input_list[-1]

outputs = []
for j, (a, b, c) in enumerate(list_of_list):

    print(f"GATE {count} AND {a} {b}") 
    one = count ## 3
    count = count+1
    print(f"GATE {count} OR {a} {b}") 
    two = count ## 4
    count = count+1
    print(f"GATE {count} NOT {one}") 
    three = count ## 5
    count = count+1
    print(f"GATE {count} AND {three} {two}") 
    four = count ## 6
    count = count+1
    print(f"GATE {count} AND {four} {c}") 
    seven = count ## 7
    count = count+1
    print(f"GATE {count} OR {four} {c}") 
    eigth = count ## 8
    count = count+1
    print(f"GATE {count} NOT {seven}") 
    nine = count ## 9
    count = count+1
    print(f"GATE {count} AND {nine} {eigth}") 
    ten = count ##10 ### E = xor(t, c)

    count = count+1
    print(f"GATE {count} OR {one} {seven}") 
    eleven = count ##11
    count = count+1
    print(f"GATE {count} NOT {a}") 
    twelve = count ##12
    count = count+1
    print(f"GATE {count} AND {twelve} {a}") 
    thirdth = count ##13 ZERO
    count = count+1
    print(f"GATE {count} AND {four} {c}") 
    eleven = count ##11
    count = count+1
    print(f"GATE {count} OR {one} {eleven}") 
    twelve = count ##12
    count = count+1


    outputs.append([(out_idx[j], ten), (out_idx[j+1], twelve)])


for x in outputs:
    for i, j in x:
        print(f"OUTPUT {i} {j}")

print(f"OUTPUT {first_line} {thirdth}")
print(f"OUTPUT {second_line} {thirdth}")

# print(f"OUTPUT {first_line} {zero}")
# print(f"OUTPUT {second_line} {zero}")


    
    