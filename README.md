## **README**

### **Advanced Lane Finding - An Exercise in Computer Vision**

#### **Victor Roy**

[GitHub Link](https://github.com/soniccrhyme/SDND-Vehicle_Detection)

[//]: # (Image References)

[example_frame]: ./report_images/example_frame.png "Example Frame"
[color_map_comp]: ./report_images/color_space_comp.png "BBoxes & Color Maps"
[bboxes_ycc]: ./report_images/bboxes_ycc.png "BBoxes for YCbCr Color Map"
[heatmap_eg]: ./report_images/heatmap_example.png "Heatmap Example"
[labels_eg]: ./report_images/labels_example.png "Labels Example"
[output_eg]: ./report_images/output_example.png "Output Example"

---
### Brief Project Description

This code detects and tracks other cars on the road that are visible from the front-center mounted dashboard camera stream. Classification made use of color histogram, spatial, and Histogram of Oriented Gradients (HOG) features.

A classifier was trained on pre-labeled images pulled from the [GTI vehicle image database](http://www.gti.ssr.upm.es/data/Vehicle_database.html) and the [KITTI vision benchmark suite](http://www.cvlibs.net/datasets/kitti/). An [XGBooost](https://xgboost.readthedocs.io/) classifier was chosen because of its speed and accuracy (a validation f score of 99.2%).

### Histogram of Oriented Gradients

#### 1. Explain how (and identify where in your code) you extracted HOG features from the training images.

HOG features are extracted via ```get_hog_features``` method found in ```Input[4]``` utilizing [scikit-image's hog function](http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_hog.html). Training features are extracted via the ```extract_features``` method found in ```Input[5]```; this method is tailored for when the input images are all the same size, and no further sliding window search is required.

#### 2. Explain how you settled on your final choice of HOG parameters.

Final HOG parameters were chosen through a method of trial and error, with the priorities being both a low false-positive rate and overall processing speed. While these priorities work against each other, the final set of parameters (found in ```Input[11]```) was found to achieve a good balance

#### 3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

The pipeline for classifier training is found in ```Input[6 & 7]```. Before training the classifier, it is necessary to run ```import_images.py``` which loads each of the training images, scales them, then converts them into the appropriate color map, and then pickles the array of images and their respective labels. These images and labels are loaded, features are extracted from the images, and then an XGBoost classifier is trained on those features.

### Sliding Window Search

#### 1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?

The code for the sliding window search is implemented in ```Input???``` via the function ```find_windows```; this function is takes motivation from the HOG subsample code used in Udacity's Vehicle Detection lesson. The boon of this function is that HOG features, which are expensive to calculate, need only be calculated once for the whole image.

The different scales determine the size of the window in the sliding window search: a scale of 1 means a 64x64 pixel window; a scale of 1.5 means a 96x96 pixel window; a scale of 2 means a 128x128 pixel window; and so on. I decided to use windows of heights (and widths) of 64, 96, and 128 pixels. Simply looking at various frames wherein other cars on the road, one of these size blocks usually encapsulates a large portion of the car, if not the whole car itself.

The overlap was determined, again, by both trial and error and empirical sampling of some choice observations. It seemed that the smaller the window (i.e. the further away the car) worked best with larger overlaps, while larger windows worked fine with smaller overlaps. Overlaps are determined by a parameter called ```cells_per_step``` defined in ```Input???``` and utilized in ```find_windows```

#### 2. Show some examples of test images to demonstrate how your pipeline is working.  What did you do to optimize the performance of your classifier?

The pipeline takes in a frame from a video stream; a frame would look something like this:  

![Example Frame][example_frame]

Then, a sliding window search is conducted where features are generated for each window, and then the classifier predicts whether a car is present within that window. Here is an example of bounding windows (boxes) that were identified as having a car, shown when converting the image into different color maps:

![Windows with Cars & Color Map Comparison][color_map_comp]

This and a few other tests showed that, in most cases, the YCbCr color space was most useful for vehicle detection:

![Positive Bounding Boxes for Example Frame using YCbCr Color Space][bboxes_ycc]

Next, a heatmap is created, where a pixel's value is how many boxes is contain that pixel:

![Heatmap Example][heatmap_eg]

The heatmap is thresholded, and then scipy's label function is used to determine how many distinct areas there are in the image:

![Labels Example][labels_eg]

And finally, the output image is created by outlining the extremes of each label's respective area:

![Output Example][output_eg]



### Video Implementation

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)


#### 2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?
