# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

class String2emoji(object):
    """docstring for String2emoji"""
    def __init__(self, argText,argFontName,argFontColor = (0,0,0,255),argBackColor = (255,255,255,0)):
        self.textList = argText
        self.fontName = argFontName
        self.backColor = argBackColor
        self.imageSize = (128,128)
        self.fontColor = argFontColor


    def getFont(self,size):
        return ImageFont.truetype(self.fontName, size, encoding='utf-8')

    def setBackColor(self,color):
        self.backColor = color

    def setFontColor(self,color):
        self.fontColor = color
    def cutEffectiveRange(self,text,wMax,hMax):
        wt, ht = self.getFont(hMax).getsize(text)
        if wt > wMax :
            wMax = wt
        hMax0 = hMax
        while self.getFont(hMax0).getsize(text)[1] > hMax :
            hMax0 = hMax0 - 1

        for i in range(hMax0,hMax0*3):
            font = self.getFont(i)
            w, h = font.getsize(text)
            img = Image.new("RGBA",(w,h),self.backColor)
            draw = ImageDraw.Draw(img)
            draw.text((0,0), text, fill=self.fontColor, font=font)
            x0 = self.stringOverBorderX(img,text,font,h)
            y0 = self.stringOverBorderY(img,text,font,w)
            x1 = self.stringUnderBorderX(img,text,font,w,h) + x0
            y1 = self.stringUnderBorderY(img,text,font,h,w) + y0
            if ((x1 >= wMax-2) and (x1 < wMax)) or ((y1 >= hMax-2) and (y1 < hMax)) :
                return (i,x0,y0,x1,y1)
    def stringOverBorderX(self,img,text,font,h):
        for x in range(0,-255,-1):
            limitFlag = 0
            for i in range(0,h-1):
                color = img.getpixel((-x,i))
                if color != self.backColor:
                    limitFlag = 1;
            if limitFlag > 0:
                return x
    def stringOverBorderY(self,img,text,font,w):
        for y in range(0,-255,-1):
            limitFlag = 0
            for i in range(0,w-1,2):
                color = img.getpixel((i,-y))
                if color != self.backColor:
                    limitFlag = 1;
            if limitFlag > 0:
                return y
    def stringUnderBorderX(self,img,text,font,w,h):
        for cx in range(w-1,0,-1):
            for cy in range(0,h-1):
                color = img.getpixel((cx,cy))
                if color != self.backColor:
                    return cx
    def stringUnderBorderY(self,img,text,font,h,w):
        for cy in range(h-1,0,-1):
            for cx in range(0,w-1,2):
                color = img.getpixel((cx,cy))
                if color != self.backColor:
                    return cy

    def getEmoji(self):
        img = Image.new("RGBA",self.imageSize,self.backColor)
        draw = ImageDraw.Draw(img)
        l = len(self.textList)

        if self.fontColor == self.backColor:
            draw.rectangle([(0,0),self.imageSize],fill=self.backColor)
            return img

        for i in range(0,l):
            if not self.textList[i]:
                continue
            img_str = Image.new("RGBA",(int(len(self.textList[i])*256/l),128),self.backColor)
            draw = ImageDraw.Draw(img_str)
            (size,x0,y0,x1,y1) = self.cutEffectiveRange(self.textList[i],len(self.textList[i])*256/l,int(127/l))
            #(size,x0,y0,x1,y1) = self.cutEffectiveRange(self.textList[i],256,128/l)
            font = self.getFont(size)
            draw.text((x0,y0), self.textList[i], fill=self.fontColor, font=font)
            img_str.crop((0,0,x1,y1))
            if x1 > 127:
                img_str = img_str.transform(img_str.size,Image.AFFINE,(x1/127.0,0,0,0,1,0),Image.BILINEAR)
                image_paste_x = 0
            else:
                image_paste_x = int((127-x1)/2)
                #image_paste_x = 0
            if l != 1:
                img.paste(img_str,(image_paste_x,int((127/l)*i+abs((127/l)-y1)*0.5)))
            else:
                img.paste(img_str,(image_paste_x,int((127-y1)/2)))
        return img