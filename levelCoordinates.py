import math
import numpy as np
import logging
from typing import List
from enum import Enum

class PointLocation(Enum):
    BOTTOM_LEFT = 1
    BOTTOM_RIGHT = 2
    TOP_RIGHT = 3

class Leveler():
    """
        Program to level the bed of the liquid handler in respect to the gantry coordinates
        
        Uses 3 fiducial points probed counterclockwise in an L shape
        
        Each point is comprised of x, y, z coordinates

        @param: logging - logging object in order to log the opperations of the module
    """
    def __init__(self, logger: logging):
        self._yaw = self._pitch = self._roll = 0
        self._p0 = self._p1 = self._p2 = np.array([0.0, 0.0, 0.0])
        self.WIDTH = 4
        self._log = logger
        self._log.info('Created calibration module')

    @property
    def roll(self):
        return self._roll

    @roll.setter
    def roll(self, roll: float):
        self._roll = roll

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, pitch: float):
        self._pitch = pitch   
    
    @property
    def yaw(self):
        return self._yaw

    @yaw.setter
    def yaw(self, yaw: float):
        self._yaw = yaw

    def probe_point(self, point: List[float], location: PointLocation):
        """Probe a point for calibration

        @param: point - x, y, z coordinates of the point
        @param: 
        """
        if location == PointLocation.BOTTOM_LEFT:
            self._p0 = point
        elif location == PointLocation.BOTTOM_RIGHT:
            self._p1 = point
        elif location == PointLocation.TOP_RIGHT:
            self._p2 = point
        else:
            self._log.error("Invalid probe number or value")
            raise ValueError

    def calculate_rotations(self):
        # calculate angles
        self._yaw = self._calculate_yaw(self._p1, self._p2)
        self._pitch = self._calculate_pitch(self._p0, self._p1)
        self._roll = self._calculate_roll(self._p2, self._p1)
        self._log.info("Leveling Done")


    def transform_point(self, point: List[float]):
        """ returns the given point relative to the new plane

        @param: p - List of x, y, z coordinates
        """
        new_point = np.array([0.0, 0.0, 0.0])
        p1 = self._p1
         # pitch rotation adjustment
        new_point[2] = (point[2] - p1[2]) * math.cos(self._pitch) - (point[1] + p1[1]) * math.sin(self._pitch) + p1[2]
        new_point[1] = (point[1] + p1[1]) * math.cos(self._pitch) + (point[2] - p1[2]) * math.sin(self._pitch) - p1[1]
        new_point[0] = point[0]
        # roll rotation adjustment
        new_point[2] = (new_point[2] - p1[2]) * math.cos(self._roll) - (new_point[0] + p1[0]) * math.sin(self._roll) + p1[2]
        new_point[0] = (new_point[0] + p1[0]) * math.cos(self._roll) + (new_point[2] - p1[2]) * math.sin(self._roll) - p1[0]
        new_point[1] = new_point[1]
        # yaw rotation adjustment
        new_point[0] = (new_point[0] - p1[0]) * math.cos(self._yaw) - (new_point[1] - p1[1]) * math.sin(self._yaw) + p1[0]
        new_point[1] = (new_point[1] - p1[1]) * math.cos(self._yaw) + (new_point[0] - p1[0]) * math.sin(self._yaw) + p1[1]
        new_point[2] = new_point[2]
        #print(new_point)

        # shift the z coordinate to account for the radius of the probe/sensor
        new_point[2] = new_point[2] + ((self.WIDTH * math.sin(self._pitch)) / math.sin(math.radians(90) - self._pitch))

        return new_point

    def _calculate_yaw(self, p1, p2):
        yDiff = p2[1] - p1[1]
        xDiff = p2[0] - p1[0]
        yaw = 0

        if np.isclose(xDiff, 0.0, rtol=1e-5, atol=1e-8) and yDiff > 0:
            yaw = math.radians(90)
        elif np.isclose(xDiff, 0.0, rtol=1e-5, atol=1e-8) and yDiff < 0:
            yaw = math.radians(-90)
        elif np.isclose(yDiff, 0.0, rtol=1e-5, atol=1e-8) and xDiff < 0:
            yaw = math.radians(180)
        else:
            yaw = yDiff / xDiff
            #yaw = math.radians(270) + np.arctan(yaw)
            yaw = np.arctan(yaw)
        return yaw

    def _calculate_pitch(self, p1, p2):
        yDiff = p2[1] - p1[1]
        zDiff = p2[2] - p1[2]
        pitch = 0

        if np.isclose(yDiff, 0.0, rtol=1e-5, atol=1e-8) and zDiff > 0:
            pitch = math.radians(90)
        elif np.isclose(yDiff, 0.0, rtol=1e-5, atol=1e-8) and zDiff < 0:
            pitch = math.radians(-90)
        elif np.isclose(zDiff, 0.0, rtol=1e-5, atol=1e-8) and yDiff < 0:
            pitch = math.radians(180)
        else:
            pitch = zDiff / yDiff
            #pitch = math.radians(90) + np.arctan(pitch)
            pitch = np.arctan(pitch)
        return pitch

    def _calculate_roll(self, p1, p2):
        xDiff = p2[0] - p1[0]
        zDiff = p1[2] - p2[2]
        roll = 0

        if np.isclose(xDiff, 0.0, rtol=1e-5, atol=1e-8) and zDiff > 0:
            roll = math.radians(90)
        elif np.isclose(xDiff, 0.0, rtol=1e-5, atol=1e-8) and zDiff < 0:
            roll = math.radians(-90)
        elif np.isclose(zDiff, 0.0, rtol=1e-5, atol=1e-8) and xDiff < 0:
            roll = math.radians(180)
        else:
            roll = zDiff / xDiff
            roll = np.arctan(roll)

        return roll

if __name__ == "__main__":
    point1 = [
        14.9296875,
        439.84101562499995,
        99.0475
    ]
    point2 = [
        14.9296875,
        30.312890624999998,
        97.97875
    ]
    point3 = [
        362.6671875,
        30.312890624999998,
        94.78625
    ]

    lv = Leveler(logger=logging)
    lv.probe_point(point1, PointLocation.BOTTOM_LEFT)
    lv.probe_point(point2, PointLocation.BOTTOM_RIGHT)
    lv.probe_point(point3, PointLocation.TOP_RIGHT)

    lv.calculate_rotations()

    p = lv.transform_point([410.5, 220.1, 120.2])

    print(p)
