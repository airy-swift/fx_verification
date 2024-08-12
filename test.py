import pandas as pd


#
# リファクタしたコードの出力を以前の出力と比較
#
def test_refactor():
    eur_jpy_5min = 'EURJPY_5min.csv'
    eur_jpy_hourly = 'EURJPY_hourly.csv'
    large_fibonacci = 'large_bullish_invalidation_patterns_with_fibonacci.csv'

    _compare(eur_jpy_5min)
    _compare(eur_jpy_hourly)
    _compare(large_fibonacci)


#
# 比較の実態
#
def _compare(file):
    before_path = '{}/{}'.format('./output_file', file)
    after_path = '{}/{}'.format('./new_output_file', file)
    #
    before = pd.read_csv(before_path)
    after = pd.read_csv(after_path)
    #
    result = before.equals(after)
    print('{}: {}'.format(after_path, result))


if __name__ == '__main__':
    test_refactor()
