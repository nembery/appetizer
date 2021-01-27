#!/usr/bin/env python3
# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Authors: Nathan Embery

import os
import sys
import shutil

from skilletlib import SkilletLoader

this_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(this_path, '.pan-cnc.yaml')

if os.path.exists(config_path):
    print('Appetizer Configuration file already found!')
    exit(0)

print('Building Appetizer Configuration ...')

repo = os.environ.get('REPO', 'https://github.com/PaloAltoNetworks/HomeSkillet.git')
repo_branch = os.environ.get('BRANCH', 'master')
repo_name = os.environ.get('NAME', 'appetizer')

local_dir = os.path.expanduser('~/.pan_cnc/appetizer')

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

sl = SkilletLoader()

repo_full_dir = os.path.join(local_dir, repo_name)
if os.path.exists(repo_full_dir):
    print('Using local dir')
    all_skillets = sl.load_all_skillets_from_dir(repo_full_dir)
else:
    print('Pulling anew')
    # do not check for self signed certs here
    os.environ['GIT_SSL_NO_VERIFY'] = "1"
    all_skillets = sl.load_from_git(repo, repo_name, repo_branch, local_dir=local_dir)

src_dir = os.path.join(repo_full_dir, 'src')

if os.path.exists(src_dir):
    print('Found a CNC APP to build')
    for d in os.listdir(src_dir):
        full_path = os.path.join(src_dir, d)
        if os.path.isdir(full_path):
            shutil.copytree(full_path, f'/app/src/{d}')

    # No need to build out a pan-cnc.yaml file if this is a CNC app already...
    sys.exit(0)

# Build out a new pan-cnc config file from here
# sort all skillets by their collection labels
collections = dict()
for skillet in all_skillets:
    for collection in skillet.collections:
        if collection in ('lib', 'Kitchen Sink'):
            continue

        if collection not in collections:
            collections[collection] = [skillet]
        else:
            collections[collection].append(skillet)

# Sort the skillet within the collection by label and record the order index, then check of order label
for collection in collections:
    collections[collection].sort(key=lambda x: x.label)
    order_index = 1000
    for skillet in collections[collection]:
        found_order_label = False
        for label in skillet.labels:
            if label == 'order':
                found_order_label = True
                setattr(skillet, 'order', skillet.labels['order'])
                break

        if not found_order_label:
            setattr(skillet, 'order', order_index)

        order_index += 1

for collection in collections:
    collections[collection].sort(key=lambda x: x.order)

context = dict()
context['collections'] = collections
context['repo'] = repo
context['repo_branch'] = repo_branch
context['app_name'] = repo_name

skillet_path = os.path.join(this_path, 'skillets/build_config')
config_builder_skillet = sl.load_skillet_from_path(skillet_path)
t = config_builder_skillet.execute(context)

if 'template' not in t:
    print('Could not parse skillet data!')
    sys.exit(1)

with open(config_path, 'w') as config_file:
    config_file.write(t['template'])

print('Appetizer Configuration File built...')
