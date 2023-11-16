import concurrent.futures

import time


def factorize(*numbers):
    divisors_list = []
    for number in numbers:
        start = time.time()
        divisors = []
        for i in range(1, number + 1):
            if number % i == 0:
                divisors.append(i)
        divisors_list.append(divisors)
        finish = time.time()
        print(finish - start)
    return list(divisors_list)


numbers = [128, 255, 99999, 10651060]
if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        for number in zip(numbers, executor.map(factorize, numbers)):
            print(number)
