# DWPriv 2.0 - Marco Mura - 2020
# changelog: the code sucks less

import os
import argparse
import platform
import sys

import xml.dom.minidom as md
import flask
from flask import render_template
import json

# ---- Global values ----
mode = ''

#load the cheatsheet.json file for generating the tooltips (contains info on each permission: permission name, description and if it directly involves PII)
#info taken from: https://developer.android.com/reference/android/Manifest.permission
with open ("cheatsheet.json") as f:
    cheatsheet = json.load(f)

# the whitelist or blacklist
bwlist = []

def generateSimpleReport():
    #load and parse the AndroidManifest.xml
    manifest = md.parse('output/AndroidManifest.xml')

    permissions = []
    features = []

    # number of used features and permissions
    permissionNumber = manifest.getElementsByTagName('uses-permission').length
    featureNumber = manifest.getElementsByTagName('uses-feature').length
    
    app = flask.Flask('my app')

    #get the package name (com.foo.bar)
    for x in manifest.getElementsByTagName('manifest'):
        packageName = x.getAttribute('package')

    for permission in manifest.getElementsByTagName('uses-permission'):
         #check against the whitelisted / blacklisted items in the specified file
        if permission.getAttribute('android:name') in bwlist:
            if permission.getAttribute("android:name") in cheatsheet:
                infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]
                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "true", "info": infoString})

            else:
                infoString = "Description: " + "no info found" + " - Directly collects PII?: no info found " + " - Protection Level: no info found" 
                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "true", "info": infoString})
        
        else: 
            if permission.getAttribute("android:name") in cheatsheet:
                infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]

                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "false", "info": infoString})

            else:
                infoString = "Description: " + "no info found" + " - Directly collects PII?: no info found " + " - Protection Level: no info found" 
                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "false", "info": infoString})

    for feature in manifest.getElementsByTagName('uses-feature'):
        features.append({"name": feature.getAttribute('android:name'), "whitelisted": "true"})

    with app.app_context():
        # generate template with no items highlighted
        report = render_template('report.html', title = packageName, permissionNumber = permissionNumber, featureNumber = featureNumber, permissions = permissions, features = features)

        reportFile = open ('reports/' + packageName + '.html', 'w')
        reportFile.write(report)
        reportFile.close()

    sys.exit()


def generateReport(packageName, permissionNumber, featureNumber, permissions, features):
    #load and parse the AndroidManifest.xml
    manifest = md.parse('output/AndroidManifest.xml')
    
    #flask stuff I guess
    app = flask.Flask('my app')    
    
    with app.app_context():
        if mode == 'w':
            # generate template whitelist
            report = render_template('wreport.html', title = packageName, permissionNumber = permissionNumber, featureNumber = featureNumber, permissions = permissions, features = features)

        if mode == 'b':
            # generate template blacklist
            report = render_template('breport.html', title = packageName, permissionNumber = permissionNumber, featureNumber = featureNumber, permissions = permissions, features = features)            

        # regardless of what type of template was generated, write the report to an html file in the reports folder
        reportFile = open ('reports/' + packageName + '.html', 'w')
        reportFile.write(report)
        reportFile.close()

def getUsesPermission(): 
    #load and parse the AndroidManifest.xml
    manifest = md.parse('output/AndroidManifest.xml')

    permissions = []

    for permission in manifest.getElementsByTagName('uses-permission'):
        #check against the whitelisted / blacklisted items in the specified file
        if permission.getAttribute('android:name') in bwlist:
            #save the permission to the permissions dictionary to generate the report later
            #if it was found in the whitelist / blacklist, save it as whitelisted: true
            #if it was found in the whitelist / blacklist, we can also provide a tooltip with more info on the permission

            #gathering additonal info on permission from cheatsheet.json
            #first check if the permission is in the cheatsheet
            if permission.getAttribute("android:name") in cheatsheet:
                #if so, create a string to pass to flask that will later be the tooltip for this specific permission

                # infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"] + " - Directly collects PII?: " + cheatsheet[permission.getAttribute("android:name")]["pii"] + " - Protection Level: " + cheatsheet[permission.getAttribute("android:name")]["protection-level"]
                infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]

                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "true", "info": infoString})

            else:
                #if permission not found in cheatsheet, don't pass tooltip info to flask, it should handle it and not generate the tooltip
                # if it wasn't found in the cheatsheet, don't generate tooltip
                infoString = "Description: " + "no info found" + " - Directly collects PII?: no info found " + " - Protection Level: no info found" 
                # infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]

                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "true", "info": infoString})
        else: 
            #if it wasn't found in the whitelist / blacklist, save it as whitelisted: false
            # but first, check if it is found in the cheatsheet

            if permission.getAttribute("android:name") in cheatsheet:
                #if so, create a string to pass to flask that will later be the tooltip for this specific permission
                # infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"] + " - Directly collects PII?: " + cheatsheet[permission.getAttribute("android:name")]["pii"] + " - Protection Level: " + cheatsheet[permission.getAttribute("android:name")]["protection-level"]
                infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]

                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "false", "info": infoString})

            else:
                #if permission not found in cheatsheet, don't pass tooltip info to flask, it should handle it and not generate the tooltip
                # if it wasn't found in the cheatsheet, don't generate tooltip
                infoString = "Description: " + "no info found" + " - Directly collects PII?: no info found " + " - Protection Level: no info found" 
                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "false", "info": infoString})

    return permissions

def main():
    #load and parse the AndroidManifest.xml
    manifest = md.parse('output/AndroidManifest.xml')

    features = []

    # number of used features and permissions
    permissionNumber = manifest.getElementsByTagName('uses-permission').length
    featureNumber = manifest.getElementsByTagName('uses-feature').length

    #get the package name (com.foo.bar)
    for x in manifest.getElementsByTagName('manifest'):
        packageName = x.getAttribute('package')

    
    permissions = getUsesPermission()
    

    """
    ----------USES FEATURE---------------
    """

    # Iterate over all the uses-feature nodes
    for permission in manifest.getElementsByTagName('uses-feature'):
        # TODO hardware features blacklist / whitelist
        """
        if permission.getAttribute('android:name') in whitelistedHardware:
            tempFeatureNumber += 1

            #save each used feature to the permissions dictionary to generate the report
            features.append({"name": permission.getAttribute('android:name'), "whitelisted": "true"})
            
        else: 
            features.append({"name": permission.getAttribute('android:name'), "whitelisted": "false"})
        """

        features.append({"name": permission.getAttribute('android:name'), "whitelisted": "true"})



    # finally, generate the report
    generateReport(packageName, permissionNumber, featureNumber, permissions, features)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--f', help='run the tool on a folder of apps')
    parser.add_argument('--i', help='run the tool on a single apk')
    parser.add_argument('--w', help='run the tool in whitelist mode. Note: a *.txt file must be provided with each item separated by a new line')
    parser.add_argument('--b', help='run the tool in blacklist mode. Note: a *.txt file must be provided with each item separated by a new line')
    parser.add_argument('--n', help='run the tool with no blacklist or whitelist, it will just extract the permissions', action='store_true')

    args = parser.parse_args()
    
    #---- various checks ----#

    if args.f and args.i:
        print ('Specify either a folder of apps, or a single apk')
        sys.exit()

    if args.w and args.b:
        print('The tool can be run in either blacklist mode, with --b, or whitelist mode with --w, but not both')
        sys.exit()

    if args.f:
        if not os.path.isdir(args.f):
            print('Directory not found')
            sys.exit()

    if args.w or args.b: 
        if not os.path.isfile(args.w or args.b):
            print('Whitelist or blacklist file not found')
            sys.exit()

    # a wise man once said: validate, don't sanitize

    listFile = ''

    if args.w: 
        mode = 'w'
        listFile = args.w

    if args.b:
        mode = 'b'
        listFile = args.b

    if args.w or args.b:
        bwlistTemp = open(listFile)

        for line in bwlistTemp.readlines():
            bwlist.append(line.rstrip())

    """
    ---- run the tool ----
    """

    # if a folder is specified
    if args.f:
        if platform.system() == 'Windows':
            for file in os.listdir(args.f):
                os.system('.\\axmldec.exe -i' + args.f + file + ' -o output/AndroidManifest.xml')
                if args.n:
                    generateSimpleReport()
                else: 
                    main()

        elif platform.system() == 'Linux':
            for file in os.listdir(args.f):
                os.system('./axmldec -i '+ args.f + file + ' -o output/AndroidManifest.xml')
                if args.n:
                    generateSimpleReport()
                
                else: 
                    main()

        # Insert mac os here

    # if a single file is specified
    if args.i:
        if platform.system() == 'Windows':
            os.system('.\\axmldec.exe -i' + args.i + ' -o output/AndroidManifest.xml')
            if args.n:
                generateSimpleReport()
            
            else:
                main()

        if platform.system() == 'Linux':
            os.system('./axmldec -i' + args.i + ' -o output/AndroidManifest.xml')
            if args.n:
                generateSimpleReport()
            
            else: 
                main()

        # Insert mac os here
