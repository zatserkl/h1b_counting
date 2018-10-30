from FieldParser import FieldParser
from collections import defaultdict
import sys


def input_line(fname_input):
    """Yields line-by-line to avoid read the whole file into the memory.
    Input:  input filename
    Output: list of fields
    """
    try:
        with open(fname_input) as ifile:
            for line in ifile:
                yield line.upper().strip().split(';')
    except FileNotFoundError:
        raise FileNotFoundError


if __name__ == '__main__':

    if len(sys.argv) >= 4:
        fname_input = sys.argv[1]
        fname_occupations = sys.argv[2]
        fname_states = sys.argv[3]

    # read a chunk of lines for heuristic parse to find fields of interest

    lines_gen = input_line(fname_input)

    try:
        header = next(lines_gen)
    except FileNotFoundError:
        print('File not found:', fname_input)
        exit()

    n_lines_parse = 1000        # the number of lines for heuristic parse
    lines = []
    for iline in range(n_lines_parse):
        try:
            line = next(lines_gen)
        except StopIteration:
            break
        lines.append(line)

    # analyse the fields
    field_parser = FieldParser(header, lines)
    field_parser.find_field_certified()
    field_parser.find_field_occupation()
    field_parser.find_field_state()

    lines_gen.close()   # to start it over for the processing

    # process the file from the beginning

    try:
        lines_gen = input_line(fname_input)  # creates a line generator
    except FileNotFoundError as e:
        print('Exception the second time')
        exit()

    header = next(lines_gen)

    # set the name for the line number for convenience
    header[0] = 'LINE'

    # string constants
    case_status_certified = 'CERTIFIED'

    # output dictionaries
    dict_job_title = defaultdict(int)
    dict_occupation = defaultdict(int)
    dict_worksite_state = defaultdict(int)

    for line in lines_gen:
        case_status = line[field_parser.certified]
        occupation = line[field_parser.occupation].replace('"', '')
        worksite_state = line[field_parser.state]

        if case_status == case_status_certified:
            dict_occupation[occupation] += 1
            dict_worksite_state[worksite_state] += 1

    # total certified applications
    total_certified = sum(dict_occupation.values())

    # sort by the name first
    occupation_pairs = sorted(dict_occupation.items(),
                              key=lambda x: x[0])
    # then sort by the number: the name sorting is stable
    occupation_pairs.sort(key=lambda x: x[1], reverse=True)

    # sort by the name first
    state_pairs = sorted(dict_worksite_state.items(),
                         key=lambda x: x[0])
    # then sort by the number: the name sorting is stable
    state_pairs.sort(key=lambda x: x[1], reverse=True)

    # write output files

    with open(fname_occupations, 'w') as ofile_occupations:
        ofile_occupations.write(
            'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        n_top = 0
        for occupation, number in occupation_pairs:
            if n_top < 10:
                n_top += 1
                ofile_occupations.write('{0};{1};{2:.1f}%\n'.format(
                    occupation.upper(), number, 100 * number / total_certified)
                    )

    with open(fname_states, 'w') as ofile_states:
        ofile_states.write(
            'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        n_top = 0
        for state, number in state_pairs:
            if n_top < 10:
                n_top += 1
                ofile_states.write('{0};{1};{2:.1f}%\n'.format(
                    state, number, 100 * number / total_certified))
