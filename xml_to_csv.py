import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    for directory in ['test','train']:
      for fruit in ['Green Apple', 'Orange']: # FIX THIS!!!!
        image_path = os.path.join(os.getcwd(), 'images/', format(directory), format(fruit))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(os.path.join('images/', format(directory), '{}_labels.csv'.format(fruit)), index=None)
        # xml_df.to_csv(os.path.join('images/', '{}_labels.csv'.format(directory)), index=None)
        print('Successfully converted xml to csv.')
    merge()

def merge():
  for directory in ['test', 'train']:
    path = 'images/{}'.format(directory)
    all_files = glob.glob(os.path.join(path, '*_labels.csv'))
    df_merged = pd.concat(pd.read_csv(f) for f in all_files)
    df_merged.to_csv('images/{}.csv'.format(directory))
    
    for file in all_files:
      os.remove(file)

main()
