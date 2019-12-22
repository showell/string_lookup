from timeit import default_timer as timer
from index import make_index, find

def print_index(index, prefix=''):
    if index.type == SMART:
        for letter, idx in index.indexes.items():
            print_index(idx, prefix+letter)

    print(prefix, index.end - index.start, index.vals[index.start])


def test_index(verifier, index):
    print('\nTEST:')

    # test correctness first
    for prefix, expected in verifier.items():
        actual = find(prefix, index)
        if actual != expected:
            print(prefix, expected)
            print('actual results', actual)
            raise Exception('find is broken')

    # next, get timing
    t = timer()
    for prefix, expected in verifier.items():
        actual = find(prefix, index)

    elapsed = timer() - t
    num_tests = len(verifier)
    print('# of vals', index.end - index.start)
    print('# of tests', num_tests)
    print('avg cost (microseconds)', elapsed * 1000000.0 / num_tests)


def get_test_data():
    names = [
        n.strip().lower() for
        n in open('names.txt').readlines()]
    return names

def get_test_prefixes(names):
    res = set()
    for name in names:
        res.add(name[:1])
        res.add(name[:2])
        res.add(name[:3])
    return sorted(list(res))

if __name__ == '__main__':
    names = get_test_data()
    prefixes = get_test_prefixes(names)

    print('build naive index')
    t = timer()
    naive_index = make_index(names)
    elapsed = timer() - t
    print('time to build (microseconds):', elapsed * 1000000)

    verifier = {}

    for prefix in prefixes:
        verifier[prefix] = find(prefix, naive_index)

    test_index(verifier, naive_index)

    print('\n\nbuild smart index')
    t = timer()
    smart_index = make_index(names, threshold=100)
    elapsed = timer() - t
    print('time to build (microseconds):', elapsed * 1000000)
    # print_index(smart_index)

    test_index(verifier, smart_index)
