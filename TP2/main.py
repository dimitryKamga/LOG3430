from src.criteres import *


def print_cases(index, case):
    print(f"d{index + 1} = {case}")


if __name__ == "__main__":
    print('\033[92m' "RACC test suites ")
    racc_test_cases = racc()

    for i in range(len(racc_test_cases)):
        print_cases(i, racc_test_cases[i])
    print("\n")

    print("RICC test suites ")
    ricc_test_cases = ricc()

    for i in range(len(ricc_test_cases)):
        print_cases(i, ricc_test_cases[i])
    print("\n")

    print("VNS test suites ")
    vns_test_cases = vns()

    for i in range(len(vns_test_cases)):
        print_cases(i, vns_test_cases[i])
    print("\n")



