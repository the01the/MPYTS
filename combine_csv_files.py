import csv
from pathlib import Path


def combine_csv_files(input_dir: str | Path, output_file: str | Path) -> None:
    input_path = Path(input_dir)
    csv_files = sorted(input_path.glob("*.csv"))

    if not csv_files:
        print("指定されたフォルダにCSVファイルが見つかりませんでした。")
        return

    with open(output_file, mode="w", newline="", encoding="utf-8-sig") as f_out:
        writer = csv.writer(f_out)
        header_written = False

        for file_path in csv_files:
            # 出力先ファイル自体が入力フォルダ内にある場合はスキップ
            if file_path.resolve() == Path(output_file).resolve():
                continue

            with open(file_path, mode="r", newline="", encoding="utf-8-sig") as f_in:
                reader = csv.reader(f_in)

                # 1行目（ヘッダ）の読み込み
                try:
                    header = next(reader)
                except StopIteration:
                    # 空のファイルはスキップ
                    continue

                # 最初の1ファイル目のみヘッダを書き込む
                if not header_written:
                    writer.writerow(["FullFileName"] + header)
                    header_written = True

                # 2行目以降（データ行）の書き込み
                for row in reader:
                    writer.writerow([file_path.name] + row)

    print(f"結合が完了しました: {output_file}")


# 使い方例
if __name__ == "__main__":
    target_folder = "./data"  # CSVファイルが入っているフォルダパス
    output_csv = "./combined.csv"  # 保存先のファイル名

    combine_csv_files(target_folder, output_csv)