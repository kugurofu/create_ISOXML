# save.py
import xml.etree.ElementTree as ET
from xml.dom import minidom
import zipfile

def save_xml(tz_values,processed_data, rows, cols, minxx, minyy, 
             bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y, 
             top_left_x, top_left_y, top_right_x, top_right_y):
    MaxX = max(top_left_x, top_right_x, bottom_left_x, bottom_right_x)
    MinX = min(top_left_x, top_right_x, bottom_left_x, bottom_right_x)
    MaxY = max(top_left_y, top_right_y, bottom_left_y, bottom_right_y)
    MinY = min(top_left_y, top_right_y, bottom_left_y, bottom_right_y)

    root = ET.Element('ISO11783_TaskData')
    root.set('DataTransferOrigin','1')
    root.set('ManagementSoftwareManufacturer','Pix4Dfields')
    root.set('ManagementSoftwareVersion','2.7.1 (5859e35030)')
    root.set('VersionMajor','4')
    root.set('VersionMinor','3')
    elem4_1 = ET.SubElement(root, 'VPN')
    elem4_1.set('A','VPN1')
    elem4_1.set('B','0')
    elem4_1.set('C','0.100000')
    elem4_1.set('D','2')
    elem4_1.set('E','cm')
    elem10 = ET.SubElement(root, 'PFD')
    elem10.set('A','PFD1')
    elem10.set('C','taikisample')
    elem10.set('D','59535')
    elem11 = ET.SubElement(elem10, 'PLN')
    elem11.set('A','1')
    elem12 = ET.SubElement(elem11, 'LSG')
    elem12.set('A','1')
    elem13_1 = ET.SubElement(elem12, 'PNT')
    elem13_1.set('A','2')
    elem13_1.set('C',str(bottom_left_y))
    elem13_1.set('D',str(bottom_left_x))
    elem13_2 = ET.SubElement(elem12, 'PNT')
    elem13_2.set('A','2')
    elem13_2.set('C',str(bottom_right_y))
    elem13_2.set('D',str(bottom_right_x))
    elem13_3 = ET.SubElement(elem12, 'PNT')
    elem13_3.set('A','2')
    elem13_3.set('C',str(top_right_y))
    elem13_3.set('D',str(top_right_x))
    elem13_4 = ET.SubElement(elem12, 'PNT')
    elem13_4.set('A','2')
    elem13_4.set('C',str(top_left_y))
    elem13_4.set('D',str(top_left_x))
    elem13_5 = ET.SubElement(elem12, 'PNT')
    elem13_5.set('A','2')
    elem13_5.set('C',str(bottom_left_y))
    elem13_5.set('D',str(bottom_left_x))
    elem15 = ET.SubElement(root, 'TSK')
    elem15.set('A','TSK1')
    elem15.set('E','PFD1')
    elem15.set('G','1')
    elem15.set('J','254')
    elem19 = ET.SubElement(elem15, 'DLT')
    elem19.set('A','DFFF')
    elem19.set('B','1')
    elem19.set('D','1000')
    
    # TZの値を設定する
    for i, value in enumerate(tz_values):
        elem_tz = ET.SubElement(elem15, 'TZN')
        elem_tz.set('A', str(i+1))
        elem_tz.set('B', str(i+1))
        elem_pdv = ET.SubElement(elem_tz, 'PDV')
        elem_pdv.set('A', '0010')
        elem_pdv.set('B', str(value))
        elem_pdv.set('C', 'PDT1')
        elem_pdv.set('E', 'VPN1')

    # 最後のTZN要素
    elem26 = ET.SubElement(elem15, 'TZN')
    elem26.set('A', '0')
    elem27 = ET.SubElement(elem26, 'PDV')
    elem27.set('A', '0010')
    elem27.set('B', '1')
    elem27.set('C', 'PDT1')
    elem27.set('E', 'VPN1')
    elem30 = ET.SubElement(elem15, 'GRD')
    elem30.set('A', str(minyy))
    elem30.set('B', str(minxx))
    elem30.set('C', f"{(MaxY-MinY)/cols:.20f}")
    elem30.set('D', f"{(MaxX-MinX)/rows:.20f}")
    elem30.set('E', str(rows))
    elem30.set('F', str(cols))
    elem30.set('G', 'GRD00001')
    elem30.set('H', str(rows*cols))
    elem30.set('I', '1')

    # インデントを付けて保存
    doc = minidom.parseString(ET.tostring(root, 'utf-8'))
    with open('TASKDATA.xml', 'w') as f:
        doc.writexml(f, encoding='utf-8', newl='\n', indent='', addindent='  ')
    # pass  # (元のsave_xml関数の内容をここに入れます)

def create_zip():
    # XMLとBINファイルをZIP化
    with zipfile.ZipFile('sample.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write('GRD00001.bin', arcname='GRD00001.bin')
        zf.write('TASKDATA.xml', arcname='TASKDATA.xml')