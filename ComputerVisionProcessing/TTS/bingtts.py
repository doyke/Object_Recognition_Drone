#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import os
import sys
import argparse
import shutil

# Define a few maps for reference
namemap = {
    "ar-EG,Female" : "Microsoft Server Speech Text to Speech Voice (ar-EG, Hoda)",
    "de-DE,Female" : "Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)",
    "de-DE,Male" : "Microsoft Server Speech Text to Speech Voice (de-DE, Stefan, Apollo)",
    "en-AU,Female" : "Microsoft Server Speech Text to Speech Voice (en-AU, Catherine)",
    "en-CA,Female" : "Microsoft Server Speech Text to Speech Voice (en-CA, Linda)",
    "en-GB,Female" : "Microsoft Server Speech Text to Speech Voice (en-GB, Susan, Apollo)",
    "en-GB,Male" : "Microsoft Server Speech Text to Speech Voice (en-GB, George, Apollo)",
    "en-IN,Male" : "Microsoft Server Speech Text to Speech Voice (en-IN, Ravi, Apollo)",
    "en-US,Male" : "Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)",
    "en-US,Female" : "Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)",
    "es-ES,Female" : "Microsoft Server Speech Text to Speech Voice (es-ES, Laura, Apollo)",
    "es-ES,Male" : "Microsoft Server Speech Text to Speech Voice (es-ES, Pablo, Apollo)",
    "es-MX,Male" : "Microsoft Server Speech Text to Speech Voice (es-MX, Raul, Apollo)",
    "fr-CA,Female" : "Microsoft Server Speech Text to Speech Voice (fr-CA, Caroline)",
    "fr-FR,Female" : "Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)",
    "fr-FR,Male" : "Microsoft Server Speech Text to Speech Voice (fr-FR, Paul, Apollo)",
    "it-IT,Male" : "Microsoft Server Speech Text to Speech Voice (it-IT, Cosimo, Apollo)",
    "ja-JP,Female" : "Microsoft Server Speech Text to Speech Voice (ja-JP, Ayumi, Apollo)",
    "ja-JP,Male" : "Microsoft Server Speech Text to Speech Voice (ja-JP, Ichiro, Apollo)",
    "pt-BR,Male" : "Microsoft Server Speech Text to Speech Voice (pt-BR, Daniel, Apollo)",
    "ru-RU,Female" : "Microsoft Server Speech Text to Speech Voice (ru-RU, Irina, Apollo)",
    "ru-RU,Male" : "Microsoft Server Speech Text to Speech Voice (ru-RU, Pavel, Apollo)",
    "zh-CN,Female" : "Microsoft Server Speech Text to Speech Voice (zh-CN, HuihuiRUS)",
    "zh-CN,Male" : "Microsoft Server Speech Text to Speech Voice (zh-CN, Kangkang, Apollo)",
    "zh-HK,Male" : "Microsoft Server Speech Text to Speech Voice (zh-HK, Danny, Apollo)",
    "zh-TW,Female" : "Microsoft Server Speech Text to Speech Voice (zh-TW, Yating, Apollo)",
    "zh-TW,Male" : "Microsoft Server Speech Text to Speech Voice (zh-TW, Zhiwei, Apollo)"
    }
    
formatmap = {
    "raw-8khz-8bit-mono-mulaw" : None,
    "raw-16khz-16bit-mono-pcm" : None,
    "riff-8khz-8bit-mono-mulaw" : None,
    "riff-16khz-16bit-mono-pcm" : None
}

# Get config from CLI args
i = 0
argsDict = {}
for item in sys.argv:
    if i == 0:
        i = i + 1
        pass
    else:
        i = i + 1
        paramname, paramval = item.partition("=")[::2]
        argsDict[paramname] = paramval

try:
    helpReq = argsDict['--help']
    print ""
    print "Usage:", sys.argv[0], '--cache=/path/to/cache --dest=/path/to/destination/file.wav --lang=en-US,Female --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text="Hello World"'
    print ""
    print "--cache         : Location of file cache. Useful if you repeatedly request"
    print "                      the same text to speech and wish to conserve bandwidth"
    print "                      and reduce Azure costs. Must be writeable."
    print "--dest          : Location for the output file. Must be writeable."
    print "--lang          : Language and gender to be spoken. Case sensitive."
    print "--fileformat    : Format of the output file."
    print "--apikey        : API key generated by Azure."
    print "--text          : Text to convert to speech. MUST be enclosed in double quotes."
    print ""
    print "Available language combinations (--lang):"
    for item, value in namemap.iteritems():
        langcombo = item.split(",")
        print "Language:", langcombo[0], "    Gender:", langcombo[1]
    print ""
    print "Available file formats:"
    for item, value in formatmap.iteritems():
        print item
    sys.exit(0)
except:
    pass
    
    

try:
    destLoc = argsDict['--dest']
except:
    print ""
    print "Error: destination location not specified."
    print ""
    print "Usage:", sys.argv[0], '--cache=/path/to/cache --dest=/path/to/destination --lang=en-US,Female --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text="Hello World"'
    print ""
    sys.exit(1)

try:
    ttsLangKey = argsDict['--lang']
except:
    print ""
    print "Error: language and gender not specified."
    print ""
    print "Usage:", sys.argv[0], '--cache=/path/to/cache  --dest=/path/to/destination --lang=en-US,Female --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text="Hello World"'
    print ""
    sys.exit(1)
    
try:
    ttsFormat = argsDict['--fileformat']
except:
    print ""
    print "Error: file format not specified."
    print ""
    print "Usage:", sys.argv[0], '--cache=/path/to/cache --dest=/path/to/destination --lang=en-US,Female --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text="Hello World"'
    print ""
    sys.exit(1)
    
try:
    ttsText = argsDict['--text']
except:
    print ""
    print "Error: text not specified."
    print ""
    print "Usage:", sys.argv[0], '--cache=/path/to/cache --dest=/path/to/destination --lang=en-US,Female --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text="Hello World"'
    print ""
    sys.exit(1)

try:
    ttsApiKey = argsDict['--apikey']
except:
    print ""
    print "Error: API key not specified."
    print ""
    print "Usage:", sys.argv[0], '--cache=/path/to/cache --dest=/path/to/destination --lang=en-US,Female --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text="Hello World"'
    print ""
    sys.exit(1)    

try:
    ttsCache = argsDict['--cache']
except:
    ttsCache = None

try:
    ttsLangGend = ttsLangKey.split(',')
    ttsLang = ttsLangGend[0]
    ttsGender = ttsLangGend[1].title()
    servicename = namemap[ttsLang + ',' + ttsGender]
except:
    print ""
    print "Error: invalid language or gender specified, or invalid combination: The following language/gender combinations are available:"
    print ""
    for item, value in namemap.iteritems():
        langcombo = item.split(",")
        print "Language:", langcombo[0], "    Gender:", langcombo[1]
    sys.exit(1)
    
try:
    formatname = formatmap[ttsFormat]
except:
    print ""
    print "Error: invalid format specified: The following formats are available:"
    print ""
    for item, value in formatmap.iteritems():
        print item
    sys.exit(1)
    
if ttsCache:
    cacheaccess = os.access(ttsCache, os.W_OK)
    if not cacheaccess:
        print "Cannot write to cache location, ignoring --cache setting..."
        ttsCache = None

m = hashlib.md5()
# Hash lang+gender+text
m.update(ttsLang + '-' + ttsGender  + '-' + ttsText)
# create filename base on MD5 hash
filename = str(m.hexdigest()) + ".wav"
if ttsCache:
    # If our file already exists, just return it so we don't have to do an API call...
    if os.path.isfile(ttsCache + '/' + filename):
        try:
            shutil.copy2(ttsCache + '/' + filename, destLoc)
            sys.exit(0)
        except (Exception) as e:
            print "Could not copy cached file:", e
            print "Exiting..."
            sys.exit(1)

# Wait to import this until after we check cache to keep things as speedy as possible...
from bingtts import Translator
translator = Translator(ttsApiKey)
try:
    data = translator.speak(ttsText, ttsLang, ttsGender, ttsFormat)
except (Exception) as e:
    print "Error retrieving speech file:", e
    sys.exit(1)

if ttsCache:
    try:
        with open(destLoc, 'w') as f:
            f.write(data)
    except (Exception) as e:
        print "Couldn't write to file", destLoc, ":", e
        sys.exit(1)
    try:
        with open(ttsCache + '/' + filename, 'w') as f:
            f.write(data)
    except (Exception) as e:
        cacheFileLoc = ttsCache + '/' + filename
        print "Couldn't write to file", cacheFileLoc, ":", e
        sys.exit(1)
else:
    try:
        with open(destLoc, 'w') as f:
            f.write(data)
    except (Exception) as e:
        print "Couldn't write to file", destLoc, ":", e
        sys.exit(1)
        
sys.exit(0)
