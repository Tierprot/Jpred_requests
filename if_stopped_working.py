import os

config = open('config.txt').read()
exec (config)

names = os.listdir(os.path.join(os.getcwd(), download_dir))
names = [name.split('.tar')[0] for name in names]
seqs = {}

with open(inp, 'r') as base:
	line = base.readline().strip().split('>')[1]

with open(line + 'fasta', 'r') as fasta:
    name = ''
    for line in fasta:
        if '>' in line:
            if line.split('>')[1].strip() not in names:
                name = line.split('>')[1]
                name = name.strip()
            else:
                name = ''
        else:
            if name:
                seqs[name] = line.strip()
            else:
                pass

with open('not_done.fasta', 'w') as output:
    output.write('seqs = {}'.format(seqs.__repr__()))
