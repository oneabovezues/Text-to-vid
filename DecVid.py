
import cv2 
import numpy as np
import tqdm


Cap = cv2.VideoCapture('output.mkv')
total_frames = int(Cap.get(cv2.CAP_PROP_FRAME_COUNT))

result = []
for i in tqdm.trange(total_frames):
    
    ret,frame = Cap.read()
    if not ret:
          print(ret)
          break
    npdata = frame.reshape(frame.shape[0]*frame.shape[1],frame.shape[2])
    mapping = np.all (npdata == [255, 255, 255], axis=1).astype(int).astype(str)
    result.append(mapping)


resultnd = np.array(result)
result1D = np.reshape(resultnd,resultnd.shape[0]*resultnd.shape[1])

 
with open('output.txt','w') as file:
     for entry in tqdm.trange(0,len(result1D),7):
           file.write(chr(int(''.join(result1D[entry:entry+7]),2))) 