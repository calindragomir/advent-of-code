import os
import concurrent.futures

SCRIPTS_LOCATION = os.path.dirname(os.path.realpath(__file__))
INPUTS_DIR = "input"


class Utilities:

    @staticmethod
    def get_full_input(pyfilename):
        input_name = os.path.basename(pyfilename).rstrip(".py")
        return Utilities.get_lines_from_file("{}.txt".format(input_name))

    @staticmethod
    def get_sample_file(pyfilename):
        input_name = os.path.basename(pyfilename).rstrip(".py")
        sample_folder = "sample"
        return Utilities.get_lines_from_file("{}/{}sample.txt".format(sample_folder, input_name))

    @staticmethod
    def get_lines_from_file(filename):
        full_path = os.path.join(SCRIPTS_LOCATION, INPUTS_DIR, filename)
        f = open(full_path, "r")
        lines = f.readlines()
        trimmed = [l.strip() for l in lines if l.strip() != ""]
        f.close()
        return trimmed

    @staticmethod
    def get_lines_from_file_including_space(filename):
        full_path = os.path.join(SCRIPTS_LOCATION, INPUTS_DIR, filename)
        f = open(full_path, "r")
        lines = f.readlines()
        trimmed = [l.strip() for l in lines]
        f.close()
        return trimmed

    @staticmethod
    def run_parallel_processes(process_inputs):
        """
        :param process_inputs: list of tuple pairs: (function-to-run, args-of-func)
        :return: list of results computed for each
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(fname, *fargs) for fname, fargs in process_inputs]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        return results

    @staticmethod
    def get_matrix_from_input(lines, data_type=str):
        return [[data_type(c) for c in line] for line in lines]

    @staticmethod
    def pairwise(iterable):
        a = iter(iterable)
        return zip(a, a)
