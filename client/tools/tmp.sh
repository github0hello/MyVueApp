if [ $1 = "upload"]; then
    cd /hy-tmp
    zip -0 -r tmp.zip /hy-tmp
    oss cp /hy-tmp/tmp.zip oss://hy-tmp/tmp.zip
elif [$1 = "download"]; then
    cd /hy-tmp
    oss  /hy-tmp cp oss://hy-tmp/tmp.zip 
    unzip tmp.zip -d /hy-tmp
fi
