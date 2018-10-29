from collections import defaultdict
import sys


def input_line(fname_input):
    """Yields line-by-line to avoid read the whole file into the memory.
    Input:  input filename
    Output: list of fields
    """
    with open(fname_input) as ifile:
        for line in ifile:
            yield line.strip().split(';')


if __name__ == '__main__':
    print('len(sys.argv) =', len(sys.argv))
    for iarg, item in enumerate(sys.argv):
        print(iarg, item)

if len(sys.argv) >= 4:
    fname_input = sys.argv[1]
    fname_occupations = sys.argv[2]
    fname_states = sys.argv[3]

# print('fname_input:', fname_input,
#       'fname_occupations:', fname_occupations,
#       'fname_states:', fname_states)

try:
    lines_gen = input_line(fname_input)  # creates a line generator
except FileNotFoundError as e:
    print(e)
    exit()

header = next(lines_gen)

# set the name for the line number for convenience
header[0] = 'LINE'

# create a dictionary: index of list element vs field name
index_field = {}
for ind, field in enumerate(header):
    index_field[field] = ind

# print(index_field)  # can be different for different years

# string constants: fields of interest
case_status_key = 'CASE_STATUS'
case_status_certified = 'CERTIFIED'
occupation_key = 'SOC_NAME'
worksite_state_key = 'WORKSITE_STATE'

# output dictionaries
dict_job_title = defaultdict(int)
dict_occupation = defaultdict(int)
dict_worksite_state = defaultdict(int)

for line in lines_gen:
    if int(line[index_field['LINE']]) == 0:
        print(line)
        print('len(data_line) =', len(line))
        for i in range(len(line)):
            print('{0:30s} {1}'.format(header[i], line[i]))

    case_status = line[index_field[case_status_key]]
    occupation = line[index_field[occupation_key]].replace('"', '')
    worksite_state = line[index_field[worksite_state_key]]

    # print(case_status_key, case_status)
    # print(occupation_key, occupation)
    # print(worksite_state_key, worksite_state)

    if case_status == case_status_certified:
        dict_occupation[occupation] += 1
        dict_worksite_state[worksite_state] += 1

# print(dict_occupation)
# print(dict_worksite_state)

# total certified applications
total_certified = sum(dict_occupation.values())

# sort by the name first
occupation_pairs = sorted(dict_occupation.items(),
                          key=lambda x: x[0])
# then sort by the number: the name sorting is stable
occupation_pairs.sort(key=lambda x: x[1], reverse=True)

# Sort in one pass. The minus sign produce reverse order.
# occupation_pairs = sorted(dict_occupation.items(),
#                           key=lambda x: (-x[1], x[0]))

# print('occupation_pairs:\n', occupation_pairs)

# sort by the name first
state_pairs = sorted(dict_worksite_state.items(),
                     key=lambda x: x[0])
# then sort by the number: the name sorting is stable
state_pairs.sort(key=lambda x: x[1], reverse=True)

# Sort in one pass. The minus sign produce reverse order.
# state_pairs = sorted(dict_worksite_state.items(),
#                      key=lambda x: (-x[1], x[0]))

# write output files

with open(fname_occupations, 'w') as ofile_occupations:
    ofile_occupations.write(
        'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    n_top = 0
    for occupation, number in occupation_pairs:
        if n_top < 10:
            n_top += 1
            print('{0};{1};{2:.1f}%'.format(
                occupation, number, 100 * number / total_certified))
            ofile_occupations.write('{0};{1};{2:.1f}%\n'.format(
                occupation, number, 100 * number / total_certified))

with open(fname_states, 'w') as ofile_states:
    ofile_states.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    n_top = 0
    for state, number in state_pairs:
        if n_top < 10:
            n_top += 1
            print('{0};{1};{2:.1f}%'.format(
                state, number, 100 * number / total_certified))
            ofile_states.write('{0};{1};{2:.1f}%\n'.format(
                state, number, 100 * number / total_certified))
