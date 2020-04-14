#!/usr/bin/env bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
set -e

# This script packages app and it's dependencies into a zip file
# that will be used by terraform to create a lambda function in aws

# variables
APP="covid19-symptoms"
ARCHIVENAME="lambda_package"
BUILD_DIR="/tmp/lambdabuild/covid19"
BUILD_DIR_APP="/tmp/lambdabuild/covid19/${APP}"


printf "%b⚓Building ${APP}"

printf "%b⚓cleaning buildir...%b\n" "${BUILD_DIR}"
rm -rf ${BUILD_DIR} && mkdir -p ${BUILD_DIR}
rsync -aP ../${APP} ${BUILD_DIR}
ls $BUILD_DIR_APP
# create a temporary virtualenv
python3 -m venv ${BUILDIR}/virtualenv

# activate the virtualenv
source ${BUILDIR}/virtualenv/bin/activate


mkdir -p ${BUILD_DIR}/lambda_package

echo Install app from $BUILD_DIR_APP ...
ls $BUILD_DIR_APP
pip install -q ${BUILD_DIR_APP}/ -U -r ${BUILD_DIR_APP}/requirements.txt -t ${BUILD_DIR}/lambda_package

#rsync -aP  ${BUILD_DIR_APP}/ ${BUILDIR}/lambda_package/
rsync -aP  ../$APP/app.py ${BUILD_DIR}/lambda_package/

    #CREATE ARCHIVE
( cd ${BUILD_DIR}/lambda_package && zip -q -r9 ${BUILD_DIR}/${ARCHIVENAME}.zip . )

cp ${BUILD_DIR}/${ARCHIVENAME}.zip ./${ARCHIVENAME}.zip
