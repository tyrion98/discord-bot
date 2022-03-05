import string
from venv import create
from googleapiclient.discovery import build
from youtube_statistics import YTstats
from collections import defaultdict


class YoutubeAssistant:


    def __init__(self) -> None:

        self.api_key = "AIzaSyA23CUrJ518IxgnWhF5XR-zrhbV7_vEe6E"

        self.youtube = build('youtube', 'v3', static_discovery=False, developerKey=self.api_key)
        #channel_id = "UCiMr9kBgaBs9--eFW72Ok-A"
        self.channel_list = defaultdict(str)

    # stores all the videos of a channel in a file
    def get_channel_info(self, channel_id):


        yt = YTstats(self.api_key, channel_id)
        yt.get_channel_statistics()
        yt.get_channel_video_data()
        success = yt.dump()
        
        #if success:
            # add channel to file
        #    self.create_channel_file(channel_id)

        # return success
        return success

    # add to channel txt
    def create_channel_file(self, channel_id):
        """
        Creates a txt file that contains the list of channel names.
        """
        # make it
        with open("./channels/channel.txt", 'a') as file:
            file.write(channel_id + "\n")

        # close file
        file.close()

    # get all channels in channels folder
    def get_channels(self):
        """
        Read the channel.txt file and extracts all the names 
        and puts them into a list.
        """

        with open("./channels/channel.txt" , "r") as file:

            lst = file.readlines()


        for c in lst:

            self.channel_list[c] = ""

    # get the latest video upload id
    def get_latest_video(self):
        """
        Reads the channel list, and checks the most recently
        uploaded video for each channel.
        """
        end = 1
        for ch in self.channel_list:

            yt = YTstats(self.api_key, ch)
            yt.get_channel_statistics()
            yt.get_channel_video_data()


            for video in yt.video_data:
                self.channel_list[ch] = video
                if end == 1:
                    break;

        print(self.channel_list)

    # good practice
    def close_socket(self):
        """
        Closes the socket we opened.
        """

        # close socket 
        self.youtube.close()