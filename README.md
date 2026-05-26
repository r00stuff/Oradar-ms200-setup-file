# ORADAR MS200 LiDAR — ROS2 Jazzy Setup

Driver for the Orbbec / Oradar MS200-TOF 2D lidar on **ROS2 Jazzy Jalisco** and **Ubuntu 24.04 (Noble)**.

This is a fork of [lehoangan2906/Oradar-ms200-setup-file](https://github.com/lehoangan2906/Oradar-ms200-setup-file) with the following fixes applied for standard ROS2 Jazzy:
- `CMakeLists.txt` replaced with a clean `ament_cmake` build (original had a broken `CATKIN`/`COLCON` detection that always defaulted to ROS1)
- `ms200_scan.launch.py` updated for Jazzy API, stable `/dev/oradar` udev symlink, and standard `/scan` topic
- `package.xml` set to the ROS2 manifest

## Hardware

| Detail | Value |
|---|---|
| Range | 0.05 – 12.0 m |
| Scan rate | 10 Hz |
| Angular resolution | 0.4° |
| Interface | UART via USB-C adapter board |
| Linux device | `ttyACM*` (VID `1a86` / PID `55d4`) |

## Prerequisites

- ROS2 Jazzy installed and sourced
- colcon build tools: `sudo apt install python3-colcon-common-extensions`

## Step 1 — Udev Rule

Creates a stable `/dev/oradar` symlink so the device name never changes between reboots.

Plug in the lidar, then confirm it appears as `ttyACM*`:

```bash
lsusb   # look for: QinHeng Electronics USB Single Serial (1a86:55d4)
ls /dev/ttyACM*
```

Install the udev rule:

```bash
sudo tee /etc/udev/rules.d/oradar.rules << 'EOF'
KERNEL=="ttyACM*",ATTRS{idVendor}=="1a86",ATTRS{idProduct}=="55d4", MODE:="0777", SYMLINK+="oradar"
EOF
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Unplug and replug the lidar, then verify:

```bash
ls -la /dev/oradar   # should show: oradar -> ttyACM0
```

## Step 2 — Build

```bash
# Clone this repo
git clone https://github.com/r00stuff/Oradar-ms200-setup-file.git ~/oradar_lidar

# Symlink into your colcon workspace
ln -s ~/oradar_lidar ~/ros2_ws/src/oradar_lidar

# Build
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select oradar_lidar
source install/setup.bash
```

## Step 3 — Run

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch oradar_lidar ms200_scan.launch.py
```

Expected output:

```
[ms200] get lidar type: ms200
[ms200] get serial port: /dev/oradar, baudrate: 230400
[ms200] lidar device connect succuss.
[ms200] get lidar scan data
[ms200] ROS topic: scan
```

## Step 4 — Verify

In a second terminal:

```bash
source ~/ros2_ws/install/setup.bash
ros2 topic hz /scan        # should show ~10 Hz
ros2 topic echo /scan --once   # should show range data
```

## Launch File Parameters

The launch file (`launch/ms200_scan.launch.py`) starts two nodes:

| Node | Description |
|---|---|
| `ms200` | Lidar driver — publishes `sensor_msgs/LaserScan` on `/scan` |
| `base_link_to_laser_frame` | Static TF from `base_link` to `laser_frame` |

**Adjust the `--z` value** in the launch file to match the actual lidar mounting height on your robot in metres (default: `0.10`).

Available parameters for the lidar node:

| Parameter | Default | Description |
|---|---|---|
| `port_name` | `/dev/oradar` | Serial port |
| `baudrate` | `230400` | Baud rate |
| `frame_id` | `laser_frame` | TF frame for scan messages |
| `scan_topic` | `scan` | Published topic name |
| `angle_min` | `0.0` | Minimum scan angle (degrees) |
| `angle_max` | `360.0` | Maximum scan angle (degrees) |
| `range_min` | `0.05` | Minimum range (metres) |
| `range_max` | `20.0` | Maximum range (metres) |
| `clockwise` | `false` | Scan direction |
| `motor_speed` | `10` | Motor speed (Hz) |
