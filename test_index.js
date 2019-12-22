let assert = require('assert')
let fs = require('fs')
let index = require('./index');


function get_test_data() {
    let payload = fs.readFileSync('names.txt', 'utf-8');
    names = payload.split(/\n/);
    names = names.map(function (n) {
        return n.toLowerCase();
    });
    return names;
}

function get_test_prefixes(names) {
    let res = new Set();

    names.forEach(function (name) {
        res.add(name.slice(0, 1));
        res.add(name.slice(0, 2));
        res.add(name.slice(0, 3));
    });

    let lst = Array.from(res);
    lst.sort();

    return lst;
}

function sanity_check() {
    let results = index.find('beth', idx);
    assert.deepEqual(results,
        [ 'beth', 'bethanne', 'bethany', 'bethena', 'bethina' ]
    );
}

function get_time(f) {
    let t1 = process.hrtime.bigint();
    f();
    let t2 = process.hrtime.bigint();
    let elapsed = Number(t2 - t1) / 1000.0;
    return elapsed;
}

function test_index(verifier, idx) {
    console.info('Testing...');

    let cnt = Object.keys(verifier).length;

    let elapsed = get_time(function() {
        Object.keys(verifier).forEach(function (prefix) {
            let expected = verifier[prefix];
            let actual = index.find(prefix, idx);
            assert.deepEqual(expected, actual);
        });
    });

    console.info('num tests', cnt);
    console.info('time per row', elapsed / cnt);
}


function main() {
    let names = get_test_data();
    let prefixes = get_test_prefixes(names);

    let naive_index;

    let elapsed = get_time(function () {
        naive_index = index.make_index(names);
    });
    console.info('build naive', elapsed);

    sanity_check(idx);

    verifier = {}

    prefixes.forEach(function (prefix) {
        verifier[prefix] = index.find(prefix, naive_index);
    });

    test_index(verifier, naive_index);
}

main();
