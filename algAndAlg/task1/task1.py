def nearest_two_power(n):
    two_in_power = 2
    power = 1
    while two_in_power <= n:
        two_in_power *= 2
        power += 1
    return power

n = int(input())
pow_two = nearest_two_power(n-1)
input_list = list(range(0, n))

l = []
output_list = []
for d in range(0, pow_two+1):
    out_break = 0
    for i in range(len(input_list)):
        try:
            y = input_list[i]
            z = input_list[i+ 2 ** d]
            print(f'GATE {n} OR {y} {z}')
            l.append([n, z])     
        
            if out_break < 2 ** d:
                output_list.append(n)        
                out_break += 1
            n += 1  
            

        except:
            continue

    for new, old in l:
        try:
            idx = input_list.index(old)
            input_list[idx] = new
        except:
            continue
    

print(f"OUTPUT 0 0")
for i, element in enumerate(output_list):
    print(f"OUTPUT {i+1} {element}")