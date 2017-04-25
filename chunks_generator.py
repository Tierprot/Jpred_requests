import os
import seq_generator


def mutations(name='name', body='MNOPASRTAUHNOPASRASRTAU', chunk_size=21, AA_voc=None, positions = []):
    if not AA_voc:
        AA_voc = ["G", "A", "V", "L", "I", "P", "F", "Y", "W", "S",
              "T", "C", "M", "N", "Q", "K", "R", "H", "D", "E"]
    else:
        pass

    seqs = {}

    # body if not positions
    if positions:
        for item in positions:
            if (item - (chunk_size // 2)) < 0:
                seqs.update({name + '_' + str(item + 1) + body[item] +
                             '_to_' + str(item + 1) + body[item]: body[0:chunk_size]})
                for stuff in AA_voc:
                    seqs.update({name + '_' + str(item + 1) + body[item] +
                                 '_to_' + str(item + 1) + stuff:
                                     body[0:item] + stuff + body[item + 1:chunk_size]})
            elif (item + (chunk_size // 2)) > len(body):
                for stuff in AA_voc:
                    seqs.update({name + '_' + str(item + 1) + body[item] +
                                 '_to_' + str(item + 1) + stuff:
                                     body[len(body) - chunk_size:item] + stuff + body[item + 1:]})
                seqs.update({name + '_' + str(item + 1) + body[item] +
                                 '_to_' + str(item + 1) + body[item]: body[len(body) - chunk_size:]})
            else:
                seqs.update({name + '_' + str(item + 1) + body[item] +
                             '_to_' + str(item + 1) + body[item]:
                                 body[item - chunk_size // 2:item + chunk_size // 2 + 1]})
                for aa in AA_voc:
                    seqs.update({name + '_' + str(item + 1) + body[item] +
                                 '_to_' + str(item + 1) + aa:
                                     body[item - chunk_size // 2:item] + aa + body[
                                                                              item + 1:item + chunk_size // 2 + 1]})
    else:
        for i in range(0, len(body) - chunk_size + 1):
            seqs.update({name + '_' + str(i + chunk_size // 2 + 1) + body[i + chunk_size // 2] +
                         '_to_' + str(i + chunk_size // 2 + 1) + body[i + chunk_size // 2]:
                             body[i:i + chunk_size]})
            for item in AA_voc:
                seqs.update({name + '_' + str(i + chunk_size // 2 + 1) + body[i + chunk_size // 2] +
                             '_to_' + str(i + chunk_size // 2 + 1) + item:
                                 body[i:i + chunk_size // 2] + item + body[(i + chunk_size // 2) + 1:i + chunk_size]})

        for i in range(len(body[0:chunk_size // 2])):
            seqs.update({name + '_' + str(i + 1) + body[i] +
                         '_to_' + str(i + 1) + body[i]: body[0:chunk_size]})
            for item in AA_voc:
                seqs.update({name + '_' + str(i + 1) + body[i] +
                             '_to_' + str(i + 1) + item:
                                 body[0:i] + item + body[i + 1:chunk_size]})

        for i in range(len(body) - chunk_size // 2, len(body)):
            seqs.update({name + '_' + str(i + 1) + body[i] +
                         '_to_' + str(i + 1) + body[i]: body[len(body) - chunk_size:]})
            for item in AA_voc:
                seqs.update({name + '_' + str(i + 1) + body[i] +
                             '_to_' + str(i + 1) + item:
                                 body[len(body) - chunk_size:i] + item + body[i + 1:]})
    return seqs


if __name__ == "__main__":

    config = open('config.txt').read()
    exec(config)

    with open(inp, 'r') as base:
        prefix = base.readline().strip().split('>')[1]
        body = []
        for line in base:
            if line:
                body.append(line.strip())
        body = ''.join(body)

    seqs = mutations(name=prefix, body=body, chunk_size=chunks, AA_voc=vocabulary, positions=positions)
    with open(prefix + '.fasta', 'w') as output:
        for name, seq in sorted(seqs.items(), key=lambda x: int(x[0].split('_')[1][:-1])
        if not 'peptide' in x[0]
        else len(seqs) + 1):
            print('>' + name)
            print(seq)
            output.write('>' + name + '\n')
            output.write(seq + '\n')
