# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 10:06:27 2019

@author: admin
"""
import numpy as np
import matplotlib.pylab as plt
import struct as struct
import sys as sys





def JPK_ASCII(Pathname):
    f           = open(Pathname,'r')
    Infor       = []
    retu_Infor  = []
    for ii in range(0,20):
        line    = f.readline()
        Infor.append(map(str,line.split()))  
    xLength     = np.float(Infor[5][2])*1e9    
    yLength     = np.float(Infor[6][2])*1e9

    xPixel      = np.int(Infor[9][2])
    yPixel      = np.int(Infor[10][2])
    
    im = np.ndarray([xPixel,yPixel])
    if Infor[16][2] == 'ac':
        for ii in range(0,14):
            line = f.readline()
            Infor.append(map(str,line.split()))
        for ii in range(xPixel):
            line = f.readline()
            im[:,ii] = map(str,line.split())
            
    if Infor[16][2] == 'contact':
        for ii in range(0,8):
            line = f.readline()
            Infor.append(map(str,line.split()))
        for ii in range(xPixel):
            line = f.readline()
            im[:,ii] = map(str,line.split())
            
    if Infor[16][2] == 'intermittent-contact':
        for ii in range(0,13):
            line = f.readline()
            Infor.append(map(str,line.split()))
        for ii in range(xPixel):
            line = f.readline()
            im[:,ii] = map(str,line.split())
    f.close()
    time_Infor = Infor[-5][-3]
    im = np.array(im)
    retu_Infor = [im,xLength,yLength,xPixel,yPixel,time_Infor]
    return retu_Infor

class Read_PHR800_T3:
    def __init__(self,Path,debug='no'):
   
#        tyEmpty8      = '0xffff0008'
#        tyBool8       = '0x00000008'
#        tyInt8        = '0x10000008'
#        tyBitSet64    = '0x11000008'
#        tyColor8      = '0x12000008'
#        tyFloat8      = '0x20000008'
#        tyTDateTime   = '0x21000008'
#        tyFloat8Array = '0x2001ffff'
#        tyAnsiString  = '0x4001ffff'
#        tyWideString  = '0x4002ffff'
#        tyBinaryBlob  = '0xffffffff'
## RecordTypes
#        rtPicoHarpT3     = '0x10303'# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $03 (PicoHarp)
#        rtPicoHarpT2     = '0x10203'# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $03 (PicoHarp)


# In the matlab file they us a "while 1 ; if; break end;end;" and each time read some header to find what the type is. 
# one need some hexadecimal constants to compare to the header.

# First I do one by one to get things clear
        f = open(Path,"rb") # open file and read it as binary
        
        
        
#        tyEmpty8 = '0xffff0008'
#        tyBool8 = '0x00000008'
#        tyInt8 = '0x10000008'
#        tyBitSet64 = '0x11000008'
#        tyColor8 = '0x12000008'
#        tyFloat8 = '0x20000008'
#        tyTDateTime = '0x21000008'
#        tyFloat8Array = '0x2001ffff'
#        tyAnsiString = '0x4001ffff'
#        tyWideString = '0x4002ffff'
#        tyBinaryBlob = '0xffffffff'
#        # RecordTypes
#        rtPicoHarpT3 = '0x10303'  # (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $03 (PicoHarp)
#        rtPicoHarpT2 = '0x10203'  # (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $03 (PicoHarp)
        #####################################################################################################################################
        #debug = 'no'
        #f = open(Path_JPK + Filename_Pico, "rb")
        # Read example
        # toto      = struct.unpack('f',f.read(4))[0] # in ns
        file_type = struct.unpack('8s', f.read(8))[0]  # string 8 character
        version = struct.unpack('8s', f.read(8))[0]
        # {DE019A49-8DAD-44E1-E18B-A9B487725615}
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        
        TagIdx = struct.unpack('i', f.read(4))[0]  # fread(fid, 1, 'int32');
        # there is a loop on this, print to print stuff . I don't care now. printed as is if -1 and something else if >-1 					# integer 32 bits ?
        TagTyp = struct.unpack('I', f.read(4))[0]
        # TagTyp is compared to the constants defined above to know what type we're dealing with. I don't know the function to convert hexadecimal to decimal
        # but I know how to convert decimal to hexadecimal. For speed consideration I might find this later on.
        
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        
        TagInt = struct.unpack('Q', f.read(8))[0]  # Here need to read 64 bits !!
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # PicoHarp 300: HWSETG SWSETG BinDATA    
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # 3.0
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # PicoHarp Software\
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # 3.0.0.1
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # 42115.6585279 # Date
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyTDateTime   = '0x21000008':
        TagFloat = struct.unpack('d', f.read(8))[0]  # have to figure out how to convert this to a usable date
        #print(TagFloat)
        
        # T3 Mode
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # Measurement_Mode, 3
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # Measurement_SubMode, 0
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008': Int8
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # TTResult_StopReason 0
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # Fast_Load_End 0
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp) == tyEmpty8      = '0xffff0008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ### TTResultFormat_TTTRRecType determine if T3 or T2 records. hex(TTResultFormat_TTTRRecType) = 0x10303 for T3 and 0x10203 for T2
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        TTResultFormat_TTTRRecType = TagInt
        #print(TagIndent, TagInt)
        
        #### TTResultFormat_BitsPerRecord #### Should be 32 bits
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        TTResultFormat_BitsPerRecord = TagInt
        #print(TagIndent, TagInt)
        
        ##### MeasDesc_BinningFactor
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        Binning_Factor = TagInt
        #print(TagIndent, TagInt)
        
        ##### MeasDesc_Offset
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        Mes_Offset = TagInt
        #print(TagIndent, TagInt)
        
        ##### MeasDesc_AcquisitionTime
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        # Aq_Time = TagInt/1e3 #seconds
        #print(TagIndent, TagInt)
        
        ##### MeasDesc_StopAt
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ##### MeasDesc_StopOnOvfl
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ###### MeasDesc_Restart
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ###### CurSWSetting_DispLog
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ##### CurSWSetting_DispAxisTimeFrom
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispAxisTimeTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ##### CurSWSetting_DispAxisCountFrom
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ##### CurSWSetting_DispAxisCountTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurves
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### CurSWSetting_DispCurve_MapTo
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # # CurSWSetting_DispCurve_Show
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #### HW_Type : Picoharp 300
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # # # ???? 930004
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # # # ???? 2.0
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # ???? 1020840
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyAnsiString = '0x4001ffff':
        TagInt = struct.unpack('Q', f.read(8))[0]
        TagString = struct.unpack(str(TagInt) + 's', f.read(TagInt))
        #print(TagString)
        
        # HWSync_Divider
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        HW_Sync_Divider = TagInt
        #print(TagIndent, TagInt)
        
        # HWSync_Offset
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWSync_CFDZeroCross
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWSync_CFDLevel
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HW_InpChannels
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWInpChan_CFDZeroCross
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWInpChan_CFDLevel
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # MeasDesc_Resolution       
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]  # integer 32 bits ?
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyFloat8 = '0x20000008', reads as 8 bytes double
        TagInt = struct.unpack('d', f.read(8))[0]
        MeasDesc_Resolution = TagInt
        #print(TagIndent, TagInt)
        
        # HW_BaseResolution 
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyFloat8 = '0x20000008', reads as 8 bytes double
        TagInt = struct.unpack('d', f.read(8))[0]
        HW_BaseResolution = TagInt
        #print(TagIndent, TagInt)
        
        # HW_ExternalDevices  
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouter_ModelCode 
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouter_Channels
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouter_Enabled 
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, -TagInt)
        
        # HWRouterChan_InputType
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('Q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        # HWRouterChan_InputLevel
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        #############################################################################
        # HWRouterChan_RisingEdge 
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        ###################################################################
        # HWRouterChan_Offset
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        # HWRouterChan_CFDPresent
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        # HWRouterChan_InputType(2)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        # HWRouterChan_InputLevel(2)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        # HWRouterChan_RisingEdge(2)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        # HWRouterChan_Offset(2)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouterChan_CFDPresent(2)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouterChan_InputType(3)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        # HWRouterChan_InputLevel(3)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        # HWRouterChan_RisingEdge(3)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        # HWRouterChan_Offset(3)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouterChan_CFDPresent(3)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouterChan_InputType(4)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        
        # HWRouterChan_InputLevel(4)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, TagInt)
        # HWRouterChan_RisingEdge(4)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        # HWRouterChan_Offset(4)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWRouterChan_CFDPresent(4)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ####################################################################################################
        # HW_Markers
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWMarkers_RisingEdge(1)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ##HWMarkers_RisingEdge(2)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWMarkers_RisingEdge(3)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        ##HWMarkers_RisingEdge(4)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # HWMarkers_Enabled(1)
        
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyBool8  = '0x00000008'
        TagInt = struct.unpack('q', f.read(8))[0]  # boolean, False if 0, TRUE if anything else... Don't care now
        #print(TagIndent, -TagInt)
        
        # HWMarkers_Enabled(2)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, -TagInt)
        
        # HWMarkers_Enabled(3)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, -TagInt)
        
        # HWMarkers_Enabled(4)
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, -TagInt)
        
        # HWMarkers_HoldOff
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]  # fread(fid, 1, 'int32');					# integer 32 bits ?
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # MeasDesc_GlobalResolution
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyFloat8 = '0x20000008': reads as 8 bytes double
        TagInt = struct.unpack('d', f.read(8))[0]
        MeasDesc_GlobalResolution = TagInt
        #print(TagIndent, TagInt)
        
        # TTResult_SyncRate
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        Sync_Rate = TagInt
        #print(TagIndent, TagInt)
        
        # TTResult_InputRate
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        InputRate = TagInt
        #print(TagIndent, TagInt)
        
        # TTResult_StopAfter
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        #print(TagIndent, TagInt)
        
        # TTResult_NumberOfRecords
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyInt8 = '0x10000008'
        TagInt = struct.unpack('Q', f.read(8))[0]
        TTResult_NumberOfRecords = TagInt
        #print(TagIndent, TagInt)
        # Header_End ##### END OF THE HEADER
        TagIndent = struct.unpack('32s', f.read(32))[0]  # string 32 character
        TagIdx = struct.unpack('i', f.read(4))[0]
        TagTyp = struct.unpack('I', f.read(4))[0]
        # hex(TagTyp)== tyEmpty8 = '0xffff0008'
        #print(TagIndent[0:10])
        
        # We can perform some tests
        #print('---- Tests 1 ----')
        if TTResultFormat_BitsPerRecord == 32:
            pass
        else:
            print('Error: not 32 bits TTR records')
        if hex(TTResultFormat_TTTRRecType) == '0x10303':
            pass
        elif hex(TTResultFormat_TTTRRecType) == '0x10203':
            print('Error, T2 format !')
        else:
            print('Error, unknown format')
        
        # if MeasDesc_GlobalResolution == 1./Sync_Rate:
        #	pass
        # else:
        #	print('Error: something is wrong with Macrotime resolution and synchronization rate')
        
        if np.round(MeasDesc_Resolution * 1e12) == Binning_Factor * HW_BaseResolution * 1e12:
            pass
        else:
            print('Error: resolution/binning problem. Check MeasDesc_Resolution = Binning_Factor*HW_Baseresolution')
        # if Input_Rate>=(Sync_Rate*5./100):
        #	print('WARNING: count rate too high for reliable single photon emission statistic. Risk of pile-up effect')
        # else:
        #	pass
        
        #print('---- End Test 1 ----')
        # Now we start looking at the data...
        #t1 = datetime.datetime.now()
        
        #print(t1)
        
        RecNum = np.zeros(TTResult_NumberOfRecords)  # the recorded number of all events
        Channel = np.zeros(TTResult_NumberOfRecords)  # the channel # of the event, if the event is photon event
        TimeTag = np.zeros(TTResult_NumberOfRecords)
        MacroTime = np.zeros(TTResult_NumberOfRecords)
        MicroTime = np.zeros(TTResult_NumberOfRecords)
        #dTime = np.zeros(TTResult_NumberOfRecords)
        #MicroTime_Ch1 = np.zeros(TTResult_NumberOfRecords)
        #dTime_Ch1 = np.zeros(TTResult_NumberOfRecords)
        #MacroTime_Ch1 = np.zeros(TTResult_NumberOfRecords)
        #MicroTime_Ch2 = np.zeros(TTResult_NumberOfRecords)
        #dTime_Ch2 = np.zeros(TTResult_NumberOfRecords)
        #MacroTime_Ch2 = np.zeros(TTResult_NumberOfRecords)
        #MicroTime_Ch3 = np.zeros(TTResult_NumberOfRecords)
        #dTime_Ch3 = np.zeros(TTResult_NumberOfRecords)
        #MacroTime_Ch3 = np.zeros(TTResult_NumberOfRecords)
        MicroTime_Ch4 = np.zeros(TTResult_NumberOfRecords)
        #dTime_Ch4 = np.zeros(TTResult_NumberOfRecords)
        MacroTime_Ch4 = np.zeros(TTResult_NumberOfRecords)
        Event_type = np.zeros(TTResult_NumberOfRecords)
        pt = np.zeros(TTResult_NumberOfRecords)
        sync = np.zeros(TTResult_NumberOfRecords)
        
        # I create this to distinguish between photon, overflow and markers
        # I use the following : 1 : photon; 2: overflow; 3: Frame marker, 4: line marker, 5: pixel marker, 0: unknown / error
        cnt_ph_Ch1 = 0  # photon
        cnt_ph_Ch2 = 0
        cnt_ph_Ch3 = 0  # photon
        cnt_ph_Ch4 = 0
        cnt_ph = 0
        cnt_ov = 0  # overflow
        cnt_ma = 0  # overall markers
        cnt_ma_f = 0  # frame marker
        cnt_ma_l = 0  # line marker
        cnt_ma_p = 0  # pixel marker
        cnt_ma_u = 0  # unknown marker
        cnt_err = 0  # errors
        ofltime = 0
        WRAPAROUND_T3 = 65536  # 2**16
        
        syncperiod = 1e9 / Sync_Rate  # in nanoseconds
        print('Sync Rate = %d / second\n', Sync_Rate)
        print('Sync Period = %5.4f ns\n', syncperiod)
        
        Hist = np.zeros(2 ** 12)
        Hist_Ch1 = np.zeros(2 ** 12)
        Hist_Ch2 = np.zeros(2 ** 12)
        Hist_Ch3 = np.zeros(2 ** 12)
        Hist_Ch4 = np.zeros(2 ** 12)
        for ii in range(TTResult_NumberOfRecords):
            T3Record = struct.unpack('I', f.read(4))[0]  # all 32 bits:   #####all data
            #   +-------------------------------+  +-------------------------------+
            #   |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|  |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|
            #   +-------------------------------+  +-------------------------------+
        
            nsync = T3Record & (2 ** 16 - 1)  # the lowest 16 bits:  #####laser
            #   +-------------------------------+  +-------------------------------+
            #   | | | | | | | | | | | | | | | | |  |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|
            #   +-------------------------------+  +-------------------------------+
            #
        
            Chan = (T3Record & ((2 ** 4 - 1) << (32 - 4))) >> (32 - 4)  # the upper 4 bits:
            #   +-------------------------------+  +-------------------------------+
            #   |x|x|x|x| | | | | | | | | | | | |  | | | | | | | | | | | | | | | | |
            #   +-------------------------------+  +-------------------------------+
            truensync = ofltime + nsync  # the true number of syncs, which is the number of syncs adding the overflow time
            MacroTime[ii] = truensync * MeasDesc_GlobalResolution * 1e9
            dtime = 0
            if (Chan <= 4):    # Chan == 1,2,3,or 4 means the event is photon event from channel 1,2,3, or 4
                if Chan == 1:
                    RecNum[ii] = ii
                    Channel[ii] = Chan
                    #truensync = ofltime + nsync
                    #TimeTag[ii] = truensync
                    #MacroTime_Ch1[ii] = truensync * MeasDesc_GlobalResolution * 1e9
                    dtime = (T3Record & (2 ** 12 - 1) << 16) >> 16  # micro arrival time coded on 12 bytes (the ones after Chan)
                    #dTime_Ch1[ii] = dtime
                    #dTime[ii] = dtime
                    #MicroTime_Ch1[ii] = dtime * MeasDesc_Resolution * 1e9  # ns
                    MicroTime[ii] = dtime * MeasDesc_Resolution   # ns
                    #Hist_Ch1[dtime] = Hist_Ch1[dtime] + 1
                    Event_type[ii] = 1
                    #cnt_ph_Ch1 = cnt_ph_Ch1 + 1
                #
                #
                #
                if Chan == 2:
                    RecNum[ii] = ii
                    Channel[ii] = Chan
                    #truensync = ofltime + nsync
                    #TimeTag[ii] = truensync
                    dtime = (T3Record & (2 ** 12 - 1) << 16) >> 16  # micro arrival time coded on 12 bytes (the ones after Chan)
                    MicroTime[ii] = dtime * MeasDesc_Resolution   # ns
                    #Hist_Ch2[dtime] = Hist_Ch2[dtime] + 1
                    Event_type[ii] = 1
                    #cnt_ph_Ch2 = cnt_ph_Ch2 + 1
        
                if Chan == 3:
                    RecNum[ii] = ii
                    Channel[ii] = Chan
                    #truensync = ofltime + nsync
                    #TimeTag[ii] = truensync
                    #MacroTime_Ch3[ii] = truensync * MeasDesc_GlobalResolution * 1e9
                    dtime = (T3Record & (2 ** 12 - 1) << 16) >> 16  # micro arrival time coded on 12 bytes (the ones after Chan)
                    #dTime_Ch3[ii] = dtime
                    MicroTime[ii] = dtime * MeasDesc_Resolution   # ns
                    #Hist_Ch3[dtime] = Hist_Ch3[dtime] + 1
                    Event_type[ii] = 1
                    #cnt_ph_Ch3 = cnt_ph_Ch3 + 1
        
                if Chan == 4:
                    RecNum[ii] = ii
                    Channel[ii] = Chan
                    truensync = ofltime + nsync
                    TimeTag[ii] = truensync
                    MacroTime_Ch4[ii] = truensync * MeasDesc_GlobalResolution 
                    dtime = (T3Record & (2 ** 12 - 1) << 16) >> 16  # micro arrival time coded on 12 bytes (the ones after Chan)
                    #dTime_Ch4[ii] = dtime
                    MicroTime[ii] = dtime * MeasDesc_Resolution*1e9   # ns
                    #Hist_Ch4[dtime] = Hist_Ch4[dtime] + 1
                    Event_type[ii] = 1
                    #cnt_ph_Ch4 = cnt_ph_Ch4 + 1
        
            elif Chan == 15:  # Chan == 15 (all bits being 1) means the event is a marker event, then we go to see the four bits telling us what marker is it
                #		markers = bitand(bitshift(T3Record,-16),15) # where these four bits are markers:
                markers = (T3Record & ((2 ** 4 - 1) << 16)) >> 16
                #   +-------------------------------+  +-------------------------------+
                #   | | | | | | | | | | | | |x|x|x|x|  | | | | | | | | | | | | | | | | |
                #   +-------------------------------+  +-------------------------------+
                cnt_ma = cnt_ma + 1
                if markers == 0:  # then this is an overflow record
                    ofltime = ofltime + WRAPAROUND_T3  # and we unwrap the numsync (=time tag) overflow
                    cnt_ov = cnt_ov + 1
                    Event_type[ii] = 2
                elif markers == 8:  #  pixel marker (the specific meaning depends on how we add the external marker signals to the marker channels)
                    cnt_ma_p = cnt_ma_p + 1
                    Event_type[ii] = 5
                elif markers == 1:  # Should be frame
                    cnt_ma_f = cnt_ma_f + 1
                    Event_type[ii] = 3
                elif markers == 4:  # Should be line
                    cnt_ma_l = cnt_ma_l + 1
                    Event_type[ii] = 4
                else:
                    cnt_ma_u = cnt_ma_u + 1
            else:
                # print ii
                # print("wrong stuff")
                cnt_err = cnt_err + 1
            # I got two guys, they are the first two events, with 0 macrotime.
        f.close()
        		# I got two guys, they are the first two events, with 0 macrotime.
        #f.close()
        #microtime_axe     = np.linspace(0,2**12*MeasDesc_Resolution*1e9,2**12)
        self.hist                 = Hist
#        self.microtime             = microtime_axe
        self.syncperiod         =syncperiod
        self.line_time          = 1
        self.num_records         = TTResult_NumberOfRecords
        self.macrotime_res         = MeasDesc_GlobalResolution#*1e-9 #ns
        self.microtime_res         = MeasDesc_Resolution#*1e-12 #ps
        self.event_num             = RecNum     
        self.event_chan            = Channel         
        self.event_timetg          = TimeTag         
#        self.event_dtime_Chan_1         = dTime_m_Chan_1
#        self.event_dtime_Chan_2         = dTime_m_Chan_2
#        self.event_dtime_Chan_3         = dTime_m_Chan_3
#        self.event_dtime_Chan_4         = dTime_m_Chan_4
        self.event_MacroTime     = MacroTime
#        self.event_macrotime_Chan_1     = MacroTime_m_Chan_1 
#        self.event_macrotime_Chan_2     = MacroTime_m_Chan_2 
#        self.event_macrotime_Chan_3     = MacroTime_m_Chan_3 
#        self.event_macrotime_Chan_4     = MacroTime_m_Chan_4 
#        self.event_microtime_Chan_1      = MicroTime_m_Chan_1
#        self.event_microtime_Chan_2      = MicroTime_m_Chan_2
#        self.event_microtime_Chan_3      = MicroTime_m_Chan_3
#        self.event_microtime_Chan_4      = MicroTime_m_Chan_4
        self.event_MicroTime     = MicroTime
        self.event_type         = Event_type
        #self.unknow_m             = MacroTime_m[Event_type==0]
        self.line_m             = MacroTime[Event_type==4]
        self.frame_m             = MacroTime[Event_type==3]
        self.pixel_m             = MacroTime[Event_type==5]
        #self.pixel_m_Chan_1       = MacroTime_m_Chan_1 [Event_type==5]
        self.nb_lines             = Event_type[Event_type==4].shape[0]
        self.nb_frame             = Event_type[Event_type==3].shape[0] 
        self.nb_pixel             = Event_type[Event_type==5].shape[0]        
        self.nb_photon             = Event_type[Event_type==1].shape[0]
        self.sync                  =sync
        self.pt                    =pt
        self.cnt_ph_Ch1            =cnt_ph_Ch1
        self.cnt_ph_Ch2            =cnt_ph_Ch2
        self.cnt_ph_Ch3            =cnt_ph_Ch3
        self.cnt_ph_Ch4            =cnt_ph_Ch4
        self.cnt_ph                =cnt_ph
        self.Hist_Ch1              =Hist_Ch1
        self.Hist_Ch2              =Hist_Ch2
        self.Hist_Ch3              =Hist_Ch3        
        self.Hist_Ch4              =Hist_Ch4  
        self.MacroTime_Ch4         =MacroTime_Ch4
        self.MicroTime_Ch4         =MicroTime_Ch4
        
    def event_type_def(self):
        print("Definition of event types:\n0: unknown / error\n1: photon\n2: overflow\n3: Frame marker\n4: line marker\n5: pixel marker")     
#    def __getitem__(self,a) :
#        return Read_PTU(self.__getitem__(a))