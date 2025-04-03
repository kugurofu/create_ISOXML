import tkinter as tk
import geopandas as gpd
from file import open_files
from save import save_xml, create_zip

def main():
    processed_data = None  # `processed_data`を初期化
    entries = {}  # TZのエントリーウィジェットを管理
    tz_values = []  # TZのリスト

    # メインウィンドウ作成
    root = tk.Tk()
    root.title("ISOXML")
    root.geometry("1500x800")

    # レイアウト設定
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=10)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=10)

    # サイドバー作成
    side_frame = tk.Frame(root)
    side_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

    # `TZ` のタイトルラベル
    tz_title = tk.Label(side_frame, text="TZ", font=("Arial", 12, "bold"))
    tz_title.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    # `TZ` のエントリーウィジェットを更新する関数
    def update_tz_entries():
        """TZエントリーを更新する関数"""
        if processed_data is None:
            return

        # 既存のエントリーを削除
        for widget in side_frame.winfo_children():
            widget.destroy()

        # 新しいエントリーを作成
        tz_title = tk.Label(side_frame, text="TZ", font=("Arial", 12, "bold"))
        tz_title.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        for i, tz in enumerate(processed_data.tz_values, start=1):
            tz_label = tk.Label(side_frame, text=str(tz), anchor='w')
            tz_label.grid(row=i, column=0, sticky='w', pady=2)

            entry = tk.Entry(side_frame, width=10, font=10)
            entry.grid(row=i, column=1, sticky='w', pady=2)

            unit_label = tk.Label(side_frame, text="mm")
            unit_label.grid(row=i, column=2, sticky='w', pady=2)

            entries[tz] = entry  # エントリーを辞書に保存

    # ファイル選択ボタンの動作
    def open_files_wrapper():
        nonlocal processed_data, tz_values
        processed_data = open_files(canvas_frame)

        update_tz_entries()  # ファイルを開いた後にTZ設定を更新

    open_button = tk.Button(root, width=15, height=2, text="ファイル", command=open_files_wrapper)
    open_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

    # `TZ` の値を `save_xml` に渡す
    def save_tz_values():
        if processed_data is None:
            print("ファイルを選択してください。")
            return
        
        tz_values_input = {tz: entries[tz].get() for tz in entries}
        print(tz_values_input)
        
        save_xml(
            tz_values_input,
            processed_data,
            processed_data.rows,
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
            processed_data.top_right_y
        )

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
