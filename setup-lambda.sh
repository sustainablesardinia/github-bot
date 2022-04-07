# setup-lambda.sh
#
# Apronta sa AWS lambda po cun sa versioni noa de su còdixi.
#
# Copyright 2022 Sustainable Sardinia
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

set -e

FUNCTION="sustainablesardinia-github-bot"
FUNCTION_NAME="get_repo_data_past_month.py"

CURRENT_DIR=$(pwd)
cd /tmp

# Create a working directory
WORKING_DIR="workingdir"
if [ -d "$WORKING_DIR" ]; then
    rm -rf $WORKING_DIR
fi
mkdir $WORKING_DIR
cd $WORKING_DIR

# Create a new Python environment
ENVIRONMENT_NAME="myenv"
PYTHON_VER="python3.8"
PYTHON_EXEC=$(which $PYTHON_VER)
if [ -z "$PYTHON_EXEC" ]; then
    echo "ERROR: This requires Python 3.8"
    exit -1
fi
pip3 install virtualenv
virtualenv --python=$PYTHON_EXEC $ENVIRONMENT_NAME
source $ENVIRONMENT_NAME/bin/activate

pip install pygithub cffi requests
deactivate

# Create zip with existing code
UPDATED_ZIP="updated_lambda.zip"
cd $ENVIRONMENT_NAME/lib/$PYTHON_VER/site-packages
cp -r $CURRENT_DIR/* ./
zip -r ../../../../$UPDATED_ZIP .

cd -
aws lambda update-function-code \
    --function-name $FUNCTION \
    --zip-file fileb://$UPDATED_ZIP
