import Image
import numpy as np
import colorsys

'''colors here are taken directly from Warhol's Che Guevara serigraph
(in order left to right, top to bottom)'''
colorset = [ 
    {
        'bg' : (255,255,0,255),
        'fg' : (50,9,125,255),
        'skin': (118,192,0,255)
    },
    {
        'bg' : (0,122,240,255),
        'fg' : (255,0,112,255),
        'skin': (255,255,0,255)
    },
    {
        'bg' : (50,0,130,255),
        'fg' : (255,0,0,255),
        'skin': (243,145,192,255)
    },
    {
        'bg' : (255,126,0,255),
        'fg' : (134,48,149,255),
        'skin': (111,185,248,255)
    },
    {
        'bg' : (255,0,0,255),
        'fg' : (35,35,35,255),
        'skin': (255,255,255,255)
    },
    {
        'bg' : (122,192,0,255),
        'fg' : (255,89,0,255),
        'skin': (250,255,160,255)
    },
    {
        'bg' : (0,114,100,255),
        'fg' : (252,0,116,255),
        'skin': (250,250,230,255)
    },
    {
        'bg' : (250,255,0,255),
        'fg' : (254,0,0,255),
        'skin': (139,198,46,255)
    },
    {
        'bg' : (253,0,118,255),
        'fg' : (51,2,126,255),
        'skin': (255,105,0,255)
    }
]

def darken_bg(image, color):
    '''composite image on top of a single-color image, effectively turning all
    transparent parts to that color'''
    color_layer = Image.new('RGBA', image.size, color) 
    masked_image = Image.composite(image, color_layer, image)
    return masked_image

def color_bg_fg(image, bg_color, fg_color):
    '''change transparent background to bg_color and change
    everything non-transparent to fg_color'''
    fg_layer = Image.new('RGBA', image.size, fg_color)
    bg_layer = Image.new('RGBA', image.size, bg_color) 
    masked_image = Image.composite(fg_layer, bg_layer, image)
    return masked_image

def color_to_color(image, src_color, dest_color, distance):
    '''change all colors close to src_color to be dest_color. 
    distance defines how close the color values have to be (from 0 to 255)'''
    arr=np.array(np.asarray(image))
    sr, sg, sb, sa = src_color # sr => source red, and so on
    r,g,b,a=np.rollaxis(arr,axis=-1)    
    mask=(  (np.abs(r-sr) <= distance)
          & (np.abs(g-sg) <= distance)
          & (np.abs(b-sb) <= distance)
          )
    arr[mask]=dest_color
    image=Image.fromarray(arr,mode='RGBA')
    return image

def white_to_color(image, color):
    '''change all colors close to white and non-transparent
    (alpha > 0) to be color.'''
    threshold=50
    dist=10
    arr=np.array(np.asarray(image))
    r,g,b,a=np.rollaxis(arr,axis=-1)    
    mask=((r>threshold)
          & (g>threshold)
          & (b>threshold)
          & (np.abs(r-g)<dist)
          & (np.abs(r-b)<dist)
          & (np.abs(g-b)<dist)
          & (a>0)
          )
    arr[mask]=color
    image=Image.fromarray(arr,mode='RGBA')
    return image

def make_warhol_single(image, bg_color, fg_color, skin_color, 
                       skin_src_color, skin_dist):
    '''create a single warhol-serigraph-style'''
    bg_fg_layer = color_bg_fg(image, bg_color, fg_color)
    bg_fg_layer.save('example/0-bg_fg_layer.png')
    temp_dark_image = darken_bg(image, (0,0,0,255))
    temp_dark_image.save('example/1-temp_dark_image.png')
    skin_mask = color_to_color(temp_dark_image,skin_src_color,(0,0,0,0),skin_dist)
    skin_mask.save('example/2-skin_mask.png')
    skin_layer = Image.new('RGBA', image.size, skin_color) 
    skin_layer.save('example/3-skin_layer.png')
    out = Image.composite(bg_fg_layer, skin_layer, skin_mask)
    out.save('example/4-out.png')
    return out

def test_warhol(image_file):
    '''create a single colored image and display it'''
    im = Image.open(image_file).convert('RGBA')
    color = colorset[0]
    bg = color['bg']
    fg = color['fg']
    skin = color['skin']
    make_warhol_single(im, bg, fg, skin).show()

#(255,205,132,255)

def warholify(image_file, skin_src_color, distance):
    im = Image.open(image_file).convert('RGBA')

    warhols = []
    for colors in colorset:
        bg = colors['bg']
        fg = colors['fg']
        skin = colors['skin']
        warhols.append(make_warhol_single(im, bg, fg, skin, 
                       skin_src_color, distance))

    x = im.size[0]
    y = im.size[1]

    blank_image = Image.new("RGB", (x*3, y*3))
    blank_image.paste(warhols[0], (0,0))
    blank_image.paste(warhols[1], (x,0))
    blank_image.paste(warhols[2], (x*2,0))
    blank_image.paste(warhols[3], (0,y))
    blank_image.paste(warhols[4], (x,y))
    blank_image.paste(warhols[5], (x*2,y))
    blank_image.paste(warhols[6], (0,y*2))
    blank_image.paste(warhols[7], (x,y*2))
    blank_image.paste(warhols[8], (x*2,y*2))

    blank_image.save('nine_weasels.png')

