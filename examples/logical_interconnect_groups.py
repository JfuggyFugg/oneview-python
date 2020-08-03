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
# Below example works till Oneview API Version 1600.

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

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
logical_interconnect_groups = oneview_client.logical_interconnect_groups
interconnect_types = oneview_client.interconnect_types

# Define the scope name to add the logical interconnect group to it
scope_name = ""

interconnect_type_name = "Synergy 10Gb Interconnect Link Module"
# Get the interconnect type by name and using the uri in the values for the fields
# "permittedInterconnectTypeUri" and create a Logical Interconnect Group.
# Note: If this type does not exist, select another name
interconnect_type = oneview_client.interconnect_types.get_by_name(interconnect_type_name)
if interconnect_type:
    pprint(interconnect_type.data)
    interconnect_type_url = interconnect_type.data["uri"]

options = {
    "type": "logical-interconnect-groupV8",
    "category": "logical-interconnect-groups",
    "name": "LIG-VCEth3",
    "uplinkSets": [],
    "interconnectMapTemplate": {
        "interconnectMapEntryTemplates": [
            {
                "permittedInterconnectTypeUri": "/rest/interconnect-types/a13a95a4-6b59-45fd-bda5-a1206d42ac4d",
                "enclosureIndex": 1,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        },
                        {
                            "relativeValue": 6,
                            "type": "Bay"
                        }
                    ]
                }
            },
            {
                "permittedInterconnectTypeUri": "/rest/interconnect-types/e51e7997-b83a-4b8d-8933-2ba9e09af10a",
                "enclosureIndex": 1,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        },
                        {
                            "relativeValue": 3,
                            "type": "Bay"
                        }
                    ]
                }
            },
            {
                "permittedInterconnectTypeUri": "/rest/interconnect-types/e51e7997-b83a-4b8d-8933-2ba9e09af10a",
                "enclosureIndex": 2,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 2,
                            "type": "Enclosure"
                        },
                        {
                            "relativeValue": 6,
                            "type": "Bay"
                        }
                    ]
                }
            },
            {
                "permittedInterconnectTypeUri": "/rest/interconnect-types/a13a95a4-6b59-45fd-bda5-a1206d42ac4d",
                "enclosureIndex": 2,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 2,
                            "type": "Enclosure"
                        },
                        {
                            "relativeValue": 3,
                            "type": "Bay"
                        }
                    ]
                }
            }
        ]
    },
    "internalNetworkUris": [],
    "consistencyCheckingForInternalNetworks": "ExactMatch",
    "ethernetSettings": {
        "type": "EthernetInterconnectSettingsV7",
        "enableFastMacCacheFailover": true,
        "macRefreshInterval": 5,
        "enableNetworkLoopProtection": true,
        "enablePauseFloodProtection": false,
        "enableRichTLV": false,
        "enableTaggedLldp": false,
        "enableStormControl": false,
        "stormControlThreshold": 1,
        "stormControlPollingInterval": 10,
        "enableCutThrough": false,
        "enableDdns": false,
        "domainName": null,
        "consistencyChecking": "ExactMatch"
    },
    "igmpSettings": {
        "type": "IgmpSettings",
        "consistencyChecking": "ExactMatch",
        "enableIgmpSnooping": false,
        "igmpSnoopingVlanIds": null,
        "igmpIdleTimeoutInterval": 260,
        "enablePreventFlooding": false,
        "enableProxyReporting": true
    },
    "snmpConfiguration": null,
    "qosConfiguration": {
        "type": "qos-aggregated-configuration",
        "activeQosConfig": {
            "type": "QosConfiguration",
            "configType": "Passthrough",
            "qosTrafficClassifiers": [],
            "uplinkClassificationType": null,
            "downlinkClassificationType": null
        },
        "inactiveFCoEQosConfig": null,
        "inactiveNonFCoEQosConfig": null,
        "consistencyChecking": "ExactMatch"
    },
    "enclosureType": "SY12000",
    "enclosureIndexes": [
        1,
        2
    ],
    "interconnectBaySet": 3,
    "redundancyType": "HighlyAvailable",
    "downlinkSpeedMode": "SPEED_50GB",
    "initialScopeUris": []
}

# Get all, with defaults
print("Get all Logical Interconnect Groups")
ligs = logical_interconnect_groups.get_all()
pprint(ligs)

# Get by uri
print("Get a Logical Interconnect Group by uri")
lig_byuri = logical_interconnect_groups.get_by_uri(ligs[0]["uri"])
pprint(lig_byuri.data)

# Get the first 10 records, sorting by name descending, filtering by name
print("Get the first Logical Interconnect Groups, sorting by name descending, filtering by name")
ligs = logical_interconnect_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='OneView Test Logical Interconnect Group'\"")
pprint(ligs)

# Get Logical Interconnect Group by property
lig = logical_interconnect_groups.get_by('name', 'LIG')[0]
print("Found lig by name: '%s'.\n  uri = '%s'" % (lig['name'], lig['uri']))

# Get Logical Interconnect Group by scope_uris
if oneview_client.api_version >= 600:
    lig_by_scope_uris = logical_interconnect_groups.get_all(scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
    if len(lig_by_scope_uris) > 0:
        print("Found %d Logical Interconnect Groups" % (len(lig_by_scope_uris)))
        i = 0
        while i < len(lig_by_scope_uris):
            print("Found Logical Interconnect Group by scope_uris: '%s'.\n  uri = '%s'" % (lig_by_scope_uris[i]['name'], lig_by_scope_uris[i]['uri']))
            i += 1
        pprint(lig_by_scope_uris)
    else:
        print("No Logical Interconnect Group found.")

# Get logical interconnect group by name
lig = logical_interconnect_groups.get_by_name(options["name"])
if not lig:
    # Create a logical interconnect group
    print("Create a logical interconnect group")
    lig = logical_interconnect_groups.create(options)
    pprint(lig.data)

# Update a logical interconnect group
print("Update a logical interconnect group")
lig_to_update = lig.data.copy()
lig_to_update["name"] = "Renamed Logical Interconnect Group"
lig.update(lig_to_update)
pprint(lig.data)

# Performs a patch operation
if oneview_client.api_version <= 500:
    scope = oneview_client.scopes.get_by_name(scope_name)
    if scope:
        print("\nPatches the logical interconnect group adding one scope to it")
        updated_lig = lig.patch('replace',
                                '/scopeUris',
                                [scope.data['uri']])
        pprint(updated_lig.data)

# Get default settings
print("Get the default interconnect settings for a logical interconnect group")
lig_default_settings = lig.get_default_settings()
pprint(lig_default_settings)

# Get settings
print("Gets the interconnect settings for a logical interconnect group")
lig_settings = lig.get_settings()
pprint(lig_settings)

# Delete a logical interconnect group
print("Delete the created logical interconnect group")
lig.delete()
print("Successfully deleted logical interconnect group")
