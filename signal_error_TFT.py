from agents import TitForTat
import math
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def main():
    NUM_OF_MOVES = 11


    verts = []
    codes = []

    a0 = TitForTat(NUM_OF_MOVES)
    a1 = TitForTat(NUM_OF_MOVES)

    signal_error = True
    # # add error in the middle of the game
    error_index = math.floor(NUM_OF_MOVES / 2)
    error_index = 0
    min_val = 10000
    max_val = -10000


    for i in range(NUM_OF_MOVES):
        a0_move = a0.make_move()
        a1_move = a1.make_move()
        add_error = signal_error and error_index == i 
        a1_move = False if add_error else a1_move
        # process output of the opponent
        a0.on_post_move(a1_move)
        a1.on_post_move(a0_move)
        print(f"i={i:2}, a0 : {str(a0_move):5} a1 : {str(a1_move):5} | score {a0.score:2}/{a1.score:2}." + (" <- error" if add_error else ""))
        
        # scale graph properly
        min_val = min(min_val, min(a0.score, a1.score))
        max_val = max(max_val, max(a0.score, a1.score))

        verts.append((a0.score, a1.score))
        # have to move to initial position before drawing
        codes.append(Path.LINETO if i != 0 else Path.MOVETO)

    path = Path(verts, codes)
    ax = plt.subplots()
    patch = patches.PathPatch(path, facecolor='white', lw=2)

    ax.add_patch(patch)
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)



    plt.show()








if __name__ == "__main__":
    main()