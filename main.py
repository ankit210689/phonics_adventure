import pygame
import pyttsx3
import random

from data.letters import LETTERS


pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phonics Adventure")

clock = pygame.time.Clock()


# ==========================================
# TEXT TO SPEECH
# ==========================================

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 35)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# ==========================================
# COLORS
# ==========================================

WHITE = (255, 255, 255)
BLACK = (35, 35, 35)

BLUE = (70, 130, 200)
GREEN = (70, 180, 100)

PURPLE = (170, 120, 220)
YELLOW = (255, 210, 70)
ORANGE = (255, 160, 80)
NEXT_GREEN = (80, 190, 120)

LIGHT_BLUE = (235, 247, 255)
LIGHT_GREEN = (235, 252, 240)

LIGHT_RED = (255, 180, 180)
RED = (200, 60, 60)

DISABLED = (210, 210, 210)


# ==========================================
# FONTS
# ==========================================

title_font = pygame.font.Font(None, 60)
letter_font = pygame.font.Font(None, 180)
lowercase_font = pygame.font.Font(None, 110)
word_font = pygame.font.Font(None, 55)
button_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
emoji_font = pygame.font.Font(None, 100)


# ==========================================
# GAME VARIABLES
# ==========================================

current_index = 0
stars = 0
game_mode = "learn"
feedback = ""
choice_buttons = []
speak_new_letter_pending = False


# ==========================================
# LETTER FUNCTIONS
# ==========================================

def current_letter():
    return LETTERS[current_index]


def speak_letter():
    letter = current_letter()

    speak(
        f"Letter {letter['name']}. "
        f"Capital {letter['uppercase']}. "
        f"Small {letter['lowercase']}. "
        f"The sound is {letter['sound']}. "
        f"{letter['uppercase']} is for {letter['word']}."
    )


def speak_sound():
    letter = current_letter()

    if letter["uppercase"] == "A":
        speak("A sounds like Aaeh")
    else:
        speak(f"{letter['uppercase']} sounds like {letter['sound']}")


def speak_word():
    letter = current_letter()
    speak(letter["word"])


# ==========================================
# DRAW BUTTON
# ==========================================

def draw_button(rect, text, color):
    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        BLACK,
        rect,
        width=2,
        border_radius=18
    )

    text_surface = button_font.render(
        text,
        True,
        BLACK
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    screen.blit(text_surface, text_rect)


def draw_creator_credit():
    credit = small_font.render(
        "Created by Ankit Pandey | GitHub: ankit210689",
        True,
        BLACK
    )

    screen.blit(
        credit,
        credit.get_rect(center=(WIDTH // 2, HEIGHT - 18))
    )


# ==========================================
# LEARNING SCREEN
# ==========================================

def draw_learning_screen():
    screen.fill(LIGHT_BLUE)

    letter = current_letter()

    title = title_font.render(
        "Let's Learn Phonics!",
        True,
        BLUE
    )

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 45))
    )

    progress_text = small_font.render(
        f"Letter {current_index + 1} of {len(LETTERS)}",
        True,
        BLACK
    )

    screen.blit(
        progress_text,
        progress_text.get_rect(center=(WIDTH // 2, 90))
    )

    bar_width = 500
    bar_height = 18
    bar_x = (WIDTH - bar_width) // 2
    bar_y = 115

    pygame.draw.rect(
        screen,
        WHITE,
        (bar_x, bar_y, bar_width, bar_height),
        border_radius=10
    )

    progress_width = int(
        bar_width * (current_index + 1) / len(LETTERS)
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (bar_x, bar_y, progress_width, bar_height),
        border_radius=10
    )

    uppercase = letter_font.render(
        letter["uppercase"],
        True,
        BLUE
    )

    screen.blit(
        uppercase,
        uppercase.get_rect(center=(450, 265))
    )

    lowercase = lowercase_font.render(
        letter["lowercase"],
        True,
        GREEN
    )

    screen.blit(
        lowercase,
        lowercase.get_rect(center=(550, 265))
    )

    phonics_text = word_font.render(
        f"Sound: /{letter['phonics']}/",
        True,
        BLACK
    )

    screen.blit(
        phonics_text,
        phonics_text.get_rect(center=(WIDTH // 2, 370))
    )

    emoji_text = emoji_font.render(
        letter["emoji"],
        True,
        BLACK
    )

    screen.blit(
        emoji_text,
        emoji_text.get_rect(center=(WIDTH // 2, 425))
    )

    word_text = word_font.render(
        letter["word"],
        True,
        BLACK
    )

    screen.blit(
        word_text,
        word_text.get_rect(center=(WIDTH // 2, 500))
    )

    back_button = pygame.Rect(80, 555, 180, 65)
    sound_button = pygame.Rect(280, 555, 180, 65)
    word_button = pygame.Rect(480, 555, 180, 65)
    next_button = pygame.Rect(680, 555, 180, 65)

    draw_button(
        back_button,
        "Back",
        PURPLE if current_index > 0 else DISABLED
    )

    draw_button(sound_button, "Sound", YELLOW)
    draw_button(word_button, "Word", ORANGE)
    draw_button(next_button, "Next", NEXT_GREEN)
    draw_creator_credit()

    return (
        back_button,
        sound_button,
        word_button,
        next_button
    )


# ==========================================
# QUIZ
# ==========================================

def start_quiz():
    global game_mode
    global feedback
    global choice_buttons

    game_mode = "quiz"
    feedback = ""

    letter = current_letter()
    choices = letter["choices"].copy()
    random.shuffle(choices)

    choice_buttons = []
    y = 285

    for choice in choices:
        button = pygame.Rect(300, y, 400, 75)
        choice_buttons.append((button, choice))
        y += 95


def draw_quiz_screen():
    screen.fill(LIGHT_GREEN)

    letter = current_letter()

    title = title_font.render(
        "Find the Word!",
        True,
        GREEN
    )

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 60))
    )

    question = word_font.render(
        f"Which word starts with /{letter['phonics']}/?",
        True,
        BLACK
    )

    screen.blit(
        question,
        question.get_rect(center=(WIDTH // 2, 155))
    )

    big_letter = lowercase_font.render(
        letter["uppercase"] + " " + letter["lowercase"],
        True,
        BLUE
    )

    screen.blit(
        big_letter,
        big_letter.get_rect(center=(WIDTH // 2, 220))
    )

    for button, choice in choice_buttons:
        color = WHITE

        if feedback and choice == feedback:
            if choice == letter["answer"]:
                color = GREEN
            else:
                color = LIGHT_RED

        draw_button(button, choice, color)

    if feedback:
        if feedback == letter["answer"]:
            message = "Great job!"
            feedback_color = GREEN
        else:
            message = "Try again!"
            feedback_color = RED

        feedback_text = word_font.render(
            message,
            True,
            feedback_color
        )

        screen.blit(
            feedback_text,
            feedback_text.get_rect(center=(WIDTH // 2, 650))
        )

    draw_creator_credit()


# ==========================================
# COMPLETION SCREEN
# ==========================================

def draw_complete_screen():
    screen.fill(LIGHT_BLUE)

    title = title_font.render(
        "Amazing!",
        True,
        GREEN
    )

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 180))
    )

    message = word_font.render(
        "You finished the alphabet!",
        True,
        BLACK
    )

    screen.blit(
        message,
        message.get_rect(center=(WIDTH // 2, 270))
    )

    score = word_font.render(
        f"Stars: {stars}",
        True,
        BLACK
    )

    screen.blit(
        score,
        score.get_rect(center=(WIDTH // 2, 350))
    )

    play_button = pygame.Rect(350, 470, 300, 75)

    draw_button(
        play_button,
        "Play Again",
        YELLOW
    )
    draw_creator_credit()

    return play_button


# ==========================================
# MAIN LOOP
# ==========================================

running = True

back_button = None
sound_button = None
word_button = None
next_button = None
play_button = None

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = event.pos

            if game_mode == "learn":

                if (
                    back_button is not None
                    and back_button.collidepoint(mouse_position)
                    and current_index > 0
                ):
                    current_index -= 1
                    feedback = ""
                    speak_new_letter_pending = True

                elif (
                    sound_button is not None
                    and sound_button.collidepoint(mouse_position)
                ):
                    speak_sound()

                elif (
                    word_button is not None
                    and word_button.collidepoint(mouse_position)
                ):
                    speak_word()

                elif (
                    next_button is not None
                    and next_button.collidepoint(mouse_position)
                ):
                    start_quiz()

            elif game_mode == "quiz":

                for button, choice in choice_buttons:

                    if button.collidepoint(mouse_position):
                        letter = current_letter()

                        if choice == letter["answer"]:
                            feedback = choice
                            stars += 1

                            speak(
                                f"Great job! "
                                f"{choice} starts with "
                                f"{letter['uppercase']}."
                            )

                            if current_index < len(LETTERS) - 1:
                                current_index += 1
                                game_mode = "learn"
                                feedback = ""
                                speak_new_letter_pending = True
                            else:
                                game_mode = "complete"

                        else:
                            feedback = choice
                            speak("Try again.")

                        break

            elif game_mode == "complete":

                if (
                    play_button is not None
                    and play_button.collidepoint(mouse_position)
                ):
                    current_index = 0
                    stars = 0
                    feedback = ""
                    game_mode = "learn"

    # Draw the current screen inside the game loop

    if game_mode == "learn":
        (
            back_button,
            sound_button,
            word_button,
            next_button
        ) = draw_learning_screen()

        play_button = None

    elif game_mode == "quiz":
        draw_quiz_screen()

        back_button = None
        sound_button = None
        word_button = None
        next_button = None
        play_button = None

    elif game_mode == "complete":
        play_button = draw_complete_screen()

        back_button = None
        sound_button = None
        word_button = None
        next_button = None

    if game_mode != "complete":
        star_text = small_font.render(
            f"Stars: {stars}",
            True,
            BLACK
        )

        screen.blit(star_text, (25, 20))

    pygame.display.flip()

    if speak_new_letter_pending:
        speak_new_letter_pending = False
        speak_letter()

    clock.tick(60)


pygame.quit()