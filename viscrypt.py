import random
import PIL.Image

class Image():

    def __init__(self,path):

        pixels = png_to_str(path);
        self.pixels = pixels.split('\n');

        if self.pixels[0] == '':
            self.pixels = self.pixels[1:];
        
##        nr_pixels = len(string)/pixelsize;
##        for n in range(nr_pixels):
##
##            pixelstring = string[n:pixelsize];
##            print(pixelstring);
##            self.pixels.append(Pixel[pixelstring]);

class Sheetpixel():

    def __init__(self,nr_black=None,partner=None,total_black=None):

        self.pixelsize = 4;
        self.subpixels = '';

        if total_black != None:

            partner_nr_black = partner.subpixels.count('x');

            if total_black == 4 and nr_black == 2:

                if partner_nr_black == 2:
                    for other_subpixel in partner.subpixels:
                        if other_subpixel == 'x':
                            self.subpixels += '.';
                        else:
                            self.subpixels += 'x';
                elif partner_nr_black == 3:
                    self.subpixels = partner.subpixels;
                    self.subpixels = self.subpixels.replace('.','@',1);
                    self.subpixels = self.subpixels.replace('x','.',2);
                    self.subpixels = self.subpixels.replace('@','x',1);
 
            elif total_black == 2 and nr_black == 2:

                if partner_nr_black == 2:
                    self.subpixels = partner.subpixels;
                elif partner_nr_black == 3:
                    self.subpixels = partner.subpixels;
                    self.subpixels = self.subpixels.replace('@','.',1);                                                             

            elif total_black == 3 and nr_black == 3:

                if partner_nr_black == 2:
                    self.subpixels = partner.subpixels;
                    self.subpixels = self.subpixels.replace('.','x',1);                                                             
                elif partner_nr_black == 3:
                    self.subpixels = partner.subpixels;

            elif total_black == 3 and nr_black == 2:

                if partner_nr_black == 2:
                    self.subpixels = partner.subpixels;
                    self.subpixels = self.subpixels.replace('x','@',1);
                    self.subpixels = self.subpixels.replace('.','x',1);
                    self.subpixels = self.subpixels.replace('@','.',1);
                elif partner_nr_black == 3:
                    self.subpixels = partner.subpixels;
                    self.subpixels = self.subpixels.replace('x','.',1);

            elif total_black == 4 and nr_black == 3:

                if partner_nr_black == 2:
                    self.subpixels = partner.subpixels;
                    self.subpixels = self.subpixels.replace('x','@',1);
                    self.subpixels = self.subpixels.replace('.','x',2);
                    self.subpixels = self.subpixels.replace('@','.',1);
                elif partner_nr_black == 3:
                    self.subpixels = partner.subpixels;
                    self.subpixels = self.subpixels.replace('.','@',1);
                    self.subpixels = self.subpixels.replace('x','.',1);
                    self.subpixels = self.subpixels.replace('@','x',1);                
            
        else:
            self.subpixels = nr_black*'x'+(self.pixelsize-nr_black)*'.';

            #Randomly shuffle them
            sp = list(self.subpixels)
            random.shuffle(sp)
            self.subpixels = ''.join(sp);        

        self.nr_black = nr_black;

class Sheet():

    def __init__(self,pixels):
        self.pixels = pixels;

    def as_string(self):

        result = '';

        for line in self.pixels:
            
            upper = '';
            lower = '';

            for pixel in line:

                upper += pixel.subpixels[:2].strip();
                lower += pixel.subpixels[2:].strip();

            result += upper + '\n' + lower + '\n';

        return result;


    def __repr__(self):

        return self.as_string();

    def save(self,path):

        pixels = self.as_string().strip().split('\n');

        values = [];

        for line in pixels:
            
            result_line = [];

            for pixel in line:

                if pixel == 'x':

                    result_line.append((0,0,0));

                elif pixel == '.':

                    result_line.append((255,255,255));

            values.append(result_line);

        values_to_png(path,values);


def generate_sheets(image,cover1 = None,cover2 = None):

    sheet1 = Sheet([]);
    sheet2 = Sheet([]);

    for nl, line in enumerate(image.pixels):

        current_sheetline1 = [];
        current_sheetline2 = [];

        for np, imagepixel in enumerate(line):

            if imagepixel == '.':

                if cover1 != None:
                    if cover1.pixels[nl][np] == 'x':
                        pixel1 = Sheetpixel(nr_black=3);
                    elif cover1.pixels[nl][np] == '.':
                        pixel1 = Sheetpixel(nr_black=2);

                    if cover2.pixels[nl][np] == 'x':
                        pixel2 = Sheetpixel(nr_black=3,total_black=3,partner=pixel1);
                    elif cover2.pixels[nl][np] == '.':
                        pixel2 = Sheetpixel(nr_black=2,total_black=3,partner=pixel1);                   

                else:
                    pixel1 = Sheetpixel(nr_black=2);
                    pixel2 = Sheetpixel(nr_black=2,total_black=2,partner=pixel1);
                                
            elif imagepixel == 'x':

                if cover1 != None:
                    if cover1.pixels[nl][np] == 'x':
                        pixel1 = Sheetpixel(nr_black=3);
                    elif cover1.pixels[nl][np] == '.':
                        pixel1 = Sheetpixel(nr_black=2);

                    if cover2.pixels[nl][np] == 'x':
                        pixel2 = Sheetpixel(nr_black=3,total_black=4,partner=pixel1);
                    elif cover2.pixels[nl][np] == '.':
                        pixel2 = Sheetpixel(nr_black=2,total_black=4,partner=pixel1);                   
                        
                else:
                    pixel1 = Sheetpixel(nr_black=2);
                    pixel2 = Sheetpixel(nr_black=2,total_black=4,partner=pixel1);

            current_sheetline1.append(pixel1);
            current_sheetline2.append(pixel2);

        sheet1.pixels.append(current_sheetline1);
        sheet2.pixels.append(current_sheetline2);
        
    return sheet1,sheet2;

def png_to_str(path):

    im = PIL.Image.open(path+'.png')
    width, height = im.size;
    im = im.convert('RGB')
    pixels = im.load();

    string = '';

    for x in range(width):
        for y in range(height):

            pixel = pixels[x,y];

            if pixel == (255,255,255):
                string += '.';
            elif pixel == (0,0,0):
                string += 'x';

        string += '\n'

    print(string);

    return string;
            
def values_to_png(path,values):

    width = len(values);
    height = len(values[0]);
    
    png = PIL.Image.new('RGB', (width,height))
    pixels = png.load()

    for x in range(width):    
        for y in range(height):
            pixels[x,y] = values[x][y];

    png.save(path+'.png','PNG');
            
if __name__ == '__main__':

    target = Image('target');
    cover1 = Image('cover1');
    cover2 = Image('cover2');
    geo = Image('geocache');

    sh1, sh2 = generate_sheets(target,cover1=cover1,cover2=cover2);
    sh1.save('sheet1');
    sh2.save('sheet2');

# Er moet nog iets gedaan worden met plekken waar cover1 en cover2 niet hetzelfde zijn
