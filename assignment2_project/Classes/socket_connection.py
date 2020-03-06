"""Creates SocketConnection class"""
import socket
import json
import sys
from Classes.socket_utils import SocketUtils
from Classes.master_menu import MasterMenu
sys.path.append("..")

# Code sourced by Matthew Bolger
class SocketConnection:
    """ This class primarily handles the socket connection for both Master and Reception Pi """
    def __init__(self):
        self.socket_utils = SocketUtils()
        with open("config.json", "r") as file:
            data = json.load(file)
        self.__reception_ip = data["reception_ip"]
        self.__master_ip = data["master_ip"]
        self.__port = data["port"]
        self.__master_address = (self.__master_ip, self.__port)
        self.__reception_address = (self.__reception_ip, self.__port)

    def master_connecting(self):
        """
        This function makes the Master Pi listen for the connection of the Reception Pi.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connected_socket:
            connected_socket.bind(self.__reception_address)
            connected_socket.listen()

            print("Listening on {}...".format(self.__reception_address))
            while True:
                print("Waiting for Reception Pi...")
                conn, addr = connected_socket.accept()
                with conn:
                    print("Connected to {}".format(addr))
                    print()

                    user = self.socket_utils.recv_json(conn)
                    master_menu = MasterMenu(user)
                    master_menu.menu()
                    self.socket_utils.send_json(conn, {"logout": True})


    def reception_connecting(self, user):
        """
        This function makes the Reception Pi search and connect to the Master Pi's IP

        Parameter:
            user (str): It passes the username to the Master Pi
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connected_socket:
            print("Connecting to {}...".format(self.__master_address))
            connected_socket.connect(self.__master_address)
            print("Connected.")

            print("Logging in as '{}'".format(user))
            self.socket_utils.send_json(connected_socket, user)

            print("Waiting for Master Pi...")
            while True:
                object_received = self.socket_utils.recv_json(connected_socket)
                if "logout" in object_received:
                    print("User '{}' has logged out.".format(user))
                    print()
                    break
                break
