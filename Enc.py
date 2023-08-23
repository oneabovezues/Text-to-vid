from PIL import Image
import cv2
import numpy
import argparse as ap
import tqdm

#parse terminal argument
Parser = ap.ArgumentParser(description='Script for converting text files to video')

Parser.add_argument('--filepath',type=str,help='File path of text file')
Parser.add_argument('--output',type=str,help='Name of output file',default='Output')
Parser.add_argument('--dimension',type=list,help='Dimension of the video in form of array,(height,width,fps)',default=[1000,1000,60])

args = Parser.parse_args()

#accepts string returns binary(unicode 7byte)
def textToBIn(text):   
    arr =[]
    for char in tqdm.trange(len(text)):
        if text[char] != ' ':
            arr.append(format(ord(text[char]),'07b'))
    return ''.join(arr)

#assigns pixel values to each binary value
def BinToPixel(Bin):
    
    key = {'1': (255, 255, 255), '0': (0, 255, 0)}
    converted_array = [key[value] for value in Bin]
    
    return converted_array

#creates video 
def VideoFromPixel(pixelArr,outputname,height,width,fps):

    #setup video specs
    framedata = height*width
    out = cv2.VideoWriter(outputname+'.mkv',cv2.VideoWriter_fourcc(*'FFV1'),fps,(height,width),isColor=True)
    
    #assign frame data
    if(len(pixelArr) > framedata):
        
        MultiPixelArr = [pixelArr[i:i+framedata] for i in range(0,len(pixelArr),framedata)]
        print('Frames proccessing:')
        for i in tqdm.trange(len(MultiPixelArr)):
            img = Image.new('RGB',(height,width),color=(0,0,0))
            img.putdata(MultiPixelArr[i])
            numpyObj = numpy.asarray(img)
            out.write(numpyObj)

    else:
        img = Image.new('RGB',(height,width),color=(0,0,0))
        img.putdata(pixelArr)
        img.save(outputname+'.jpeg')
    out.release()
    print('Video processed')

#error handling(or lack thereof)
try:
    file = open(args.filepath)
    print(args)
except Exception as e:
    print(e)
else:
    bin = textToBIn(file.read())
    pixels = BinToPixel(bin)
    VideoFromPixel(pixels,args.output,args.dimension[0],args.dimension[1],args.dimension[2])
    
