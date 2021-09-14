def largestFactor(n):
    biggest = 1
    for i in range(1,n):
        if n % i == 0:
            biggest = i
    return biggest

if __name__ == '__main__':
    print(largestFactor(1))