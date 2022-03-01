import pygame

try:
    class Companion(pygame.sprite.Sprite):
        def __init__(self, pos, groups, obstacle_sprites):
            super().__init__(groups)
            self.image = pygame.image.load(f'graphics/test/companion.png')
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
            self.img = 'companion'
            self.direction = pygame.math.Vector2()
            self.speed = 10
            self.up = ['companion', 'companion']
            self.down = ['companion', 'companion']
            self.left = ['companion', 'companion']
            self.right = ['companion', 'companion']
            self.movettex = 0
            self.movettey = 0
            self.current_frame = 0
            self.is_attack = False
            self.attack_cooldown = 500  # в миллисекундах

            self.obstacle_sprites = obstacle_sprites

        def move(self, speed):
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center

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
            self.move(self.speed)

            self.image = pygame.image.load(f'graphics/test/{self.img}.png').convert_alpha()
except Exception as e:
    print(e.__repr__())
