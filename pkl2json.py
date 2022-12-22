import os
import json
import pickle
import numpy


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


out = pickle.load(open(
    '/home/umutlu/AI-City-Anomaly-Detection/extension/mmdetection/results_test_processed.pkl','rb'))
img_names = []

with open('/media/data/umutlu/AIC20_track4/test_processed_images_info.json','r') as f:
  for line in f:
      data = json.loads(line)
      img_names.append(data["filename"])
imgs = {}
for i in range(1,101):
  imgs[str(i)]={}

for i,name in enumerate(img_names):
    tmp_box = out[i][0]
    if len(tmp_box)>0:
        video = name.split('/')[0]
        img_name = name.split('/')[-1]
        frame = img_name.split('_')[0]+'.jpg'
        j = img_name.split('_')[1].split('.')[0]
        if frame not in imgs[video]:
            imgs[video][frame] = {"4":[]}
        for box in tmp_box:
            imgs[video][frame][j].append([box[:4].tolist(),box[4]])
for i in range(1,101):
  with open('../detection_results/test_static_2/video'+str(i)+'.json','w+') as f:
    json.dump(imgs[str(i)],f,cls=MyEncoder)

out = pickle.load(open('/home/umutlu/AI-City-Anomaly-Detection/extension/mmdetection/results_test_subset_ori.pkl','rb'))
img_names = []
with open('/media/data/umutlu/AIC20_track4/subset_test_ori_images_info.json','r') as f:
  for line in f:
      data = json.loads(line)
      img_names.append(data["filename"])
imgs = {}
for i in range(1,101):
  imgs[str(i)]={}
for i,name in enumerate(img_names):
    tmp_box = out[i][0]
    if len(tmp_box)>0:
      video = name.split('/')[0]
      img_name = name.split('/')[-1]
      frame = img_name
      if frame not in imgs[video]:
          imgs[video][frame] = []
      for box in tmp_box:
        if box[4]>0.1:
          imgs[video][frame].append(box[:5].tolist())
for i in range(1,101):
  with open('../detection_results/test_framebyframe_2/video'+str(i)+'.txt','w') as f:
    imgs_ = imgs[str(i)]
    for img in imgs_:
        for box in imgs_[img]:
            if box is None:
                continue
            else:
                f.write("%d,-1,%d,%d,%d,%d,%.4f,-1,-1,-1\n"%(int(img.split('.')[-2]),box[0],box[1],box[2]-box[0]+1,box[3]-box[1]+1,box[4]))
