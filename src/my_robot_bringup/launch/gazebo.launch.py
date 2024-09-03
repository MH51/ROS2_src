from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
import os

def generate_launch_description():
    # Get the path to the URDF file and the RViz configuration file
    pkg_share = FindPackageShare(package='rob_description').find('rob_description')
    urdf_file = os.path.join(pkg_share, 'urdf', 'robo.urdf.xacro')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'urdf_config.rviz')

    # Declare the launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Process the URDF file
    robot_description = Command(['xacro ', urdf_file])

    # Include the Gazebo launch file
    gazebo_launch_file = os.path.join(FindPackageShare('gazebo_ros').find('gazebo_ros'), 'launch', 'gazebo.launch.py')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Define the robot state publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}]
    )

    # Define the joint state publisher GUI node
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Define the RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Define the spawn entity node
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-topic', 'robot_description'],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        gazebo,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
        spawn_entity_node
    ])

  """https://www.youtube.com/watch?v=b8VwSsbZYn0"""  