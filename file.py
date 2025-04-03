# file.py
from tkinter import filedialog
from tkinter import ttk, filedialog, simpledialog
from process_data import process_and_display

def open_files(canvas_frame):
    # ファイル選択ダイアログ
    file_path1 = filedialog.askopenfilename(title="regionファイルを選択してください")
    file_path2 = filedialog.askopenfilename(title="gridファイルを選択してください")

    if file_path1 and file_path2:
        print(f"選択されたファイル1: {file_path1}")
        print(f"選択されたファイル2: {file_path2}")

        # ユーザーにTZ値を入力させる
        default_tz = 254
        # default_tz = simpledialog.askinteger("圃場外TZ", "圃場外領域のTZ値を決めてください:", minvalue=1, maxvalue=999)
    
        if default_tz is None:
            return  # ユーザーがキャンセルした場合は処理を中断

        processed_data = process_and_display(file_path1, file_path2, canvas_frame, default_tz)

        return processed_data
