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

