from pygame import * #через звездочку не импортируем
'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
       #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height): # параметры которые нужно указывать при создании спрайта , тоесть изображение спрайта его координата икс и игрик скорость передвижения и тд
        super().__init__() #метод вызывающий наследование из класса родителя

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (wight, height)) # вместе 55,55 - параметры
        self.speed = player_speed #скорость плеера

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x #координата икс плеера
        self.rect.y = player_y #координата игрик плеера

    def reset(self): #отображение картинки на экране
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update_r(self): #передвижение с помощью клавиш для 1 платформы
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5: #если нажали стрелочку вверх и если координата y платформы > 5 то двигаем платформу 1 вверх
            self.rect.y -= self.speed 
        if keys[K_DOWN] and self.rect.y < win_height - 80: #если нажали стрелочку вниз и если y координата платформы меньше height экрана -80 то двигаем платформу 1 вверх
            self.rect.y += self.speed
    def update_l(self): #передвижение с помощью клавиш для 2 платформы
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5: #если нажали w то двигаем платформу 2 вверх
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed  #если нажали s и если y координата платформы меньше height экрана -80 то двигаем платформу 2 вверх

#Игровая сцена:
back = (200, 255, 255) # цвет фона (background)
win_width = 600 #размеры окна
win_height = 500
window = display.set_mode((win_width, win_height)) #создание окна
window.fill(back) #заливка окна

#флаги отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60 #кол-во фпс

#создания мяча и ракетки    
racket1 = Player('racket.png', 30, 200, 4, 50, 150) # создание спрайтов
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

font.init() #инициализация шрифтов
font = font.Font(None, 35) #создание шрифта
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0)) #присвоение текста 
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

speed_x = 3 #скорость изменения различных координат(x, y)
speed_y = 3

while game: #пока игра не закончена повторять цикл игры
    for e in event.get(): #если есть ивент то 
        if e.type == QUIT: #если ивент - попытка выхода
            game = False #закончить игру

    if finish != True: #пока игра не закончена
        window.fill(back) #заливка окна
        racket1.update_l() #заставляем ракетки подчиняться функции апдейт тоесть двигаться
        racket2.update_r()
        ball.rect.x += speed_x #говорим мячику двигаться
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball): #если мяч столкнулся с любой из 2 ракеток
            speed_x *= -1 #поменять направление его движения координате икс
            speed_y *= 1

        # если мяч достигает границ экрана меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        # если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True

        # если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True

        racket1.reset() #отрисовка всех спрайтов
        racket2.reset()
        ball.reset()

    display.update() #обновление сцены
    clock.tick(FPS) #ставим кол-во фпс
