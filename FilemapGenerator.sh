#!/bin/bash
set +e
OUT="OUT"
ROOT=$(pwd)
UTILS="Utils"
DATA="Data"
STATIC=$ROOT/$DATA/$RESOURCE_DIR
echo $STATIC
mkdir -p $OUT

# если файлы лежат в гит репозитории, то получаем их таким образом
# touch head
# LAST_COMMIT=$(cat head)
# cd $DATA/$RESOURCE_DIR
# CURRENT_COMMIT=$(git rev-parse HEAD)
# NEW_FILES=$(git diff --color --name-only $LAST_COMMIT $CURRENT_COMMIT)
# echo $CURRENT_COMMIT > "$ROOT/head"


# для любых случаев
mkdir -p previous_build
mkdir -p current_build
rm current_build/* -rf
cp "$STATIC" current_build -r

NEW_FILES=$(rsync -rcn --out-format="%n" current_build/ previous_build/ | grep ".*[^\/]\$")

#DELETED_FILES=$(rsync -rcn --out-format="%n" previous_build/ current_build/ | grep ".*[^\/]\$")

mkdir -p "$ROOT/$OUT/DATA/$BUILD_NUMBER"
cd "$STATIC/"
cd ../
cp --parents -t "$ROOT/$OUT/DATA/$BUILD_NUMBER" $NEW_FILES

mkdir -p "$ROOT/$OUT/VERSIONS/"
#python "$ROOT/$UTILS/FilemapGenerator.py" "$ROOT/$OUT/DATA/" >  "$ROOT/$OUT/VERSIONS/$BUILD_NUMBER"

cd "$ROOT/$OUT/DATA/"
echo "" > out.txt
for version in $(ls -d */)
do
	cd $version;
    for f in $(find . -type f -printf  "%P\n")
    do
      echo $f";"$(basename $version)";"$(md5sum $f |cut -f 1 -d " ")";"$(stat -c %Y $f) >> ../out.txt
    done
    cd ../
done
cat out.txt | sort -t ";" -k2 -g | sort -t ";" -k1 -u > "$ROOT/$OUT/VERSIONS/$BUILD_NUMBER"
echo $BUILD_NUMBER > "$ROOT/$OUT/VERSIONS/current"
cd "$ROOT"
cp current_build/* previous_build -r




