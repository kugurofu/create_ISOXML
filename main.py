# main.py
import tkinter as tk
from file import open_files
from save import save_xml, create_zip

def main():
    processed_data = None  # `processed_data`を初期化しておく

    # メインウィンドウ作成
    root = tk.Tk()
    root.title("ISOXML")
    root.geometry("1500x800")

    # レイアウト設定
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=10)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=10)

    # 上部にファイル選択ボタン
    def open_files_wrapper():
        nonlocal processed_data
        processed_data = open_files(canvas_frame)

    open_button = tk.Button(root, width=15, height=2, text="ファイル", command=open_files_wrapper)
    open_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

    # TZの設定サイドバーを表示
    side_frame = tk.Frame(root)
    side_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

    # TZのタイトルラベル
    tz_title = tk.Label(side_frame, text="TZ", font=("Arial", 12, "bold"))
    tz_title.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    # TZ番号と入力フィールドのリスト
    tz_values = [
        ("1", True),
        ("2", True),
        ("3", True),
        ("4", True),
        ("5", True)
    ]

    # エントリーウィジェットを保持する辞書
    entries = {}

    # 各TZのラベルとエントリーを作成
    for i, (tz, has_entry) in enumerate(tz_values, start=1):
        # TZ番号のラベル
        tz_label = tk.Label(side_frame, text=tz, anchor='w')
        tz_label.grid(row=i, column=0, sticky='w', pady=2)

        if has_entry:
            # エントリーウィジェット
            entry = tk.Entry(side_frame, width=10, font=10)
            entry.grid(row=i, column=1, sticky='w', pady=2)
            # 単位ラベル
            unit_label = tk.Label(side_frame, text="mm")
            unit_label.grid(row=i, column=2, sticky='w', pady=2)
            # エントリーを辞書に保存（後でアクセスする場合）
            entries[tz] = entry
        else:
            # 空白または別のウィジェットを配置する場合
            placeholder = tk.Label(side_frame, text="")
            placeholder.grid(row=i, column=1, sticky='w', pady=2)
            placeholder2 = tk.Label(side_frame, text="")
            placeholder2.grid(row=i, column=2, sticky='w', pady=2)

    # tz_valuesをsave_xmlに渡すための関数を定義
    def save_tz_values():
        if processed_data is None:
            print("ファイルを選択してください。")
            return
        tz_values = [entries[tz].get() for tz in entries]
        save_xml(tz_values, processed_data, processed_data.rows, 
        processed_data.cols, 
        processed_data.minxx, 
        processed_data.minyy,
        processed_data.bottom_left_x, 
        processed_data.bottom_left_y, 
        processed_data.bottom_right_x, 
        processed_data.bottom_right_y, 
        processed_data.top_left_x, 
        processed_data.top_left_y, 
        processed_data.top_right_x, 
        processed_data.top_right_y)
    
    fonts = ("", 12)

    # XML保存ボタン
    save_button = tk.Button(root, width=15, height=2, font=fonts, text="XMLを保存", command=save_tz_values)
    save_button.grid(row=2, column=0, padx=10, pady=10, sticky='sw')

    # ZIP保存ボタン
    create_button = tk.Button(root, width=15, height=2, font=fonts, text="zipに保存", command=create_zip)
    create_button.grid(row=3, column=0, padx=10, pady=10, sticky='sw')

    # 下部にグラフ表示用のフレーム
    canvas_frame = tk.Frame(root, width="1000", height="700")
    canvas_frame.propagate(False)
    canvas_frame.grid(row=1, column=1, padx=10, pady=10, sticky='se')

    # GUIループ開始
    root.mainloop()

if __name__ == '__main__':
    main()
