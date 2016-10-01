__author__ = 'Bones'

import tarfile
import os
import time


class JpredArchive():
    download_directory = 'download'
    job_name_tag = '.name'
    prediction_file = '.concise'
    prob_E = "JNETPROPE:"
    prob_C = "JNETPROPC:"
    prob_H = "JNETPROPH:"

    def __init__(self, filename, download_dir=download_directory):
        try:

            self.filename = filename
            self.archive = tarfile.open(os.path.join(os.getcwd(), download_dir + '\\' + filename + '.tar.gz'))
            self.files = self.archive.getmembers()
        except Exception as Exp:
            print(Exp)

    def collect_information(self):
        # probabilities
        try:
            self.C, self.E, self.H = self.probabilities()
        except Exception as Exp:
            print(Exp, self.filename)
            print('problem with probabilities')
            time.sleep(5)

        # close archive
        self.close()
        return True

    def probabilities(self):
        try:
            data = next(file.name for file in self.files if file.name.endswith(self.prediction_file))
            data = self.archive.extractfile(data)
            C, E, H = '', '', ''
            for string in data:
                if self.prob_C in string.decode("utf-8"):
                    C = self.convertation(string, self.prob_C)
                if self.prob_E in string.decode("utf-8"):
                    E = self.convertation(string, self.prob_E)
                if self.prob_H in string.decode("utf-8"):
                    H = self.convertation(string, self.prob_H)
                if C and E and H:
                    break
            return C, E, H

        except Exception as Exp:
            print(Exp)

    def convertation(self, string, parameter):
        result = string.decode("utf-8").strip()
        result = result.replace(parameter, '').split(',')
        result = [float(num) for num in result if num]
        return result

    def close(self):
        self.archive.close()
        return True
            

if __name__ == "__main__":
    archive = JpredArchive('jp_ZOIVzIJ')
    archive.collect_information()
    print(archive.E)
