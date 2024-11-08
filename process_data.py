# process_data.py
import geopandas as gpd
from pyproj import Transformer
import numpy as np
from shapely.geometry import MultiPoint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import shapely
import fiona
import tkinter as tk

# data_container
class ProcessedData:
    def __init__(self, top_left_x, top_left_y, top_right_x, top_right_y,
                 bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y,
                 rows, cols, minxx, minyy):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y
        self.rows = rows
        self.cols = cols
        self.minxx = minxx
        self.minyy = minyy

def process_and_display(PATH1, PATH2, canvas_frame):    
    # Try to repair the shapefile by setting SHAPE_RESTORE_SHX to YES
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        # Geopandas でshpを読み込む
            gdf_rg = gpd.read_file(PATH1)
            gdf_pt = gpd.read_file(PATH2)

    # CRS の確認
    print("Region CRS:", gdf_rg.crs)
    print("Grid CRS:", gdf_pt.crs)

    # regionレイヤCRS を EPSG:4326 に変換（いらないかも）
    if gdf_rg.crs != "EPSG:4326":
        gdf_rg = gdf_rg.to_crs(epsg=4326)
        #gdf_pt = gdf_pt.to_crs(epsg=4326)

    # 座標系の変換
    epsg2455_to_epsg4326 = Transformer.from_crs("epsg:2455", "epsg:4326")

    # 点群の分類結果を格納するためのリスト
    point_classes = []

    # ポリゴン指定 
    target_poly2 = gdf_rg[gdf_rg['TZ'] == 2].geometry
    target_poly1 = gdf_rg[gdf_rg['TZ'] == 1].geometry
    target_poly3 = gdf_rg[gdf_rg['TZ'] == 3].geometry
    target_poly4 = gdf_rg[gdf_rg['TZ'] == 4].geometry
    target_poly5 = gdf_rg[gdf_rg['TZ'] == 5].geometry
    target_poly254 = gdf_rg[gdf_rg['TZ'] == 254].geometry

    # 各点について分類を行う
    for i in range(len(gdf_pt)):
        temp = gdf_pt['geometry'][i]
        lat, lon = epsg2455_to_epsg4326.transform(temp.y, temp.x)
        point = shapely.geometry.point.Point(lon, lat)
    
        if any(target_poly1.contains(point)):
            point_classes.append(1)
        elif any(target_poly2.contains(point)):
            point_classes.append(2)
        elif any(target_poly3.contains(point)):
            point_classes.append(3)
        elif any(target_poly4.contains(point)):
            point_classes.append(4)
        elif any(target_poly5.contains(point)):
            point_classes.append(5)
        else:
            point_classes.append(254)

    # グリッドの境界を使用して行数と列数を計算
    minx, miny, maxx, maxy = gdf_pt.total_bounds
    num_cells = len(gdf_pt)
    cell_width = maxx - minx
    cell_height = maxy - miny
    cols = int(np.sqrt(num_cells * (cell_height / cell_width)))
    rows = num_cells // cols
    print(rows)
    print(cols)

    # 並び替え
    data2D = np.array(point_classes).reshape(rows, cols)
    data2D[data2D == 254] = 0
    point_classes = [0 if x==254 else x for x in point_classes]
    data2D_rotate = np.rot90(data2D)

    # 可視化
    fig, ax = plt.subplots()
    cax = ax.imshow(data2D_rotate, cmap='jet', origin='lower') # origin='lower'
    cbar = fig.colorbar(cax)
    cbar.set_label('TZ')  # カラーバーにラベルを追加

    # 既存のキャンバスがあれば削除
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # MatplotlibのグラフをTkinterに表示
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)  # グラフをフレーム内に拡張して配置

    # 投影座標系で回転矩形を作成する方法
    # regionレイヤを投影座標系に変換（例: UTM Zone 33N）
    if gdf_rg.crs != "EPSG:32633":
        gdf_rg = gdf_rg.to_crs(epsg=32633)

    # 対象となる地物IDのリスト
    selected_feature_ids = [1, 2, 3, 4, 5]  # 例: IDが1, 2, 3, 4, 5の地物

    # 対象となる地物の頂点を格納するリスト
    selected_vertices = []

    # gridレイヤCRS を EPSG:4326 に変換（既に変換されていない場合）
    if gdf_pt.crs != "EPSG:4326":
        gdf_pt = gdf_pt.to_crs(epsg=4326)

    # 対象となる地物をフィルタリング
    selected_gdf = gdf_rg[gdf_rg['TZ'].isin(selected_feature_ids)]

    # 各フィーチャのジオメトリから頂点座標を取得
    for geom in selected_gdf.geometry:
        if geom.is_empty:
            continue
        if geom.geom_type == 'Polygon':
            vertices = list(geom.exterior.coords)
        elif geom.geom_type == 'MultiPolygon':
            vertices = [point for poly in geom for point in poly.exterior.coords]
        selected_vertices.extend(vertices)

    # 重複を排除
    selected_vertices = list(set(selected_vertices))

    # ShapelyでMultiPointオブジェクトを作成
    points = MultiPoint(selected_vertices)

    # 最小の回転矩形を計算
    min_rotated_rect = points.minimum_rotated_rectangle

    # 回転矩形の外周座標を取得
    rect_exterior = np.array(min_rotated_rect.exterior.coords)

    # 座標を地理座標系に戻す
    min_rotated_rect_geo = gpd.GeoSeries([min_rotated_rect], crs="EPSG:32633").to_crs(epsg=4326)
    rect_exterior_geo = np.array(min_rotated_rect_geo[0].exterior.coords)

    # 四隅の座標を出力
    print("回転矩形の四隅の座標（投影座標系で計算し、EPSG:4326に変換）:")
    for point in rect_exterior_geo[:-1]:  # 最後の点は始点と重複するので省略
        print(f"X: {point[0]}, Y: {point[1]}")

    # 各座標をx, yに分けて格納
    bottom_left_x, bottom_left_y = rect_exterior_geo[1]
    bottom_right_x, bottom_right_y = rect_exterior_geo[2]
    top_right_x, top_right_y = rect_exterior_geo[3]
    top_left_x, top_left_y = rect_exterior_geo[0]

    print(f"Top Left: ({top_left_x}, {top_left_y})")
    print(f"Top Right: ({top_right_x}, {top_right_y})")
    print(f"Bottom Right: ({bottom_right_x}, {bottom_right_y})")
    print(f"Bottom Left: ({bottom_left_x}, {bottom_left_y})")

    minyy, minxx =epsg2455_to_epsg4326.transform(miny, minx)

    # バイナリファイルとして保存
    binary_data = np.array(data2D_rotate, dtype=np.uint8)
    binary_data.tofile('GRD00001.bin')

     # `ProcessedData`オブジェクトを作成し、必要なデータを保持
    processed_data = ProcessedData(
        top_left_x, top_left_y, top_right_x, top_right_y,
        bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y,
        rows, cols, minxx, minyy
    )
    return processed_data