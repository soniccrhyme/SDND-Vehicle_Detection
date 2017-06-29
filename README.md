## **README**

### **Advanced Lane Finding - An Exercise in Computer Vision**

#### **Victor Roy**

[GitHub Link](https://github.com/soniccrhyme/SDND-Vehicle_Detection)

[//]: # (Image References)


---
### Brief Project Description

This code detects and tracks other cars on the road that are visible from the front-center mounted dashboard camera stream. Classification made use of color histogram, spatial, and Histogram of Oriented Gradients (HOG) features.

A classifier was trained on pre-labeled images pulled from the [GTI vehicle image database](http://www.gti.ssr.upm.es/data/Vehicle_database.html) and the [KITTI vision benchmark suite](http://www.cvlibs.net/datasets/kitti/). An [XGBooost](https://xgboost.readthedocs.io/) classifier was chosen because of its speed and accuracy (a validation f score of 99.2%).

### Histogram of Oriented Gradients

#### 1. Explain how (and identify where in your code) you extracted HOG features from the training images.

HOG features are extracted via ```get_hog_features``` method found in Input[4] utilizing [scikit-image's hog function](http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_hog.html). Training features are extracted via the ```extract_features``` method found in Input[5]; this method is tailored for when the input images are all the same size, and no further sliding window search is required. 

#### 2. Explain how you settled on your final choice of HOG parameters.

#### 3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

### Sliding Window Search

#### 1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?

#### 2. Show some examples of test images to demonstrate how your pipeline is working.  What did you do to optimize the performance of your classifier?

### Video Implementation

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)


#### 2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?
