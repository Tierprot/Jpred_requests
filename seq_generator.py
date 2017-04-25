__author__ = 'Tierprot'


class MutGen():
    AA_voc = ["G", "A", "V", "L", "I", "P", "F", "Y", "W", "S",
              "T", "C", "M", "N", "Q", "K", "R", "H", "D", "E"]

    def __init__(self, input_file, positions=None, vocabulary=None, chunkSize=None):
        try:
            main_name, main_sequence = MutGen.load_seq(input_file)
            self.main_name = main_name
            self.sequences = {main_name: main_sequence}
        except Exception as exp:
            print(exp)

        # if one needs a collection of peptides which have a mutation instead of whole protein
        # chunkSize - size of such peptides
        self.chunkSize = chunkSize

        # restricting AA mutation variations
        if vocabulary:
            self.AA_voc = vocabulary
        # restriction of positions to mutate
        if positions:
            self.positions = positions

        else:
            main_name = ''.join(list(self.sequences.keys()))
            self.positions = list(range(len(self.sequences[main_name])))

    @staticmethod
    def load_seq(input_file):
        # loading of a base sequence
        name, sequence = '', ''
        with open(input_file, 'r') as base:
            for line in base:
                if '>' in line:
                    name = line.strip()
                    name = name[1:]
                else:
                    sequence += line.strip()
        return name, sequence


    def gen_mut(self):
        # generation of provided mutations
        if self.chunkSize:
            pass
        else:
            try:
                for position in self.positions:
                    for mutation in self.AA_voc:
                        if mutation != self.sequences[self.main_name][position]:
                            name = self.main_name + '_' + str(position) + self.sequences[self.main_name][position] \
                                    + '_to_' + str(position) + mutation
                            seq = self.sequences[self.main_name]
                            seq = seq[:position] + mutation + seq[position+1:]
                            self.sequences.update({name: seq})
            except Exception as exp:
                print(exp)

    def get_titles(self):
        try:
            return list(self.sequences.keys())
        except Exception:
            print("Object is empty")
            return None

    def get_sequence(self, key):
        try:
            return self.sequences[key]
        except Exception:
            print("No record with key {} was found!".format(key))

    def save_fasta(self):
        # saving sequences to a file in a fasta format
        sorted_seqs = sorted(self.sequences.items())
        with open(self.main_name + '.fasta', "w") as output:
            for record, sequence in sorted_seqs:
                output.write('>' + record + '\n')
                output.write(sequence + '\n')