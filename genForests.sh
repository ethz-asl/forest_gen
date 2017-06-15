#!/bin/bash

#check args
if [ "$#" -ne 4 ]
then
    echo "Generates random forests to evaluate path planning"
    echo "Usage: $0 <number of worlds to gen> <world side length> <tree density> <octomap res>"
    exit 1
fi

echo "generating worlds"
python genWorlds.py --num_worlds $1 --world_length $2 --tree_density $3 --high_res 0

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

roscore &

for FILE in $DIR/worlds/*.world; do
    NAME=$(basename "$FILE" .world)
    echo " "
    echo "Generating octomap of $NAME"
    echo " "
    rosrun gazebo_ros gzserver $FILE &

    rosservice call /world/get_octomap "{bounding_box_origin: {x: 0, y: 0, z: 2.5}, bounding_box_lengths: {x: $2, y: $2, z: 5}, leaf_size: $4, filename: '$DIR/octomaps/$NAME.bt'}" --wait
    killall gzserver
done

echo "done"
