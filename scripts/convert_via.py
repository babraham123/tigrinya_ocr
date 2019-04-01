#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to convert via segmentation output json to classsification training files.

from dh_segment.io import via

collection = 'mycollection'
annotation_file = 'via_annontations.json'
masks_dir = './masks'
images_dir = './train'

def main():
    # Load all the data in the annotation file
    # (the file may be an exported project or an export of the annotations)
    # via_data = via.load_annotation_data(annotation_file)

    # In the case of an exported project file, you can set ``only_img_annotations=True``
    # to get only the image annotations
    via_annotations = via.load_annotation_data(annotation_file, only_img_annotations=True)

    # Collect the annotated regions
    working_items = via.collect_working_items(via_annotations, collection, images_dir)

    # Collect the attributes and options
    if '_via_attributes' in via_data.keys():
        list_attributes = via.parse_via_attributes(via_data['_via_attributes'])
    else:
        list_attributes = via.get_via_attributes(via_annotations)

    # Create one mask per option per attribute
    via.create_masks(masks_dir, working_items, list_attributes, collection)
    print('Created masks. {} regions, {} attributes.'.format(len(working_items), len(list_attributes)))


if __name__ == '__main__':
    main()
