from timeit import default_timer as timer

NAIVE = 0
SMART = 1

class Index:
    pass


def make_index(vals, threshold=None):
    end = len(vals)

    return _build_index(
            vals,
            start=0,
            end=end,
            threshold=threshold,
            offset=0
            )

def _build_index(
        vals,
        start,
        end,
        threshold,
        offset
        ):

    if threshold is None or (end - start < threshold):
        idx = Index()
        idx.type = NAIVE
        idx.vals = vals
        idx.offset = offset
        idx.start = start
        idx.end = end
        return idx

    indexes = {}

    i = start
    while i < end:
        sub_start = i

        if offset >= len(vals[i]):
            i += 1
            continue

        letter = vals[i][offset]
        i += 1
        while i < end and vals[i][offset] == letter:
            i += 1
        sub_end = i

        idx = _build_index(
                vals,
                sub_start,
                sub_end,
                threshold,
                offset+1
                )

        indexes[letter] = idx

    '''
    for letter, idx in indexes.items():
        print(letter, idx.offset, names[idx.start:idx.end])
    '''

    smart_index = Index()
    smart_index.type = SMART
    smart_index.vals = vals
    smart_index.indexes = indexes
    smart_index.offset = offset
    smart_index.start = start
    smart_index.end = end

    return smart_index

def print_index(index, prefix=''):
    if index.type == SMART:
        for letter, idx in index.indexes.items():
            print_index(idx, prefix+letter)

    print(prefix, index.end - index.start, index.vals[index.start])


def find(prefix, index):
    if index.type == SMART:
        offset = index.offset

        if offset >= len(prefix):
            return index.vals[index.start:index.end]

        letter = prefix[offset]
        indexes = index.indexes
        if letter not in indexes:
            return []

        sub_index = indexes[letter]
        return find(prefix, sub_index)

    if index.type == NAIVE:
        offset = index.offset
        end_offset = len(prefix)
        vals = index.vals
        start = index.start
        end = index.end

        if offset >= end_offset:
            return vals[start:end]

        pref = prefix[offset:]

        i = start
        while i < index.end:
            if pref == vals[i][offset:end_offset]:
                break
            i += 1

        if i == index.end:
            return []


        j = i
        while j < index.end:
            if pref != vals[j][offset:end_offset]:
                break
            j += 1

        return vals[i:j]

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
