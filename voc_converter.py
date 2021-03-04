import os
from PIL import Image

INDEX_FILE = './GroundTruth/groundtruth0000-9999.txt'
VOC_NAME = 'VOCDevkit'
VOC_ANNOTATION_DIR = './VOCDevkit/Annotations'


def build_xml(key, data):
    print('processing ' + key + '...')
    image_id = int(key)
    pid = int((image_id / 1000))
    dir_name_left = str(pid) + '000'
    dir_name_right = str(pid) + '999'
    image_dir_name = './image%s-%s/%s.png' % (dir_name_left, dir_name_right, key)
    img = Image.open(image_dir_name)

    xml_file = open(VOC_ANNOTATION_DIR + '/' + key + '.xml', 'w+')
    xml_template = '''<annotation>  
    <folder>{0}</folder>
    <filename>{1}</filename>
    <source>
        <database>CCTSDB</database>  
        <annotation>CCTSDB</annotation>  
        <image>flickr</image>  
    </source>  
    <size>
        <width>{2}</width>  
        <height>{3}</height>  
        <depth>3</depth>  
    </size>
    <segmented>0</segmented>
'''.format(VOC_NAME, key + '.png', img.size[0], img.size[1])

    # xml_file.write(xml_template)

    for obj in data:
        xml_template += ('''
    <object>
		<name>{0}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{1}</xmin>
			<ymin>{2}</ymin>
			<xmax>{3}</xmax>
			<ymax>{4}</ymax>
        </bndbox>
    </object>
'''.format(obj[-1], obj[0], obj[1], obj[2], obj[3]))
    xml_file.write(xml_template + '</annotation>')
    xml_file.close()

def main():
    # Make dirs to contain the result
    os.makedirs("./VOCDevkit/Annotations", exist_ok=True)
    os.makedirs("./VOCDevkit/JPEGImages", exist_ok=True)

    # read all indexes
    f_index = open(INDEX_FILE, 'r')
    lines = f_index.readlines()

    data_map = {}

    for line in lines:
        segs = line[0:-1].split(';')
        key = segs[0].split('.')[0]
        data_map.setdefault(key, [])
        data_map[key].append(segs[1:])

    for k in data_map.keys():
        build_xml(k, data_map[k])


if __name__ == '__main__':
    main()

