#!/bin/bash

for file in `find ./ -name "*.md"`
do
    echo $file
    sed -i 's/cdn.jsdelivr.net\/gh\/mo-xiaoxiu\/imagefrommyblog@main\/data/myblog-1308923350.cos.ap-guangzhou.myqcloud.com\/img/g' $file
done
