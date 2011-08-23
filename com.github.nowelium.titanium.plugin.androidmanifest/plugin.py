#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Titanium Compiler plugin
# com.github.nowelium.titanium.plugin.androidmanifest
#

import os
import sys

orientation = 'portrait'

def insPortrait(file):
  for text in file:
    if 0 <= text.strip().find('android:configChanges="keyboardHidden|orientation"'):
      yield text.replace('android:configChanges="keyboardHidden|orientation"', 'android:configChanges="keyboardHidden|orientation" android:screenOrientation="' + orientation + '"')
    else:
      yield text

def hook_gen_android_manifest(config, builder, org_generate_android_manifest):
  def rewrite_android_manifest(*args):
    org_generate_android_manifest(*args)

    path = os.path.abspath(os.path.join(config['build_dir'], 'AndroidManifest.xml'))
    file = open(path)
    newValue = [x for x in insPortrait(file)]
    file.close()

    newFile = open(path, "w")
    newFile.writelines(newValue)
    newFile.close()

    builder.generate_android_manifest = org_generate_android_manifest

  return rewrite_android_manifest

def compile(config):
  print '[INFO] com.github.nowelium.titanium.plugin.androidmanifest plugin loaded'

  builder = config['android_builder']
  org_android_manifest = builder.generate_android_manifest
  builder.generate_android_manifest = hook_gen_android_manifest(config, builder, org_android_manifest)

