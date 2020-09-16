### Reference: 
https://www.pyimagesearch.com/2018/09/24/opencv-face-recognition/
https://github.com/Ravi-Singh88/Face-Recognition-OpenCV-Facenet/blob/master/extract_embeddings.py
https://github.com/bhavyanth7777/RealTimeFacialRecognition_AI_Project


### Terminal run by steps:


#### Step 1
```
python3 extract_embeddings.py --dataset dataset \
	--embeddings output/embeddings.pickle \
	--detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7
```	

#### Step 2
```
python3 train_model.py --embeddings output/embeddings.pickle \
  	--recognizer output/recognizer.pickle \
  	--le output/le.pickle
```	  

#### Step 3 - Image and Video of recognition
```
python3 recognize.py --detector face_detection_model \
  	--embedding-model openface_nn4.small2.v1.t7 \
  	--recognizer output/recognizer.pickle \
  	--le output/le.pickle \
  	--image images/vu.jpg

python3 recognize_video.py --detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7 \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle
```	
