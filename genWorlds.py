from lxml import etree
import random
import math
import copy
import argparse
from collections import namedtuple

class Tree:
  def __init__(self, id_in, pose_in, scale_in, mesh_num_in):
    self.id = 'tree' + str(id_in)
    self.pose = pose_in
    self.scale = scale_in
    self.mesh_num = mesh_num_in

class GenXML:
  def __init__(self):
    self.root = etree.Element('world',name='default')

    #add ground
    include_el = etree.Element('include')
    ground_el = etree.Element('uri')
    ground_el.text = 'model://ground_plane'
    include_el.append(ground_el)
    self.root.append(include_el)

    #add sun
    include_el = etree.Element('include')
    sun_el = etree.Element('uri')
    sun_el.text = 'model://sun'
    include_el.append(sun_el)
    self.root.append(include_el)

    #disable shadows
    scene_el= etree.Element('scene')
    shadows_el = etree.Element('shadows')
    shadows_el.text = '0'
    scene_el.append(shadows_el)
    self.root.append(scene_el)

    #create the forest base model
    model_el = etree.Element('model', name = 'forest')
    static_el = etree.Element('static')
    static_el.text = 'true'
    model_el.append(static_el)
    self.root.append(model_el)

    #add octomap plugin
    oct_plug_el = etree.Element('plugin', name = 'gazebo_octomap',
                                filename = 'librotors_gazebo_octomap_plugin.so')
    self.root.append(oct_plug_el)

    #add rotors interface plugin
    rotors_plug_el = etree.Element('plugin', name = 'ros_interface_plugin',
                                   filename =
                                   'librotors_gazebo_ros_interface_plugin.so')
    self.root.append(rotors_plug_el)

  def add_model(self, name_in, pose_in, scale_in, mesh_num_in, models_type):

    link_el = etree.Element('link', name = name_in)

    pose_el = etree.Element('pose')
    pose_el.text = ''.join(str(e) + ' ' for e in pose_in)
    link_el.append(pose_el)

    visual_el = etree.Element('visual', name = 'visual')
    geometry_el = etree.Element('geometry')
    mesh_el = etree.Element('mesh')
    uri_el = etree.Element('uri')
    uri_el.text = 'file://' + models_type + '/Tree' + str(mesh_num_in) + '.dae'
    mesh_el.append(uri_el)
    scale_el = etree.Element('scale')
    scale_el.text = str(scale_in) + ' ' + str(scale_in) + ' ' + str(scale_in)
    mesh_el.append(scale_el)
    geometry_el.append(mesh_el)
    visual_el.append(geometry_el)
    link_el.append(visual_el)

    collision_el = etree.Element('collision', name = 'collision')
    collision_el.append(copy.deepcopy(geometry_el))
    contacts_el = etree.Element('max_contacts')
    contacts_el.text = '0'
    collision_el.append(contacts_el)
    link_el.append(collision_el)

    self.root.find('model').append(link_el)

  def output_xml(self):
    sdf = etree.Element('sdf',version='1.4')
    sdf.append(self.root)

    return '<?xml version="1.0"?>\n' + etree.tostring(sdf, pretty_print=True)

class World:
  TOTAL_NUM_MESHES = 6

  def __init__(self, world_length, use_high_res):
    self.world_length = world_length
    self.trees = []

    if(use_high_res):
      self.models_type = 'models_high_res'
    else:
      self.models_type = 'models_low_res'

  def _gen_random_tree(self):
    id_num = len(self.trees)
    x = random.uniform(-self.world_length/2, self.world_length/2)
    y = random.uniform(-self.world_length/2, self.world_length/2)
    angle = random.uniform(0, 2*math.pi)
    scale = random.uniform(0.3, 1)
    mesh_num = random.randint(1, self.TOTAL_NUM_MESHES)

    return Tree(id_num, [x,y,0,0,0,angle], scale, mesh_num)

  def add_trees(self, num_trees):
    for i in range(num_trees):
      self.trees.append(self._gen_random_tree())

  def save_world(self, filename):

    xml = GenXML()
    for tree in self.trees:
      xml.add_model(tree.id, 
                    tree.pose, 
                    tree.scale, 
                    tree.mesh_num, 
                    self.models_type)

    text_file = open(filename, "w")
    text_file.write(xml.output_xml())
    text_file.close()

def gen_worlds(save_path, num_worlds, world_length, num_trees, use_high_res):
  for i in range(num_worlds):
    world = World(world_length, use_high_res)
    world.add_trees(num_trees)
    world.save_world(save_path + '/forest' + str(i) + '.world')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a random gazebo forest.')
    parser.add_argument('--num_worlds', type=int, help='Number of worlds to generate')
    parser.add_argument('--world_length', type=int, help='Length and width of world in m')
    parser.add_argument('--tree_density', type=float, help='Number of trees per m^2')
    parser.add_argument('--high_res', type=int, help='Use high res tree models')
    args = parser.parse_args()

    gen_worlds('./worlds', args.num_worlds, args.world_length, 
               int(args.world_length*args.world_length*args.tree_density),
               bool(args.high_res))