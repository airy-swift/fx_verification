import pandas as pd

import service.data_frame_handler
import service.file_handler


class Process:
    def __init__(self):
        self.file = service.file_handler.FileHandler()
        self.datetime_key = 'DateTime'
        self.bullish_candle_datetime_key = 'Bullish Candle Datetime'
        self.invalidation_candle_datetime_key = 'Invalidation Candle Datetime'
        self.numbering_key = 'G'  # 2ページ目でナンバリングしてるやつ

    #
    # 1ファイル目
    # 後続のための下処理
    #
    def resampling(self):
        df_handler = service.data_frame_handler.DataFrameHandler()
        df_handler.load_df(self.file.get_input_file_path())

        df_handler.convert_to_datetime(self.datetime_key)
        df_handler.set_index(self.datetime_key)

        # Union[Series, DataFrame]
        df_hourly = df_handler.get_resampling('h')
        df_5min = df_handler.get_resampling('5min')

        df_handler.reset_index(df_5min)

        df_handler.save_as_csv(df_hourly, self.file.get_output_hourly_path())
        df_handler.save_as_csv(df_5min, self.file.get_output_5min_path(), index=False)

    #
    # 2ページ目
    # 大陽線否定パターンをCSVに出力
    #
    def output_negation_of_large_bullish(self):
        df_handler = service.data_frame_handler.DataFrameHandler()
        df_handler.load_df(self.file.get_output_hourly_path())
        df_handler.convert_to_datetime(self.datetime_key)

        df_handler.numbering(self.numbering_key)
        df_handler.calc_rolling_avg_body()

        large_bullish_df = df_handler.get_large_bullish()
        filtered_large_bullish_df = df_handler.filter_large_bullish(large_bullish_df, self.numbering_key, 48)

        invalidation_patterns = df_handler.get_negation_of_large_bullish(filtered_large_bullish_df, self.datetime_key)
        invalidation_patterns_df = pd.DataFrame(invalidation_patterns)

        df_handler.save_as_csv(invalidation_patterns_df, self.file.get_output_large_fibonacci_path(), index=False)

    #
    # 3ページ目
    # 検証データ確認のためのデータをフィルタし、並べる
    #
    def merge_raw_fibonacci(self):
        large_df_handler = service.data_frame_handler.DataFrameHandler()
        eurjpy_df_handler = service.data_frame_handler.DataFrameHandler()

        # CSVファイルを読み込む
        large_df_handler.load_df(self.file.get_output_large_fibonacci_path(), parse_dates=[self.bullish_candle_datetime_key, self.invalidation_candle_datetime_key])
        eurjpy_df_handler.load_df(self.file.get_output_5min_path(), parse_dates=[self.datetime_key])

        # 結果を保存するためのリスト
        output_data = []
        # 1つ目のファイルの各行について処理
        for index, row in large_df_handler.df.iterrows():
            invalidation_time = row[self.invalidation_candle_datetime_key]

            # 2つ目のファイルで対応する日時を探す
            matching_rows = eurjpy_df_handler.df[eurjpy_df_handler.df[self.datetime_key] == invalidation_time]
            # なければ次へ
            if matching_rows.empty:
                continue

            # 11:05から150時間分のデータを抽出（5分足で12データ/時 x 150時間 = 1800データ）
            start_index = matching_rows.index[0] + 1  # 次の5分（11:05）から始めるために+1
            end_index = start_index + 1800

            # Extract the 150-hour data
            extracted_data = eurjpy_df_handler.df.df.iloc[start_index:end_index]

            # オリジナル行を出力データに追加
            output_data.append(row.values.tolist())

            # 150時間分のデータを追加
            for extracted_index, extracted_row in extracted_data.iterrows():
                combined_row = row.tolist() + extracted_row.values.tolist()
                output_data.append(combined_row)

        # 新しいDataFrameを作成
        output_columns = list(large_df_handler.df.columns) + list(eurjpy_df_handler.df.columns)
        output_df = pd.DataFrame(output_data, columns=output_columns)

        # 新しいCSVファイルに出力
        eurjpy_df_handler.save_as_csv(output_df, )
        output_df.to_csv(self.file.merged_output, index=False)


if __name__ == '__main__':
    process = Process()

    process.resampling()
    process.output_negation_of_large_bullish()
    process.merge_raw_fibonacci()
