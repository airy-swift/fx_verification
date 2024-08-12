import pandas as pd


class DataFrameHandler:
    def __init__(self):
        self.df = None

    def load_df(self, input_csv_path, parse_dates=None):
        self.df = pd.read_csv(input_csv_path, parse_dates=parse_dates)

    def set_index(self, key):
        self.df.set_index(key, inplace=True)

    def reset_index(self, df):
        df.reset_index(inplace=True)

    def numbering(self, key):
        self.df[key] = range(1, len(self.df) + 1)

    def convert_to_datetime(self, key):
        self.df[key] = pd.to_datetime(self.df[key])

    def get_resampling(self, time_unit):
        # WARN: hと5minでLowとHighが逆だったことがその内関係するのか？
        return self.df.resample(time_unit).agg({
            'Open': 'first',
            'Low': 'min',
            'High': 'max',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()

    # 過去240時間の平均実体を計算
    def calc_rolling_avg_body(self):
        self.df['body'] = (self.df['Close'] - self.df['Open']).abs()
        self.df['rolling_avg_body'] = self.df['body'].rolling(window=240).mean()

    # 大陽線を検出・抽出
    def get_large_bullish(self):
        self.df['is_large_bullish'] = (self.df['Close'] > self.df['Open']) & (
                self.df['body'] >= 4 * self.df['rolling_avg_body'])
        return self.df[self.df['is_large_bullish']].copy()

    # [key]行の数の差が[gap]以下の大陽線をフィルタリング
    def filter_large_bullish(self, large_bullish_df, key, gap):
        filtered_indices = []
        prev_index = None

        for index, row in large_bullish_df.iterrows():
            if prev_index is not None and (row[key] - prev_index <= gap):
                filtered_indices.append(prev_index)
            prev_index = row[key]

        return large_bullish_df[~large_bullish_df[key].isin(filtered_indices)]

    # 大陽線の安値を実体で下回ったローソク足を検出
    def get_negation_of_large_bullish(self, filtered_large_bullish_df, datetime_key):
        invalidation_patterns = []

        for idx, bullish_row in filtered_large_bullish_df.iterrows():
            for i in range(1, 51):
                if idx + i < len(self.df):
                    if self._is_bullish_invalidation(bullish_row, self.df.iloc[idx + i]):
                        # 大陽線から大陽線否定足までの最高値を調査
                        high_in_period = self.df.iloc[idx:idx + i + 1]['High'].max()
                        bullish_low = bullish_row['Low']

                        # フィボナッチリトレースメントの計算
                        period_body = high_in_period - bullish_low
                        fib_levels = {
                            '-38.2%': bullish_low + 1.382 * period_body,
                            '0%': high_in_period,
                            '38.2%': bullish_low + 0.618 * period_body,
                            '78.6%': bullish_low + 0.214 * period_body,
                            '100%': bullish_low,
                            '138.2%': bullish_low - 0.382 * period_body,
                            '161.8%': bullish_low - 0.618 * period_body
                        }

                        invalidation_patterns.append({
                            'Bullish Candle Datetime': bullish_row[datetime_key],
                            'Invalidation Candle Datetime': self.df.iloc[idx + i][datetime_key],
                            'Bullish Low': bullish_low,
                            'High in Period': high_in_period,
                            **fib_levels,
                        })
                        break
        return invalidation_patterns

    def save_as_csv(self, df, path, index=True):
        df.to_csv(path, index=index)
        print('Saved as', path)

    def _is_bullish_invalidation(self, large_bullish_row, candle_row):
        return candle_row['Close'] < large_bullish_row['Low']