from http_requests import seq_fetcher
from collections import deque
from tar_gz import JpredArchive
import os
import argparse
import time
import re

parser = argparse.ArgumentParser()

parser.add_argument('--main_name', nargs=1, action='store')

main_name = parser.parse_args().main_name[0]

config = open('config.txt').read()
exec(config)

names = os.listdir(os.path.join(os.getcwd(), download_dir))
names = [name.split('.tar')[0] for name in names]

ref = JpredArchive(main_name, download_dir=download_dir)
ref.collect_information()
results = {}

for key in sorted(names):
    if main_name != key:
        print('analyzing ',key)
        try:
            archive = JpredArchive(key, download_dir=download_dir)
            archive.collect_information()
            neigbourhood = re.search(r'\d+', key)
            neigbourhood = int(neigbourhood.group(0))

            if neigbourhood - radius < 0:
                radiusL = len(ref.E[:neigbourhood])
                radiusR = radius
            elif neigbourhood + radius >= len(ref.E):
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
            print('done')
        except Exception as Exp:
            print(Exp)
            print('error on archive {}'.format(key))
            results[key] = {'archive': key,
                            'E': 'error',
                            'C': 'error',
                            'H': 'error'}
        
    else:
        pass

with open('results.txt', 'w') as res:
    for item in sorted(results.items()):
        if item[0] != main_name:
            try:
                print('{}    H: {:.2f}, E: {:.2f}, C: {:.2f}'.format(item[0], item[1]['H'],
                                                                 item[1]['E'], item[1]['C']))
                res.write('{}    H: {:.2f}, E: {:.2f}, C: {:.2f}\n'.format(item[0], item[1]['H'],
                                                                       item[1]['E'], item[1]['C']))
            except:
                print('{}    H: {}, E: {}, C: {}'.format(item[0], item[1]['H'],
                                                                     item[1]['E'], item[1]['C']))
                res.write('{}    H: {}, E: {}, C: {}\n'.format(item[0], item[1]['H'],
                                                                       item[1]['E'], item[1]['C']))