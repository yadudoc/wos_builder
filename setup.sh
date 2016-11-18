#!/bin/bash

sed -i 's/\<records\ xmlns\=\"http:\/\/scientific.thomsonreuters.com\/schema\/wok5.4\/public\/FullRecord\"/records/; 10q' $1
