import random
import pygame
from sys import exit
import os

# Possible bugs
"""Cards are being wiped before senior player makes move, making it harder to realize the move"""

# Constants
SCREEN_WIDTH = 1070
SCREEN_HEIGHT = 620
TITLE = "Rung - Play With Friends"
FPS = 30
CARD_WIDTH = 70
CARD_HEIGHT = 90
CARDS_PLACEMENT_Y = 20
CARDS_PLACEMENT_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
FRAME_WIDTH = 60
FRAME_HEIGHT = 70
PROFILE_WIDTH, PROFILE_HEIGHT = 54, 64
SUPPORTED_FILES = (".jpg", ".jpeg", ".png", ".gif")
IMAGES_FOLDER_PATH = "./Data/Images/"
INACTIVE_GAME_INSTRUCTION = "Press Enter to play again. Press Esc to exit."
AUTHOR = ""
SCORECARD_XY = [(220, 160), (745, 367)]
SCORECARD_SIZE = (60, 70)
TEAM1_SCORE = 0
TEAM2_SCORE = 0
RUNG_CARD_BG_COLOR = "green"
game_on = True

# initializing pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("./Data/Images/Icons/favicon.png").convert_alpha())

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
LIGHT_GREY = "#333333"

# In-game Variables
PLAYER_ONE_CARDS = []
PLAYER_TWO_CARDS = []
PLAYER_THREE_CARDS = []
PLAYER_FOUR_CARDS = []
p2n4_card_rect = pygame.Rect((0, 0), (CARD_HEIGHT, (CARD_WIDTH / 2)))
p1n3_card_rect = pygame.Rect((0, 0), ((CARD_WIDTH / 2), CARD_HEIGHT))
p1_xy = []
p2_xy = []
p3_xy = []
p4_xy = []
PLAYER_ONE_CARDS_RECT = []
RUNNING_SUIT = ""
HAND = False
CARDS_BACK_LIST = []
PLAYERS_ALLOWED = [True, False, False, False]
PLAYERS_PLAYED_CARDS = [[], [], [], []]
CURRENT_PLAYER = [True, False, False, False]
ACTIVE_PLAYER = [True, False, False, False]
SENIOR_PLAYER = [False, False, False, False]
LAST_PLAYED_TICKS = 0
text_font = pygame.font.Font(None, 50)
FRAME_RECTS = {}
FRAME_BACKGROUND_COLOR = "white"
PLAYED_HANDS_INFO = []
RUNG = ""
RUNG_SELECTION_SURFACE = pygame.surface.Surface((SCREEN_WIDTH, 200))
RUNG_SELECTION_SURFACE.fill("white")
SUIT_RECTS = []
CARD_BACKGROUND = pygame.surface.Surface((CARD_WIDTH, CARD_HEIGHT))
CARD_BACKGROUND.fill("white")
CARD_BACKGROUND_ROTATED = pygame.transform.rotate(CARD_BACKGROUND, 90)
MOVE_STARTER = [False, False, False, False]
MOVE_NO = 0
PREVIOUS_SENIOR = ""
TOTAL_MOVES_TAKEN = 0
WINNER_STATE = None
WINNER_TEXT = text_font.render(f"{WINNER_STATE}", False, BLACK)
INACTIVE_GAME_TEXT = text_font.render(f"{INACTIVE_GAME_INSTRUCTION}", False, BLACK)
WIPE_CARDS_REQUEST = [False, False, False, False]
WIPE_CARDS = False
wipe_cards_time = None
wipe_cards_done_time = None
WIPE_CARDS_DONE = False
PLAYERS_LAST_PLAYED_TICKS = [0, 0, 0, 0]
GAME_END = False
AUTHOR_TEXT = text_font.render(f"{AUTHOR}", True, WHITE)
FINAL_SCORES = text_font.render(f"Team 1 Score: {TEAM1_SCORE}, Team 2 Score: {TEAM2_SCORE}", False, BLACK)
START_EVENT = pygame.USEREVENT + 1
STOP_EVENT = pygame.USEREVENT + 2


def fetch_data(folder_names, width, height):
    global FRAME_WIDTH, FRAME_HEIGHT
    images = {}
    for directory in folder_names:
        f_folder = os.listdir(f"{IMAGES_FOLDER_PATH}{directory}")
        for f_path in f_folder:
            if f_path.endswith(SUPPORTED_FILES):
                k, _ = os.path.splitext(f_path)
                img_path = os.path.join(f"{IMAGES_FOLDER_PATH}{directory}", f_path)
                images[k] = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (width, height))
    return images


# Cards Images
card_images = fetch_data(["Spades", "Hearts", "Diamonds", "Clubs"], CARD_WIDTH, CARD_HEIGHT)

# Frames
frame_images = fetch_data(["Frames"], FRAME_WIDTH, FRAME_HEIGHT)
frame_names = list(frame_images.keys())
frame_names = sorted(frame_names)

# Frame Background Image
FRAME_BG = pygame.surface.Surface((FRAME_WIDTH, FRAME_HEIGHT))
FRAME_BG.fill("white")
rotated_frame_bg = [pygame.transform.rotate(FRAME_BG, 90), pygame.transform.rotate(FRAME_BG, 270)]
FRAME_BACKGROUND = {
    "0": pygame.surface.Surface((FRAME_WIDTH, FRAME_HEIGHT)),
    "1": rotated_frame_bg[1],
    "2": pygame.surface.Surface((FRAME_WIDTH, FRAME_HEIGHT)),
    "3": rotated_frame_bg[0]
}
FRAME_BACKGROUND["0"].fill("white")
FRAME_BACKGROUND["2"].fill("white")

# Avatars
avatar_images = fetch_data(["Avatars"], PROFILE_WIDTH, PROFILE_HEIGHT)
avatar_names = list(avatar_images.keys())

# Scoreboards
scoreboard_images = fetch_data(["Scoreboards"], SCORECARD_SIZE[0], SCORECARD_SIZE[1])
scoreboard_img = pygame.transform.scale(pygame.image.load("./Data/Images/Backgrounds/Brown.jpg"), (57, 67))
scoreboard_img.set_alpha(208)

# BACKGROUND IMAGES
screen_bg_img = pygame.image.load("./Data/Images/Backgrounds/360_F_325384191_sg1D5lYWfRedGQsBm8xIHnsSAUUUVxGE.jpg")
screen_bg_img = pygame.transform.scale(screen_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen_bg_rect = screen_bg_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# Card Background Image
card_bg_img = pygame.image.load("./Data/Images/Card Backs/card-back-black.png").convert_alpha()
card_bg_img = pygame.transform.scale(card_bg_img, (CARD_WIDTH, CARD_HEIGHT))
rotated_c_bg_img = pygame.transform.rotate(card_bg_img, 270)

# Suits Images
suit_images = fetch_data(["Suits"], 80, 80)

# Crown Images
folder = os.listdir("./Data/Images/Crowns")
crown_images = []
crown_rects = []
for file_name in folder:
    if file_name.lower().endswith(("jpg", "png", "jpeg", "png")):
        alpha_image = pygame.image.load(f"./Data/Images/Crowns/{file_name}").convert_alpha()
        image = pygame.transform.scale(alpha_image, (50, 50))
        crown_images.append(image)
        crown_rects.append(image.get_rect())

# Basic Code
for index in range(13):
    """Make list of each player's cards location on screen"""
    p1_xy.append(((index * (CARD_WIDTH / 2)) + CARDS_PLACEMENT_X, SCREEN_HEIGHT - CARD_HEIGHT - CARDS_PLACEMENT_Y))
    p2_xy.append((CARDS_PLACEMENT_Y, (index * CARD_WIDTH / 2) + CARDS_PLACEMENT_Y + (CARDS_PLACEMENT_Y / 4)))
    p3_xy.append(((index * CARD_WIDTH / 2) + CARDS_PLACEMENT_X, CARDS_PLACEMENT_Y))
    p4_xy.append((SCREEN_WIDTH - CARD_HEIGHT - CARDS_PLACEMENT_Y, ((13 - index) * CARD_WIDTH / 2)))

for ind in range(13):
    PLAYER_ONE_CARDS_RECT.append(pygame.Rect((p1_xy[ind]), ((CARD_WIDTH / 2), CARD_HEIGHT)))

for index in range(13):
    CARDS_BACK_LIST.append(card_bg_img)

for index in range(13):
    PLAYED_HANDS_INFO.append({})

for i, suit in enumerate(suit_images.values()):
    SUIT_RECTS.append(suit.get_rect(topleft=(int(f"{i + 3}60"), (SCREEN_HEIGHT // 2) - 40)))


# Functions


def start_timer(event, delay):
    pygame.time.set_timer(event, delay)


def stop_timer(event):
    pygame.time.set_timer(event, 0)


def is_game_end():
    """Check if game is ended"""
    global PLAYER_ONE_CARDS, PLAYER_TWO_CARDS, PLAYER_THREE_CARDS, PLAYER_FOUR_CARDS, game_on, WINNER_STATE, \
        WINNER_TEXT, GAME_END, TEAM1_SCORE, TEAM2_SCORE, FINAL_SCORES
    if [l for l in PLAYERS_PLAYED_CARDS] == [[], [], [], []] and MOVE_NO >= 12:
        if TEAM2_SCORE > TEAM1_SCORE:
            WINNER_STATE = f"Team 2 has taken {TEAM2_SCORE} hands. Team 2 is the WINNER!"
        elif TEAM1_SCORE == TEAM2_SCORE:
            WINNER_STATE = f"It's a DRAW!"
        else:
            WINNER_STATE = f"Team 1 has has taken {TEAM1_SCORE} hands, Team 1 is the WINNER!"

        WINNER_TEXT = text_font.render(f"{WINNER_STATE}", False, BLACK)
        FINAL_SCORES = text_font.render(f"Team 1 Score: {TEAM1_SCORE}, Team 2 Score: {TEAM2_SCORE}", False, BLACK)
        game_on = False
        GAME_END = True


def restart_checker():
    global game_on, TEAM1_SCORE, TEAM2_SCORE, PLAYER_ONE_CARDS, PLAYER_TWO_CARDS, PLAYER_THREE_CARDS, PLAYER_FOUR_CARDS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if not game_on:
                if event.key == pygame.K_RETURN:
                    game_on = True
                    TEAM1_SCORE = 0
                    TEAM2_SCORE = 0
                    PLAYER_ONE_CARDS, PLAYER_TWO_CARDS, PLAYER_THREE_CARDS, PLAYER_FOUR_CARDS = deal_cards()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


def inactive_state():
    global WINNER_TEXT, INACTIVE_GAME_TEXT, AUTHOR_TEXT, FINAL_SCORES
    if WINNER_TEXT is not None and INACTIVE_GAME_TEXT is not None:
        screen.blit(WINNER_TEXT, (40, (SCREEN_HEIGHT // 2)-100))
        screen.blit(FINAL_SCORES, (170, (SCREEN_HEIGHT // 2)+50))


def exit_game():
    """Exit Game on cross or on pressing any key"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def white_frame_bg():
    """Make frame's background white"""
    global FRAME_BACKGROUND
    for k, v in FRAME_BACKGROUND.items():
        v.fill("white")


def deal_cards() -> list:
    """Shuffles and divides cards to four players"""
    deck = list(card_images.keys())
    random.shuffle(deck)
    return [sorted(deck[N * 13:(N + 1) * 13]) for N in range(4)]


def blit_card(img, background, xy):
    """Blit card with card background image"""
    screen.blit(background, xy)
    screen.blit(img, xy)


def start_game():
    """Start the game"""
    global WIPE_CARDS_REQUEST

    def wipe_card_check(requester):
        global PLAYERS_PLAYED_CARDS, WIPE_CARDS_REQUEST, WIPE_CARDS, wipe_cards_time, WIPE_CARDS_DONE, \
            wipe_cards_done_time
        if WIPE_CARDS_REQUEST[requester-1]:
            WIPE_CARDS = True
            wipe_cards_time = pygame.time.get_ticks()
            WIPE_CARDS_REQUEST = [False, False, False, False]
        if wipe_cards_time is not None:
            if WIPE_CARDS and pygame.time.get_ticks() >= wipe_cards_time + 1000:
                for ran in range(4):
                    if ran != SENIOR_PLAYER.index(True):
                        PLAYERS_PLAYED_CARDS[0] = []
                        PLAYERS_PLAYED_CARDS[ran] = []

                WIPE_CARDS_DONE = True
                wipe_cards_done_time = pygame.time.get_ticks()
                WIPE_CARDS = False

    def took_moves():
        global TOTAL_MOVES_TAKEN, PLAYERS_PLAYED_CARDS
        moves_taken = (MOVE_NO + 1) - TOTAL_MOVES_TAKEN
        TOTAL_MOVES_TAKEN += moves_taken
        return moves_taken

    def manage_seniors():
        global FRAME_BACKGROUND_COLOR, FRAME_BACKGROUND, PLAYED_HANDS_INFO, PREVIOUS_SENIOR, SENIOR_PLAYER,  \
            MOVE_STARTER, PLAYERS_PLAYED_CARDS, PLAYERS_ALLOWED, TEAM1_SCORE, TEAM2_SCORE, CURRENT_PLAYER, GAME_END

        current_senior = find_senior(PLAYED_HANDS_INFO)
        # if I > 0:
        #     current_senior = None

        def senior_player(player_no):
            global SENIOR_PLAYER, MOVE_STARTER, PLAYERS_ALLOWED, CURRENT_PLAYER
            SENIOR_PLAYER = [False, False, False, False]
            SENIOR_PLAYER[player_no-1] = True
            MOVE_STARTER = [False, False, False, False]
            MOVE_STARTER[player_no-1] = True
            PLAYERS_ALLOWED = [False, False, False, False]
            PLAYERS_ALLOWED[player_no-1] = True
            CURRENT_PLAYER = [False, False, False, False]
            CURRENT_PLAYER[player_no-1] = True

        def manage_score():
            global TEAM1_SCORE, TEAM2_SCORE, PREVIOUS_SENIOR
            no_of_moves = took_moves()
            if current_senior == 1 or current_senior == 3:
                TEAM1_SCORE += no_of_moves
                senior_player(current_senior)
            else:
                TEAM2_SCORE += no_of_moves
                senior_player(current_senior)
            PREVIOUS_SENIOR = 0

        if current_senior:
            if GAME_END:
                no_of_moves = took_moves()
                if current_senior == 1 or current_senior == 3:
                    TEAM1_SCORE += no_of_moves
                    senior_player(current_senior)
                else:
                    TEAM2_SCORE += no_of_moves
                    senior_player(current_senior)
                PREVIOUS_SENIOR = 0
            else:
                if current_senior == PREVIOUS_SENIOR:
                    manage_score()
                else:
                    PREVIOUS_SENIOR = current_senior
                    if current_senior == 1:
                        SENIOR_PLAYER = [True, False, False, False]
                        MOVE_STARTER = [True, False, False, False]
                        PLAYERS_ALLOWED = [True, False, False, False]
                        CURRENT_PLAYER = [True, False, False, False]
                    elif current_senior == 2:
                        SENIOR_PLAYER = [False, True, False, False]
                        MOVE_STARTER = [False, True, False, False]
                        PLAYERS_ALLOWED = [False, True, False, False]
                        CURRENT_PLAYER = [False, True, False, False]
                    elif current_senior == 3:
                        SENIOR_PLAYER = [False, False, True, False]
                        MOVE_STARTER = [False, False, True, False]
                        PLAYERS_ALLOWED = [False, False, True, False]
                        CURRENT_PLAYER = [False, False, True, False]
                    elif current_senior == 4:
                        SENIOR_PLAYER = [False, False, False, True]
                        MOVE_STARTER = [False, False, False, True]
                        PLAYERS_ALLOWED = [False, False, False, True]
                        CURRENT_PLAYER = [False, False, False, True]


    def manage_crowns(player_no, frame_rect):
        """Put crown on the profile of senior player."""
        if player_no < 3:
            crown_rect = crown_images[3].get_rect(center=frame_rect.topright)
            crown_img = pygame.transform.rotate(crown_images[3], 280)
            screen.blit(crown_img, crown_rect)
        elif player_no == 3:
            crown_rect = crown_images[3].get_rect(center=frame_rect.bottomright)
            crown_img = pygame.transform.rotate(crown_images[3], 190)
            screen.blit(crown_img, crown_rect)
        else:
            crown_rect = crown_images[3].get_rect(center=(frame_rect.bottomleft[0] - 5, frame_rect.bottomleft[1] - 5))
            crown_img = pygame.transform.rotate(crown_images[3], 110)
            screen.blit(crown_img, crown_rect)

    def find_senior(data_dict):
        global MOVE_NO, MOVE_STARTER, RUNG
        # Get the cards played in the current move
        cards = list(data_dict[MOVE_NO].values())
        if not cards:
            return None
        # Determine the basic suit from the first player's card
        basic_suit = data_dict[MOVE_NO][f"Player {MOVE_STARTER.index(True) + 1}"].split()[0]
        same_suit_cards = []
        diff_suit_cards = []
        for card in cards:
            suit, rank = card.split()
            if suit == basic_suit:
                same_suit_cards.append((suit, int(rank)))
            else:
                diff_suit_cards.append((suit, int(rank)))
        # If there are cards of the basic suit, find the highest rank among them
        if len(same_suit_cards) == 4:
            senior_card = max(same_suit_cards, key=lambda x: x[1])
        else:
            # If no cards of the basic suit, check for trump (RUNG) cards
            rung_cards = [card for card in diff_suit_cards if card[0] == RUNG]
            if rung_cards:
                senior_card = max(rung_cards, key=lambda x: x[1])
            else:
                # If no trump cards, find the highest rank among the different suit cards
                senior_card = max(same_suit_cards, key=lambda x: x[1])
        # Find the player number corresponding to the senior card
        senior_card_str = f"{senior_card[0]} {senior_card[1]}"
        for key, value in data_dict[MOVE_NO].items():
            if value == senior_card_str:
                return int(key.split()[1])
        return None

    def make_senior_move(cards):
        global RUNG, SENIOR_PLAYER
        card = random.choice(cards)
        card = max(cards, key=lambda x: x[1])
        return card

    def play_card(card):
        global RUNNING_SUIT, HAND, PLAYERS_PLAYED_CARDS, PLAYER_ONE_CARDS, PLAYERS_ALLOWED, CURRENT_PLAYER, \
            MOVE_STARTER, MOVE_NO, SENIOR_PLAYER
        if MOVE_NO == 0:
            MOVE_STARTER = [True, False, False, False]
        PLAYERS_PLAYED_CARDS[0].append(card)
        PLAYER_ONE_CARDS.remove(card)
        PLAYED_HANDS_INFO[MOVE_NO]["Player 1"] = card
        white_frame_bg()
        if MOVE_NO == 0 or SENIOR_PLAYER[0]:
            RUNNING_SUIT, _ = card.split(" ")
        HAND = 1
        PLAYERS_ALLOWED[1] = True
        CURRENT_PLAYER[1] = True

    def bot_hand(card):
        global RUNNING_SUIT
        card_suit, _ = card.split(" ")
        if card_suit.lower() == RUNNING_SUIT.lower():
            return card
        else:
            return 0

    def made_move(player_no):
        global PLAYERS_ALLOWED
        if player_no == 4:
            PLAYERS_ALLOWED[player_no - 1] = False
            PLAYERS_ALLOWED[player_no * 0] = True
            CURRENT_PLAYER[player_no - 1] = False
            CURRENT_PLAYER[player_no * 0] = True
        else:
            PLAYERS_ALLOWED[int(player_no) - 1] = False
            PLAYERS_ALLOWED[int(player_no)] = True
            CURRENT_PLAYER[int(player_no) - 1] = False
            CURRENT_PLAYER[int(player_no)] = True
        white_frame_bg()

    def player1_cards(cards):
        global LAST_PLAYED_TICKS, MOVE_NO, PLAYERS_PLAYED_CARDS, PLAYERS_LAST_PLAYED_TICKS, WIPE_CARDS_REQUEST, \
        RUNNING_SUIT, PLAYED_HANDS_INFO
        for _i, card in enumerate(cards):
            card_bg_green = False
            c_suit, c_rank = card.split(" ")
            img = card_images[card]
            m_x, m_y = pygame.mouse.get_pos()
            legal_cards_index = [cards.index(card) for card in cards if card.split()[0] == RUNNING_SUIT]
            if SENIOR_PLAYER[0]:
                manage_crowns(1, FRAME_RECTS[f"0"])
            if SENIOR_PLAYER[0] or RUNNING_SUIT not in [cd.split()[0] for cd in cards]:
                if PLAYER_ONE_CARDS_RECT[_i].collidepoint(m_x, m_y):
                    if pygame.mouse.get_pressed()[0]:
                        if PLAYERS_ALLOWED[0]:
                            play_card(card)
                            PLAYERS_ALLOWED[0] = False
                            CURRENT_PLAYER[0] = False
                            PLAYERS_LAST_PLAYED_TICKS[0] = pygame.time.get_ticks()
                            if MOVE_STARTER[1]:
                                manage_seniors()
                                MOVE_NO += 1
                                WIPE_CARDS_REQUEST = [True, False, False, False]
                                print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
            elif MOVE_NO != 0 and RUNNING_SUIT in [cd.split()[0] for cd in cards]:
                if _i in legal_cards_index:
                    if PLAYER_ONE_CARDS_RECT[_i].collidepoint(m_x, m_y):
                        if pygame.mouse.get_pressed()[0]:
                            if PLAYERS_ALLOWED[0]:
                                play_card(card)
                                PLAYERS_ALLOWED[0] = False
                                CURRENT_PLAYER[0] = False
                                PLAYERS_LAST_PLAYED_TICKS[0] = pygame.time.get_ticks()
                                if MOVE_STARTER[1]:
                                    manage_seniors()
                                    MOVE_NO += 1
                                    WIPE_CARDS_REQUEST = [True, False, False, False]
                                    print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
            if c_suit == RUNG:
                CARD_BACKGROUND.fill(RUNG_CARD_BG_COLOR)
                card_bg_green = True
            else:
                CARD_BACKGROUND.fill("white")
            blit_card(img, CARD_BACKGROUND, PLAYER_ONE_CARDS_RECT[_i])

            if card_bg_green:
                CARD_BACKGROUND.fill("white")
        for card in PLAYERS_PLAYED_CARDS[0]:
            blit_card(card_images[card], CARD_BACKGROUND, (462, 339))
        wipe_card_check(1)

    def player2_cards(cards):
        global MOVE_NO, PLAYERS_PLAYED_CARDS, WIPE_CARDS_REQUEST, WIPE_CARDS_DONE, PLAYERS_LAST_PLAYED_TICKS, \
            RUNNING_SUIT, wipe_cards_done_time
        for n, card in enumerate(cards):
            img = rotated_c_bg_img
            x, y = p2_xy[12 - n]
            if SENIOR_PLAYER[1]:
                manage_crowns(2, FRAME_RECTS[f"1"])

            if PLAYERS_ALLOWED[1]:
                if SENIOR_PLAYER[1]:
                    if WIPE_CARDS_DONE:
                            senior_card = make_senior_move(cards)
                            PLAYERS_PLAYED_CARDS[1].append(senior_card)
                            PLAYER_TWO_CARDS.remove(senior_card)
                            PLAYED_HANDS_INFO[MOVE_NO]["Player 2"] = senior_card
                            made_move(2)
                            RUNNING_SUIT = senior_card.split()[0]
                            PLAYERS_LAST_PLAYED_TICKS[1] = pygame.time.get_ticks()
                            WIPE_CARDS_DONE = False
                    if MOVE_STARTER[2]:
                        manage_seniors()
                        MOVE_NO += 1
                        WIPE_CARDS_REQUEST = [False, True, False, False]
                        print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
                else:
                    if HAND:
                        to_play = bot_hand(card)
                        if pygame.time.get_ticks() - PLAYERS_LAST_PLAYED_TICKS[0] >= 1800:
                            if to_play:
                                PLAYERS_PLAYED_CARDS[1].append(to_play)
                                PLAYER_TWO_CARDS.remove(to_play)
                                PLAYED_HANDS_INFO[MOVE_NO]["Player 2"] = to_play
                                made_move(2)
                                PLAYERS_LAST_PLAYED_TICKS[1] = pygame.time.get_ticks()
                                if MOVE_STARTER[2]:
                                    manage_seniors()
                                    MOVE_NO += 1
                                    WIPE_CARDS_REQUEST = [False, True, False, False]
                                    print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
                            elif n == (len(cards) - 1) and not to_play:
                                crd = cards[(random.randint(0, (len(cards) - 1)))]
                                PLAYERS_PLAYED_CARDS[1].append(crd)
                                PLAYER_TWO_CARDS.remove(crd)
                                PLAYED_HANDS_INFO[MOVE_NO]["Player 2"] = crd
                                made_move(2)
                                PLAYERS_LAST_PLAYED_TICKS[1] = pygame.time.get_ticks()
                                if MOVE_STARTER[2]:
                                    manage_seniors()
                                    MOVE_NO += 1
                                    WIPE_CARDS_REQUEST = [False, True, False, False]
                                    print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
            screen.blit(img, (x, y))
        for card in PLAYERS_PLAYED_CARDS[1]:
            front_img = pygame.transform.rotate(card_images[card], 270)
            blit_card(front_img, CARD_BACKGROUND_ROTATED, (355, 257))
        wipe_card_check(2)

    def player3_cards(cards):
        global MOVE_NO, PLAYERS_PLAYED_CARDS, WIPE_CARDS_REQUEST, WIPE_CARDS_DONE, PLAYERS_LAST_PLAYED_TICKS, \
            RUNNING_SUIT
        for _n, card in enumerate(cards):
            # img = card_images[card]
            img = card_bg_img
            x, y = p3_xy[12 - _n]
            if SENIOR_PLAYER[2]:
                manage_crowns(3, FRAME_RECTS[f"2"])

            if PLAYERS_ALLOWED[2]:
                if SENIOR_PLAYER[2]:
                    if WIPE_CARDS_DONE:
                        senior_card = make_senior_move(cards)
                        PLAYERS_PLAYED_CARDS[2].append(senior_card)
                        PLAYER_THREE_CARDS.remove(senior_card)
                        PLAYED_HANDS_INFO[MOVE_NO]["Player 3"] = senior_card
                        made_move(3)
                        RUNNING_SUIT = senior_card.split()[0]
                        PLAYERS_LAST_PLAYED_TICKS[2] = pygame.time.get_ticks()
                        WIPE_CARDS_DONE = False
                    if MOVE_STARTER[3]:
                        manage_seniors()
                        MOVE_NO += 1
                        WIPE_CARDS_REQUEST = [False, False, True, False]
                        print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
                else:
                    if HAND:
                        to_play = bot_hand(card)
                        if pygame.time.get_ticks() - PLAYERS_LAST_PLAYED_TICKS[1] >= 1800:
                            if to_play:
                                PLAYERS_PLAYED_CARDS[2].append(to_play)
                                PLAYER_THREE_CARDS.remove(to_play)
                                PLAYED_HANDS_INFO[MOVE_NO]["Player 3"] = to_play
                                made_move(3)
                                PLAYERS_LAST_PLAYED_TICKS[2] = pygame.time.get_ticks()
                                if MOVE_STARTER[3]:
                                    manage_seniors()
                                    MOVE_NO += 1
                                    WIPE_CARDS_REQUEST = [False, False, True, False]
                                    print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
                            elif _n == (len(cards) - 1) and not to_play:
                                crd = cards[(random.randint(0, (len(cards) - 1)))]
                                PLAYERS_PLAYED_CARDS[2].append(crd)
                                PLAYER_THREE_CARDS.remove(crd)
                                PLAYED_HANDS_INFO[MOVE_NO]["Player 3"] = crd
                                made_move(3)
                                PLAYERS_LAST_PLAYED_TICKS[2] = pygame.time.get_ticks()
                                if MOVE_STARTER[3]:
                                    manage_seniors()
                                    MOVE_NO += 1
                                    WIPE_CARDS_REQUEST = [False, False, True, False]
                                    print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
            screen.blit(img, (x, y))
        for card in PLAYERS_PLAYED_CARDS[2]:
            CARD_BACKGROUND.fill("white")
            blit_card(card_images[card], CARD_BACKGROUND, (462, 155))
        wipe_card_check(3)

    def player4_cards(cards):
        global MOVE_NO, PLAYERS_PLAYED_CARDS, WIPE_CARDS_REQUEST, WIPE_CARDS_DONE, PLAYERS_LAST_PLAYED_TICKS, \
            RUNNING_SUIT
        for _ind, card in enumerate(cards):
            # img = card_images[card]
            img = rotated_c_bg_img
            x, y = p4_xy[_ind]
            if SENIOR_PLAYER[3]:
                manage_crowns(4, FRAME_RECTS[f"3"])

            if PLAYERS_ALLOWED[3]:
                if SENIOR_PLAYER[3]:
                    if WIPE_CARDS_DONE:
                            senior_card = make_senior_move(cards)
                            PLAYERS_PLAYED_CARDS[3].append(senior_card)
                            PLAYER_FOUR_CARDS.remove(senior_card)
                            PLAYED_HANDS_INFO[MOVE_NO]["Player 4"] = senior_card
                            made_move(4)
                            RUNNING_SUIT = senior_card.split()[0]
                            PLAYERS_LAST_PLAYED_TICKS[3] = pygame.time.get_ticks()
                            WIPE_CARDS_DONE = False
                    if MOVE_STARTER[0]:
                        manage_seniors()
                        MOVE_NO += 1
                        WIPE_CARDS_REQUEST = [False, False, False, True]
                        print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
                else:
                    if HAND:
                        to_play = bot_hand(card)
                        if pygame.time.get_ticks() - PLAYERS_LAST_PLAYED_TICKS[2] >= 1800:
                            if to_play:
                                PLAYERS_PLAYED_CARDS[3].append(to_play)
                                PLAYER_FOUR_CARDS.remove(to_play)
                                PLAYED_HANDS_INFO[MOVE_NO]["Player 4"] = to_play
                                made_move(4)
                                PLAYERS_LAST_PLAYED_TICKS[3] = pygame.time.get_ticks()
                                if MOVE_STARTER[0]:
                                    manage_seniors()
                                    MOVE_NO += 1
                                    WIPE_CARDS_REQUEST = [False, False, False, True]
                                    print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)
                            elif _ind == (len(cards) - 1) and not to_play:
                                crd = cards[(random.randint(0, (len(cards) - 1)))]
                                PLAYERS_PLAYED_CARDS[3].append(crd)
                                PLAYER_FOUR_CARDS.remove(crd)
                                PLAYED_HANDS_INFO[MOVE_NO]["Player 4"] = crd
                                made_move(4)
                                PLAYERS_LAST_PLAYED_TICKS[3] = pygame.time.get_ticks()
                                if MOVE_STARTER[0]:
                                    manage_seniors()
                                    MOVE_NO += 1
                                    WIPE_CARDS_REQUEST = [False, False, False, True]
                                    print("PLAYERS PLAYED CARDS: ", PLAYERS_PLAYED_CARDS)

            screen.blit(img, (x, y))
        for card in PLAYERS_PLAYED_CARDS[3]:
            front_img = pygame.transform.rotate(card_images[card], 270)
            blit_card(front_img, CARD_BACKGROUND_ROTATED, (550, 257))
        wipe_card_check(4)

    def player_turn_manager(player_no):
        global FRAME_BACKGROUND_COLOR, FRAME_BACKGROUND
        if CURRENT_PLAYER[player_no - 1]:
            if pygame.time.get_ticks() % 1000 < 500:
                FRAME_BACKGROUND[str(player_no - 1)].fill("green")
            else:
                FRAME_BACKGROUND[str(player_no - 1)].fill("white")

    def display_cards():
        """Puts players' cards on screen"""
        player1_cards(PLAYER_ONE_CARDS)
        player2_cards(PLAYER_TWO_CARDS)
        player3_cards(PLAYER_THREE_CARDS)
        player4_cards(PLAYER_FOUR_CARDS)

    def scoreboards():
        """Show scoreboards on screen"""
        screen.blit(scoreboard_img, (SCORECARD_XY[0][0] + 1, SCORECARD_XY[0][1] + 2.5))
        screen.blit(scoreboard_img, (SCORECARD_XY[1][0] + 1, SCORECARD_XY[1][1] + 2.5))
        screen.blit(scoreboard_images["ScorePanel Removedbg"], SCORECARD_XY[0])
        screen.blit(scoreboard_images["ScorePanel Removedbg"], SCORECARD_XY[1])
        score1_text = text_font.render(f"{TEAM1_SCORE}", True, LIGHT_GREY)
        score2_text = text_font.render(f"{TEAM2_SCORE}", True, LIGHT_GREY)
        screen.blit(score1_text, (SCORECARD_XY[0][0] + 22, SCORECARD_XY[0][1] + 20))
        screen.blit(score2_text, (SCORECARD_XY[1][0] + 22, SCORECARD_XY[1][1] + 20))

    # Put players' cards on screen
    display_cards()

    # Put scoreboard on screen
    scoreboards()
    player_turn_manager(1)
    player_turn_manager(2)
    player_turn_manager(3)
    player_turn_manager(4)


def manage_avatars(player_no, avatar_no, x, y, rotate=False, r_angle=270):
    """Player's avatar manager"""
    global FRAME_RECTS, FRAME_BACKGROUND_COLOR
    # Frame
    f_bg = FRAME_BACKGROUND[str(player_no)]
    frame = frame_images[frame_names[3]]

    # Avatar
    avatar_img = avatar_images[avatar_names[avatar_no - 1]]
    if rotate:
        avatar_img = pygame.transform.rotate(avatar_img, r_angle)
        frame = pygame.transform.rotate(frame, r_angle)
    FRAME_RECTS[str(player_no)] = frame.get_rect()
    FRAME_RECTS[str(player_no)] = FRAME_RECTS[str(player_no)].move((x, y))
    avatar_rect = avatar_img.get_rect()
    avatar_rect = avatar_rect.move((x + 4), (y + 2))

    # Display frame and avatar
    screen.blits([(f_bg, FRAME_RECTS[str(player_no)]), (frame, FRAME_RECTS[str(player_no)]), (avatar_img, avatar_rect)])


def before_rung(sample_cards):
    """Manage game state when rung is not set"""
    global p1_xy, p2_xy, p3_xy, p4_xy, RUNG_SELECTION_SURFACE, RUNG
    for e, cards in enumerate(sample_cards):
        if e == 0:
            for no, card in enumerate(cards):
                img = card_images[card]
                blit_card(img, CARD_BACKGROUND, PLAYER_ONE_CARDS_RECT[no + 8])
        elif e == 1:
            for _no, card in enumerate(cards):
                img = rotated_c_bg_img
                x, y = p2_xy[12 - _no]
                screen.blit(img, (x, y))
        elif e == 2:
            for i_no, card in enumerate(cards):
                # img = card_images[card]
                img = card_bg_img
                x, y = p3_xy[12 - i_no]
                screen.blit(img, (x, y))
        else:
            for ind_no, card in enumerate(cards):
                # img = card_images[card]
                img = rotated_c_bg_img
                x, y = p4_xy[ind_no]
                screen.blit(img, (x, y))
    screen.blit(RUNG_SELECTION_SURFACE, (0, ((SCREEN_HEIGHT / 2) - 100)))
    m_x, m_y = pygame.mouse.get_pos()
    for _i, (_key, _suit) in enumerate(suit_images.items()):
        screen.blit(_suit, SUIT_RECTS[_i])
        if SUIT_RECTS[_i].collidepoint(m_x, m_y):
            if pygame.mouse.get_pressed()[0]:
                RUNG = _key


def blit_profiles():
    """Blit all players' profile"""
    # Player 1 Profile
    manage_avatars(0, avatar_no=3, x=int((13 * (CARD_WIDTH / 1.8)) + CARDS_PLACEMENT_X),
                   y=int(p1_xy[12][1] + 35))

    # Player 2 Profile
    manage_avatars(1, avatar_no=1, x=int((p2_xy[0][0] - 140) + (CARDS_PLACEMENT_X / 2 - 5)),
                   y=int((13 * (CARD_WIDTH / 1.8)) + CARDS_PLACEMENT_Y + (CARDS_PLACEMENT_Y / 4)),
                   rotate=True)

    # Player 3 Profile
    manage_avatars(2, avatar_no=5, x=int((13 * (CARD_WIDTH / 1.8)) + CARDS_PLACEMENT_X),
                   y=int(p3_xy[0][1] - 15), rotate=True, r_angle=180)

    # Player 4 Profile
    manage_avatars(3, avatar_no=4, x=int((p4_xy[0][0] + 30)),
                   y=int((13 * (CARD_WIDTH / 1.8)) + CARDS_PLACEMENT_Y + (CARDS_PLACEMENT_Y / 4)),
                   rotate=True, r_angle=90)


def main():
    """Main Function"""
    global PLAYER_ONE_CARDS, PLAYER_TWO_CARDS, PLAYER_THREE_CARDS, PLAYER_FOUR_CARDS
    PLAYER_ONE_CARDS, PLAYER_TWO_CARDS, PLAYER_THREE_CARDS, PLAYER_FOUR_CARDS = deal_cards()
    sample_cards = [
        sorted(random.sample(PLAYER_ONE_CARDS, 5)),
        sorted(random.sample(PLAYER_TWO_CARDS, 5)),
        sorted(random.sample(PLAYER_THREE_CARDS, 5)),
        sorted(random.sample(PLAYER_FOUR_CARDS, 5))
    ]
    while True:
        exit_game()
        is_game_end()
        restart_checker()
        # Put background image on screen
        screen.blit(screen_bg_img, screen_bg_rect)
        screen.blit(AUTHOR_TEXT, (300, SCREEN_HEIGHT // 2))
        blit_profiles()
        if game_on:
            if RUNG:
                start_game()
            else:
                before_rung(sample_cards)
        else:
            inactive_state()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
