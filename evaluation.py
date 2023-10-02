from sudoku import Sudoku
import matplotlib.pyplot as plt
import numpy as np

def eval():
    """
    Function for evaluating the solver for different sudoku puzzles.

    ---
    plots a graph containing the solvers progress.
    """
    #solving
    s1 = Sudoku('sudoku/easy.txt'); s1.solve()
    s2 = Sudoku('sudoku/medium.txt'); s2.solve()
    s3 = Sudoku('sudoku/hard.txt'); s3.solve()
    s4 = Sudoku('sudoku/veryhard.txt'); s4.solve()

    #comparing progress
    p1 = s1.progress #progress is a array containing the number of completed variables.
    p2 = s2.progress
    p3 = s3.progress
    p4 = s4.progress

    #plotting progresses
    progresses = [p1, p2, p3, p4]
    x_length = max(len(p) for p in progresses)
    for p in progresses:
        while(len(p) < x_length): p.append(81)

    fig, ax = plt.subplots()
    plt.title("Performance vs backtrack")
    plt.xlabel("backtracks")
    plt.ylabel("# found variables")
    ax.plot(np.arange(x_length), progresses[0], label="easy board")
    ax.plot(np.arange(x_length), progresses[1], label="medium board")
    ax.plot(np.arange(x_length), progresses[2], label="hard board")
    ax.plot(np.arange(x_length), progresses[3], label="very hard board")
    ax.legend()
    
    plt.savefig("test.png")

if __name__ == "__main__":
    eval()

