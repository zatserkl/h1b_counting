from collections import defaultdict
import states


class FieldParser:
    """Finds in the header indices of fields of interest
    """
    def __init__(self, header, lines):
        self.lines = lines
        # assume that the first line is a header
        self.header = header

        # set the name for the line number for convenience
        self.header[0] = 'LINE'

        # indices of the fields of interest
        self.certified = None
        self.occupation = None
        self.state = None

    def find_field_certified(self):
        # # create a dictionary: index of list element vs field name
        # index_field = {}
        # for ind, field in enumerate(self.header):
        #     index_field[field] = ind

        certified_dict = defaultdict(int)
        for line in self.lines:
            for ifield, field in enumerate(line):
                if field.upper() == 'CERTIFIED':
                    certified_dict[ifield] += 1

        certified_list = sorted(certified_dict.items(),
                                key=lambda x: x[1], reverse=True)
        # print('certified_list:', certified_list,
        #       'certified_list[0][0] =', certified_list[0][0])
        self.certified = certified_list[0][0]

    def find_field_occupation(self):
        """Use common occupations to find this field
        """
        occupations = [
                'SOFTWARE DEVELOPERS, APPLICATIONS',
                'ACCOUNTANTS AND AUDITORS',
                'COMPUTER OCCUPATIONS, ALL OTHER',
                'COMPUTER SYSTEMS ANALYST',
                'DATABASE ADMINISTRATORS',
                'SOFTWARE DEVELOPERS, SYSTEM SOFTWARE',
                'COMPUTER PROGRAMMERS',
                'OPERATIONS RESEARCH ANALYSTS',
                'MANAGEMENT ANALYSTS',
                'ELECTRONICS ENGINEERS, EXCEPT COMPUTER',
                'FINANCIAL SPECIALISTS, ALL OTHERS',
                'OCCUPATIONS IN SYSTEMS ANALYSIS AND PROGRAMMING']

        # try to guess a field in the header first
        occupation_header = [
                             'SOC_NAME',                # 2017
                             'OCCUPATIONAL_TITLE',      # 2008
                             'LCA_CASE_SOC_NAME'        # 2010
        ]

        for ifield, field in enumerate(self.header):
            # print(ifield, '\t', field)
            if field.upper() in occupation_header:
                self.occupation = ifield
                print('occupation:', self.occupation)
                return

        # if we are here, we did not find the field in header
        # print('\nfind_field_occupation: look for popular occupations')

        # make sure that we know index of CERTIFIED field
        if self.certified is None:
            self.find_field_certified()

        occupation_dict = defaultdict(int)
        for line in self.lines:
            if line[self.certified].upper() != 'CERTIFIED':
                continue
            for ifield, field in enumerate(line):
                if field.replace('"', '').upper() in occupations:  # strip '"'
                    # print('-->', field)
                    occupation_dict[ifield] += 1

        occupation_list = sorted(occupation_dict.items(),
                                 key=lambda x: x[1], reverse=True)
        # print('occupation_list:', occupation_list,
        #       'occupation_list[0][0] =', occupation_list[0][0])
        self.occupation = occupation_list[0][0]

    def find_field_state(self):
        """We found from the data that the state of interest comes second.
        -- there are two states for 2014's, but we need the first one
        -- to skip attorney's state require the state in each line
        """
        # # create a dictionary: index of list element vs field name
        # index_field = {}
        # for ind, field in enumerate(self.header):
        #     index_field[field] = ind

        state_dict = defaultdict(int)
        for line in self.lines:
            if line[self.certified].upper() != 'CERTIFIED':
                continue
            for ifield, field in enumerate(line):
                if field.upper() in states.states:
                    state_dict[ifield] += 1

        state_list = sorted(state_dict.items(),
                            key=lambda x: x[1], reverse=True)

        # look for the second element
        # print('state_list:', state_list,
        #       'state_list[0][0] =', state_list[1][0])
        self.state = state_list[1][0]
