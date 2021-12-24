# -*- coding: utf-8 -*-
# Toolbox with different classes and functions
# S. Vassant 2015/05/14
# V1:     JPK_image:  Read JPK ascii data and create a image with different in-built variables.
#         Read_T3: - Read T3 files from PicoHarp (photon, markers)
#                 - Function to make 2D intensity plots, with progress bar
# To be implemented
# V2 :     Read_T3: - Histogram at each point of the image
#                 - Average lifetime at each point of the image
#         Fit function with simple, and bi-exponential at least
#         Instrument function convolution 
import numpy as np
import matplotlib.pylab as plt
import struct as struct
import sys as sys

def convert_mev_microns(toto):
    """ convertit de meV en microns, et vice-versa """
    hb=1.05458e-34
    ev=1.60218e-19
    c= 3e8
    return 1e6*hb*2*np.pi*c/(toto*1e-3*ev)

class JPK_image:
    """ Image = JPK_image(Path)
    Loads an ASCII saved image from the JPK software.
    Path should be the full path of the file.\n
    Image.axex : x axe used for plotting, in microns
    Image.axey : y axe used for plotting, in microns
    Image.duty_cycle : Real acquisition time for a line (the rest being used as overscan) normalized to a line time
    Image.image : 2D matrix containing the image\n
    Image.max : max value of the image
    Image.min : min value of the image
    Image.max_ind : index of max value of the image
    Image.min_ind : index of min value of the image\n
    Image.scan_rate : scanning rate used for the image\n
    Image.x_dim : number of pixels in the x direction
    Image.x_size : physical image size in x direction (microns)
    Image.y_dim : number of pixels in the y direction
    Image.x_dim : physical image size in x direction (microns)\n
    Image.plot_im : Mehtod, creates a plot of the image """
    def __init__(self,Path):
        fs = open(Path, 'r')
        for i_line in np.linspace(0,14,15): # I read the first lines, where there is some important informations
            txt = fs.readline()
            if i_line == 5:
                self.x_size         = np.float(txt[11:]) # dimension en m fast scan
            if i_line == 6:
                self.y_size         = np.float(txt[11:]) # dimension en m slow scan
            if i_line == 9:
                self.x_dim         = np.int(txt[10:]) # dimension en pixels fast scan
            if i_line == 10:
                self.y_dim         = np.int(txt[10:]) # dimension en pixels slow scan
            if i_line == 13:
                self.scan_rate     = np.float(txt[11:-1]) # Scan rate in Hz
            if i_line == 14:
                self.duty_cycle     = np.float(txt[13:-1])

        self.image     = np.ndarray((self.y_dim,self.x_dim), dtype = float) # Create the image matrix
        self.axex     = np.linspace(0,self.x_size,self.x_dim)*1e6 #microns
        self.axey     = np.linspace(0,self.y_size,self.y_dim)*1e6 #microns

        nb_line = -1 # I need to count the lines to fill the matrix
        while 1:
            #print(nb_line)
            txt = fs.readline()
            if ((txt =='')|(txt == '\r\n')):  # Loop exit condition, end of file
                break
            if txt[0] =='#': # I skip the remaining headers
                pass
            else: # Now the real data starts
                ii=-1 #counter for index finding
                i_pos=0
                index_line = np.zeros(self.x_dim-1,dtype = int)#[] # I should have x_dim-1 number separators.
                while 1: # I look in all the characters of the line. The pixel values are separated by a space ' '.
                    ii = ii+1
                    #print(len(txt))
                    if (txt[ii:ii+1] == ' '):
                        index_line[i_pos] = ii#.append(ii)
                        i_pos = i_pos+1
                        #print(i_pos)
                    if (txt[ii:ii+4] == '\r\n'):
                        break
                    if ii== len(txt): # 20150801 S. Vassant: Could not stop with previous condition. Had to add this. Might have something to do with copy via FTP.
                        #print(txt[ii-4:])
                        break
                # Now that I have all the indexes, i.e. pixel value position in my line, I can fill my image matrix.

                #line                 = np.zeros(self.x_dim)
                # I fill the first point separately
                self.image[nb_line,0]             = np.float(txt[:index_line[0]])
                for iii in range (index_line.size -1):
                    self.image[nb_line,iii+1]    = (np.float(txt[index_line[iii]:index_line[iii+1]]))
                self.image[nb_line,-1]    = np.float(txt[index_line[-1]:])
                nb_line             = nb_line+1
        fs.close()
        self.max = np.max(self.image)
        self.min = np.min(self.image)
        self.max_ind = np.where(self.image == self.max)
        self.min_ind = np.where(self.image == self.min)
    def plot_im(self):
        F = plt.figure()
        Fax = F.add_subplot(111)
        Fax.pcolorfast(self.axex,self.axey,self.image)
        Fax.set_xlabel(r'x ($\mu$m)')
        Fax.set_ylabel(r'y ($\mu$m)')
        Fax.set_title('JPK image')
        F.show()

class Read_PTU:
    def __init__(self,Path,debug='no'):

        f = open(Path,"rb") # open file and read it as binary
        file_type          = struct.unpack('8s',f.read(8))[0] # string 8 character
        version              = struct.unpack('8s',f.read(8))[0] # string 8 character
        #{DE019A49-8DAD-44E1-E18B-A9B487725615}
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]#fread(fid, 1, 'int32');
        # there is a loop on this, print to print stuff . I don't care now. printed as is if -1 and something else if >-1                     # integer 32 bits ?
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #TagTyp is compared to the constants defined above to know what type we're dealing with. I don't know the function to convert hexadecimal to decimal
        # but I know how to convert decimal to hexadecimal. For speed consideration I might find this later on.

        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]    # Here need to read 64 bits !!
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)

        # PicoHarp 300: HWSETG SWSETG BinDATA    
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)
            # print(TagString)

        #3.0
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))

        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)

        #PicoHarp Software\
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)# print(TagString)

        #3.0.0.1
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)# print(TagString)

        #42115.6585279 # Date
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyTDateTime   = '0x21000008':
        TagFloat = struct.unpack('d',f.read(8))[0] #have to figure out how to convert this to a usable date
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            #print(TagInt)
            print(TagFloat)# print(TagString)# print(TagString)

        #T3 Mode
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]    
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)# print(TagString)# print(TagString)

        #Measurement_Mode, 3
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #Measurement_SubMode, 0
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008': Int8
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #TTResult_StopReason 0
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #Fast_Load_End 0
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp) == tyEmpty8      = '0xffff0008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)


        ### TTResultFormat_TTTRRecType determine if T3 or T2 records. hex(TTResultFormat_TTTRRecType) = 0x10303 for T3 and 0x10203 for T2
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        TTResultFormat_TTTRRecType = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### TTResultFormat_BitsPerRecord #### Should be 32 bits
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        TTResultFormat_BitsPerRecord = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ##### MeasDesc_BinningFactor
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        Binning_Factor = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ##### MeasDesc_Offset
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        Mes_Offset = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ##### MeasDesc_AcquisitionTime
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0] 
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        Aq_Time = TagInt/1e3 #seconds
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString) print(TagIndent,TagInt)

        ##### MeasDesc_StopAt
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ##### MeasDesc_StopOnOvfl
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ###### MeasDesc_Restart
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ###### CurSWSetting_DispLog
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ##### CurSWSetting_DispAxisTimeFrom
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispAxisTimeTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ##### CurSWSetting_DispAxisCountFrom
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        ##### CurSWSetting_DispAxisCountTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurves
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### CurSWSetting_DispCurve_MapTo
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # # CurSWSetting_DispCurve_Show
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        #### HW_Type : Picoharp 300
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]    
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)# print(TagString)# print(TagString)

        # # # ???? 930004
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]    
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)# print(TagString)# print(TagString) 

        # # # ???? 2.0
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]    
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)# print(TagString)# print(TagString) 

        # ???? 1020840
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt         = struct.unpack('Q',f.read(8))[0]    
        TagString     = struct.unpack(str(TagInt)+'s',f.read(TagInt))
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            print(TagString)# print(TagString)# print(TagString)# print(TagString) 

        # HWSync_Divider
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        HW_Sync_Divider = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWSync_Offset
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWSync_CFDZeroCross
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWSync_CFDLevel
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HW_InpChannels
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWInpChan_CFDZeroCross
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWInpChan_CFDLevel
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # MeasDesc_Resolution       
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]                    # integer 32 bits ?
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyFloat8 = '0x20000008', reads as 8 bytes double
        TagInt         = struct.unpack('d',f.read(8))[0]
        MeasDesc_Resolution = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HW_BaseResolution 
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyFloat8 = '0x20000008', reads as 8 bytes double
        TagInt         = struct.unpack('d',f.read(8))[0]
        HW_BaseResolution = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HW_ExternalDevices  
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)
        # HWRouter_ModelCode 
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HW_Markers 
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_RisingEdge 
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_RisingEdge 
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_RisingEdge 
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_RisingEdge 
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_Enabled
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_Enabled
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_Enabled
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_Enabled
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyBool8  = '0x00000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] # boolean, False if 0, TRUE if anything else... Don't care now
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # HWMarkers_HoldOff
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]# fread(fid, 1, 'int32');                    # integer 32 bits ?
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] 
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # MeasDesc_GlobalResolution
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyFloat8 = '0x20000008': reads as 8 bytes double
        TagInt         = struct.unpack('d',f.read(8))[0] 
        MeasDesc_GlobalResolution = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # TTResult_SyncRate
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0] 
        Sync_Rate = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # TTResult_InputRate
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt         = struct.unpack('Q',f.read(8))[0] 
        Input_Rate = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # TTResult_StopAfter
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] 
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # TTResult_NumberOfRecords
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        #hex(TagTyp)== tyInt8 = '0x10000008' 
        TagInt         = struct.unpack('Q',f.read(8))[0] 
        TTResult_NumberOfRecords = TagInt
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagInt)
            #print(TagString)# print(TagString)# print(TagString)# print(TagIndent,TagInt)

        # Header_End ##### END OF THE HEADER
        TagIndent     = struct.unpack( '32s', f.read(32))[0]     # string 32 character
        TagIdx         = struct.unpack('i',f.read(4))[0]
        TagTyp         = struct.unpack('I',f.read(4))[0]
        if debug == 'yes':
            print(TagIndent)
            print(TagIdx)
            print(hex(TagTyp))
            print(TagIndent[0:10])

        # We can perform some tests
        print('---- Read PTU Tests 1 ----')
        if TTResultFormat_BitsPerRecord ==32:
            pass
        else:
            print('Error: not 32 bits TTR records')
        if hex(TTResultFormat_TTTRRecType) == '0x10303':
            mes_type='T3'
        elif hex(TTResultFormat_TTTRRecType) == '0x10203':
            mes_type='T2'
            print('Error, T2 format !')
        else:
            print('Error, unknown format')

        if MeasDesc_GlobalResolution == 1./Sync_Rate:
            pass
        else:
            print('Error: something is wrong with Macrotime resolution and synchronization rate')

        if np.round(MeasDesc_Resolution*1e12)== Binning_Factor*HW_BaseResolution*1e12:
            pass
        else:
            print('Error: resolution/binning problem. Check MeasDesc_Resolution = Binning_Factor*HW_Baseresolution')
        if Input_Rate>=(Sync_Rate*5./100):
            print('WARNING: count rate too high for reliable single photon emission statistic. Risk of pile-up effect')
        else:
            pass

        print('---- End Read PTU Test 1 ----')
        #print(MeasDesc_GlobalResolution)
        # Read PT3



        RecNum_m         = np.zeros(TTResult_NumberOfRecords)
        Channel_m         = np.zeros(TTResult_NumberOfRecords)
        TimeTag_m         = np.zeros(TTResult_NumberOfRecords)
        MacroTime_m     = np.zeros(TTResult_NumberOfRecords)
        MicroTime_m     = np.zeros(TTResult_NumberOfRecords)
        dTime_m         = np.zeros(TTResult_NumberOfRecords)
        Event_type         = np.zeros(TTResult_NumberOfRecords) # I create this to distinguish between photon, overflow and markers
        # I use the following : 1 : photon; 2: overflow; 3: Frame marker, 4: line marker, 5: pixel marker, 0: unknown / error
        cnt_ph             = 0 # photon
        cnt_ov             = 0 # overflow
        cnt_ma            = 0 # overall markers
        cnt_ma_f        = 0 # frame marker
        cnt_ma_l        = 0 # line marker
        cnt_ma_p        = 0 # pixel marker
        cnt_ma_u        = 0 # unknown marker
        cnt_err            = 0 # errors
        ofltime         = 0
        WRAPAROUND_T3    = 65536  # 2**16
        WRAPAROUND_T2    = 210698240
        Hist             = np.zeros(2**12) 

        for ii in range (TTResult_NumberOfRecords):
            # Progress bar
            p = np.ceil(100*ii/(TTResult_NumberOfRecords-1))
            if ii == 0:
                p_before=0.1
                print('\r Reading file : %d%%' %p)
            if p==p_before:
                pass
            else:                
                print('\r Reading file : %d%%' %p)
            p_before=p
            #sys.stdout.write('\r Reading file : %d%%' %(100*ii/(TTResult_NumberOfRecords-1)))
            #sys.stdout.flush()

            T3Record     = struct.unpack('I',f.read(4))[0]         # all 32 bits:
            #   +-------------------------------+  +-------------------------------+ 
            #   |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|  |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|
            #   +-------------------------------+  +-------------------------------+    
            
            if mes_type=='T3':
                nsync         = T3Record&(2**16-1)                     # the lowest 16 bits:  
            #   +-------------------------------+  +-------------------------------+ 
            #   | | | | | | | | | | | | | | | | |  |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|
            #   +-------------------------------+  +-------------------------------+    
            #
            elif mes_type=='T2':
                nsync         = T3Record&(2**28-1)                     # the lowest 28 bits:  
            #   +-------------------------------+  +-------------------------------+ 
            #   | | | | |X|X|X|X|X|X|X|X|X|X|X|X|  |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|
            #   +-------------------------------+  +-------------------------------+    
            #

            Chan         = (T3Record&((2**4-1)<<(32-4)))>>(32-4) # the upper 4 bits:
            #   +-------------------------------+  +-------------------------------+ 
            #   |x|x|x|x| | | | | | | | | | | | |  | | | | | | | | | | | | | | | | |
            #   +-------------------------------+  +-------------------------------+       
            
            truensync         = ofltime + nsync
            RecNum_m[ii]     = ii
            Channel_m[ii]     = Chan
            TimeTag_m[ii]     = truensync
            
            if mes_type=='T3':
                MacroTime_m[ii] = truensync*MeasDesc_GlobalResolution #s
            elif mes_type=='T2':
                MacroTime_m[ii] = truensync*MeasDesc_GlobalResolution #s

            if (Chan<=4):
                if mes_type=='T3':
                    if (Chan>=1):
                        dtime             = (T3Record&(2**12-1)<<16)>>16 # micro arrival time coded on 12 bytes (the ones after Chan)
                        dTime_m[ii]     = dtime
                        MicroTime_m[ii] = dtime*MeasDesc_Resolution*1e9 #ns
                        Hist[dtime]     = Hist[dtime]+1
                        Event_type[ii]  = 1
                        cnt_ph             = cnt_ph+1
                if mes_type=='T2':
                    dtime             = 0#(T3Record&(2**12-1)<<16)>>16 # micro arrival time coded on 12 bytes (the ones after Chan)
                    dTime_m[ii]     = dtime
                    MicroTime_m[ii] = 0#dtime*MeasDesc_Resolution*1e9 #ns
                    Hist[dtime]     = 0#Hist[dtime]+1
                    Event_type[ii]  = 1
                    cnt_ph             = cnt_ph+1
                     

            elif Chan==15:
                if mes_type=='T3':
                    #markers = bitand(bitshift(T3Record,-16),15) # where these four bits are markers:
                    markers         = (T3Record&((2**4-1)<<16))>>16
                    #   +-------------------------------+  +-------------------------------+ 
                    #   | | | | | | | | | | | | |x|x|x|x|  | | | | | | | | | | | | | | | | |
                    #   +-------------------------------+  +-------------------------------+
                    cnt_ma             = cnt_ma+1
                if mes_type=='T2':
                    #markers = bitand(T3Record,15) # where these four bits are markers:
                    markers = T3Record&(2**4-1)    
                    #   +-------------------------------+  +-------------------------------+ 
                    #   | | | | | | | | | | | | | | | | |  | | | | | | | | | | | | |X|X|X|X|
                    #   +-------------------------------+  +-------------------------------+
                    cnt_ma             = cnt_ma+1
                if markers==0:
                    if mes_type=='T3':                               # then this is an overflow record
                        ofltime         = ofltime + WRAPAROUND_T3  # and we unwrap the numsync (=time tag) overflow
                    if mes_type=='T2':
                        ofltime         = ofltime + WRAPAROUND_T2
                    cnt_ov             = cnt_ov+1
                    Event_type[ii]     = 2

                elif markers==1:
                    cnt_ma_p        = cnt_ma_p+1
                    Event_type[ii]  = 5 

                elif markers==4:    # Should be frame
                    cnt_ma_f         = cnt_ma_f+1
                    Event_type[ii]  = 3

                elif markers==8:    # Should be line
                    cnt_ma_l     = cnt_ma_l+1
                    Event_type[ii]  = 4

                else :
                    cnt_ma_u = cnt_ma_u +1                                       
            else:
                cnt_err = cnt_err+1
        f.close()
        microtime_axe     = np.linspace(0,2**12*MeasDesc_Resolution*1e9,2**12) # nanoseconds
        
        self.hist                 = Hist
        self.microtime             = microtime_axe
        self.line_time          = 1
        self.num_records         = TTResult_NumberOfRecords
        self.macrotime_res         = MeasDesc_GlobalResolution#*1e-9 #ns
        self.microtime_res         = MeasDesc_Resolution#*1e-12 #ps
        self.event_num             = RecNum_m     
        self.event_chan         = Channel_m         
        self.event_timetg         = TimeTag_m         
        self.event_dtime         = dTime_m 
        self.event_macrotime     = MacroTime_m     
        self.event_microtime     = MicroTime_m     
        self.event_type         = Event_type
        self.line_m             = MacroTime_m[Event_type==4]
        self.frame_m             = MacroTime_m[Event_type==3]
        self.pixel_m             = MacroTime_m[Event_type==5]
        self.nb_lines             = Event_type[Event_type==4].shape[0]
        self.nb_frame             = Event_type[Event_type==3].shape[0] 
        self.nb_pixel             = Event_type[Event_type==5].shape[0]        
        self.nb_photon             = Event_type[Event_type==1].shape[0]
    #def __getitem__(self,a) :
    #    return Read_PTU(self.__getitem__(a))
    def event_type_def(self):
        print("Definition of event types:\n0: unknown / error\n1: photon\n2: overflow\n3: Frame marker\n4: line marker\n5: pixel marker")
    def make_2D_image(self,x_dim,y_dim,duty_cycle):
        """ Fabricate a 2D intensity image in a x_dim x y_dim matrix, trace and retrace.
        Duty cycle takes into account the overrun of the AFM and should be found in the AFM file.
        The resulting matrix are saved in self.intens_t and self.intens_rt for trace and retrace respectively"""
        Flim_Int_t = np.zeros([x_dim,y_dim])
        Flim_Int_rt = np.zeros([x_dim,y_dim])
        # before starting things, I should check wether I have a trace+retrace or not
        if self.nb_lines<(2*y_dim):
            print('Not enough lines in the data, reduce y_dim')
        else:
            Line_time = (self.line_m[1]-self.line_m[0])*duty_cycle
            cnt_t = -1
            cnt_rt = -1
            for ii in range(2*y_dim):
                # Progress bar
                sys.stdout.write('\r Processing data : %d%%' %(100*ii/(2*y_dim-1)))
                sys.stdout.flush()
                
                #I have a line offset. like the JPK starts to record only after the first line... So I add +2 to the counter ii
                pixels_times = np.linspace(self.line_m[ii+2],self.line_m[ii+2]+ Line_time,x_dim+1)
                if np.mod(ii,2)==0:
                    cnt_t = cnt_t+1
                    for iii in range(x_dim):
                        Temp     = self.event_type[(self.event_macrotime>=pixels_times[iii]) & (self.event_macrotime<=pixels_times[iii+1])]
                        Flim_Int_t[cnt_t,iii]     = Temp[Temp==1].shape[0]#Event_type[(MacroTime_m>=pixels_times[iii]) & (MacroTime_m<=pixels_times[iii+1])].shape[0]        
                else:
                    cnt_rt = cnt_rt+1
                    for iii in range(x_dim):
                        Temp     = self.event_type[(self.event_macrotime>=pixels_times[iii]) & (self.event_macrotime<=pixels_times[iii+1])]
                        Flim_Int_rt[cnt_rt,x_dim-iii-1]     = Temp[Temp==1].shape[0]
            self.intens_t = Flim_Int_t
            self.intens_rt = Flim_Int_rt
    def plot_intens(self,axe_x,axe_y):
        """ Plot the 2D intensity map.
        make_2D_image should be run before.
        axe_x and axe_y are expected in microns"""
        if hasattr(self,'intens_t'):
            F = plt.figure()
            Fax = F.add_subplot(111)
            Fax.pcolorfast(axe_x,axe_y,self.intens_t)
            Fax.set_xlabel(r'x ($\mu$m)')
            Fax.set_ylabel(r'y ($\mu$m)')
            Fax.set_title('PicoHarp Trace')
            F.show()

            F = plt.figure()
            Fax = F.add_subplot(111)
            Fax.pcolorfast(axe_x,axe_y,self.intens_rt)
            Fax.set_xlabel(r'x ($\mu$m)')
            Fax.set_ylabel(r'y ($\mu$m)')
            Fax.set_title('PicoHarp Retrace')
            F.show()
        else:
            print('run .make_2D_image first !')

def Read_spe_3(spefilename, verbose=False):
    """ 
    Read a binary PI SPE file into a python dictionary

    Inputs:

        spefilename --  string specifying the name of the SPE file to be read
        verbose     --  boolean print debug statements (True) or not (False)

        Outputs
        spedict     
        
            python dictionary containing header and data information
            from the SPE file
            Content of the dictionary is:
            spedict = {'data':[],    # a list of 2D numpy arrays, one per image
            'IGAIN':pimaxGain,
            'EXPOSURE':exp_sec,
            'SPEFNAME':spefilename,
            'OBSDATE':date,
            'CHIPTEMP':detectorTemperature
            }

    I use the struct module to unpack the binary SPE data.
    Some useful formats for struct.unpack_from() include:
    fmt   c type          python
    c     char            string of length 1
    s     char[]          string (Ns is a string N characters long)
    h     short           integer 
    H     unsigned short  integer
    l     long            integer
    f     float           float
    d     double          float

    The SPE file defines new c types including:
        BYTE  = unsigned char
        WORD  = unsigned short
        DWORD = unsigned long


    Example usage:
    Given an SPE file named test.SPE, you can read the SPE data into
    a python dictionary named spedict with the following:
    >>> import piUtils
    >>> spedict = piUtils.readSpe('test.SPE')
    """
  
    # open SPE file as binary input
    spe = open(spefilename, "rb")
    
    # Header length is a fixed number
    nBytesInHeader = 4100

    # Read the entire header
    header = spe.read(nBytesInHeader)
    
    # version of WinView used
    swversion = struct.unpack_from("16s", header, offset=688)[0]
    
    # version of header used
    # Eventually, need to adjust the header unpacking
    # based on the headerVersion.  
    headerVersion = struct.unpack_from("f", header, offset=1992)[0]
  
    # which camera controller was used?
    controllerVersion = struct.unpack_from("h", header, offset=0)[0]
    if verbose:
        print "swversion         = ", swversion
        print "headerVersion     = ", headerVersion
        print "controllerVersion = ", controllerVersion
    
    # Date of the observation
    # (format is DDMONYYYY  e.g. 27Jan2009)
    date = struct.unpack_from("9s", header, offset=20)[0]
    
    # Exposure time (float)
    exp_sec = struct.unpack_from("f", header, offset=10)[0]
    
    # Intensifier gain
    pimaxGain = struct.unpack_from("h", header, offset=148)[0]

    # Not sure which "gain" this is
    gain = struct.unpack_from("H", header, offset=198)[0]
    
    # Data type (0=float, 1=long integer, 2=integer, 3=unsigned int)
    data_type = struct.unpack_from("h", header, offset=108)[0]

    comments = struct.unpack_from("400s", header, offset=200)[0]

    # CCD Chip Temperature (Degrees C)
    detectorTemperature = struct.unpack_from("f", header, offset=36)[0]

    # The following get read but are not used
    # (this part is only lightly tested...)
    analogGain = struct.unpack_from("h", header, offset=4092)[0]
    noscan = struct.unpack_from("h", header, offset=34)[0]
    pimaxUsed = struct.unpack_from("h", header, offset=144)[0]
    pimaxMode = struct.unpack_from("h", header, offset=146)[0]

    ########### here's from Kasey
    #int avgexp 2 number of accumulations per scan (why don't they call this "accumulations"?)
#TODO: this isn't actually accumulations, so fix it...    
    accumulations = struct.unpack_from("h", header, offset=668)[0]
    if accumulations == -1:
        # if > 32767, set to -1 and 
        # see lavgexp below (668) 
        #accumulations = struct.unpack_from("l", header, offset=668)[0]
        # or should it be DWORD, NumExpAccums (1422): Number of Time experiment accumulated        
        accumulations = struct.unpack_from("l", header, offset=1422)[0]
        
    """Start of X Calibration Structure (although I added things to it that I thought were relevant,
       like the center wavelength..."""
    xcalib = {}
    
    #SHORT SpecAutoSpectroMode 70 T/F Spectrograph Used
    xcalib['SpecAutoSpectroMode'] = bool( struct.unpack_from("h", header, offset=70)[0] )

    #float SpecCenterWlNm # 72 Center Wavelength in Nm
    xcalib['SpecCenterWlNm'] = struct.unpack_from("f", header, offset=72)[0]
    
    #SHORT SpecGlueFlag 76 T/F File is Glued
    xcalib['SpecGlueFlag'] = bool( struct.unpack_from("h", header, offset=76)[0] )

    #float SpecGlueStartWlNm 78 Starting Wavelength in Nm
    xcalib['SpecGlueStartWlNm'] = struct.unpack_from("f", header, offset=78)[0]

    #float SpecGlueEndWlNm 82 Starting Wavelength in Nm
    xcalib['SpecGlueEndWlNm'] = struct.unpack_from("f", header, offset=82)[0]

    #float SpecGlueMinOvrlpNm 86 Minimum Overlap in Nm
    xcalib['SpecGlueMinOvrlpNm'] = struct.unpack_from("f", header, offset=86)[0]

    #float SpecGlueFinalResNm 90 Final Resolution in Nm
    xcalib['SpecGlueFinalResNm'] = struct.unpack_from("f", header, offset=90)[0]

    #  short   BackGrndApplied              150  1 if background subtraction done
    xcalib['BackgroundApplied'] = struct.unpack_from("h", header, offset=150)[0]
    BackgroundApplied=False
    if xcalib['BackgroundApplied']==1: BackgroundApplied=True

    #  float   SpecGrooves                  650  Spectrograph Grating Grooves
    xcalib['SpecGrooves'] = struct.unpack_from("f", header, offset=650)[0]

    #  short   flatFieldApplied             706  1 if flat field was applied.
    xcalib['flatFieldApplied'] = struct.unpack_from("h", header, offset=706)[0]
    flatFieldApplied=False
    if xcalib['flatFieldApplied']==1: flatFieldApplied=True
    
    #double offset # 3000 offset for absolute data scaling */
    xcalib['offset'] = struct.unpack_from("d", header, offset=3000)[0]

    #double factor # 3008 factor for absolute data scaling */
    xcalib['factor'] = struct.unpack_from("d", header, offset=3008)[0]
    
    #char current_unit # 3016 selected scaling unit */
    xcalib['current_unit'] = struct.unpack_from("c", header, offset=3016)[0]

    #char reserved1 # 3017 reserved */
    xcalib['reserved1'] = struct.unpack_from("c", header, offset=3017)[0]

    #char string[40] # 3018 special string for scaling */
    xcalib['string'] = struct.unpack_from("40c", header, offset=3018)
    
    #char reserved2[40] # 3058 reserved */
    xcalib['reserved2'] = struct.unpack_from("40c", header, offset=3058)

    #char calib_valid # 3098 flag if calibration is valid */
    xcalib['calib_valid'] = struct.unpack_from("c", header, offset=3098)[0]

    #char input_unit # 3099 current input units for */
    xcalib['input_unit'] = struct.unpack_from("c", header, offset=3099)[0]
    """/* "calib_value" */"""

    #char polynom_unit # 3100 linear UNIT and used */
    xcalib['polynom_unit'] = struct.unpack_from("c", header, offset=3100)[0]
    """/* in the "polynom_coeff" */"""

    #char polynom_order # 3101 ORDER of calibration POLYNOM */
    xcalib['polynom_order'] = struct.unpack_from("c", header, offset=3101)[0]

    #char calib_count # 3102 valid calibration data pairs */
    xcalib['calib_count'] = struct.unpack_from("c", header, offset=3102)[0]

    #double pixel_position[10];/* 3103 pixel pos. of calibration data */
    xcalib['pixel_position'] = struct.unpack_from("10d", header, offset=3103)

    #double calib_value[10] # 3183 calibration VALUE at above pos */
    xcalib['calib_value'] = struct.unpack_from("10d", header, offset=3183)

    #double polynom_coeff[6] # 3263 polynom COEFFICIENTS */
    xcalib['polynom_coeff'] = struct.unpack_from("6d", header, offset=3263)

    #double laser_position # 3311 laser wavenumber for relativ WN */
    xcalib['laser_position'] = struct.unpack_from("d", header, offset=3311)[0]

    #char reserved3 # 3319 reserved */
    xcalib['reserved3'] = struct.unpack_from("c", header, offset=3319)[0]

    #unsigned char new_calib_flag # 3320 If set to 200, valid label below */
    #xcalib['calib_value'] = struct.unpack_from("BYTE", header, offset=3320)[0] # how to do this?

    #char calib_label[81] # 3321 Calibration label (NULL term'd) */
    xcalib['calib_label'] = struct.unpack_from("81c", header, offset=3321)

    #char expansion[87] # 3402 Calibration Expansion area */
    xcalib['expansion'] = struct.unpack_from("87c", header, offset=3402)
    ########### end of Kasey's addition

    if verbose:
        print "date      = ["+date+"]"
        print "exp_sec   = ", exp_sec
        print "pimaxGain = ", pimaxGain
        print "gain (?)  = ", gain
        print "data_type = ", data_type
        print "comments  = ["+comments+"]"
        print "analogGain = ", analogGain
        print "noscan = ", noscan
        print "detectorTemperature [C] = ", detectorTemperature
        print "pimaxUsed = ", pimaxUsed

    # Determine the data type format string for
    # upcoming struct.unpack_from() calls
    if data_type == 0:
        # float (4 bytes)
        dataTypeStr = "f"  #untested
        bytesPerPixel = 4
        dtype = "float32"
    elif data_type == 1:
        # long (4 bytes)
        dataTypeStr = "l"  #untested
        bytesPerPixel = 4
        dtype = "int32"
    elif data_type == 2:
        # short (2 bytes)
        dataTypeStr = "h"  #untested
        bytesPerPixel = 2
        dtype = "int32"
    elif data_type == 3:  
        # unsigned short (2 bytes)
        dataTypeStr = "H"  # 16 bits in python on intel mac
        bytesPerPixel = 2
        dtype = "int32"  # for numpy.array().
        # other options include:
        # IntN, UintN, where N = 8,16,32 or 64
        # and Float32, Float64, Complex64, Complex128
        # but need to verify that pyfits._ImageBaseHDU.ImgCode cna handle it
        # right now, ImgCode must be float32, float64, int16, int32, int64 or uint8
    else:
        print "unknown data type"
        print "returning..."
        sys.exit()
  
    # Number of pixels on x-axis and y-axis
    nx = struct.unpack_from("H", header, offset=42)[0]
    ny = struct.unpack_from("H", header, offset=656)[0]
    
    # Number of image frames in this SPE file
    nframes = struct.unpack_from("l", header, offset=1446)[0]

    if verbose:
        print "nx, ny, nframes = ", nx, ", ", ny, ", ", nframes
    
    npixels = nx*ny
    npixStr = str(npixels)
    fmtStr  = npixStr+dataTypeStr
    if verbose:
        print "fmtStr = ", fmtStr
    
    # How many bytes per image?
    nbytesPerFrame = npixels*bytesPerPixel
    if verbose:
        print "nbytesPerFrame = ", nbytesPerFrame

    # Create a dictionary that holds some header information
    # and contains a placeholder for the image data
    spedict = {'data':[],    # can have more than one image frame per SPE file
                'IGAIN':pimaxGain,
                'EXPOSURE':exp_sec,
                'SPEFNAME':spefilename,
                'OBSDATE':date,
                'CHIPTEMP':detectorTemperature,
                'COMMENTS':comments,
                'XCALIB':xcalib,
                'ACCUMULATIONS':accumulations,
                'FLATFIELD':flatFieldApplied,
                'BACKGROUND':BackgroundApplied,
                'WL':[]
                }
    
    # Now read in the image data
    # Loop over each image frame in the image
    if verbose:
        print "Reading image frames number ",
    
    for ii in range(nframes):
        #iistr = str(ii)
        data = spe.read(nbytesPerFrame)
        if verbose:
            print ii," ",
    
        # read pixel values into a 1-D numpy array. the "=" forces it to use
        # standard python datatype size (4bytes for 'l') rather than native
        # (which on 64bit is 8bytes for 'l', for example).
        # See http://docs.python.org/library/struct.html
        dataArr = np.array(struct.unpack_from("="+fmtStr, data, offset=0),
                            dtype=dtype)

        # Resize array to nx by ny pixels
        # notice order... (y,x)
        dataArr.resize((ny, nx))
        #print dataArr.shape

        # Push this image frame data onto the end of the list of images
        # but first cast the datatype to float (if it's not already)
        # this isn't necessary, but shouldn't hurt and could save me
        # from doing integer math when i really meant floating-point...
        spedict['data'].append( dataArr.astype(float) )

    #if verbose:
    #    print('######### Reading Footer ############')
    if verbose:
        #print('bouah')
        print('######### Reading Footer ############')    
    
    
    footer = spe.read()
    index_start = []
    index_stop=[]
    counter = -1
    for char in footer:
        counter = counter+1
        if char=='<': # tree stuff
            index_start.append(counter)
        elif char=='>':
            index_stop.append(counter)
        else:
            pass

    #Now i have all my 'fields'
    for ii in range(len(index_start)):
        if verbose:
            print footer[index_start[ii]+1:index_stop[ii]]
        
        if footer[index_start[ii]+1:index_stop[ii]]=='Wavelength xml:space="preserve"':
            start_wl = index_stop[ii]+1
            stop_wl = index_start[ii+1]

    #cnt_sep = []
    cnt_index = -1
    start_ind = start_wl
    wl = []
    for char in footer[start_wl:stop_wl]:
        cnt_index= cnt_index+1
        if char ==',':
            wl.append(np.float(footer[start_ind:start_wl+cnt_index]))
            start_ind = start_wl+cnt_index+1
    # I miss the last one.
    wl.append(np.float(footer[start_ind:stop_wl]))
    wl = np.array(wl)
    #print('toto')
    spedict['WL'].append(wl) 

    return spedict

def Correct_Comsmic_Rays(Spec):
    diff_spec = np.diff(Spec)
    Cray_pos = np.where(diff_spec>= np.mean(3*np.abs(diff_spec)))

    corr_spec = Spec.copy()

    for ii in Cray_pos:
        #Seems these rays can be 4 points wide !
        try :
            corr_spec[ii] = (corr_spec[ii-1] + corr_spec[ii+5])/2
            corr_spec[ii+1] = (corr_spec[ii] + corr_spec[ii+5])/2
            corr_spec[ii+2] = (corr_spec[ii+1] + corr_spec[ii+5])/2
            corr_spec[ii+3] = (corr_spec[ii+2] + corr_spec[ii+5])/2
        except:
            pass
    return corr_spec

def Read_WinSpec(Path,borne1 = 0,borne2 = 0) :
    """ Charge un fichier provenant d'un fichier exporte par OPUS en tableua de points, entre borne1 et borne2 en cm-1 (250 et 450 par defaut). Path est le chemin complet avec le nom du fichier. Eviter les ~/  """
    x,y=[],[]
    fs = open(Path, 'r')
   
    while 1: 
        txt = fs.readline()
        if ((txt =='')|(txt == '\r\n')): 
            break
        ii=-1
        index_line=[]
        while 1: # on cherche le premier espace qui limite le premier nombre
            ii = ii+1
            if (txt[ii:ii+1] == ';'):
                index_line.append(ii)
            if (txt[ii:ii+4] == '\r\n'):
                break
        x.append(float(txt[:index_line[0]]))
        y.append(float(txt[index_line[0]+1:]))  
    fs.close()
    x = np.array(x)
    y = np.array(y)
    if ((borne1 == 0) & (borne2 == 0)) :
        pass    
    else :
        index_ok = ((x<borne2) & (x>borne1))
        x = x[index_ok]
        y = y[index_ok]

    return x,y

def NP(R,k,eps1,epsm):
    """ Calculates approximation of nanoparticle polarizability, absorption and scattering crosssection.
    alpha, sig_abs,sig_sca = NP(R,k,eps1,epsm) 
    R is the NP radius, 
    k is the wavevector (2*np.pi/wl), wl is the wavelength in meter
    eps1 the dielectric function of the NP
    epsm the dielectric function of the surrounding medium."""

    alpha = 4*np.pi*(R**3)*(eps1 - epsm)/(eps1 + 2*epsm)
    sig_abs = k*alpha.imag
    sig_sca = (k**4)/(6*np.pi)*(np.abs(alpha))**2
    return alpha, sig_abs,sig_sca

def call_epsilon(longueur_onde, mat, x=0.3,y=0,z=0) :
    """return dielectric function of following materials :\n - \n -AlAs\n -SiC\n -InAs \n -InSb \n -InP \n -GaSb \n -AlSb\n -GaAs_ssbandes(x=dopage cm-2,y= w12meV,z= gamma), \n -GaAs_dope(x=dopage en cm-3)\n -AlGaAs_Kim (x = valeurs précises)\n -AlGaAs_Kim_Interp(x = composition Al)\n -Au_Pardo( autour de 3 microns)\n -Au_Etchegoin \n -Au_Ordal \n-Verre (constant, eps = 2.25)
    longueur_onde is the wavelength in microns.
    mat a string describing the material
    x,y,z are supplementary inputs. Refer to sepcific material to check how they are used"""
    
    eps0=8.854e-12
    mel=9.109e-31
    hb=1.05458e-34
    ev=1.60218e-19
    c= 3e8
    #pi= np.pi de la bibliothèque numpy.
    if  mat == 'GaAs' :
        epsinf = 11
        wL = 292.1
        wT = 268.7
        T= 2.4 #Palik Value
        #T= 1 # Modif
        v=1e4/longueur_onde #cm-1
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat =='PbTe':
        epsinf = 32.8
        #eps_s = 388
        wT = 32
        wL = 114.01
        T = 26
        v=1e4/longueur_onde #cm-1
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif  mat == 'GaAs_mod' :
        epsinf = 11
        wL = 291.55
        wT = 268.7
        T= 2.4 #Palik Value
        #T= 1 # Modif
        v=1e4/longueur_onde #cm-1
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif  mat == 'GaAs_Lockwood' :
        epsinf = 10.88
        wL = 292.01
        wT = 268.41
        T1= 2.33 #Palik Value
        T2 = 2.51
        #T= 1 # Modif
        v=1e4/longueur_onde #cm-1
        epsilon = epsinf*((wL**2-v**2+1j*T1*v)/(wT**2-v**2+1j*T2*v))
    elif  mat == 'GaAs_noloss' :
        epsinf = 11
        wL = 292.1
        wT = 267.98
        T= 0 #Palik Value
        #T= 1 # Modif
        v=1e4/longueur_onde #cm-1
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat == 'CdO':
        # Rieder et al 1972. 
        wT = 262 #±2
        wL = 478#±25
        T = 1.1 # pas clairement id 
        epsinf = 5.4
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
        
    elif mat == 'LiF':
        wT = 305
        wL = np.sqrt((9.02/1.1)*wT**2)
        T = 1.1
        epsinf = 1.93
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat =='GaP':
        wL = 402.4
        wT = 363.4
        T = 1.1
        epsinf = 9.1
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat =='AlAs':
        wL = 401.5
        wT = 361.8
        T = 8
        epsinf = 8.2
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat == 'SiC':
        epsinf  =6.7
        wL      =969 #cm-1
        wT      =793 #cm-1
        T       =4.76 #cm-1
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat == 'GaN':
        epsinf=5.35
        wL=746
        wT=559
        T=4
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat == 'InAs':
        epsinf=11.7
        wL=240
        wT=218
        T=4
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat =='InSb':
        epsinf=15.68
        wL=190.4
        wT=179.1
        T= 2.86
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat =='InP':
        epsinf=9.61
        wL=345.0
        wT=303.7
        T=3.5
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif mat =='InP_Lockwood':
        epsinf=9.61
        wL=345.32
        TL = 0.95
        wT=303.62
        TT=2.80
        v=1e4/longueur_onde #cm-1   
        epsilon = epsinf*((wL**2-v**2-1j*TL*v)/(wT**2-v**2-1j*TT*v))


    elif  mat == 'GaAs_Ideal' :
        epsinf = 10.9
        wL = 291.2
        wT = 267.98
        T= 0 #Palik Value
        #T= 1 # Modif
        v=1e4/longueur_onde #cm-1
        
        epsilon = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
    elif ((mat=='GaSb') | (mat=='AlSb')| (mat=='AlGaSb')):
        if mat=='GaSb':
            x=0
        if mat=='AlSb':
            x=1
        
        v=1e4/longueur_onde #cm-1
        epsinf = 14.5-4.62*x
    # Type GaSb :
        vt1 = 227.1 - 11.7*x -9.6*x**2
        vl1 = 235.7 - 21.6*x - 8.2*x**2
        g1 = 1.01 + 21.78*x -21.43*x**2
        S1 = (vl1**2 -vt1**2)*epsinf

    # Type AlSb 
        vt2 = 312.7 + 14*x - 7.9*x**2
        vl2 = 313+28.6*x -2.1*x**2
        g2 = 8.34 + 2.37*x - 8.84*x**2
        S2 = (vl2**2 -vt2**2)*epsinf
        if mat=='GaSb':
            epsilon = epsinf + S1/(vt1**2 - v**2 - 1j*g1*v)
        if mat=='AlSb':
            epsilon = epsinf + S2/(vt2**2 - v**2 - 1j*g2*v)
        else :
            epsilon = epsinf + S1/(vt1**2 - v**2 - 1j*g1*v) + S2/(vt2**2 - v**2 - 1j*g2*v);
        
    elif mat == 'AlGaAs_Kim_Interp' :
        
        v = 1e4/longueur_onde
        vl1 = 292.7 - 53.61*x+ 21.73*x**2
        vt1 = 268.8 - 10.65*x- 4.746*x**2
        vl2 = 360   + 71.28*x- 29.78*x**2
        vt2 = 358.3 + 7.141*x- 3.649*x**2
        
        gl1 = 3.056 + 8.514*x
        gt1 = 3.761 + 16.62*x #Home made interpolation value
        #gt1 = 3.761 + 2.62*x  # Modif
        gl2 = 12.11 - 8.81*x
        gt2 = 13.7 - 8.817*x #Home made interpolation value
        #gt2 = 10.7 - 8.817*x # Modif
        epsinf = 10.9 -2.544*x + 0.6554*x**2 - 0.8159*x**3
        epsilon = epsinf*(((vl1**2)-(v**2)-1j*v*gl1)*((vl2**2)-(v**2)-1j*v*gl2))/(((vt1**2)-(v**2)-1j*v*gt1)*((vt2**2)-(v**2)-1j*v*gt2))
        
    elif mat == 'AlGaAs_Kim_Interp_noloss' :
        
        v = 1e4/longueur_onde
        vl1 = 292.7 - 53.61*x+ 21.73*x**2
        vt1 = 268.8 - 10.65*x- 4.746*x**2
        vl2 = 360   + 71.28*x- 29.78*x**2
        vt2 = 358.3 + 7.141*x- 3.649*x**2
        
        gl1 = 0
        gt1 = 0 #Home made interpolation value
        #gt1 = 3.761 + 2.62*x  # Modif
        gl2 = 0
        gt2 = 0 #Home made interpolation value
        #gt2 = 10.7 - 8.817*x # Modif
        epsinf = 10.9 -2.544*x + 0.6554*x**2 - 0.8159*x**3
        epsilon = epsinf*(((vl1**2)-(v**2)-1j*v*gl1)*((vl2**2)-(v**2)-1j*v*gl2))/(((vt1**2)-(v**2)-1j*v*gt1)*((vt2**2)-(v**2)-1j*v*gt2))
        
    elif mat == 'AlGaAs_Kim' :
        v=1e4/longueur_onde #cm-1
        if (x==0.14) :
            vt1 = 267.1
            vl1 = 285.7
            gt1 = 5.67
            gl1     = 4.85
            vt2     = 358.8
            vl2     = 369.0
            gt2     = 10.56
            gl2     = 11.31
            epsinf  = 10.57
        
        elif (x==0.18) :
    
            vt1     = 266.9
            vl1     = 283.4
            gt1     = 8.76
            gl1     = 4.24
            vt2     = 360.1
            vl2     = 372.4
            gt2     = 12.20
            gl2     = 10.24
            epsinf  = 10.47
    
        elif(x==0.30) :
    
            vt1     = 265.2
            vl1     = 278.3
            gt1     = 8.64
            gl1     = 6.15
            vt2     = 360.2
            vl2     = 379.1
            gt2     = 12.10
            gl2     = 9.42
            epsinf  = 10.16
    
        elif(x==0.36) :
    
            vt1     = 264.5
            vl1     = 276.5
            gt1     = 10.69
            gl1     = 5.58
            vt2     = 360.4
            vl2     = 381.3
            gt2     = 12.23
            gl2     = 8.08
            epsinf  = 10.04
    
        elif (x==0.44) :
       
            vt1     = 262.9
            vl1     = 273.7
            gt1     = 10.5
            gl1     = 6.44
            vt2     = 360.2
            vl2     = 385.4 
            gt2     = 9.55 
            gl2     = 7.90
            epsinf  = 9.84
    
        elif(x== 0.54) :
        
            vt1     = 261.8 # Original value
            vl1     = 269.8 # Original value
            gt1     = 12.43 # Original value
            #gt1     = 8
            gl1     = 7.97 # Original value
            #gl1     = 2
            vt2     = 361.5 # Original value
            #vt2     = 357
            vl2     = 390.1 # Original value
            #vl2     = 380
            gt2     = 8.75 # Original value
            gl2     = 8.68 # Original value
            epsinf  = 9.60 # Original value
        else : 
            print 'Pas un bonne valeur de x... seulement dispo : 0.14 0.18 0.3 0.36 0.44 0.54'
            vt1     = 1
            vl1     = 1
            gt1     = 1
            gl1     = 1
            vt2     = 1
            vl2     = 1
            gt2     = 1
            gl2     = 1
            epsinf  = 1
            
        epsilon =  epsinf*(((vl1**2)-(v*v)-1j*v*gl1)*((vl2**2)-(v*v)-1j*v*gl2))/\
        (((vt1**2)-(v*v)-1j*v*gt1)*((vt2**2)-(v*v)-1j*v*gt2))
    
        
    elif mat == 'Au_Pardo' :
        par = longueur_onde
        lambdap = 1.589540866244842e-07
        gaga = 0.0077
        toto = lambdap/(par*1e-6)
        epsilon = 1 - 1.0/(toto**2 + 1j*gaga)
    elif mat == 'Ag_Nordlander' :
        w = convert_mev_microns(longueur_onde)*1e-3
        sig = 3157.56
        A1 = -1.160e5
        A2 = -4.252
        A3 = -0.4960
        A4 = -2.118
        B1 = -3050
        B2 = -0.8385
        B3 = -13.85
        B4 = -10.23
        C1 = 3.634e8
        C2 = 112.2
        C3 = 1.815
        C4 = 14.31
        #epsilon = 1 + sig/(1j*w) + C1/(w**2 + A1*1j*w + B1) +C2/(w**2 + A2*1j*w + B2)+ C3/(w**2 + A3*1j*w + B3) +C4/(w**2 + A4*1j*w + B4)
        epsilon = 1 - sig/(1j*w) + C1/(w**2 - A1*1j*w + B1) +C2/(w**2 - A2*1j*w + B2)+ C3/(w**2 - A3*1j*w + B3) +C4/(w**2 - A4*1j*w + B4)
    elif mat == 'Au_Nordlander' :
        #
        w = convert_mev_microns(longueur_onde)*1e-3
        sig = 1355.01
        A1 = -8.577e4
        A2 = -2.875
        A3 = -997.6
        A4 = -1.630
        B1 = -1.156e4
        B2 = 0
        B3 = -3090
        B4 = -4.409
        C1 = 5.557e7
        C2 = 2.079e3
        C3 = 6.921e5
        C4 = 26.15
        epsilon = 1 + sig/(1j*w) + C1/(w**2 + A1*1j*w + B1) +C2/(w**2 + A2*1j*w + B2)+ C3/(w**2 + A3*1j*w + B3) +C4/(w**2 + A4*1j*w + B4)
        
    elif mat == 'Au_Etchegoin_mod' :
        #Etchegoin, Le Ru, Meyer, Journal of Chemical Physics125, 164705
        #(2006)
        par = longueur_onde*1e3
        epsinf     = 1.54
        lambdap    = 143      #nm
        gammap     = 14500    #nm
        #A1         = 1.27
        A1         = 1.31
        phi1       = -np.pi/4  #rad
        lambda1    = 470      #nm
        gamma1     = 1900     #nm
        #A2         = 1.1
        A2         = 1
        phi2       = -np.pi/4  #rad
        lambda2    = 325      #nm
        gamma2     = 1060     #nm
        epsilon = epsinf-1/(lambdap**2*((par**(-2))+1j/(gammap*par))) +\
         (A1/lambda1)*( (np.exp(1j*phi1)/(1/lambda1-1/par-1j/gamma1)) +\
         (np.exp(-1j*phi1)/(1/lambda1+1/par+1j/gamma1))) + \
         (A2/lambda2)*( (np.exp(1j*phi2)/(1/lambda2-1./par-1j/gamma2))+ \
         (np.exp(-1j*phi2)/(1/lambda2+1/par+1j/gamma2)))
    elif mat == 'Au_Etchegoin' :
        #Etchegoin, Le Ru, Meyer, Journal of Chemical Physics125, 164705
        #(2006)
        par = longueur_onde*1e3
        epsinf     = 1.54
        lambdap    = 143      #nm
        gammap     = 14500    #nm
        A1         = 1.27
        #A1         = 1.31
        phi1       = -np.pi/4  #rad
        lambda1    = 470      #nm
        gamma1     = 1900     #nm
        A2         = 1.1
        #A2         = 1
        phi2       = -np.pi/4  #rad
        lambda2    = 325      #nm
        gamma2     = 1060     #nm
        epsilon = epsinf-1/(lambdap**2*((par**(-2))+1j/(gammap*par))) +\
         (A1/lambda1)*( (np.exp(1j*phi1)/(1/lambda1-1/par-1j/gamma1)) +\
         (np.exp(-1j*phi1)/(1/lambda1+1/par+1j/gamma1))) + \
         (A2/lambda2)*( (np.exp(1j*phi2)/(1/lambda2-1./par-1j/gamma2))+ \
         (np.exp(-1j*phi2)/(1/lambda2+1/par+1j/gamma2)))    
    elif mat =='GaAs_dope':
        
        par = longueur_onde
        v           = 1e4/par
        epsinf      = 10.9
        wL          = 291.2
        wT          = 267.98
        T           = 2.54
        epsGaAs     =epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
        dopage      = x #cm-3
        n3D         = x*1e6 #passage en m-3 %1cm = 1e-2m ; %1cm3 = 1e-6m3, %1cm-3 = 1e6m-3
        meffective  = mel*0.067
        
        # G.Yu et al. ASS 199 p160-165 (2002)
        gammap      = 5.17e-13 + 2.23e-13*np.exp(-dopage/7.62e16) # le dopage est en cm-3 dans cette expression. gaamap est en secondes
        gammap      = y # cm-1 
        
        #gammap      = y
        wpSI        = maystre((n3D*ev**2)/(eps0*epsinf*meffective)) #SI : sr.s-1
        wp          = (wpSI*1e-2)/(2*np.pi*c)# conversion cm-1  
            
        eps_elibres = epsinf*wp**2/(v**2 + 1j*v*gammap);
        epsilon         = epsGaAs - eps_elibres;
    elif mat =='Si_dope':
        
        par = longueur_onde
        v           = 1e4/par
        epsinf      = 11.68
        
        dopage      = x #cm-3
        n3D         = x*1e6 #passage en m-3 %1cm = 1e-2m ; %1cm3 = 1e-6m3, %1cm-3 = 1e6m-3
        meffective  = mel*0.29
        
        # G.Yu et al. ASS 199 p160-165 (2002)
        gammap      = 5.17e-13 + 2.23e-13*np.exp(-dopage/7.62e16) # le dopage est en cm-3 dans cette expression. gaamap est en secondes
        gammap      = y # cm-1 
        
        #gammap      = y
        wpSI        = sqrts.maystre((n3D*ev**2)/(eps0*epsinf*meffective)) #SI : sr.s-1
        wp          = (wpSI*1e-2)/(2*np.pi*c)# conversion cm-1  
            
        eps_elibres = epsinf*wp**2/(v**2 + 1j*v*gammap);
        epsilon         = epsinf - eps_elibres;

       
    elif mat == 'Au_Ordal':
        v = 1e4/longueur_onde
        vp=7.25e4
        g=215
        epsilon = 1-vp*vp/(v*(v+1j*g))
    elif mat == 'Au_Ideal':
        v = 1e4/longueur_onde
        vp=7.25e4
        g=0
        epsilon = 1-vp*vp/(v*(v+1j*g))
    elif mat == 'Verre' :
        epsilon = 2.25*np.ones(np.shape(longueur_onde)) 
    elif mat == 'Verre2' :
        epsilon = 2.0736*np.ones(np.shape(longueur_onde)) 
    elif mat == 'Ti':
        # Ordal AO 24, 4493
        v = 1e4/longueur_onde;
        vp = 2.03e4; #cm-1 ??? moyen ce truc, a vérifier...
        g = 3.82e2; #cm-1
        epsilon = 1-vp*vp/(v*(v+1j*g))
    elif mat =='Ag':
        v = 1e4/longueur_onde
        vp=1e4/(1.24/8.4)
        g=1e-3/(2.99e8*2.2e-14)
        epsilon = 1-vp*vp/(v*(v+1j*g))
    elif mat == 'Al_Ordal':
        v = 1e4/longueur_onde
        vp= 11.9e4
        g= 6.6e2
        epsilon = 1-vp*vp/(v*(v+1j*g))
    elif mat =='Ag_Ordal':
        v       = 1e4/longueur_onde
        vp      = 7.27e4
        g       = 1.45e2
        epsilon = 1-vp*vp/(v*(v+1j*g))
    elif mat =='Ag_Ordal_Ideal':
        v       = 1e4/longueur_onde
        vp      = 7.27e4
        g       = 0
        epsilon = 1-vp*vp/(v*(v+1j*g))
    elif mat =='Cu_Ideal':
        v       = 1e4/longueur_onde
        vp      = 1e-2*11.23e15/(2*np.pi*c)
        g       = 0.732e2
        epsilon = 1-vp*vp/(v*(v+1j*g))
#TODO : check this model, self_energy missing...
#    elif mat =='Al2O3':
#        v       = 1e4/longueur_onde
#        epsinf  = 3.03
#        S1      = 0.42
#        O1      = 373.86
#        A11     = 24.41
#        w011    = 199.33
#        G11     = 248.9
#        
#        S2 = 2.73
#        O2 = 439.71
#        A12 = 5.68
#        w012 = 423.58
#        G12 = 38.51
#        
#        S3 = 2.87
#        O3 = 580.42
#        A13 = 1.43
#        w013 = 371.13
#        G13 = 190.22
#        A23 = 10.12
#        w023 = 536.83
#        G23 = 117.73
#        A33 = 15.56
#        w033 = 914.59
#        G33 = 33.25
#        A43 = 6.13
#        w043 = 1299.6
#        G43 = 895.54
#        
#        S4 = 0.15
#        O4 = 638.35
#        A14 = 6.77
#        w014 = 640.36
#        G14 = 30.03
#        
#        epsilon = epsinf + (S1*O1**2)/(O1**2 - v**2 - 2*O1*Self_energ(A11,w011,G11,v))\
#                         + (S2*O2**2)/(O2**2 - v**2 - 2*O2*Self_energ(A12,w012,G12,v))\
#                         + (S3*O3**2)/(O3**2 - v**2 - 2*O3*( Self_energ(A13,w013,G13,v)\
#                                                           + Self_energ(A23,w023,G23,v)\
#                                                           + Self_energ(A33,w033,G33,v)\
#                                                           + Self_energ(A43,w043,G43,v)))\
#                         + (S4*O4**2)/(O4**2 - v**2 - 2*O4*Self_energ(A14,w014,G14,v))
#                                                           
                         
        
    elif ((mat == 'vide') or (mat == 'Vide')) :
        epsilon = np.ones(np.shape(longueur_onde))
    elif mat == 'GaAs_ssbandes' :
        #% retourne la fonction dielectrique de GaAs avec une transition intersousbande en fonction de l'epaisseur de la tranche de gaas et du
        #% dopage de la couche : dopage2D en nb d'e- par cm-2, w12mev en meV, gamma en  s-1
           
        #%% GaAs
        dopage2D = x
        w12meV = y
        gamma = z
        epsinf = 11
        wL = 291.2
        wT = 267.98
        T= 2.4
        v=1e4/longueur_onde #cm-1
       
        epsGaAs = epsinf*(1+(wL**2-wT**2)/(wT**2-v**2-1j*T*v))
        
        if dopage2D == 0:
            eps_ssbandes = 0
        elif w12meV ==0:
            eps_ssbandes =0
        else :
    
            meffective          = 0.0636*mel #kg
            d_eq                = 3.8e-9 # m
            force_oscillateur   = (2*meffective/hb)*((w12meV*1e-3*ev/hb)*d_eq**2) # SI
            ns                  = (dopage2D/20e-7)*1e6 # passage de cm-2 ? m-2 On fixe l'epaisseur du puit a 20nm, ordre de grandeur...
            wp2                 = (ns*force_oscillateur*ev**2)/(meffective*eps0) # SI
            w                   = 2*np.pi*c/(longueur_onde*1e-6) # SI
            eps_ssbandes        = wp2/(w**2 - (w12meV*1e-3*ev/hb)**2 + 1j*gamma*w)
            
        epsilon             = epsGaAs - eps_ssbandes    

    else:
        print 'A pas compris le materiau ton eps est = 0'
        epsilon = 0
    
#    for index in range(len(epsilon)) :
#        
#        if type(epsilon[index]) == np.complex128 :
#            if epsilon[index].imag<0 :
#                epsilon[index] = epsilon[index].conjugate
                
    if type(epsilon)==complex:
        epsilon = epsilon.real + 1j*np.abs(epsilon.imag)            
    return epsilon



    # """ Reads the files saved from the PicoHarp software and save via copy/paste in Notepad.
    # time,time_unit,Mat = Read_PicoHarp(Path)
    # time is the time axis (microtime), 
    # time_unit the unit of time (in ps ?)
    # Mat is a matrix containing the different histograms (traces, up to 8, numbered 0 to 7 in the PicoHarp software)"""
def Read_PicoHarp(Path):
    """ Reads the files saved from the PicoHarp software and save via copy/paste in Notepad.
    time,time_unit,Mat = Read_PicoHarp(Path)
    time is the time axis (microtime), 
    time_unit the unit of time (in ps ?)
    Mat is a matrix containing the different histograms (traces, up to 8, numbered 0 to 7 in the PicoHarp software)"""
    fs = open(Path, 'r')
    #first, find numbe of curves
    i_lignes = -1
    while 1: 
        txt = fs.readline()
        i_lignes = i_lignes +1
        if ((txt =='')|(txt == '\r\n')): 
            break

        if txt[:14] =="#display curve":
            txt = fs.readline() # je passe a la ligne d apres
            n_trace = 0
            ii=-1
            while 1:
                ii = ii+1
                if (txt[ii] == '\t'):
                    n_trace = n_trace+1
                if txt[ii:ii+2]=='\t\n':
                    break
                
                


        if txt[:11] =="#ns/channel":
            time_unit = np.zeros(n_trace)
            txt = fs.readline()
            iindex = []
            ii = -1
            while 1:
                ii = ii+1
                if (txt[ii] == '\t'):
                    iindex.append(ii)
                if txt[ii:ii+2]=='\t\n':
                    break
            time_unit[0]= np.float(txt[:iindex[0]].replace(',','.'))
            for i_tu in range(n_trace-1):
                time_unit[i_tu+1] = np.float(txt[iindex[i_tu]:iindex[i_tu+1]].replace(',','.'))
        
    fs.close()

    n_trace = n_trace
    i_lignes = i_lignes -8 # il y a 10 lignes de commentaires +2 sautées pour trouver des infos...
    Mat = np.zeros((i_lignes,n_trace))
    time = np.linspace(0,i_lignes,i_lignes)
    fs = open(Path, 'r')
    ii = -1
    while 1: 
        txt = fs.readline()
        ii = ii+1
        if ((txt =='')|(txt == '\r\n')): 
            break
        if ii>=10:
            iindex=[]
            iii=-1
            while 1:
                iii = iii+1
                if (txt[iii] == '\t'):
                    iindex.append(iii)
                if txt[iii:iii+2]=='\t\n':
                    break
            Mat[ii-10,0] = txt[:iindex[0]]        
            for i_c in range(n_trace-1):
                Mat[ii-10,i_c+1] = txt[iindex[i_c]:iindex[i_c+1]]
    return time,time_unit,Mat    


def Read_PicoHarp2(Path):
    fs = open(Path, 'r')
    #first, find numbe of curves
    i_lignes = -1
    while 1: 
        txt = fs.readline()
        i_lignes = i_lignes +1
        if ((txt =='')|(txt == '\r\n')): 
            break

        if txt[:14] =="#display curve":
            txt = fs.readline() # je passe a la ligne d apres
            n_trace = 0
            ii=-1
            while 1:
                ii = ii+1
                if (txt[ii] == '\t'):
                    n_trace = n_trace+1
                if txt[ii:ii+3]=='\t\r\n':
                    break
                
        if txt[:11] =="#ns/channel":
            time_unit = np.zeros(n_trace)
            txt = fs.readline()
            iindex = []
            ii = -1
            while 1:
                ii = ii+1
                if (txt[ii] == '\t'):
                    iindex.append(ii)
                if txt[ii:ii+3]=='\t\r\n':
                    break
                
            time_unit[0]= np.float(txt[:iindex[0]].replace(',','.'))
            for i_tu in range(n_trace-1):
                time_unit[i_tu+1] = np.float(txt[iindex[i_tu]:iindex[i_tu+1]].replace(',','.'))
    fs.close()
    n_trace = n_trace
    i_lignes = i_lignes -8 # il y a 10 lignes de commentaires +2 sautées pour trouver des infos...
    Mat = np.zeros((i_lignes,n_trace))
    time = np.linspace(0,i_lignes,i_lignes)
    fs = open(Path, 'r')
    ii = -1
    while 1: 
        txt = fs.readline()
        ii = ii+1
        if ((txt =='')|(txt == '\r\n')): 
            break
        if ii>=10:
            iindex=[]
            iii=-1
            while 1:
                iii = iii+1
                if (txt[iii] == '\t'):
                    iindex.append(iii)
                if txt[iii:iii+3]=='\t\r\n':
                    break
                
            Mat[ii-10,0] = txt[:iindex[0]]        
            for i_c in range(n_trace-1):
                Mat[ii-10,i_c+1] = txt[iindex[i_c]:iindex[i_c+1]]
    fs.close()
    return time,time_unit,Mat

def Read_RealTime_JPK(Fullpath):
    """ Mat = Read_RealTime_JPK(Path)
    Read real time trace from the JPK real time oscilloscope.
    Mat is a dictionnary with keys
    """
    fs = open(Fullpath,'r')
    txt = fs.readline()
    #freq = np.float(txt[18:]) #sample rate  in Hz
    
    txt = fs.readline()
    #txt = fs.readline()
    ii = -1
    indexes = []
    for truc in txt:
        ii = ii+1
        if truc ==' ':
            indexes.append(ii)
    
    columns_name = []
    ii = -1
    for index in indexes:
        ii = ii+1
        if ii >=2: #skip first space that does not count and start at the second 
            columns_name.append(txt[indexes[ii-1]:index].replace('"','').replace(' ',''))
    # miss the last
    columns_name.append(txt[index:].replace('\r\n','').replace(' ',''))
    
    Mat = {}
    for name in columns_name:
            Mat[name] = []
            
            
    while 1: 
        txt = fs.readline()
        if (txt =='#\r\n'): 
                break
    # Data begins
    
    
    while 1: 
        txt = fs.readline()
        #print(txt)
        if ((txt =='')|(txt == '\r\n')): 
            break
        #print(txt)
        ii = -1
        indexes = []
        indexes.append(0) # for the rest need a starting point
        for truc in txt:
            ii = ii+1
            if truc ==' ':
                indexes.append(ii)
        indexes.append(len(txt)) # to get the last
        ii = 0 
        for name in columns_name:
            Mat[name].append(np.float(txt[indexes[ii]:indexes[ii+1]]))
            ii = ii+1
    #for name in columns_name:
    #    Mat[name] = np.array( Mat[name])
    fs.close()
    return Mat 

def Read_spe_2X(spefilename, verbose=False):
    """ 
    Read a binary PI SPE file into a python dictionary

    Inputs:

        spefilename --  string specifying the name of the SPE file to be read
        verbose     --  boolean print debug statements (True) or not (False)

        Outputs
        spedict     
        
            python dictionary containing header and data information
            from the SPE file
            Content of the dictionary is:
            spedict = {'data':[],    # a list of 2D numpy arrays, one per image
            'IGAIN':pimaxGain,
            'EXPOSURE':exp_sec,
            'SPEFNAME':spefilename,
            'OBSDATE':date,
            'CHIPTEMP':detectorTemperature
            }

    I use the struct module to unpack the binary SPE data.
    Some useful formats for struct.unpack_from() include:
    fmt   c type          python
    c     char            string of length 1
    s     char[]          string (Ns is a string N characters long)
    h     short           integer 
    H     unsigned short  integer
    l     long            integer
    f     float           float
    d     double          float

    The SPE file defines new c types including:
        BYTE  = unsigned char
        WORD  = unsigned short
        DWORD = unsigned long


    Example usage:
    Given an SPE file named test.SPE, you can read the SPE data into
    a python dictionary named spedict with the following:
    >>> import piUtils
    >>> spedict = piUtils.readSpe('test.SPE')
    """
  
    # open SPE file as binary input
    spe = open(spefilename, "rb")
    
    # Header length is a fixed number
    nBytesInHeader = 4100

    # Read the entire header
    header = spe.read(nBytesInHeader)
    
    # version of WinView used
    swversion = struct.unpack_from("16s", header, offset=688)[0]
    
    # version of header used
    # Eventually, need to adjust the header unpacking
    # based on the headerVersion.  
    headerVersion = struct.unpack_from("f", header, offset=1992)[0]
  
    # which camera controller was used?
    controllerVersion = struct.unpack_from("h", header, offset=0)[0]
    if verbose:
        print "swversion         = ", swversion
        print "headerVersion     = ", headerVersion
        print "controllerVersion = ", controllerVersion
    
    # Date of the observation
    # (format is DDMONYYYY  e.g. 27Jan2009)
    date = struct.unpack_from("9s", header, offset=20)[0]
    
    # Exposure time (float)
    exp_sec = struct.unpack_from("f", header, offset=10)[0]
    
    # Intensifier gain
    pimaxGain = struct.unpack_from("h", header, offset=148)[0]

    # Not sure which "gain" this is
    gain = struct.unpack_from("H", header, offset=198)[0]
    
    # Data type (0=float, 1=long integer, 2=integer, 3=unsigned int)
    data_type = struct.unpack_from("h", header, offset=108)[0]

    comments = struct.unpack_from("400s", header, offset=200)[0]

    # CCD Chip Temperature (Degrees C)
    detectorTemperature = struct.unpack_from("f", header, offset=36)[0]

    # The following get read but are not used
    # (this part is only lightly tested...)
    analogGain = struct.unpack_from("h", header, offset=4092)[0]
    noscan = struct.unpack_from("h", header, offset=34)[0]
    pimaxUsed = struct.unpack_from("h", header, offset=144)[0]
    pimaxMode = struct.unpack_from("h", header, offset=146)[0]

    ########### here's from Kasey
    #int avgexp 2 number of accumulations per scan (why don't they call this "accumulations"?)
#TODO: this isn't actually accumulations, so fix it...    
    accumulations = struct.unpack_from("h", header, offset=668)[0]
    if accumulations == -1:
        # if > 32767, set to -1 and 
        # see lavgexp below (668) 
        #accumulations = struct.unpack_from("l", header, offset=668)[0]
        # or should it be DWORD, NumExpAccums (1422): Number of Time experiment accumulated        
        accumulations = struct.unpack_from("l", header, offset=1422)[0]
        
    """Start of X Calibration Structure (although I added things to it that I thought were relevant,
       like the center wavelength..."""
    xcalib = {}
    
    #SHORT SpecAutoSpectroMode 70 T/F Spectrograph Used
    xcalib['SpecAutoSpectroMode'] = bool( struct.unpack_from("h", header, offset=70)[0] )

    #float SpecCenterWlNm # 72 Center Wavelength in Nm
    xcalib['SpecCenterWlNm'] = struct.unpack_from("f", header, offset=72)[0]
    
    #SHORT SpecGlueFlag 76 T/F File is Glued
    xcalib['SpecGlueFlag'] = bool( struct.unpack_from("h", header, offset=76)[0] )

    #float SpecGlueStartWlNm 78 Starting Wavelength in Nm
    xcalib['SpecGlueStartWlNm'] = struct.unpack_from("f", header, offset=78)[0]

    #float SpecGlueEndWlNm 82 Starting Wavelength in Nm
    xcalib['SpecGlueEndWlNm'] = struct.unpack_from("f", header, offset=82)[0]

    #float SpecGlueMinOvrlpNm 86 Minimum Overlap in Nm
    xcalib['SpecGlueMinOvrlpNm'] = struct.unpack_from("f", header, offset=86)[0]

    #float SpecGlueFinalResNm 90 Final Resolution in Nm
    xcalib['SpecGlueFinalResNm'] = struct.unpack_from("f", header, offset=90)[0]

    #  short   BackGrndApplied              150  1 if background subtraction done
    xcalib['BackgroundApplied'] = struct.unpack_from("h", header, offset=150)[0]
    BackgroundApplied=False
    if xcalib['BackgroundApplied']==1: BackgroundApplied=True

    #  float   SpecGrooves                  650  Spectrograph Grating Grooves
    xcalib['SpecGrooves'] = struct.unpack_from("f", header, offset=650)[0]

    #  short   flatFieldApplied             706  1 if flat field was applied.
    xcalib['flatFieldApplied'] = struct.unpack_from("h", header, offset=706)[0]
    flatFieldApplied=False
    if xcalib['flatFieldApplied']==1: flatFieldApplied=True
    
    #double offset # 3000 offset for absolute data scaling */
    xcalib['offset'] = struct.unpack_from("d", header, offset=3000)[0]

    #double factor # 3008 factor for absolute data scaling */
    xcalib['factor'] = struct.unpack_from("d", header, offset=3008)[0]
    
    #char current_unit # 3016 selected scaling unit */
    xcalib['current_unit'] = struct.unpack_from("c", header, offset=3016)[0]

    #char reserved1 # 3017 reserved */
    xcalib['reserved1'] = struct.unpack_from("c", header, offset=3017)[0]

    #char string[40] # 3018 special string for scaling */
    xcalib['string'] = struct.unpack_from("40c", header, offset=3018)
    
    #char reserved2[40] # 3058 reserved */
    xcalib['reserved2'] = struct.unpack_from("40c", header, offset=3058)

    #char calib_valid # 3098 flag if calibration is valid */
    xcalib['calib_valid'] = struct.unpack_from("c", header, offset=3098)[0]

    #char input_unit # 3099 current input units for */
    xcalib['input_unit'] = struct.unpack_from("c", header, offset=3099)[0]
    """/* "calib_value" */"""

    #char polynom_unit # 3100 linear UNIT and used */
    xcalib['polynom_unit'] = struct.unpack_from("c", header, offset=3100)[0]
    """/* in the "polynom_coeff" */"""

    #char polynom_order # 3101 ORDER of calibration POLYNOM */
    xcalib['polynom_order'] = struct.unpack_from("c", header, offset=3101)[0]

    #char calib_count # 3102 valid calibration data pairs */
    xcalib['calib_count'] = struct.unpack_from("c", header, offset=3102)[0]

    #double pixel_position[10];/* 3103 pixel pos. of calibration data */
    xcalib['pixel_position'] = struct.unpack_from("10d", header, offset=3103)

    #double calib_value[10] # 3183 calibration VALUE at above pos */
    xcalib['calib_value'] = struct.unpack_from("10d", header, offset=3183)

    #double polynom_coeff[6] # 3263 polynom COEFFICIENTS */
    xcalib['polynom_coeff'] = struct.unpack_from("6d", header, offset=3263)

    #double laser_position # 3311 laser wavenumber for relativ WN */
    xcalib['laser_position'] = struct.unpack_from("d", header, offset=3311)[0]

    #char reserved3 # 3319 reserved */
    xcalib['reserved3'] = struct.unpack_from("c", header, offset=3319)[0]

    #unsigned char new_calib_flag # 3320 If set to 200, valid label below */
    #xcalib['calib_value'] = struct.unpack_from("BYTE", header, offset=3320)[0] # how to do this?

    #char calib_label[81] # 3321 Calibration label (NULL term'd) */
    xcalib['calib_label'] = struct.unpack_from("81c", header, offset=3321)

    #char expansion[87] # 3402 Calibration Expansion area */
    xcalib['expansion'] = struct.unpack_from("87c", header, offset=3402)
    ########### end of Kasey's addition

    if verbose:
        print "date      = ["+date+"]"
        print "exp_sec   = ", exp_sec
        print "pimaxGain = ", pimaxGain
        print "gain (?)  = ", gain
        print "data_type = ", data_type
        print "comments  = ["+comments+"]"
        print "analogGain = ", analogGain
        print "noscan = ", noscan
        print "detectorTemperature [C] = ", detectorTemperature
        print "pimaxUsed = ", pimaxUsed

    # Determine the data type format string for
    # upcoming struct.unpack_from() calls
    if data_type == 0:
        # float (4 bytes)
        dataTypeStr = "f"  #untested
        bytesPerPixel = 4
        dtype = "float32"
    elif data_type == 1:
        # long (4 bytes)
        dataTypeStr = "l"  #untested
        bytesPerPixel = 4
        dtype = "int32"
    elif data_type == 2:
        # short (2 bytes)
        dataTypeStr = "h"  #untested
        bytesPerPixel = 2
        dtype = "int32"
    elif data_type == 3:  
        # unsigned short (2 bytes)
        dataTypeStr = "H"  # 16 bits in python on intel mac
        bytesPerPixel = 2
        dtype = "int32"  # for numpy.array().
        # other options include:
        # IntN, UintN, where N = 8,16,32 or 64
        # and Float32, Float64, Complex64, Complex128
        # but need to verify that pyfits._ImageBaseHDU.ImgCode cna handle it
        # right now, ImgCode must be float32, float64, int16, int32, int64 or uint8
    else:
        print "unknown data type"
        print "returning..."
        sys.exit()
  
    # Number of pixels on x-axis and y-axis
    nx = struct.unpack_from("H", header, offset=42)[0]
    ny = struct.unpack_from("H", header, offset=656)[0]
    
    # Number of image frames in this SPE file
    nframes = struct.unpack_from("l", header, offset=1446)[0]

    if verbose:
        print "nx, ny, nframes = ", nx, ", ", ny, ", ", nframes
    
    npixels = nx*ny
    npixStr = str(npixels)
    fmtStr  = npixStr+dataTypeStr
    if verbose:
        print "fmtStr = ", fmtStr
    
    # How many bytes per image?
    nbytesPerFrame = npixels*bytesPerPixel
    if verbose:
        print "nbytesPerFrame = ", nbytesPerFrame

    # Create a dictionary that holds some header information
    # and contains a placeholder for the image data
    spedict = {'data':[],    # can have more than one image frame per SPE file
                'IGAIN':pimaxGain,
                'EXPOSURE':exp_sec,
                'SPEFNAME':spefilename,
                'OBSDATE':date,
                'CHIPTEMP':detectorTemperature,
                'COMMENTS':comments,
                'XCALIB':xcalib,
                'ACCUMULATIONS':accumulations,
                'FLATFIELD':flatFieldApplied,
                'BACKGROUND':BackgroundApplied
                }
    
    # Now read in the image data
    # Loop over each image frame in the image
    if verbose:
        print "Reading image frames number ",
    for ii in range(nframes):
        #iistr = str(ii)
        data = spe.read(nbytesPerFrame)
        if verbose:
            print ii," ",
    
        # read pixel values into a 1-D numpy array. the "=" forces it to use
        # standard python datatype size (4bytes for 'l') rather than native
        # (which on 64bit is 8bytes for 'l', for example).
        # See http://docs.python.org/library/struct.html
        dataArr = np.array(struct.unpack_from("="+fmtStr, data, offset=0),
                            dtype=dtype)

        # Resize array to nx by ny pixels
        # notice order... (y,x)
        dataArr.resize((ny, nx))
        #print dataArr.shape

        # Push this image frame data onto the end of the list of images
        # but first cast the datatype to float (if it's not already)
        # this isn't necessary, but shouldn't hurt and could save me
        # from doing integer math when i really meant floating-point...
        spedict['data'].append( dataArr.astype(float) )

    if verbose:
        print ""
  
    return spedict

class Read_PT3:
    def __init__(self,Path,debug='no'):

        f = open(Path, "rb")
        f = open(Path,'rb')
        f.read(584) # Reads all the shit above
        MeasDesc_Resolution      = struct.unpack('f',f.read(4))[0] # in ns macro resolution
        
        #MeasDesc_Resolution = 32e-3 # in ns
        f.read(116)
        CntRate0    = struct.unpack('i',f.read(4))[0]
        MeasDesc_GlobalResolution = 1./CntRate0
        print(MeasDesc_GlobalResolution)
        f.read(12)
        TTResult_NumberOfRecords     = struct.unpack('i',f.read(4))[0]
        Hdrsize     = struct.unpack('i',f.read(4))[0] #Size of special header
        if (Hdrsize != 0): #depending of point or image mode, header is there or not... 
            ImgHdr      = struct.unpack('36i',f.read(Hdrsize*4)) 
        else :
            pass

        # Read PT3

        RecNum_m         = np.zeros(TTResult_NumberOfRecords)
        Channel_m         = np.zeros(TTResult_NumberOfRecords)
        TimeTag_m         = np.zeros(TTResult_NumberOfRecords)
        MacroTime_m     = np.zeros(TTResult_NumberOfRecords)
        MicroTime_m     = np.zeros(TTResult_NumberOfRecords)
        dTime_m         = np.zeros(TTResult_NumberOfRecords)
        Event_type         = np.zeros(TTResult_NumberOfRecords) # I create this to distinguish between photon, overflow and markers
        # I use the following : 1 : photon; 2: overflow; 3: Frame marker, 4: line marker, 5: pixel marker, 0: unknown / error
        cnt_ph             = 0 # photon
        cnt_ov             = 0 # overflow
        cnt_ma            = 0 # overall markers
        cnt_ma_f        = 0 # frame marker
        cnt_ma_l        = 0 # line marker
        cnt_ma_p        = 0 # pixel marker
        cnt_ma_u        = 0 # unknown marker
        cnt_err            = 0 # errors
        ofltime         = 0
        WRAPAROUND         = 65536  # 2**16
        Hist             = np.zeros(2**12) 

        for ii in range (TTResult_NumberOfRecords):
            T3Record     = struct.unpack('I',f.read(4))[0]         # all 32 bits:
            #   +-------------------------------+  +-------------------------------+ 
            #   |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|  |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|
            #   +-------------------------------+  +-------------------------------+    
            
            nsync         = T3Record&(2**16-1)                     # the lowest 16 bits:  
            #   +-------------------------------+  +-------------------------------+ 
            #   | | | | | | | | | | | | | | | | |  |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|
            #   +-------------------------------+  +-------------------------------+    
            #
            
            Chan         = (T3Record&((2**4-1)<<(32-4)))>>(32-4) # the upper 4 bits:
            #   +-------------------------------+  +-------------------------------+ 
            #   |x|x|x|x| | | | | | | | | | | | |  | | | | | | | | | | | | | | | | |
            #   +-------------------------------+  +-------------------------------+       
            
            truensync         = ofltime + nsync
            RecNum_m[ii]     = ii
            Channel_m[ii]     = Chan
            TimeTag_m[ii]     = truensync
            MacroTime_m[ii] = truensync*MeasDesc_GlobalResolution*1e9 #ns
            
            if ((Chan ==1)|(Chan ==2)|(Chan ==3)|(Chan ==4)):
                dtime             = (T3Record&(2**12-1)<<16)>>16 # micro arrival time coded on 12 bytes (the ones after Chan)
                dTime_m[ii]     = dtime
                MicroTime_m[ii] = dtime*MeasDesc_Resolution*1e9 #ns
                Hist[dtime]     = Hist[dtime]+1
                Event_type[ii]  = 1
                cnt_ph             = cnt_ph+1

            elif Chan==15:
                #markers = bitand(bitshift(T3Record,-16),15) # where these four bits are markers:
                markers         = (T3Record&((2**4-1)<<16))>>16
                #   +-------------------------------+  +-------------------------------+ 
                #   | | | | | | | | | | | | |x|x|x|x|  | | | | | | | | | | | | | | | | |
                #   +-------------------------------+  +-------------------------------+
                cnt_ma             = cnt_ma+1

                if markers==0:                               # then this is an overflow record
                    ofltime         = ofltime + WRAPAROUND  # and we unwrap the numsync (=time tag) overflow
                    cnt_ov             = cnt_ov+1
                    Event_type[ii]     = 2

                elif markers==1:
                    cnt_ma_p        = cnt_ma_p+1
                    Event_type[ii]  = 5 

                elif markers==4:    # Should be frame
                    cnt_ma_f         = cnt_ma_f+1
                    Event_type[ii]  = 3

                elif markers==8:    # Should be line
                    cnt_ma_l     = cnt_ma_l+1
                    Event_type[ii]  = 4

                else :
                    cnt_ma_u = cnt_ma_u +1                                       
            else:
                cnt_err = cnt_err+1
        f.close()
        microtime_axe     = np.linspace(0,2**12*MeasDesc_Resolution*1e9,2**12) # nanoseconds
        
        self.hist                 = Hist
        self.microtime             = microtime_axe
        self.line_time          = 1
        self.num_records         = TTResult_NumberOfRecords
        self.macrotime_res         = MeasDesc_GlobalResolution#*1e-9 #ns
        self.microtime_res         = MeasDesc_Resolution#*1e-12 #ps
        self.event_num             = RecNum_m     
        self.event_chan         = Channel_m         
        self.event_timetg         = TimeTag_m         
        self.event_dtime         = dTime_m 
        self.event_macrotime     = MacroTime_m     
        self.event_microtime     = MicroTime_m     
        self.event_type         = Event_type
        self.line_m             = MacroTime_m[Event_type==4]
        self.frame_m             = MacroTime_m[Event_type==3]
        self.pixel_m             = MacroTime_m[Event_type==5]
        self.nb_lines             = Event_type[Event_type==4].shape[0]
        self.nb_frame             = Event_type[Event_type==3].shape[0] 
        self.nb_pixel             = Event_type[Event_type==5].shape[0]        
        self.nb_photon             = Event_type[Event_type==1].shape[0]
    
    def event_type_def(self):
        print("Definition of event types:\n0: unknown / error\n1: photon\n2: overflow\n3: Frame marker\n4: line marker\n5: pixel marker")
    def make_2D_image(self,x_dim,y_dim,duty_cycle):
        """ Fabricate a 2D intensity image in a x_dim x y_dim matrix, trace and retrace.
        Duty cycle takes into account the overrun of the AFM and should be found in the AFM file.
        The resulting matrix are saved in self.intens_t and self.intens_rt for trace and retrace respectively"""
        Flim_Int_t = np.zeros([x_dim,y_dim])
        Flim_Int_rt = np.zeros([x_dim,y_dim])
        # before starting things, I should check wether I have a trace+retrace or not
        if self.nb_lines<(2*y_dim):
            print('Not enough lines in the data, reduce y_dim')
        else:
            Line_time = (self.line_m[1]-self.line_m[0])*duty_cycle
            cnt_t = -1
            cnt_rt = -1
            for ii in range(2*y_dim):
                sys.stdout.write('\r Processing data : %d%%' %(100*ii/(2*y_dim-1)))
                sys.stdout.flush()
                #I have a line offset. like the JPK starts to record only after the first line... So I add +2 to the counter ii
                pixels_times = np.linspace(self.line_m[ii+2],self.line_m[ii+2]+ Line_time,x_dim+1)
                if np.mod(ii,2)==0:
                    cnt_t = cnt_t+1
                    for iii in range(x_dim):
                        Temp     = self.event_type[(self.event_macrotime>=pixels_times[iii]) & (self.event_macrotime<=pixels_times[iii+1])]
                        Flim_Int_t[cnt_t,iii]     = Temp[Temp==1].shape[0]#Event_type[(MacroTime_m>=pixels_times[iii]) & (MacroTime_m<=pixels_times[iii+1])].shape[0]        
                else:
                    cnt_rt = cnt_rt+1
                    for iii in range(x_dim):
                        Temp     = self.event_type[(self.event_macrotime>=pixels_times[iii]) & (self.event_macrotime<=pixels_times[iii+1])]
                        Flim_Int_rt[cnt_rt,x_dim-iii-1]     = Temp[Temp==1].shape[0]
            self.intens_t = Flim_Int_t
            self.intens_rt = Flim_Int_rt
    def plot_intens(self,axe_x,axe_y):
        """ Plot the 2D intensity map.
        make_2D_image should be run before.
        axe_x and axe_y are expected in microns"""
        if hasattr(self,'intens_t'):
            F = plt.figure()
            Fax = F.add_subplot(111)
            Fax.pcolorfast(axe_x,axe_y,self.intens_t)
            Fax.set_xlabel(r'x ($\mu$m)')
            Fax.set_ylabel(r'y ($\mu$m)')
            Fax.set_title('PicoHarp Trace')
            F.show()

            F = plt.figure()
            Fax = F.add_subplot(111)
            Fax.pcolorfast(axe_x,axe_y,self.intens_rt)
            Fax.set_xlabel(r'x ($\mu$m)')
            Fax.set_ylabel(r'y ($\mu$m)')
            Fax.set_title('PicoHarp Retrace')
            F.show()
        else:
            print('run .make_2D_image first !')


def powerpoint_style(fig,Axe_tick_size=15,Line_size=3) :
    """ Elargit les traits, agrandit les labels.""" 
    #fig = plt.gcf()
    def myfunc(x):
        return hasattr(x, 'set_linewidth')
    for o in fig.findobj(myfunc):
        o.set_linewidth(Line_size)
           
    def myfunc(x):
        return hasattr(x, 'set_markersize')
    for o in fig.findobj(myfunc):
        o.set_markersize(Line_size+4)
    def myfunc(x):
        return hasattr(x, 'set_markeredgewidth')
    for o in fig.findobj(myfunc):
        o.set_markeredgewidth(Line_size)
    for ax in fig.axes:
    
        # trouve tous les trucs avec linewidth et les modifie
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(Axe_tick_size)
            
        #for item in ([ax.xaxis.label, ax.yaxis.label]):
        #    item.set_fontsize(Axe_tick_size+5)
        for line in ax.get_xticklines() + ax.get_yticklines():
            line.set_markersize(Line_size+2)
            line.set_markeredgewidth(Line_size)

def Read_JPKsweep(Path):
    x,y,z=[],[],[]
    index_line = []
    fs = open(Path, 'r')
    #print('Open new fic') 
    #index_array = 0
    while 1: 
        txt = fs.readline()
        #print(txt)
        if ((txt =='')|(txt == '\r\n')): 
            break
        if txt[0] =='#':
            pass
        else:
            #print(txt)
            ii=-1
            index_line=[]
            while 1: # on cherche le premier espace qui limite le premier nombre
                ii = ii+1 
                if (txt[ii:ii+1] == '\t'):
                    index_line.append(ii)
                if (txt[ii:ii+4] == '\r\n'):
                    break
            x.append(float(txt[:index_line[0]]))
            y.append(float(txt[index_line[0]+1:index_line[1]]))
            z.append(float(txt[index_line[1]+1:]))  
    
            
    fs.close()
    x = np.array(x) # frequency (Hz)
    y = np.array(y) # amplitude (V)
    z = np.array(z) # phase (deg)
    return x,y,z


def convert_to_powerdensity(P):
    """ Given an incident power P into the microscope objective, what is the power density in a confocal spot of different size"""
    A1 = np.pi*500e-9/4 # 500nm diameter
    dPm2 = P/A1 # unit of P/m2
    dPcm2 = dPm2/1e4
    print("power density = %s mW/m2"%dPm2)
    print("power density = %s mW/cm2"%dPcm2)

# Different square-root definition to cut in the complex plane
def maystre(z): # diagonale dans le plan complexe
    return np.sqrt(1j)*np.sqrt(-1j*z)

def antima(z): # partie imaginaire négative
    return -np.sqrt(-1j)*np.sqrt(1j*z)

def posimag(z): # partie imaginaire positive
    return 1j*np.conj(np.sqrt(np.conj(-z)))



# Argh j'ai efface la classe qu'il fallait... Je sais pas trop avec git comment faire.. 

def near(z):
    z = np.array(z,dtype=complex)
    racine = z.copy()
    racine[0] = maystre(z[0])
    for ii in range(np.size(z)-1):
        racine1 = maystre(z[ii+1])
        racine2 = antima(z[ii+1])
        if (np.abs(racine[ii]-racine1) < np.abs(racine[ii]-racine2)):
            racine[ii+1] = racine1
        else:
            racine[ii+1] = racine2
    return racine
#Recup !
class Near:
    def __init__(self, value):
        self.previous = value
    def next(self,z):
        s = np.sqrt(z)
        d1 = np.abs(self.previous - s)
        d2 = np.abs(self.previous + s)
        self.previous = ((d1 <= d2)*2-1)*s
        return self.previous            
