# forest_gen
Generates randomized Poisson forests to use for UAV collision avoidance evaluations.

Input: map size and density
Output: Gazebo world file and (optionally) Octomap

**Authors**: Zachary Taylor, zachary.taylor@mavt.ethz.ch 

**Maintainers**: Zachary Taylor, zachary.taylor@mavt.ethz.ch and Helen Oleynkova, helen.oleynikova@mavt.ethz.ch 

**Affiliation**: Autonomous Systems Lab, ETH Zurich 

## Bibliography
If using these datasets, please cite:

Helen Oleynikova, Michael Burri, Zachary Taylor, Juan Nieto, Roland Siegwart, and Enric Galceran, “**Continuous-Time Trajectory Optimization for Online UAV Replanning**”. In *IEEE Int. Conf. on Intelligent Robots and Systems* (IROS), 2016.

[[PDF here]](http://helenol.github.io/publications/iros_2016_replanning.pdf)

```
@inproceedings{oleynikova2016continuous-time,
  author={Oleynikova, Helen and Burri, Michael and Taylor, Zachary  and  Nieto, Juan and Siegwart, Roland and Galceran, Enric},
  booktitle={IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  title={Continuous-Time Trajectory Optimization for Online UAV Replanning},
  year={2016}
}
```

## Installation Requirements
* ROS indigo and up
* [rotors_simulator](https://github.com/ethz-asl/rotors_simulator) for octomap generation from Gazebo worlds.
* Recommended: [volumetric_mapping](git@github.com:ethz-asl/volumetric_mapping.git) for using Octomap as a ROS library within other programs.

## Package Contents
* 
*
*
*


## Generating New Environments
