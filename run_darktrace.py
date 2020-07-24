import os
import argparse
import platform
import sys

parser = argparse.ArgumentParser()

parser.add_argument('--f', help='run the tool on a folder of apps')
parser.add_argument('--i', help='run the tool on a single apk')

args = parser.parse_args()

# print(platform.system())

"""
---- various checks ----
"""

if args.f and args.i:
    print ('Specify either a folder of apps, or a single apk')
    sys.exit()

if args.f:
    if not os.path.isdir(args.f):
        print('Directory not found')
        sys.exit()

"""
---- run the tool ----
"""

# if a folder is specified
if args.f:
    if platform.system() == 'Windows':
        for file in os.listdir(args.f):
            os.system('axmldec.exe -i' + args.f + file + ' -o output/AndroidManifest.xml')
            os.system('python darktrace.py')

    elif platform.system() == 'Linux':
        for file in os.listdir(args.f):
            os.system('./axmldec -i '+ args.f + file + ' -o output/AndroidManifest.xml')
            os.system('python darktrace.py')

    # Insert mac os here

# if a single file is specified
if args.i:
    if platform.system() == 'Windows':
        os.system('axmldec.exe -i' + args.i + ' -o output/AndroidManifest.xml')
        os.system('python darktrace.py')

    if platform.system() == 'Linux':
        os.system('./axmldec -i' + args.i + ' -o output/AndroidManifest.xml')
        os.system('python darktrace.py')

    # Insert mac os here