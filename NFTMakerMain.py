import cv2, os, subprocess, tqdm, keyboard, time, sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def rgb_to_hex(r,g,b):
    hex = '#%02x%02x%02x' % (r, g, b)
    return hex.replace("#", "")

def main():
    pygame.init()
    files = [f for f in os.listdir(os.getcwd() + r"\NFTS") if os.path.isfile(os.path.join(os.getcwd() + r"\NFTS", f))]
    for key, f in enumerate(files): print(f"{key} == {f}")
    image = cv2.imread("NFTS/" + files[int(input("Type in the number of the image you want to use:"))])
    dominant_resolution_xy = image.shape[1] if image.shape[1] > image.shape[0] else image.shape[0]
    max_resolution = 32 
    
    adjustment_value = max_resolution / dominant_resolution_xy
    
    usr_input = input(f"The image will be scaled by a factor of {adjustment_value}, continue? [Y]:").lower()
    tolerance = int(input("Enter the tolerance value which defines how much different a color has to be to be counted as a different one. [Paint time and detail become lower the higher this value is]:"))
    if usr_input == "y": pass 
    else: sys.exit()
    
    image = cv2.resize(image, (round(image.shape[1]*adjustment_value), round(image.shape[0]*adjustment_value)), interpolation=cv2.INTER_LINEAR)

    colors = []
    positions_with_color = []
    loop_contin = False

    for y in tqdm.tqdm(range(0, image.shape[0]), desc="Optimizing drawing"):
        for x in range(0,image.shape[1]):
            for key, val in enumerate(colors):
                if image[y, x, 2] in range(val[0]-tolerance, val[0]+tolerance+1) and image[y, x, 1] in range(val[1]-tolerance, val[1]+tolerance+1) and image[y, x, 0] in range(val[2]-tolerance, val[2]+tolerance+1):
                    positions_with_color[key].append([654+x*20,190+y*20, x, y])
                    loop_contin = True
                    break
        
            if loop_contin == True:
                loop_contin = False
                continue
         
            colors.append([image[y,x,2], image[y,x,1], image[y,x,0]])
            positions_with_color.append([rgb_to_hex(image[y,x,2], image[y,x,1], image[y,x,0]), [654+x*20,190+y*20, x, y]])

    background = pygame.display.set_mode((576, 576))

    for color_and_positions in tqdm.tqdm(positions_with_color, desc="Rendering preview"):
        rgb_color = tuple(int(color_and_positions[0][i:i+2], 16) for i in (0, 2, 4))
        for pos in color_and_positions[1:]:
            pygame.draw.rect(background, rgb_color, pygame.Rect(pos[2]*18,pos[3]*18,19,19))

    running = True
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

    print(f"Ready to start drawing! \nWaiting for key 'alt'")
    keyboard.wait("alt")

    for color_and_positions in tqdm.tqdm(positions_with_color, desc="Drawing progress"):

        subprocess.run(f"change_pointer_color.exe {color_and_positions[0]}")
        while not os.path.isfile("block_file"):
            pass
        os.remove("block_file")

        for pos in color_and_positions[1:]:
            if keyboard.is_pressed("end"): return
            subprocess.run(f"press.exe {pos[0]} {pos[1]}")

if __name__ == "__main__":
    main()

