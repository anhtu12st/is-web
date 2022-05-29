import cv2
import numpy as np
import time
import cv2
import numpy as np
from PIL import Image
import joblib # save / load model
from skimage.transform import pyramid_gaussian
from skimage.feature import hog

import imutils
from sklearn.preprocessing import scale


class NMS(object):
    def __init__(self, overlap_threshold=0.1):
        self.overlap_threshold = overlap_threshold

    def __call__(self, boxes, probs):
        return self.non_max_suppression_fast(boxes=boxes, probs = probs)

    def non_max_suppression_fast(self, boxes, probs):
        # if there are no boxes, return an empty list
        if len(boxes) == 0:
            return [], []
        # if the bounding boxes integers, convert them to floats --
        # this is important since we'll be doing a bunch of divisions
        if boxes.dtype.kind == "i":
            boxes = boxes.astype("float")

        # initialize the list of picked indexes
        keep = []

        # grab the coordinates of the bounding boxes
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        # rearrange the location boxes by confidence score
        order = probs.argsort()
       
        # compute the area of the bounding boxes and sort the bounding
        # boxes by the bottom-right y-coordinate of the bounding box
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        # keep looping while some indexes still remain in the indexes
        # list
        while len(order) > 0:
            # grab the last index in the indexes list and add the
            # index value to the list of picked indexes

            # last = len(idxs) - 1
            # i = idxs[last]
            i = order[-1]
            keep.append(i)
            order = order[:-1]
            if len(order) == 0:
              break
            # find the largest (x, y) coordinates for the start of
            # the bounding box and the smallest (x, y) coordinates
            # for the end of the bounding box
            xx1 = np.maximum(x1[i], x1[order])
            yy1 = np.maximum(y1[i], y1[order])
            xx2 = np.minimum(x2[i], x2[order])
            yy2 = np.minimum(y2[i], y2[order])

            # compute the width and height of the bounding box
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            IOU = area[order] + area[i] - (w * h)
            # compute the ratio of overlap
            overlap = (w * h) / area[order]
            # min(area[order], area[i])

            # delete all indexes from the index list that have
            # idxs = np.delete(idxs, np.concatenate(([last],
            #                                        np.where(overlap > overlapThresh)[0])))
            order = order[np.where(overlap < self.overlap_threshold)]
      
        # return only the bounding boxes that were picked using the
        # integer data type

        return boxes[np.array(keep)].astype("int"), probs[np.array(keep)]

class ObjectDetector(object):
    def __init__(self, model_path = None, width = 64, height = 128, nms_threshold = 0.4, human_threshold = 0.7, cnn_model = 0):
      self.window_width = width
      self.window_height = height
      self.window_step = 16
      if model_path != None: 
        self.svm_model = joblib.load(model_path)
      self.cnn_model = cnn_model
      self.nms = NMS(nms_threshold)
      self.prob_threshold = human_threshold



    def read_image_with_pillow(self, img_path, is_gray=True):
        pil_im = Image.open(img_path).convert('RGB')
        img = np.array(pil_im) 
        img = img[:, :, ::-1].copy()  # Convert RGB to BGR 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img
    
    def fit_svm(self, f):
        # predict
        pred_y1 = self.svm_model.predict(np.array([f]))
        pred_y = self.svm_model.predict_proba(np.array([f]))[0]
        # class_probs = pred_y[0]
        # max_class, max_prob = max(enumerate(class_probs), key=operator.itemgetter(1))
        if pred_y[1]  > pred_y[0]: 
        # is_person = max_class == 1
          is_person=1
        else: 
          is_person=0
        return is_person, pred_y[1]

    def sliding_window(self, img_path): 
        if self.cnn_model != 0: 
          img = cv2.imread(img_path)
        else:
          img = self.read_image_with_pillow(img_path=img_path, is_gray=True)
        minAxis_Image = 250
        img = imutils.resize(img, width=min(minAxis_Image, img.shape[1]))

        h, w = img.shape[:2]        
        n_windows = 0
        boxes = []
        probs = []
        i=0
        # print(img)
        for img_scale in pyramid_gaussian(img, downscale=1.2, channel_axis=True):
          # img_scale=img/255
          if img_scale.shape[0] < self.window_height or img_scale.shape[1] < self.window_width:
              break
          # if (i>0):
          #   break
          new_height, new_width = img_scale.shape[:2]
          new_img = np.copy(img_scale.astype('float32'))
          # add='./images/scale'+str(i)+'.jpg'
          # print(img_scale)
          i+=1
          # cv2.imwrite(add, img_scale)
          max_x = new_width - self.window_width
          max_y = new_height - self.window_height


          # print('Scale (h=%d, w=%d)' % (new_height, new_width))
          
          x = 0
          y = 0
          
          while y <= max_y:
              while x <= max_x:
                  n_windows += 1
                  patch = new_img[y:y+self.window_height,x:x+self.window_width]
                  if self.cnn_model == 0: 
                    f = hog(patch)
                    is_person, prob = self.fit_svm(f)
                  else: 
                    prob = self.cnn_model.predict(np.array([patch]))[0][0]
                    is_person = 1 if prob > self.prob_threshold else 0

                  if is_person and prob > self.prob_threshold:
                      x1 = int(x/new_width*w)
                      y1 = int(y/new_height*h)
                      x2 = int((x+self.window_width)/new_width*w)
                      y2 = int((y+self.window_height)/new_height*h)
                      boxes.append(np.array([x1, y1, x2, y2]))
                      probs.append(prob)

                  x += self.window_step
                  pass
              x = 0
              y += self.window_step
              pass                
          pass
        return (boxes, probs, n_windows)
          



    def __call__(self, img_path):
        # time_start = time.time()
        (boxes, probs, n_windows) = self.sliding_window(img_path)
        print("Count boxes "+str(len(boxes)))
        boxes, probs = self.nms(np.array(boxes), np.array(probs))
        d_img = cv2.imread(img_path)
        minAxis_Image = 250
        d_img = imutils.resize(d_img, width=min(minAxis_Image, d_img.shape[1]))

        for box, prob in zip(boxes, probs):
            # print(prob)
            # print(box)
            d_img = cv2.rectangle(d_img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(d_img, str(round(float(prob), 2)), (box[0], box[1]-5), cv2.FONT_HERSHEY_SIMPLEX, min(self.window_width,self.window_height)/(250), (36,255,12), 1)

        # time_end = time.time()
        # print('Processed %d windows in %.2f seconds' % (n_windows, time_end-time_start))
        return d_img