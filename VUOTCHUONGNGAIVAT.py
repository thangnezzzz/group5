import pygame
import os
import json
import random
from sys import exit

pygame.init()
pygame.mixer.init()

# Music
background_music = "sound/background.mp3"  # Đường dẫn đến nhạc nền
game_over_music = "sound/gameover.mp3"     # Đường dẫn đến nhạc game over
traffic_music="sound/traffic.mp3"
click_sound = pygame.mixer.Sound("sound/mouseclick.mp3")
level_music= pygame.mixer.Sound("sound/thangcap.mp3")
crash_sound= pygame.mixer.Sound("sound/crashsound.mp3")
heal_sound= pygame.mixer.Sound("sound/healsound.mp3")
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # -1 để phát lặp vô hạn
pygame.mixer.music.set_volume(0.5)
level_music.set_volume(3)
crash_sound.set_volume(0.2)
pygame.mixer.music.set_volume(0.21234)


# Size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 720


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY=(20,20,20)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW=(250,172,2)
PINK=(252,3,227)


# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GROUP 5")

#ICON
icon=pygame.image.load("image/xenen.png")
pygame.display.set_icon(icon)


LIVES=1
selected_car_index = 0  # Xe mặc định là xe đầu tiên


def display_level(level):
    font = pygame.font.Font(None, 240)
    for _ in range(10):  # Hiển thị nhấp nháy 6 lần
        level_text = font.render(f"LEVEL {level}", True, GREEN if _ % 2 == 0 else PINK)
        screen.blit(
            level_text,
            (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2.5 - level_text.get_height() // 2.5),
        )
        pygame.display.flip()
        pygame.time.delay(180)  # Chờ 300ms


def display_lives(lives):
    font_lives = pygame.font.Font("fonts/pixelfont.ttf", 35)
    lives_text = font_lives.render(f"x{lives}", True, GREEN)
    screen.blit(lives_text, (60,71))
   
# Heart class
class Heart:
    def __init__(self):
        self.image = pygame.image.load("image/heart.png")  # Hình trái tim
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# Car class
class Car:
    def __init__(self):
        global selected_car_index
        self.image = pygame.image.load(car_images[selected_car_index][0])
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 8.5
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
       
    def move_up(self):
        if self.y > 0:
            self.y -= self.speed


    def move_down(self):
        if self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
   
# Obstacle class
class Obstacle:
    def __init__(self):
        self.obstacle_images = [
            pygame.image.load("image/rocket1.png"),
            pygame.image.load("image/obstacle1.png"),
            pygame.image.load("image/trashcan.png"),
            pygame.image.load("image/obstacle3.png"),
            pygame.image.load("image/obstacle4.png"),
            pygame.image.load("image/bullet.png"),
            pygame.image.load("image/rock.png"),
            pygame.image.load("image/bomb.png")
        ]
   
        self.image = random.choice(self.obstacle_images)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0, 10+SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(5, 12)

    def update(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


car_images = [
    ("image/xe1.png", pygame.image.load("image/xe1.png")),  
    ("image/xe2.png", pygame.image.load("image/xe2.png")),  
    ("image/xe3.png", pygame.image.load("image/xe3.png")),  
    ("image/xe5.png", pygame.image.load("image/xe5.png")),
    ("image/xe6.png", pygame.image.load("image/xe6.png"))    
]
street_scroll = 0
def draw_street(scroll):
    background_img = pygame.image.load("image/thongdiep.png")
    screen.blit(background_img, (0, 600))
    lane_width = 100
    for i in range(8):  # 8 đường kẻ trong một lần cuộn
        # Vẽ các đường kẻ trắng và vàng
        pygame.draw.rect(screen, WHITE, (0, 0, 10, SCREEN_HEIGHT))  # Viền trắng bên trái
        pygame.draw.rect(screen, WHITE, (790, 0, 10, SCREEN_HEIGHT))  # Viền trắng bên phải

        # Các đường kẻ giữa là màu vàng
        offset = i * 150 + scroll
        pygame.draw.rect(screen, YELLOW, (100, offset % SCREEN_HEIGHT - 85, 20, 85))
        pygame.draw.rect(screen, YELLOW, (305, offset % SCREEN_HEIGHT - 85, 20, 85))
        pygame.draw.rect(screen, YELLOW, (505, offset % SCREEN_HEIGHT - 85, 20, 85))
        pygame.draw.rect(screen, YELLOW, (690, offset % SCREEN_HEIGHT - 85, 20, 85))

def save_high_score(score):
    data = {"high_score": score}
    with open("high_score.json", "w") as f:
        json.dump(data, f)

# Hàm để tải high_score từ tệp
def load_high_score():
    if os.path.exists("high_score.json"):
        with open("high_score.json", "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    return 0  # Nếu chưa có tệp, trả về 0

# Main game
def game():
    high_score = load_high_score()
    global street_scroll
    pygame.mixer.music.load(traffic_music)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # -1 để phát lặp vô hạn


    running = True
    clock = pygame.time.Clock()
    car = Car()
    obstacles = []
    hearts = []
    score = 0
    lives = LIVES
   
    #
    level = 1  # Bắt đầu từ level 1
    obstacle_speed_increment = 3  # Tăng tốc độ mỗi cấp độ
   


    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False

    # Load the image
    background_img = pygame.image.load("image/thongdiep.png")
    background_img = pygame.transform.scale(background_img, (800, 120))
    live_img = pygame.image.load("image/heart.png")
    live_img = pygame.transform.scale(live_img, (60-15, 50-15))
    while running:
        screen.fill(GRAY)
        # Draw the image at (0, 600)
        screen.blit(live_img,(15,80))
        # pygame.draw.rect(screen, WHITE, (0,700,800,20))
        draw_street(street_scroll)


        street_scroll += 6  # Tăng giá trị cuộn, 5 là tốc độ
        if street_scroll >= SCREEN_HEIGHT:
            street_scroll = 0  # Đặt lại khi cuộn hết màn hình
        background_img = pygame.image.load("image/thongdiep.png")
        background_img = pygame.transform.scale(background_img, (800, 120))
        screen.blit(background_img, (0, 600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car.move_left()
                    moving_left = True
                elif event.key == pygame.K_RIGHT:
                    car.move_right()
                    moving_right = True
                elif event.key == pygame.K_UP:
                    moving_up = True
                    car.move_up()
                elif event.key == pygame.K_DOWN:
                    moving_down = True
                    car.move_down()


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                elif event.key == pygame.K_RIGHT:
                    moving_right = False
                elif event.key == pygame.K_UP:
                    moving_up = False
                elif event.key == pygame.K_DOWN:
                    moving_down = False
           
        if moving_left:
                car.move_left()
        if moving_right:
                car.move_right()
        if moving_up:
                car.move_up()
        if moving_down:
                car.move_down()




        # Add new obstacles
        if random.randint(1, 37) == 1:
            new_obstacle = Obstacle()
            # Tăng tốc độ dựa trên cấp độ
            new_obstacle.speed += (level - 1) * obstacle_speed_increment
            obstacles.append(new_obstacle)

        if random.randint(1, 900) == 1:  # 1% cơ hội để trái tim xuất hiện
            new_heart = Heart()
            hearts.append(new_heart)


        # Update and draw obstacles
        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw()
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
                score += 1
                if high_score < score:
                    high_score = score

                 # Tăng cấp độ mỗi 10 điểm
                if score % 17 == 0:
                    level = min(level + 1, 100)  # Giới hạn cấp độ tối đa là 10
                    level_music.play()
                    display_level(level)
                   
            # Check for collision
            if (
                car.x < obstacle.x + obstacle.width
                and car.x + car.width > obstacle.x
                and car.y < obstacle.y + obstacle.height
                and car.y + car.height > obstacle.y
            ):
                lives -= 1  # Trừ một mạng
                crash_sound.play()
                obstacles.remove(obstacle)
               


                if lives <= 0:
                    save_high_score(high_score)
                    running = False
                else:
                    # Xe nhấp nháy khi bị va chạm
                    for _ in range(5):
                        car.draw()
                        pygame.display.flip()
                        pygame.time.delay(100)
                        pygame.draw.rect(screen, BLACK, (car.x, car.y, car.width, car.height))
                        pygame.display.flip()
                        pygame.time.delay(100)


        # Cập nhật và vẽ các heart
        for heart in hearts[:]:
            heart.update()
            heart.draw()
            if heart.y > SCREEN_HEIGHT:
                hearts.remove(heart)


            # Kiểm tra va chạm giữa xe và heart
            if (
                car.x < heart.x + heart.width
                and car.x + car.width > heart.x
                and car.y < heart.y + heart.height
                and car.y + car.height > heart.y
            ):
                lives += 1  # Thêm một mạng
                heal_sound.play()
                hearts.remove(heart)


        # Draw car
        car.draw()


        # Display score
        score_font=pygame.font.Font("fonts/pixelfont.ttf",35)
        font = pygame.font.Font(None, 40)
        score_text = score_font.render(f"SCORE: {score}", True, GREEN)
        level_text = score_font.render(f"LV: {level}", True, RED)
        screen.blit(score_text, (18, -1))
        screen.blit(level_text, (18, 35))
        high_score_font = pygame.font.Font("fonts/pixelfont.ttf", 35)
        high_score_text = high_score_font.render(f"{int(high_score)}:Record", True, GREEN)
        screen.blit(high_score_text, (605, -1))
        display_lives(lives)


        pygame.display.flip()
        clock.tick(60)
    game_over_screen(score,high_score)

def draw_image_button(image, x, y, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_img = pygame.image.load(image)
    button_rect = button_img.get_rect(topleft=(x, y))
    
    # Hiệu ứng lún khi bấm chuột
    if button_rect.collidepoint(mouse):  # Khi chuột trỏ vào nút
        if click[0]:  # Khi nhấn chuột trái
            screen.blit(button_img, (x, y + 5))  # Lún xuống 5px
            if action:
                action()
        else:
            screen.blit(button_img, (x, y))  # Trạng thái hover
    else:
        screen.blit(button_img, (x, y))  # Trạng thái bình thường

    return button_rect


def car_selection_menu():
    global selected_car_index
    selecting = True
    arrow_offset_left = 0  # Độ lún của mũi tên trái
    arrow_offset_right = 0  # Độ lún của mũi tên phải
    arrow_press_distance = 15  # Khoảng cách lún xuống
    arrow_frames = 5  # Số frame để hiệu ứng lún xuống diễn ra


    # Tải hình ảnh mũi tên và xe
    phai_img = pygame.image.load("image/phai.png")
    trai_img = pygame.image.load("image/trai.png")
    enter_img=pygame.image.load("image/enter.png")
    screen.blit(enter_img,(300,600))
    while selecting:
        # Vẽ nền và các phần tĩnh (chỉ cần vẽ một lần)
        screen.fill(BLACK)
        screen.blit(enter_img,(300,600))
        font = pygame.font.Font(None, 50)
        title_fonts = pygame.font.Font("fonts/pixelfont.ttf", 70)
        title_text = title_fonts.render("CHOOSE YOUR CAR", True, GREEN)
        instructions_text = font.render("Press                      to start", True, YELLOW)


        # Hiển thị tiêu đề và hướng dẫn
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT - 100))


        # Hiển thị xe hiện tại
        car_image = car_images[selected_car_index][1]
        car_image = pygame.transform.scale(car_image, (100, 200))  # Tỷ lệ xe
        screen.blit(car_image, (SCREEN_WIDTH // 2 - car_image.get_width() // 2, SCREEN_HEIGHT // 2 - 100))


        # Vẽ mũi tên với độ lún
        screen.blit(trai_img, (95, 310 + arrow_offset_left))
        screen.blit(phai_img, (600, 310 + arrow_offset_right))


        # Lắng nghe sự kiện bàn phím
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Chuyển sang xe trước đó và lún mũi tên trái
                    click_sound.play()
                    selected_car_index = (selected_car_index - 1) % len(car_images)
                    for frame in range(arrow_frames):
                        arrow_offset_left = arrow_press_distance // (frame + 1)
                        screen.fill(BLACK)
                        # Vẽ lại giao diện sau khi có hiệu ứng
                        screen.blit(enter_img,(300,600))
                        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
                        screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT - 100))
                        screen.blit(car_image, (SCREEN_WIDTH // 2 - car_image.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
                        screen.blit(trai_img, (95, 310 + arrow_offset_left))
                        screen.blit(phai_img, (600, 310 + arrow_offset_right))
                        pygame.display.flip()
                        pygame.time.delay(10)
                    arrow_offset_left = 0


                elif event.key == pygame.K_RIGHT:  
                    click_sound.play() #Âm thanh tiếng phím 
                    selected_car_index = (selected_car_index + 1) % len(car_images)
                    for frame in range(arrow_frames):
                        arrow_offset_right = arrow_press_distance // (frame + 1)
                        screen.fill(BLACK)
                        # Vẽ lại giao diện sau khi có hiệu ứng
                        screen.blit(enter_img,(300,600))
                        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
                        screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT - 100))
                        screen.blit(car_image, (SCREEN_WIDTH // 2 - car_image.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
                        screen.blit(trai_img, (95, 310 + arrow_offset_left))
                        screen.blit(phai_img, (600, 310 + arrow_offset_right))
                        pygame.display.flip()
                        pygame.time.delay(10)
                    arrow_offset_right = 0


                elif event.key == pygame.K_RETURN:  # Chọn xe và bắt đầu game
                    selecting = False


        pygame.display.flip()




def game_over_screen(score,high_score):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_over_music)
    pygame.mixer.music.set_volume(2.5)
    pygame.mixer.music.play()




    screen.fill(BLACK)
    font_large = pygame.font.Font("fonts/pixelfont.ttf", 120)
    font_small = pygame.font.Font(None, 36)


    # Hiển thị "Game Over"
    game_over_text = font_large.render("GAME OVER", True, RED)
    screen.blit(
        game_over_text,
        (
            SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - 200,
        ),
    )


    # Hiển thị điểm số
    score_text = font_small.render(f"Your Score: {score}", True, WHITE)
    high_score_text=font_small.render(f"Your High Score: {high_score}", True, WHITE)
    screen.blit(
        score_text,
        (
            SCREEN_WIDTH // 2 - score_text.get_width() // 2,
            SCREEN_HEIGHT // 2,
        ),
    )
    screen.blit(
        high_score_text,
        (
            SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + 50 ,
        ),
    )

    # Hướng dẫn tiếp tục
    continue_text = font_small.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
    screen.blit(
        continue_text,
        (
            SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + 100,
        ),
    )
    pygame.display.flip()


    # Vòng lặp chờ người chơi quyết định
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Nhấn 'R' để chơi lại
                    waiting = False
                    game()
                elif event.key == pygame.K_q:  # Nhấn 'Q' để thoát
                    pygame.quit()
                    exit()


    print(f"Game Over! Your score is {score}.")


def draw_button(text, x, y, width, height, normal_color, hover_color, text_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, normal_color, (x, y, width, height))


    font = pygame.font.Font(None, 40)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)


    return pygame.Rect(x, y, width, height)


def button_click_effect(button_rect, action):
    original_y = button_rect.y
    press_distance = 20
    frames = 5


    for i in range(frames):
        button_rect.y += press_distance / frames
        screen.fill(BLACK)
        # Vẽ lại các phần tử khác của menu ở đây
        pygame.draw.rect(screen, GREEN, button_rect)
        pygame.display.flip()
        pygame.time.delay(20)


    for i in range(frames):
        button_rect.y -= press_distance / frames
        screen.fill(BLACK)
        # Vẽ lại các phần tử khác của menu ở đây

        pygame.draw.rect(screen, GREEN, button_rect)
        pygame.display.flip()
        pygame.time.delay(20)


    button_rect.y = original_y
    action()


# Main menu function
def main_menu():
    menu_running = True
    
    
    

    while menu_running:
        duongpho_img = pygame.image.load("image/vuivui.png")
        duongpho_img = pygame.transform.scale(duongpho_img, (800,720))
        traffic_img = pygame.image.load("image/trafficlight.png")
        xenen_img = pygame.image.load("image/xenen.png")
        screen.fill(BLACK)
        screen.blit(duongpho_img,(0,0))
        # screen.blit(traffic_img, (70-10,550+1))
        # screen.blit(traffic_img, (630-10,550+1))
        font = pygame.font.Font("fonts/pixelfont.ttf", 73)
        title_text = font.render("GO THROUGH OBSTACLES", True, YELLOW)
        title_text1 = font.render("GO THROUGH OBSTACLES", True, BLACK)
        title_y = 100  # Đặt vị trí y của tiêu đề cao hơn
        screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2 + 2, title_y + 2))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 1.985, title_y))


        start_button = draw_image_button("image/startbutton.png", 300, 250, game)
        quit_button = draw_image_button("image/exitbutton.png", 300, 400, pygame.quit)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    button_click_effect(start_button, lambda: None)
                    pygame.time.delay(500)  # Chờ 1 giây
                    car_selection_menu()
                    game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if start_button.collidepoint(event.pos):
                        click_sound.play()
                        button_click_effect(start_button, lambda: None)
                        pygame.time.delay(500)  # Chờ 1 giây
                        car_selection_menu()
                        game()
                    elif quit_button.collidepoint(event.pos):
                        click_sound.play()
                        button_click_effect(quit_button, lambda: None)
                        pygame.time.delay(500)  # Chờ 1 giây
                        pygame.quit()
                        exit()


        pygame.display.flip()


    pygame.quit()




if __name__ == "__main__":
    main_menu()

