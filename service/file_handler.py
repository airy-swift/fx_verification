import os


class FileHandler:
    def __init__(self):
        self.cwd = os.getcwd()
        self.input_dir = './input_file'
        self.output_dir = './new_output_file'

        self.input_file = 'EURJPY.csv'
        self.output_eurjpy_5min = 'EURJPY_5min.csv'
        self.output_eurjpy_hourly = 'EURJPY_hourly.csv'
        self.output_large_fibonacci = 'large_bullish_invalidation_patterns_with_fibonacci.csv'
        self.merged_output = 'merged_output.csv'

    def get_input_file_path(self):
        return os.path.join(self.cwd, self.input_dir, self.input_file)

    def get_output_5min_path(self):
        return os.path.join(self.cwd, self.output_dir, self.output_eurjpy_5min)

    def get_output_hourly_path(self):
        return os.path.join(self.cwd, self.output_dir, self.output_eurjpy_hourly)

    def get_output_large_fibonacci_path(self):
        return os.path.join(self.cwd, self.output_dir, self.output_large_fibonacci)
