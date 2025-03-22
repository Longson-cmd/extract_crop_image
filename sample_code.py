
from pprintpp import pprint
from torchvision.transforms import Resize, ToTensor, Compose
import glob  # For retrieving file paths
import json  # For reading JSON annotation files
import cv2  # OpenCV for handling video frames
from torch.utils.data import Dataset  # PyTorch Dataset class for handling data

class MyFootballDataset(Dataset):  # Inherits from PyTorch Dataset
    def __init__(self, root):
        # Get paths of all video files (.mp4) in the directory, remove ".mp4" from filenames
        video_paths = [file_path.replace(".mp4", "") for file_path in glob.iglob("{}/*/*.mp4".format(root))]
        
        # Get paths of all annotation files (.json), remove ".json" from filenames
        anno_paths = [file_path.replace(".json", "") for file_path in glob.iglob("{}/*/*.json".format(root))]

        # Keep only paths that have both a corresponding video and annotation file
        self.valid_paths = list(set(video_paths) & set(anno_paths))

        self.total_frames = 0  # Stores total number of frames across all videos
        from_id = 0  # Keeps track of starting frame index for each video
        self.video_select = {}  # Dictionary mapping video paths to their frame index ranges

        # Iterate over each valid video path
        for path in self.valid_paths:
            cap = cv2.VideoCapture("{}.mp4".format(path))  # Open video file
            self.total_frames += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get total frames in video
            self.video_select[path] = [from_id, self.total_frames - 1]  # Store frame range for this video
            from_id = self.total_frames  # Update starting frame index for next video

    def __len__(self):
        # Returns total number of frames in all videos
        return self.total_frames

    def __getitem__(self, item):
        # Determine which video contains the requested frame
        for path, (begin, end) in self.video_select.items():
            if begin <= item <= end:  # Check if the frame index falls within this video's range
                item -= begin  # Adjust frame index relative to this video
                break  # Stop searching once the correct video is found

        # Open the video and seek to the required frame
        cap = cv2.VideoCapture("{}.mp4".format(path))  # Open video file
        cap.set(cv2.CAP_PROP_POS_FRAMES, item)  # Set frame position to requested index
        flag, frame = cap.read()  # Read the frame

        # Open corresponding annotation JSON file
        with open("{}.json".format(path), "r") as json_file:
            annotations = json.load(json_file)["annotations"]  # Load annotations list

        # Filter annotations for players in this frame (category_id == 4)
        players = [anno for anno in annotations if anno["image_id"] - 1 == item and anno["category_id"] == 4]

        # Lists to store cropped player images, jersey numbers, and team colors
        list_players = []
        list_jerseys = []
        list_colors = []

        # Iterate over detected players and extract relevant information
        for player in players:
            xmin, ymin, w, h = player["bbox"]  # Get bounding box coordinates
            xmax = int(xmin + w)  # Calculate bottom-right x coordinate
            ymax = int(ymin + h)  # Calculate bottom-right y coordinate
            xmin = int(xmin)  # Convert to integer
            ymin = int(ymin)  # Convert to integer
            
            # Crop the player region from the frame
            list_players.append(frame[ymin:ymax, xmin:xmax, :])

            # Store player's jersey number
            list_jerseys.append(player["attributes"]["jersey_number"])

            # Store player's team jersey color
            list_colors.append(player["attributes"]["team_jersey_color"])

        # Return the cropped players' images, their jersey numbers, and their team colors
        return list_players, list_jerseys, list_colors
    
from PIL import Image
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data_train = MyFootballDataset('C:/Users/PC/Desktop/unfinish_project/prepare_dataset/footballs/football_train')
    print(len(data_train))


    list_players, list_jerseys, list_colors = data_train[3000]
    print(list_jerseys)
    print(list_colors)
    print(list_players)
    

    for players in list_players:
        image = players
        plt.imshow(image)
        plt.axis('off')
        plt.show()

