import pygame
pygame.init()

BLACK = 0,0,0
PLAYER1 = 255,0,0
PLAYER2 = 0,0,255
PLAYER3 = 0,255,0
PLAYER4 = 255, 255, 0
WHITE = 255, 255, 255
FENCE_COLOR = 0, 255, 255
FENCE_WIDTH = 3
POTENTIAL_HIGHLIGHT = 0, 100, 100
HIGHLIGHT = 0, 200, 200

COLORS = [PLAYER1, PLAYER2, PLAYER3, PLAYER4]

ROWS = 9

pygame.font.init()

class QuoridorVisualizer:
    def __init__(self, width=640, height=480):
        self.screen = pygame.display.set_mode((width, height))

        self.width = width
        self.height = height
        self.box_size = height / (ROWS + 2)
        self.radius = self.box_size / 2
        self.left_disp_offset = self.box_size * 2
        self.top_disp_offset = self.box_size

        self.game_closed = False


    def draw_board(self, canonical_board, potential_moves = [], current_space = [], potential_fences = [], current_fence = []):
        if not self.game_closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_closed = True
                    pygame.quit()

            # Reset screen
            self.screen.fill(BLACK)

            # Drawing the grid
            for row_num in range(0, 10):
                row_start = (self.left_disp_offset, self.top_disp_offset + (self.box_size * row_num))
                row_end = (self.left_disp_offset + (self.box_size * 9), self.top_disp_offset + (self.box_size * row_num))
                pygame.draw.line(self.screen, WHITE, row_start, row_end)
            for col_num in range(0, 10):
                col_start = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset)
                col_end = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset + (self.box_size * 9))
                #if col_num > 0:
                #    col_label = my_font.render(str(col_num), 1, WHITE)
                #    self.screen.blit(col_label, (self.left_disp_offset + (self.box_size * col_num) - self.box_size / 2, self.height - 40))
                pygame.draw.line(self.screen, WHITE, col_start, col_end)

            # Drawing potential squares
            for position in potential_moves:
                pygame.draw.rect(self.screen, POTENTIAL_HIGHLIGHT, pygame.Rect(int(self.box_size * position.coord.x) + self.left_disp_offset + 1, int(self.box_size * position.coord.y) + self.top_disp_offset + 1, self.box_size - 1, self.box_size - 1))

            # Drawing current cursor position for move
            for position in current_space:
                pygame.draw.rect(self.screen, HIGHLIGHT, pygame.Rect(int(self.box_size * position.coord.x) + self.left_disp_offset + 1, int(self.box_size * position.coord.y) + self.top_disp_offset + 1, self.box_size - 1, self.box_size - 1))

            # Drawing pieces
            for i in range(len(canonical_board.pawns)):
                pawn = canonical_board.pawns[i]
                pos = (int(self.box_size * (pawn.x + 0.5)) + self.left_disp_offset + 1,
                        int(self.box_size * (pawn.y + 0.5)) + self.top_disp_offset + 1)
                pygame.draw.circle(self.screen, COLORS[i], pos, self.radius - 1)

            # Drawing fences
            for fence in canonical_board.horizontal_fences:
                self.draw_fence(fence.first, fence.is_horizontal, FENCE_COLOR)
            for fence in canonical_board.vertical_fences:
                self.draw_fence(fence.first, fence.is_horizontal, FENCE_COLOR)

            # Draw potential fences
            for fence in potential_fences:
                self.draw_fence(fence.coord, fence.is_horizontal, POTENTIAL_HIGHLIGHT)

            # Draw current potential fence
            for fence in current_fence:
                self.draw_fence(fence.coord, fence.is_horizontal, HIGHLIGHT)

            #for row_num, row in enumerate(canonical_board):
            #    for col_num, element in enumerate(row):
            #        pos = (int(self.box_size * (col_num + 0.5)) + self.left_disp_offset,
            #               int(self.box_size * (row_num + 0.5)) + self.top_disp_offset)
            #        if element == red_label:
            #            pygame.draw.circle(self.screen, RED, pos, self.radius)
            #        elif element == blue_label:
            #            pygame.draw.circle(self.screen, BLUE, pos, self.radius)
            pygame.display.flip()
            pygame.time.wait(1000)

    def draw_fence(self, coord, is_horizontal, color):
        second_x = coord.x
        second_y = coord.y
        if is_horizontal:
            second_x += 2
        else:
            second_y += 2
        pos1 = (int(self.box_size * coord.x) + self.left_disp_offset,
                int(self.box_size * coord.y) + self.top_disp_offset)
        pos2 = (int(self.box_size * second_x) + self.left_disp_offset,
                int(self.box_size * second_y) + self.top_disp_offset)
        pygame.draw.line(self.screen, color, pos1, pos2, FENCE_WIDTH)