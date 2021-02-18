import random

import arcade

# Miscare_Gravitatie
Speed = 12
Jump_Speed = 50
Gravitatie = 5

# Marime Fereatra
VIEWPORT_MARGIN = 66
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Marime Fereastra
TILE_WIDTH_HEIGH = 70
MAP_WIDTH = TILE_WIDTH_HEIGH * 50
MAP_HEIGHT = TILE_WIDTH_HEIGH * 17

# Definirea culorilor pentru stars
bg_star_color = arcade.make_transparent_color(arcade.color.WHITE, 95)
fg_star_colors = [arcade.color.WHITE, arcade.color.BABY_BLUE, arcade.color.AQUA, arcade.color.BUFF,
                  arcade.color.ALIZARIN_CRIMSON]


def create_starfield(shape_list, color=bg_star_color, random_color=False):
    for i in range(300):  # 200 darab csillag
        x = random.randint(-100, 5280)  # csillag x pozíciója 0-1280 között
        y = random.randint(0, 720)  # csillag y pozíciója 0-720 között
        w = random.randint(1, 3)  # csillag széllessége 1-3 pixel között
        h = random.randint(1, 3)  # csillag magassága 1-3 pixel között
        if random_color:  # Ha a random_color True,
            color = random.choice(fg_star_colors)  # akkor véletlenszerűen kiválasztunk egy színt a fg_star_colors-ból
        star = arcade.create_rectangle_filled(x, y, w, h, color)  # minden csillag egy kicsi négyszög lesz
        shape_list.append(star)  # Itt adjuk hozzá a ShapeElementList-hez az új csillagot.


def spatiu_miscare(x, _min, _max):
    return max(min(x, _max), _min)


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(center_x=100, center_y=200)
        self.textures = []

        self.textures.append(arcade.load_texture("caracter_sunete/robot.png"))
        self.textures.append(arcade.load_texture("caracter_sunete/robot.png", flipped_horizontally=True))
        self.texture = self.textures[0]

    def update_texture(self):
        if self.change_x > 0:
            self.texture = self.textures[0]
        elif self.change_x < 0:
            self.texture = self.textures[1]


class ZenGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.center_window()
        map = arcade.read_tmx("maps/map.tmx")
        self.platform = arcade.tilemap.process_layer(map, "platforma", use_spatial_hash=True)
        self.frum = arcade.tilemap.process_layer(map, "frum", use_spatial_hash=True)
        self.pct_int = arcade.tilemap.process_layer(map, "puncteinteractiune", use_spatial_hash=True)
        # Puncte
        self.viata_minus = arcade.tilemap.process_layer(map, "viataminus", use_spatial_hash=True)
        self.plus5puncte = arcade.tilemap.process_layer(map, "plus5puncte", use_spatial_hash=True)
        self.plus1punct = arcade.tilemap.process_layer(map, "plus1punct", use_spatial_hash=True)
        self.ladders = arcade.tilemap.process_layer(map, "scari", use_spatial_hash=True, )
        self.player = Player()
        self.miscare = arcade.PhysicsEnginePlatformer(self.player, self.platform, gravity_constant=Gravitatie,
                                                      ladders=self.ladders)
        self.sunet_saritura = arcade.load_sound("caracter_sunete/jump5.wav")
        self.view_left = 0
        self.view_bottom = 0
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        self.set_fullscreen(not self.fullscreen)
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        self.minus_viata = 10
        self.puncte_ecran = 0
        self.viata_minus_sunet = arcade.load_sound("caracter_sunete/hurt2.wav")
        self.plus_puncte_sunet = arcade.load_sound("caracter_sunete/coin1.wav")
        muzica_fundal = arcade.load_sound("caracter_sunete/funkyrobot.mp3")
        arcade.play_sound(muzica_fundal, 0.8)

        # Az első csillagmező, előtérben.
        self.fg_stars1 = arcade.ShapeElementList()
        create_starfield(self.fg_stars1, random_color=True)

        # Az második csillagmező, előtérben.
        self.fg_stars2 = arcade.ShapeElementList()
        self.fg_stars2.center_y = 720  # Ezt az ablak tetejére helyezzük.
        create_starfield(self.fg_stars2, random_color=True)

        # Az első csillagmező, háttérben.
        self.bg_stars1 = arcade.ShapeElementList()
        create_starfield(self.bg_stars1)

        # Az második csillagmező, háttérben.
        self.bg_stars2 = arcade.ShapeElementList()
        self.bg_stars2.center_y = 720  # Ezt az ablak tetejére helyezzük.
        create_starfield(self.bg_stars2)

        # Előtérben lévő csillagok mozgási sebessége.
        self.fg_star_speed = 100
        # Háttérben lévő csillagok mozgási sebessége.
        self.bg_star_speed = 60

    def move_stars(self, dt):
        # Minden frame-ben levonunk az előtérben lévő csillagmező y pozíziójából, 100 * dt értéket.
        self.fg_stars1.center_y -= self.fg_star_speed * dt
        self.fg_stars2.center_y -= self.fg_star_speed * dt

        # Minden frame-ben levonunk a háttérben lévő csillagmező y pozíziójából, 60 * dt értéket.
        self.bg_stars1.center_y -= self.bg_star_speed * dt
        self.bg_stars2.center_y -= self.bg_star_speed * dt

        # Ha bármelyik csillagmező y pozíciója kisseb mint -720, akkor a 720-as pozícióba (ablak teteje) helyezzük.
        if self.fg_stars1.center_y < -720:
            self.fg_stars1.center_y = 720
        if self.fg_stars2.center_y < -720:
            self.fg_stars2.center_y = 720
        if self.bg_stars1.center_y < -720:
            self.bg_stars1.center_y = 720
        if self.bg_stars2.center_y < -720:
            self.bg_stars2.center_y = 720

    def on_draw(self):
        arcade.start_render()
        self.platform.draw()
        self.pct_int.draw()
        self.viata_minus.draw()
        self.plus1punct.draw()
        self.plus5puncte.draw()
        self.ladders.draw()
        self.frum.draw()
        self.player.draw()
        arcade.draw_text(f"Viata: {self.minus_viata} ", arcade.get_viewport()[0] + 1180, arcade.get_viewport()[2] + 680,
                         arcade.color.RED, font_size=20)
        arcade.draw_text(f"Puncte: {self.puncte_ecran}", arcade.get_viewport()[0] + 10, arcade.get_viewport()[2] + 680,
                         arcade.color.YELLOW, font_size=20)
        

        # Csillag batch-ok megrajzolása.
        self.fg_stars1.draw()
        self.fg_stars2.draw()
        self.bg_stars1.draw()
        self.bg_stars2.draw()

    def on_update(self, delta_time: float):
        self.move_stars(delta_time)
        self.miscare.update()
        self.player.update_texture()
        self.player.center_x = spatiu_miscare(self.player.center_x, 30, MAP_WIDTH - TILE_WIDTH_HEIGH - 10)
        changed = False
        # Scroll stanga
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True
        # Scroll dreapta
        right_boundary = self.view_left + WINDOW_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll sus
        top_boundary = self.view_bottom + WINDOW_HEIGHT - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll jos
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)
        if changed:
            arcade.set_viewport(self.view_left,
                                WINDOW_WIDTH + self.view_left,
                                self.view_bottom,
                                WINDOW_HEIGHT + self.view_bottom)

        minus_viata = arcade.check_for_collision_with_list(self.player, self.viata_minus)
        for minus in minus_viata:
            minus.kill()
            self.minus_viata = self.minus_viata - 4
            arcade.play_sound(self.viata_minus_sunet, 0.6)

        plus5_puncte = arcade.check_for_collision_with_list(self.player, self.plus5puncte)
        for plus5 in plus5_puncte:
            plus5.kill()
            self.puncte_ecran += 5
            arcade.play_sound(self.plus_puncte_sunet, 0.6)

        plus1_punct = arcade.check_for_collision_with_list(self.player, self.plus1punct)
        for plus1 in plus1_punct:
            plus1.kill()
            self.puncte_ecran += 1
            arcade.play_sound(self.plus_puncte_sunet, 0.6)



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT:
            self.player.change_x = Speed
        if symbol == arcade.key.LEFT:
            self.player.change_x = -Speed
        if symbol == arcade.key.SPACE:
            if self.miscare.can_jump():
                self.player.change_y = Jump_Speed
                arcade.play_sound(self.sunet_saritura)
        if symbol == arcade.key.UP:
            if self.miscare.is_on_ladder():
                self.player.change_y = Speed
        if symbol == arcade.key.DOWN:
            if self.miscare.is_on_ladder():
                self.player.change_y = -Speed
        if symbol == arcade.key.ESCAPE:
            exit()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT or symbol == arcade.key.LEFT:
            self.player.change_x = 0
        if symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.player.change_y = 0


win = ZenGame(WINDOW_WIDTH, WINDOW_HEIGHT, "ZenGame")
arcade.run()
