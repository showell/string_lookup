const NAIVE = 0;
const SMART = 1;

exports.make_index = function (vals, threshold) {
    const start = 0;
    const end = vals.length;
    const offset = 0;

    return _build_index(
        vals,
        start,
        end,
        threshold,
        offset
    );
    return;
}

function _build_index(
    vals,
    start,
    end,
    threshold,
    offset) {

    if (!threshold || (end - start < threshold)) {
        idx = { type: NAIVE};
        idx.vals = vals;
        idx.offset = offset;
        idx.start = start;
        idx.end = end;

        return idx;
    }

    let indexes = {};

    let i = start;
    while (i < end) {
        let sub_start = i;

        if (offset >= vals[i].length) {
            i += 1
            continue
        }

        let letter = vals[i][offset];
        i += 1;
        while ((i < end) && (vals[i][offset] == letter)) {
            i += 1;
        }

        let sub_end = i;

        let idx = _build_index(
                vals,
                sub_start,
                sub_end,
                threshold,
                offset+1
                );

        indexes[letter] = idx
    }

    smart_index = { type: SMART };
    smart_index.vals = vals;
    smart_index.indexes = indexes;
    smart_index.offset = offset;
    smart_index.start = start;
    smart_index.end = end;

    return smart_index;
}

exports.find = function (prefix, index) {
    let offset = index.offset;
    let vals = index.vals;

    if (index.type == SMART) {
        if (offset >= prefix.length) {
            return vals.slice(index.start, index.end);
        }

        let letter = prefix[offset];
        let indexes = index.indexes;
        if (!indexes[letter]) {
            return [];
        }

        let sub_index = indexes[letter];
        return exports.find(prefix, sub_index)
    }

    if (index.type == NAIVE) {
        let end_offset = prefix.length;
        let start = index.start;
        let end = index.end;

        if (offset >= end_offset) {
            return vals.slice(start, end);
        }

        let pref = prefix.slice(offset);

        let i = start;
        while (i < end) {
            if (pref == vals[i].slice(offset, end_offset)) {
                break;
            }
            i += 1;
        }

        if (i == index.end) {
            return [];
        }

        let j = i;
        while (j < index.end) {
            if (pref != vals[j].slice(offset, end_offset)) {
                break;
            }
            j += 1;
        }

        return vals.slice(i, j);
    }


    throw Error('unexpected');
};

return exports;
