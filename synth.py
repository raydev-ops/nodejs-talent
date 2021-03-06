# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG)

# Run the gapic generator
gapic = gcp.GAPICGenerator()
versions = ["v4beta1"]
for version in versions:
    library = gapic.node_library(
        "talent", version, config_path="/google/cloud/talent/"
        f"artman_talent_{version}.yaml",
        artman_output_name=f"talent-v4beta1")
    s.copy(library, excludes=['README.md', 'package.json', '.eslintrc.yml'])

# Copy common templates
common_templates = gcp.CommonTemplates()
templates = common_templates.node_library()
s.copy(templates, excludes=['.eslintrc.yml'])

# cleanup some hiccups in jsdoc comments.
s.replace("src/index.js",
r"""\/\*\*
 \* @namespace google
 \*/""",
r"""
/**
 * @namespace google
 */
/**
 * @namespace google.protobuf
 */
 /**
 * @namespace google.longrunning
 */
 /**
 * @namespace google.rpc
 */
/**
 * @namespace google.type
 */
""")

# [START fix-dead-link]
s.replace('**/doc/google/protobuf/doc_timestamp.js',
        'https:\/\/cloud\.google\.com[\s\*]*http:\/\/(.*)[\s\*]*\)',
        r"https://\1)")
# [END fix-dead-link]

s.replace('src/v4beta1/doc/google/cloud/talent/v4beta1/doc_company.js',
        '"https:\/\/www\.google\.com"',
        '`https://www.google.com`')

# Node.js specific cleanup
subprocess.run(["npm", "install"])
subprocess.run(["npm", "run", "fix"])
