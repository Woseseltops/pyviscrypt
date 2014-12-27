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


def generate_sheets(targets,topcover = None,bottomcover = None):

    #Create the first sheet
    topsheet = Sheet([]);

    for nl, line in enumerate(topcover.pixels):

        current_sheetline = [];

        for np, imagepixel in enumerate(line):

            if imagepixel == 'x':
                pixel = Sheetpixel(nr_black=3);
            elif imagepixel == '.':
                pixel = Sheetpixel(nr_black=2);

            current_sheetline.append(pixel);

        topsheet.pixels.append(current_sheetline);

    bottomsheets = [];

    for target in targets:

        bottomsheet = Sheet([]);
        
        for nl, line in enumerate(target.pixels):

            current_sheetline = [];
            
            for np, imagepixel in enumerate(line):

                partner_pixel = topsheet.pixels[nl][np];

                if imagepixel == '.':

                    if bottomcover.pixels[nl][np] == 'x':
                        pixel = Sheetpixel(nr_black=3,total_black=3,partner=partner_pixel);
                    elif bottomcover.pixels[nl][np] == '.':
                        pixel = Sheetpixel(nr_black=2,total_black=3,partner=partner_pixel);                   
                                    
                elif imagepixel == 'x':

                    if bottomcover.pixels[nl][np] == 'x':
                        pixel = Sheetpixel(nr_black=3,total_black=4,partner=partner_pixel);
                    elif bottomcover.pixels[nl][np] == '.':
                        pixel = Sheetpixel(nr_black=2,total_black=4,partner=partner_pixel);                   
                            
                current_sheetline.append(pixel);

            bottomsheet.pixels.append(current_sheetline);

        bottomsheets.append(bottomsheet);
        
    return topsheet,bottomsheets;

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

    fish = Image('fish');
    w_cover = Image('w');
    h_cover = Image('h');
    geo = Image('geocache');
    coord = Image('coord');

    topsheet, bottomsheets = generate_sheets([fish,w_cover,h_cover,geo,coord],topcover=h_cover,bottomcover=geo);

    topsheet.save('topsheet');
    for n, bottomsheet in enumerate(bottomsheets):
        bottomsheet.save('bottomsheet'+str(n));
