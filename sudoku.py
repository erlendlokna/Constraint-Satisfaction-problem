from CSP import CSP
import time
from PIL import Image, ImageDraw, ImageFont

class Sudoku(CSP):
    def __init__(self, filename: str):
        """Instantiate a CSP representing the Sudoku board found in the text
        file named 'filename' in the current directory.

        Parameters
        ----------
        filename : str
            Filename of the Sudoku board to solve
        """
        super().__init__()

        self.filename = filename

        board = list(map(lambda x: x.strip(), open(filename, 'r')))

        for row in range(9):
            for col in range(9):
                if board[row][col] == '0':
                    self.add_variable('%d-%d' % (row, col), list(map(str,
                                                                    range(1, 10))))
                else:
                    self.add_variable('%d-%d' % (row, col), [board[row][col]])

        for row in range(9):
            self.add_all_different_constraint(['%d-%d' % (row, col)
                                            for col in range(9)])
        for col in range(9):
            self.add_all_different_constraint(['%d-%d' % (row, col)
                                            for row in range(9)])
        for box_row in range(3):
            for box_col in range(3):
                cells = []
                for row in range(box_row * 3, (box_row + 1) * 3):
                    for col in range(box_col * 3, (box_col + 1) * 3):
                        cells.append('%d-%d' % (row, col))
                self.add_all_different_constraint(cells)

    def solve(self, output_filename=None): 
        t0 = time.time()
        self.backtracking_search() #running backtrack search.
        t1 = time.time()
        
        print(f"\nsolution for {self.filename}\n") #printing and saving solution as image. 
        self.print_solution()
        if output_filename: self.solution_as_img(output_filename)
        print(f"backtracks called: {self.backtracks_called}")
        print(f"backtrack failures: {self.backtrack_failures}")
        print(f"compute time: {round(t1- t0,3)} seconds")



    def print_solution(self):
        """Convert the representation of a Sudoku solution as returned from
        the method CSP.backtracking_search(), into a human readable
        representation.
        """
        assert self.solution,  'no solutions calculated. Run backtrach_search()'

        for row in range(9):
            for col in range(9):
                print(self.solution['%d-%d' % (row, col)][0], end=" "),
                if col == 2 or col == 5:
                    print('|', end=" "),
            print("")
            if row == 2 or row == 5:
                print('------+-------+------')

    def solution_as_img(self, output_filename):

        """Save the Sudoku solution as a PNG image.

        Parameters
        ----------
        output_filename : str
            The name of the output PNG file.
        """
        #image init:
        image_size = (540, 540)  # Increased image size for higher quality
        cell_size = (60, 60)  # Increased cell size
        image = Image.new("RGB", image_size, "white")
        draw = ImageDraw.Draw(image)

        font_size = 34  # Choose a larger font size
        font = ImageFont.truetype("sudoku/arial.ttf", font_size)  # Use a specific font with the desired size

        for row in range(9):
            for col in range(9):
                cell_value = int(self.solution['%d-%d' % (row, col)][0])

                # Position of number:
                x = col * cell_size[0] + 20 
                y = row * cell_size[1] + 20 

                # Draw number:
                draw.text((x, y), str(cell_value), fill="black", font=font)

        # Draw grid lines with thicker borders
        line_width = 1  # width of lines that are not borders
        border_width = 8  # Border width
        #vertical lines:
        for row in range(0, 10):
            line_y = row * cell_size[1]
            draw.line(
                [(0, line_y), (image_size[0], line_y)],
                fill="black",
                width=border_width if row in [0, 3, 6, 9] else line_width,
            )
        #horisontal lines
        for col in range(0, 10):
            line_x = col * cell_size[0]
            draw.line(
                [(line_x, 0), (line_x, image_size[1])],
                fill="black",
                width=border_width if col in [0, 3, 6, 9] else line_width,
            )

        # Save the image
        image.save(output_filename)

if __name__ == "__main__":
    #Easy sudoku
    Sudoku("sudoku/easy.txt").solve(output_filename="sudoku/easy_sol.png")
    
    #medium sudoku
    Sudoku("sudoku/medium.txt").solve(output_filename="sudoku/medium_sol.png")

    #hard sudoku
    Sudoku("sudoku/hard.txt").solve(output_filename="sudoku/hard_sol.png")

    #very hard sudoku
    Sudoku("sudoku/veryhard.txt").solve(output_filename="sudoku/veryhard_sol.png")

