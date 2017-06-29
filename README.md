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
[smooth_output_eg]: ./report_images/smooth_output_example.png "Smooth Output Example"

---
### Project Files

- ```Vehicle_Tracker.ipynb``` - jupyter notebook contains the bulk of the pipeline and requisite functions
- ```tracker.py``` - ``Tracker()`` class definition, used for smoothing across frames
- ```input_images.py``` - run first; reads in training images and converts to parameter defined color space; resultant array of images is pickled along with respective labels. Training images can be found at [Udacity's project github](https://github.com/udacity/CarND-Vehicle-Detection)
- ```project_video.mp4``` - video input to be processed
- ```result.mp4``` - output video from processing ```project_video.mp4``` via pipeline in ```Vehicle_Tracker.ipynb```

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

Processing single frames yields bounding boxes which abruptly change from frame to frame. This can be mitigated by smoothing heatmaps over several frames (discussed further in Video Implementation, Question 2). The boxes yielded by smoothing across frames can be seen below (same frame, taken from result.mp4, largely similar result):

![Smoothed Output Example][smoothed_output_eg]



#### 3. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

False positives were few. Increasing the heatmap threshold incurs a tradeoff between limiting false positives and exasperating fasle negatives. Luckily, the XGBoost classifier performs extremely well, achieving an f1-score of 99.2% when the YCbCr color space is used.

Still, a few false positives peaked through, especially when the video goes over the bridge. Another problem was that when the pipeline processed one frame at a time, the bounding boxes were jump with each frame. Both the problem of false positives as well as the jumpy bounding boxes are ameliorated by averaging heatmaps over several frames. This was done by invoking a simple ```Tracker()``` class (found in tracker.py), which had a lone property, ```self.recent_heatmaps```.


### Video

Project Video: [GitHub](https://github.com/soniccrhyme/SDND-Vehicle_Detection/blob/master/result.mp4)  


### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Few problems & challenges:

- Processing Speed: as written, the vehicle detection method runs at about 2.50 seconds per frame; if its to run in real time, it would need to be 50-100x faster (depending on the frame-rate of the incoming video). This might be achieved several ways: 1) by limiting the sliding window search to the edges of the video and around previous vehicle detections; 2)
- That white car!! - after the second bridge, there are a few seconds (more than I'd care to explicitly number) where the white car is not detected at all. I noticed that in this particular circumstance, the RGB color space did better than the YCbCr; a solution might thus involve using multiple color spaces as opposed to just one. I avoided this step because it would've nearly doubled the amount of time it would take to process each frame. Another possible solution is just to train the classifier on images of the white car directly from the video feed - for real autonomous vehicle projects, this may very well be a better long-run solution, especially since in-car computation time is much more limited.  
- As the lapse with the white car showed, the pipeline seems to have a harder time detecting cars that are either further away or exhibit lower contrast with their surroundings. Shadows, cloud cover and cityscapes might represent scenarios in which this pipeline will likely fail. As written, I don't imagine it would fare too well in the dark, either.
- The pipeline still generates a few false positives, most notably on the first bridge, where it detects a vehicle in part of the guardrail (and maybe detects one or two cars coming in the opposite direction). Smoothing across several frames didn't make these false-positives disappear. Reducing the incidence of false positives may be achieved by adding more training images, or perhaps by adding more features (more color spaces, more orientation bins for HOG features, etc).
- As written, the pipeline doesn't really utilize object-oriented programming. I have made a single class (```Tracker()```), with one property (```self.recent_heatmaps```), but that's a half-measure. The code still uses global variables and such. Ideally, I would like to make the pipeline more OO, thus more inline with best practices and, hopefully, more elegant.
-
