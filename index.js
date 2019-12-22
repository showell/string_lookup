const NAIVE = 0;
const SMART = 1;

exports.make_index = function (vals) {
    const start = 0;
    const end = vals.length;
    const threshold = undefined;
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

    if (!threshold) {
        idx = { type: NAIVE};
        idx.vals = vals;
        idx.offset = offset;
        idx.start = start;
        idx.end = end;

        return idx;
    }

    throw Error('not implemented yet');
}

exports.find = function (prefix, index) {
    if (index.type == NAIVE) {
        let offset = index.offset;
        let end_offset = prefix.length;
        let vals = index.vals;
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
