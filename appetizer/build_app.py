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

from skilletlib import SkilletLoader

this_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(this_path, '.pan-cnc.yaml')

if os.path.exists(config_path):
    print('Appetizer Configuration file already found!')
    exit(0)

print('Building Appetizer Configuration ...')

repo = os.environ.get('REPO', 'https://github.com/PaloAltoNetworks/iron-skillet.git')
repo_branch = os.environ.get('BRANCH', 'panos_v9.0')
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
    all_skillets = sl.load_from_git(repo, repo_name, repo_branch, local_dir=local_dir)

# sort all skillets by their collection labels
collections = dict()
for skillet in all_skillets:
    for collection in skillet.collections:
        if collection not in collections:
            collections[collection] = list()
        else:
            collections[collection].append(skillet)

context = dict()
context['collections'] = collections
context['repo'] = repo
context['repo_branch'] = repo_branch
context['app_name'] = repo_name

skillet_path = os.path.join(this_path, 'skillets/build_config')
config_builder_skillet = sl.load_skillet_from_path(skillet_path)
t = sl.execute_template_skillet(config_builder_skillet, context)

with open(config_path, 'w') as config_file:
    config_file.write(t)

print('Appetizer Configuration File built...')
