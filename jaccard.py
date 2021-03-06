import csv,sys
import itertools as I

FUZZERS = {}

def jaccard_index(Fa, Fb):
    ALL_A = [m for prog in FUZZERS[Fa] for m in FUZZERS[Fa][prog]]
    ALL_B = [m for prog in FUZZERS[Fb] for m in FUZZERS[Fb][prog]]

    intersection = [m for m in ALL_A if m in ALL_B]
    union = list(set(ALL_A + ALL_B))
    return len(intersection) / len(union)


def jaccard_distance(Fa, Fb):
    return 1 - jaccard_index(Fa, Fb)


def jaccard_index_p(Fa, Fb, prog):
    ALL_A = [m for m in FUZZERS[Fa][prog]]
    ALL_B = [m for m in FUZZERS[Fb][prog]]

    intersection = [m for m in ALL_A if m in ALL_B]
    union = list(set(ALL_A + ALL_B))
    return len(intersection) / len(union)


def jaccard_distance_p(Fa, Fb, prog):
    return 1 - jaccard_index_p(Fa, Fb, prog)



# exec_id,prog,mut_id,run_ctr,fuzzer,mut_type,covered_file_seen,covered_by_seed,time_found,found_by_seed,
# total_time,confirmed,seed_timeout,crashed,stage
def load_mutants(fname):
    my_data = []
    with open(fname) as f:
        lines = csv.DictReader(f)
        for line in lines:
            assert line['found_by_seed'] == '0', line['found_by_seed']
            fuzzer = line['fuzzer']
            prog = line['prog']
            found_by_seed = line['found_by_seed']
            if found_by_seed == '1': continue
            time_found = line['time_found']
            confirmed = line['confirmed']
            if confirmed != '1': continue
            if fuzzer not in FUZZERS: FUZZERS[fuzzer] = {}
            if prog not in FUZZERS[fuzzer]: FUZZERS[fuzzer][prog] = []
            FUZZERS[fuzzer][prog].append('%s:%s' % (line['prog'], line['mut_id']))
            my_data.append(line)
    return my_data

data_file = sys.argv[1]

data = load_mutants(data_file)
print('Mutants Killed', len(data))

fuzzers = list(FUZZERS.keys())
#print(fuzzers)

print('Jaccard Distane (dissimilarity)')
#for a,b in I.combinations(fuzzers, 2):
#    distance = jaccard_distance(a,b)
#    print( a, b, ':', round(distance, 2))

for prog in FUZZERS[fuzzers[0]]:
    print(prog)
    for fA in fuzzers:
        total = 0
        for fB in fuzzers:
            if fA == fB: continue
            distance = jaccard_distance_p(fA,fB, prog)
            total += distance
            print( fA, fB, ':', round(distance, 2))
        print(round(total/(len(fuzzers)-1), 2))
    print()
