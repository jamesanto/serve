#!/bin/bash
set -x

TEST_DIR=./ts/torch_handler/unit_tests
case $PWD/ in
  *ts/torch_handler/unit_tests/) echo "Running tests";;
  *) echo "Error! Must start in unit_tests directory"; exit 1;;
esac

cd ../../../

test_image_classifier () {
  wget -nc -q -O \
    $TEST_DIR/models/tmp/model.pt \
    https://download.pytorch.org/models/resnet152-b121ed2d.pth

  cp -r examples/image_classifier/resnet_152_batch/* $TEST_DIR/models/tmp
  python -m pytest $TEST_DIR/test_image_classifier.py
}

test_mnist_classifier () {

  cp -r examples/image_classifier/mnist/* $TEST_DIR/models/tmp
  python -m pytest $TEST_DIR/test_mnist_kf.py
}



test_image_segmenter () {
  wget -nc -q -O \
    $TEST_DIR/models/tmp/model.pt \
    https://download.pytorch.org/models/fcn_resnet101_coco-7ecb50ca.pth
  cp -r examples/image_segmenter/fcn/* $TEST_DIR/models/tmp
  python -m pytest $TEST_DIR/test_image_segmenter.py
}

test_envelope () {
  python $TEST_DIR/models/base_model.py
  mv base_model.pt $TEST_DIR/models/tmp/model.pt
  cp $TEST_DIR/models/base_model.py $TEST_DIR/models/tmp/model.py
  python -m pytest $TEST_DIR/test_envelopes.py
}

test_object_detector () {
  wget -nc -q -O \
    $TEST_DIR/models/tmp/model.pt \
    https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth
  cp -r examples/object_detector/fast-rcnn/* $TEST_DIR/models/tmp
  python -m pytest $TEST_DIR/test_object_detector.py
}

test_envelope
test_image_classifier
test_image_segmenter
test_object_detector
test_mnist_classifier
