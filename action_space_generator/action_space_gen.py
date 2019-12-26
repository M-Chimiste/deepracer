import json
import tkinter as tk

"""
Application to create action space json files for deepracer.
"""

class ActionGenerator:
    def __init__(self, max_angle, max_speed,
                angle_granularity, speed_granularity):
        """
        Class for creating action spaces for local deepracer training
        """

        assert isinstance(max_angle, int), 'Angle must be an integer.'
        assert abs(max_angle) >= 30 , 'Maximum angle must not exceed 30 degrees.'
        assert max_speed >= 0.8 , 'Maximum speed must be 0.8 or greater.'
        assert 8 >= max_speed, 'Maximum speed cannot exeed 8.0.'

        self.__max_speed = max_speed
        self.__max_angle = max_angle
        self.__angle_granularity = angle_granularity
        self.__speed_granularity = speed_granularity
    
    # Encapsulation for variables
    def get_max_speed(self):
        """Returns max_speed attribute."""
        max_speed = self.__max_speed
        return max_speed
    
    def set_max_speed(self, max_speed):
        """Sets max speed attribute."""
        assert max_speed >= 0.8 , 'Maximum speed must be 0.8 or greater.'
        assert 8 >= max_speed, 'Maximum speed cannot exeed 8.0.'
        self.__max_speed = max_speed
    
    def get_max_angle(self):
        """Returns max_angle attribute"""
        max_angle = self.__max_angle
        return max_angle
    
    def set_max_angle(self, max_angle):
        assert abs(max_angle) >= 30 , 'Maximum angle must not exceed 30 degrees.'
        self.__max_angle = max_angle
    
    def get_speed_granularity(self):
        """Returns speed_granularity attribute"""
        speed_granularity = self.__speed_granularity
        return speed_granularity
    
    def set_speed_graularity(self, speed_granularity):
        """Sets speed_granularity attribute."""
        self.__speed_granularity = speed_granularity
    
    def get_angle_granularity(self):
        """Returns the angle_granularity attribute."""
        angle_granularity = self.__angle_granularity
    
    def set_angle_granularity(self, angle_granularity):
        """Sets the angle_granularity attribute."""
        self.__angle_granularity = angle_granularity
    
    def _save_json(self, action_space_dictionary):
        """Method to save action_space_dictionary as a json file."""
        file_path = 'model_metadata.json'
        json.dump(action_space_dictionary, file_path)

    def generate_action_space(self):
        max_angle = abs(self.get_max_angle)
        max_speed = self.get_max_speed
        angle_granularity = self.get_angle_granularity
        speed_granularity = self.get_speed_granularity

        index_space = int(angle_granularity * speed_granularity)
        max_neg_angle = -1 * max_angle
        