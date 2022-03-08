import string
import json
from venv import create
from googleapiclient.discovery import build
from youtube_statistics import YTstats
from collections import defaultdict


class YoutubeAssistant:
    """
    Assists the YTStats class by retrieving recent video data
    and checking for any updates in a channel's json file.
    """

    def __init__(self) -> None:
        
        self.api_key = "AIzaSyA23CUrJ518IxgnWhF5XR-zrhbV7_vEe6E"

        self.youtube = build('youtube', 'v3', static_discovery=False, developerKey=self.api_key)
        #channel_id = "UCiMr9kBgaBs9--eFW72Ok-A"
        self.channel_list = defaultdict(str)

        self.channel_names = list()

    # stores all the videos of a channel in a file
    def get_channel_info(self, channel_id):
        """
        Checks if a channel id is valid, if it is then adds it to the supported channels list.
        """

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

            self.channel_list[c.rstrip("\n")] = ""

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

            # store in dictionary 
            for video in yt.video_data:
                self.channel_list[ch] = video
                if end == 1:
                    self.channel_names.append(yt.video_data[video]["channelTitle"])
                    break;

    # check json file
    def check_json(self):
        """
        Check the json file and see if the latest video we retrieved
        from a given channel is equal to what we previously had.
        If not then update the channel json file and upload new video
        to discord.
        """
        i = 0
        is_new = None
        for channel in self.channel_names:
            file_name = "./channels/" + channel.lower() + ".json"
            json_file = open(file_name, 'r')

            data = json.load(json_file)

            # check if latest video == to the most recent video on the channel
            is_new = self.is_new_video(data, i)
            # close file 
            json_file.close()
            i+=1

        print(is_new)

    # check if a change
    def is_new_video(self, data, i):
        """
        Checks if a new video has been uploaded in all the supported channels.
        Returns True if a new video has been uploaded and false if not.
        """

        channels = list(self.channel_list.keys())

        channel_id = channels[i].rstrip("\n")
        for vid in data[channel_id]["video_data"]:

            if vid == self.channel_list[channel_id]:

                return False

            break

        return True

    # good practice
    def close_socket(self):
        """
        Closes the socket we opened.
        """

        # close socket 
        self.youtube.close()