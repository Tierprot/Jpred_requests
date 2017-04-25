from http_requests import seq_fetcher
from collections import deque
from tar_gz import JpredArchive
import os
import time
import re

config = open('config.txt').read()
exec(config)

names = os.listdir(os.path.join(os.getcwd(), download_dir))
names = [name.split('.tar')[0] for name in names]

values = [item for item in names if item.split('_')[1]==item.split('_')[-1]]
keys = [item for item in names if item.split('_')[1]!=item.split('_')[-1]]

mapping = {}
for key in keys:
    for value in values:
        if key.split('_')[1]==value.split('_')[1]:
            mapping.update({key:value})

for item, value in mapping.items():
    print(item,value)

results = {}

for key in sorted(mapping):
    print('analyzing ', key)
    try:
        ref = JpredArchive(mapping[key], download_dir=download_dir)
        ref.collect_information()
        archive = JpredArchive(key, download_dir=download_dir)
        archive.collect_information()
        neigbourhood = re.search(r'\d+', mapping[key])
        neigbourhood = int(neigbourhood.group(0))

        if neigbourhood - radius < 0:
            radiusL = len(ref.E[:neigbourhood])
            radiusR = radius
        elif neigbourhood + radius >= neigbourhood + chunks//2:
            radiusL = radius
            radiusR = len(ref.E[neigbourhood:]) - 1
        else:
            radiusL = radius
            radiusR = radius

        E_z = [(archive.E[i], ref.E[i]) for i in range(chunks//2 - radiusL, chunks//2 + radiusR + 1)]
        C_z = [(archive.C[i], ref.C[i]) for i in range(chunks//2 - radiusL, chunks//2 + radiusR + 1)]
        H_z = [(archive.H[i], ref.H[i]) for i in range(chunks//2 - radiusL, chunks//2 + radiusR + 1)]

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


with open('results.txt', 'w') as res:

    for item in sorted(results.items(), key = lambda data : int(data[0].split('_')[1][:-1])):
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