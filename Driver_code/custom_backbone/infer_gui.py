import os
import json
import argparse
import matplotlib.pyplot as plt

from visual_tools import GuiInferenceViewer

# Import your custom backbone
from matterport_resnet import ResNet50, ResNet101, preprocess_input

# You can add or override existing backbone model
# and corresponding preprocessing function as follows:
from classification_models import Classifiers
Classifiers._models.update({
    'resnet50': [ResNet50, preprocess_input],
    'resnet101': [ResNet101, preprocess_input],
})

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Run Mask R-CNN detector.')

    parser.add_argument('-c', '--model_cfg', required=False,
                        default='MaskRCNN_coco.cfg',
                        metavar='/path/to/MaskRCNN_coco.cfg',
                        help='Path to MaskRCNN_coco.cfg file')
    parser.add_argument('-i', '--image_dir', required=False,
                        default='images',
                        metavar='/path/to/directory',
                        help='Path to a directory containing images')
    parser.add_argument('-w', '--weights', required=False,
                        default='MaskRCNN_coco.h5',
                        metavar='/path/to/MaskRCNN_coco.h5',
                        help='Path to maskrcnn weights.h5 file')
    parser.add_argument('-t', '--threshold', required=False,
                        type=float,
                        default=0.5,
                        metavar='Threshold value for inference',
                        help='Must be between 0 and 1.')
    parser.add_argument('-l', '--label', required=False,
                        type=str,
                        default='coco_class_names.json',
                        metavar='/path/to/coco_class_names.json',
                        help='Path to class json file')
    args = parser.parse_args()

    assert args.threshold >= 0.0 and args.threshold < 1.0, \
        'Invalid threshold value {} given'.format(args.threshold)

    if args.label is not None:
        assert os.path.exists(args.label)
        fp = open(args.label, 'r')
        coco_class = json.load(fp)
        fp.close()
    else:
        coco_class = None

    viewer = GuiInferenceViewer(args.image_dir, args.model_cfg, args.weights, args.threshold, coco_class)
    plt.show()
