import pygame

try:
    class Player(pygame.sprite.Sprite):
        def __init__(self, pos, groups, obstacle_sprites):
            super().__init__(groups)
            self.image = pygame.image.load(f'graphics/test/down-stay.png')
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
            self.img = 'down-right'
            self.direction = pygame.math.Vector2()
            self.speed = 10

            #названия спрайтов состояний героя
            self.up = ['up-right', 'up-left']
            self.down = ['down-right', 'down-left']
            self.left = ['left-right', 'left-left']
            self.right = ['right-right', 'right-left']

            self.movettex = 0
            self.movettey = 0

            self.current_frame = 0

            #cut content man
            self.is_attack = False
            self.attack_cooldown = 500  # в миллисекундах

            self.obstacle_sprites = obstacle_sprites

        def input(self):
            #отвечает за принятие нажатых клавиш,
            # указание направления движения
            # и переключение спрайтов, соотвествующих с состоянию героя
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.movettey -= 1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                # self.timer = pygame.time.set_timer()
                self.movettey += 1
            else:
                self.direction.y = 0
                if self.movettey > 0:
                    self.img = 'down-stay'
                elif self.movettey < 0:
                    self.img = 'up-stay'
                self.movettey = 0
                self.current_frame = 0
                # self.img = 'down-stay'

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.movettex += 1
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.movettex -= 1
            else:
                self.direction.x = 0
                if self.movettex > 0:
                    self.img = 'right-stay'
                elif self.movettex < 0:
                    self.img = 'left-stay'
                self.movettex = 0
                self.current_frame = 0

            if self.movettey > 0 and (self.movettey % 5 == 0 or abs(self.movettey) == 1):
                self.img = self.down[(self.current_frame + self.movettey) % 2]

            elif self.movettey < 0 and (self.movettey % 5 == 0 or abs(self.movettey) == 1):
                self.img = self.up[-(self.current_frame - self.movettey) % 2]

            if self.movettex > 0 and (self.movettex % 5 == 0 or abs(self.movettex) == 1):
                self.img = self.right[(self.current_frame + self.movettex) % 2]

            elif self.movettex < 0 and (self.movettex % 5 == 0 or abs(self.movettex) == 1):
                self.img = self.left[-(self.current_frame - self.movettex) % 2]
            #плейсхолдер
            if keys[pygame.K_SPACE] and not self.is_attack:
                self.is_attack = True
                self.attack_time = pygame.time.get_ticks()
                print('attack')
            elif keys[pygame.K_LSHIFT] and not self.is_attack:
                self.is_attack = True
                print('magic')

        #отвечает за движение персонажа
        def move(self, speed):
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center

        #cut content man
        def get_cooldown(self):
            self.current_time = pygame.time.get_ticks()
            if self.is_attack:
                if self.current_time - self.attack_time >= self.attack_cooldown:
                    self.is_attack = False


        #проверка на коллизию с объектами
        def collision(self, direction):
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:  # движение вправо
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # движение влево
                            self.hitbox.left = sprite.hitbox.right

            if direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:  # движение вниз
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # движение вверх
                            self.hitbox.top = sprite.hitbox.bottom

        def update(self):
            self.input()
            self.move(self.speed)
            self.get_cooldown()

            self.image = pygame.image.load(f'graphics/test/{self.img}.png').convert_alpha()
except Exception as e:
    print(e.__repr__())
