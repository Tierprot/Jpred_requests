from http_requests import seq_fetcher
from collections import deque
from seq_generator import MutGen
from tar_gz import JpredArchive
import time
import re
import os


#TODO : переписать в виде двух отдельных программ, так что бы после завершения загрузки одна дергала другую
#TODO : вторая программа должна уметь работать просто с набором файлов который ей дадут, при этом на вход должно
#TODO : поступать хотя бы одно имя относитально которого будут считаться все остальные файлы

if __name__ == '__main__':

    config = open('config.txt').read()
    exec (config)

    try:
        names = os.listdir(os.path.join(os.getcwd(), download_dir))
    except FileNotFoundError as exp:
        os.mkdir(os.path.join(os.getcwd(), download_dir))
        names=[]

    names = [name.split('.tar')[0] for name in names]
    seqs = {}

    with open(inp, 'r') as base:
        line = base.readline().strip().split('>')[1]

    with open(line + '.fasta', 'r') as fasta:
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

    jobs_to_be_done = deque(seq_fetcher(name, seqs[name], download_dir=download_dir)
                            for name in seqs)
    jobs_in_action = deque()

    if len(seqs)<in_action_deq_size:
        in_action_deq_size = len(seqs)

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

    print('all jobs are done!')