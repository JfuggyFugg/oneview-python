# -*- coding: utf-8 -*-
###
# (C) Copyright [2019] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run this example you must define a path to a valid file
firmware_path = "<path_to_firmware_bundle>"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

# Upload a firmware bundle
print("\nUpload a firmware bundle")
firmware_bundle_information = oneview_client.firmware_bundles.upload(file_path=firmware_path)
print("\n Upload successful! Firmware information returned: \n")
pprint(firmware_bundle_information)
