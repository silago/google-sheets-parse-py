#!/bin/bash
set +e
#set -x
OUT="OUT" ROOT=$(pwd) UTILS="Utils" DATA="Data"
STATIC=$ROOT/$DATA/$RESOURCE_DIR
mkdir -p $OUT

mkdir -p previous_build/$RESOURCES_DATA_DIRECTORY
mkdir -p current_build/$RESOURCES_DATA_DIRECTORY
mkdir -p previous_build/$PARSED_DATA_DIRECTORY
mkdir -p current_build/$PARSED_DATA_DIRECTORY

rm current_build/* -rf
cp   "$STATIC" "current_build/$RESOURCES_DATA_DIRECTORY" -r

python Utils/ConfigParser.py "$GOOGLE_SHEET" "current_build/$PARSED_DATA_DIRECTORY"
python ConfigUploader.py "$GOOGLE_SHEET" "current_build/$PARSED_DATA_DIRECTORY" $DB_CONNECTION_STRING

#exclude data
for f in $CLIENT_EXCLUDE
do
	rm current_build/$PARSED_DATA_DIRECTORY/$f.json
done


NEW_ASSETS_FILES=$(rsync -rcn --out-format="%n" current_build/$RESOURCES_DATA_DIRECTORY/ previous_build/$RESOURCES_DATA_DIRECTORY/ | grep ".*[^\/]\$")
rsync -rcn --out-format="%n" current_build/$PARSED_DATA_DIRECTORY/ previous_build/$PARSED_DATA_DIRECTORY/
NEW_DATA_FILES=$(rsync -rcn --out-format="%n" current_build/$PARSED_DATA_DIRECTORY/ previous_build/$PARSED_DATA_DIRECTORY/ | grep ".*[^\/]\$")

mkdir -p "$ROOT/$OUT/DATA/$BUILD_NUMBER/"
mkdir -p "$ROOT/$OUT/DATA/$BUILD_NUMBER/$PARSED_DATA_DIRECTORY/"
mkdir -p "$ROOT/$OUT/DATA/$BUILD_NUMBER/$RESOURCES_DATA_DIRECTORY/"


cd "$ROOT/current_build"


cd $PARSED_DATA_DIRECTORY
cp --parents -t "$ROOT/$OUT/DATA/$BUILD_NUMBER/$PARSED_DATA_DIRECTORY" $NEW_DATA_FILES
cd ../


mkdir -p "$ROOT/$OUT/VERSIONS/$PARSED_DATA_DIRECTORY"
mkdir -p "$ROOT/$OUT/VERSIONS/$RESOURCES_DATA_DIRECTORY"


cd "$ROOT/$OUT/DATA/"

echo "" > assets.txt

#find and add files
for version in $(ls -d */)
do
	cd $version/$PARSED_DATA_DIRECTORY;
    for f in $(find . -type f -printf  "%P\n")
    do
      echo CONFIG";"$PARSED_DATA_DIRECTORY/$f";"$(basename $version)";"$(md5sum $f |cut -f 1 -d " ")";"$(stat -c %Y $f)";"$(stat -c%s $f) >> ../../assets.txt
    done
    cd ../../
done

mkdir "$ROOT/$OUT/VERSIONS/$BUILD_NUMBER/"
echo "$ROOT/$OUT/VERSIONS/"
ls "$ROOT/$OUT/VERSIONS/$BUILD_NUMBER/"


#sort by path order by version non empty strings
cat assets.txt | sort -t ";" -k 3,3 -g -r | sort -t ";" -k 2,2 -u | grep -v -e '^$' > "$ROOT/$OUT/VERSIONS/$BUILD_NUMBER/Assets.csv"


echo $BUILD_NUMBER > "$ROOT/$OUT/VERSIONS/current"
cd "$ROOT"
cp current_build/* previous_build -r

rsync -avx --no-perms --no-owner --no-group  -O OUT/ $RSYNC_DESTINATION