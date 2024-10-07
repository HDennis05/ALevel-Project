from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import customtkinter
from classes import *

def moreInfoColour(image):
    """
    Parameters: image - Image to be worked on
    Takes an image works out the colour of four pixels and calculates an average
    This colour is used as the background to a button which will be overlaid on the image.
    Returns colour in Hex notation
    """
    def convert(rgb):
        """
        Parameters: rgb - colour in rgb notation
        Converts rbg colours to hex colours
        """
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'


    pix = image.load()

    xs = [340,430,340,430]
    ys = [210,210,240,240]

    colours=[]
    rTotal = 0
    gTotal = 0
    bTotal = 0
    for n in range(0,len(xs)):
        x=xs[n]
        y=ys[n]
                              
        pixels = pix[x,y]
        rTotal += pixels[0]
        gTotal += pixels[1]
        bTotal += pixels[2]
        colours.append([pixels[0],pixels[1],pixels[2]])

    colour = [rTotal//4, gTotal//4, bTotal//4]

    return convert(colour)


def curveCorners(im,size):
    """
    Parameters: im - Image to have the corners curved
                size - The size of the image to have the corners curved, eg. "big","normal","mini"
    Takes an image and its size and utilises alpha masking to curve the corners and make them transparent
    Returns new image
    """
    if size == "big":
        w=450
        h=260
        rad=50

    if size == "normal":
        w=140
        h=140
        rad=20

    if size == "mini":
        w=70
        h=70
        rad=10

    #black square
    circle = Image.new('L', (rad*2, rad*2), 0)
    draw = ImageDraw.Draw(circle)
    #white circle leaving black corners
    draw.ellipse((0, 0, rad*2, rad*2), fill=255)

    #image for alpha channel
    alpha = Image.new('L', (w,h), 255)
    
    #paste the black corners onto alpha image
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad*2)), (0, h-rad))
    alpha.paste(circle.crop((rad, 0, rad*2, rad)), (w-rad, 0))
    alpha.paste(circle.crop((rad, rad, rad*2, rad*2)), (w-rad, h-rad))

    #uses alpha as mask for transparency
    im.putalpha(alpha)

    return im

