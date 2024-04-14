from typing import List, Tuple
from PIL import Image
import math

MAX_IMAGE_SIZE = (1024, 1024)

def get_frames(img: Image.Image) -> int: return img.n_frames # type: ignore -- This. Is. An. Int.

def extract_frames(img: Image.Image) -> List[Image.Image]:
    images: List[Image.Image] = []
    
    for i in range(get_frames(img)):
        img.seek(i)
        new_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
        new_img.paste(img) # type: ignore
        images.append(new_img)
        
    return images

def scale_tuple_by_float(t: Tuple[float, float], scale: float) -> Tuple[float, float]: return (t[0] * scale, t[1] * scale)
# def scale_tuple_by_tuple(t: Tuple[float, float], scale: Tuple[float, float]) -> Tuple[float, float]: return (t[0] * scale[0], t[1] * scale[1])
def floor_tuple(t: Tuple[float, float]) -> Tuple[int, int]: return (math.floor(t[0]), math.floor(t[1]))

def main(img: Image.Image):
    print(f"Loading frames..")
    frames = extract_frames(img)
    print(f"Amount of frames: {len(frames)}")
    positions = math.ceil(math.sqrt(len(frames))) ** 2
    print(f"Available positions: {positions}")
    frame_scale_y = img.size[1] * (1 / img.size[0])
    print(f"Frame scale: {frame_scale_y}")
    image_area = MAX_IMAGE_SIZE[0] * MAX_IMAGE_SIZE[1]
    base = math.sqrt(image_area / positions / frame_scale_y)
    print(f"Base size: {base}")
    frame_size_scaled = floor_tuple((base, base * frame_scale_y))
    print(f"Scaled image size: {frame_size_scaled}")
    
    print("Resizing frames..")
    frames = [i.resize(frame_size_scaled) for i in frames] # type: ignore
    
    print("Creating output..")
    IMAGE_SIZE = (
        math.floor(MAX_IMAGE_SIZE[0] / frame_size_scaled[0]) * frame_size_scaled[0],
        math.floor(MAX_IMAGE_SIZE[1] / frame_size_scaled[1]) * frame_size_scaled[1],
    )
    print(f"Cropped image size: {IMAGE_SIZE}")
    output_image = Image.new('RGBA', IMAGE_SIZE)
    pos_x = 0
    pos_y = 0
    for frame in frames:
        output_image.paste(frame, (pos_x, pos_y)) # type: ignore
        
        pos_x += frame_size_scaled[0]
        if pos_x > IMAGE_SIZE[0] - frame_size_scaled[0]:
            pos_x = 0
            pos_y += frame_size_scaled[1]
    
    output_image.save("output.png") # type: ignore
    print("Creating output script..")
    with open("base.lua", "r") as f:
        base_script = f.read()
        
    isLooping = img.info["loop"] == 0 # type: ignore
    
    output_script = ""
    output_script += f"local FRAMES = {len(frames)}\n"
    output_script += f"local FPS = {math.floor(1000 / img.info['duration'])}\n" # type: ignore
    output_script += f"local FRAME_SIZE = Vector2.new({frame_size_scaled[0]}, {frame_size_scaled[1]})\n"
    output_script += f"local IMAGE_SIZE = Vector2.new({IMAGE_SIZE[0]}, {IMAGE_SIZE[1]})\n"
    output_script += f"local SHOULD_IMAGE_LOOP = {'true' if isLooping else 'false'}\n"
    output_script += "\n"
    output_script += "-- Script\n"
    output_script += base_script
    
    with open("output.lua", "w") as f:
        f.write(output_script)

if __name__ == "__main__":
    with Image.open("input.gif") as img: # type: ignore
        main(img)
