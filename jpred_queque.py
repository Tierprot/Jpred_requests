from http_requests import seq_fetcher
from collections import deque
from seq_generator import MutGen
from tar_gz import JpredArchive
import time
import re


#TODO : переписать в виде двух отдельных программ, так что бы после завершения загрузки одна дергала другую
#TODO : вторая программа должна уметь работать просто с набором файлов который ей дадут, при этом на вход должно
#TODO : поступать хотя бы одно имя относитально которого будут считаться все остальные файлы

if __name__ == '__main__':
    '''download_dir = 'downloads'
    in_action_deq_size = 10
    pause = 0.5
    radius = 5
    positions = [14]
    vocabulary = ['T', 'W', 'A']'''

    config = open('config.txt').read()
    exec(config)

    mutations = MutGen('input.txt', positions=positions, vocabulary=vocabulary, chunkSize=chunks)
    mutations.gen_mut()
    mutations.save_fasta()

    jobs_to_be_done = deque(seq_fetcher(name, mutations.sequences[name], download_dir=download_dir)
                            for name in mutations.sequences)
    jobs_in_action = deque()

    if len(mutations.sequences)<in_action_deq_size:
        in_action_deq_size = len(mutations.sequences)

    for i in range(in_action_deq_size):
        jobs_in_action.append(jobs_to_be_done.pop())

    while jobs_in_action:

        for i in reversed(range(len(jobs_in_action))):
            if jobs_in_action[i].check_url and not jobs_in_action[i].results_url:
                jobs_in_action[i].check
                print('job {} is in the process'.format(jobs_in_action[i].name))

            elif jobs_in_action[i].results_url and not jobs_in_action[i].complete:
                jobs_in_action[i].pull

                if jobs_to_be_done:
                    print('removing {} job'.format(jobs_in_action[i].name))
                    del jobs_in_action[i]
                    jobs_in_action.append(jobs_to_be_done.pop())
                    print('job {} added'.format(jobs_in_action[i].name))
                else:
                    del jobs_in_action[i]

            elif not jobs_in_action[i].check_url:
                try:
                    jobs_in_action[i].push
                    print("job {} started".format(jobs_in_action[i].name))
                except Exception as exp:
                    print('job {} got exception: '.format(jobs_in_action[i], exp))
                    pass
            time.sleep(pause)


    ref = JpredArchive(mutations.main_name, download_dir=download_dir)
    ref.collect_information()
    results = {}

    for key in sorted(mutations.sequences.keys()):
        if mutations.main_name != key:
            try:
                archive = JpredArchive(key, download_dir=download_dir)
                archive.collect_information()
                neigbourhood = re.search(r'\d+', key)
                neigbourhood = int(neigbourhood.group(0))

                if neigbourhood - radius < 0:
                    radiusL = len(ref.E[:neigbourhood])
                    radiusR = radius
                elif neigbourhood + radius > len(ref.E):
                    radiusL = radius
                    radiusR = len(ref.E[neigbourhood:]) - 1
                else:
                    radiusL = radius
                    radiusR = radius

                E_z = [(archive.E[i], ref.E[i]) for i in range(neigbourhood - radiusL, neigbourhood + radiusR + 1)]
                C_z = [(archive.C[i], ref.C[i]) for i in range(neigbourhood - radiusL, neigbourhood + radiusR + 1)]
                H_z = [(archive.H[i], ref.H[i]) for i in range(neigbourhood - radiusL, neigbourhood + radiusR + 1)]

                E = (sum((E_a - E_r) ** 2 for E_a, E_r in E_z) / (radiusL + radiusR + 1)) ** 0.5
                C = (sum((C_a - C_r) ** 2 for C_a, C_r in C_z) / (radiusL + radiusR + 1)) ** 0.5
                H = (sum((H_a - H_r) ** 2 for H_a, H_r in H_z) / (radiusL + radiusR + 1)) ** 0.5

                E_sign = -1 if sum((E_a - E_r) for E_a, E_r in E_z) < 0 else 1
                C_sign = -1 if sum((C_a - C_r) for C_a, C_r in C_z) < 0 else 1
                H_sign = -1 if sum((H_a - H_r) for H_a, H_r in H_z) < 0 else 1

                results[key] = {'archive': key,
                                'E': E * E_sign,
                                'C': C * C_sign,
                                'H': H * H_sign}
            except Exception:
                results[key] = {'archive': key,
                                'E': 'error',
                                'C': 'error',
                                'H': 'error'}

    with open('results.txt', 'w') as res:
        for item in sorted(results.items()):
            if item[0] != mutations.main_name:
                print('{}    H: {:.2f}, E: {:.2f}, C: {:.2f}'.format(item[0], item[1]['H'],
                                                                    item[1]['E'], item[1]['C']))
                res.write('{}    H: {:.2f}, E: {:.2f}, C: {:.2f}\n'.format(item[0], item[1]['H'],
                                                                    item[1]['E'], item[1]['C']))

