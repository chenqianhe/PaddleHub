# Copyright (c) 2019  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from paddle_hub.tools import utils
from paddle_hub.tools.downloader import default_downloader
import paddle_hub as hub
import os
import shutil


class LocalModuleManager:
    def __init__(self, module_home=None):
        self.local_modules_dir = module_home if module_home else hub.MODULE_HOME
        self.modules_dict = {}
        if not os.path.exists(self.local_modules_dir):
            utils.mkdir(self.local_modules_dir)
        elif os.path.isfile(self.local_modules_dir):
            #TODO(wuzewu): give wanring
            pass

    def check_module_valid(self, module_path):
        #TODO(wuzewu): code
        return True

    def all_modules(self, update=False):
        if not update and self.modules_dict:
            return self.modules_dict
        self.modules_dict = {}
        for sub_dir_name in os.listdir(self.local_modules_dir):
            sub_dir_path = os.path.join(self.local_modules_dir, sub_dir_name)
            if os.path.isdir(sub_dir_path) and self.check_module_valid(
                    sub_dir_path):
                #TODO(wuzewu): get module name
                module_name = sub_dir_name
                self.modules_dict[module_name] = sub_dir_path

        return self.modules_dict

    def search_module(self, module_name, update=False):
        self.all_modules(update=update)
        return self.modules_dict.get(module_name, None)

    def install_module(self, module_name, module_version=None, upgrade=False):
        self.all_modules(update=True)
        if module_name in self.modules_dict:
            module_dir = self.modules_dict[module_name]
            print("module %s already install in %s" % (module_name, module_dir))
            return
        url = hub.default_hub_server.get_module_url(
            module_name, version=module_version)
        #TODO(wuzewu): add compatibility check
        if not url:
            tips = "can't found module %s" % module_name
            if module_version:
                tips += " with version %s" % module_version
            print(tips)
            return

        default_downloader.download_file_and_uncompress(
            url=url, save_path=hub.MODULE_HOME, save_name=module_name)

    def uninstall_module(self, module_name):
        self.all_modules(update=True)
        if not module_name in self.modules_dict:
            print("%s is not installed" % module_name)
            return

        module_dir = self.modules_dict[module_name]
        shutil.rmtree(module_dir)
        print("Successfully uninstalled %s" % module_name)


default_module_manager = LocalModuleManager()