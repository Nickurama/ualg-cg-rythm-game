import pygame
import random
import csv
from io import StringIO
import math
from note import Note
from core_ext.scene import Scene
from vfx import VFX

class BmPlayer:
    IMG_POOL = [
        "images/note1.png",
        "images/note2.png",
        "images/note3.png",
    ]

    SCORE_PERFECT = 300
    SCORE_GOOD = 100
    SCORE_OK = 50

    COMBO_MULTIPLIER = 0.1

    PERFECT_RANGE = 0.10
    GOOD_RANGE = 0.20
    OK_RANGE = 0.40

    MISS_SOUND_COMBO_THRESHOLD = 5
    SONG_VOLUME = 1.0
    HIT_SOUND_VOLUME = 0.15
    MISS_SOUND_VOLUME = 0.3

    VFX_WIDTH = 0.8
    VFX_HEIGHT = 1.3

    KEY_POS_0 = "d"
    KEY_POS_1 = "f"
    KEY_POS_2 = "j"
    KEY_POS_3 = "k"

    POSX_0 = -1.2
    POSX_1 = -0.4
    POSX_2 = 0.4
    POSX_3 = 1.2
    POSY_START = 2.1
    POSY_PERFECT = -1.3
    POSZ = 3.0
    RADIUS = 0.5
    RESOLUTION = 8
    DEFAULT_R = 1.0
    DEFAULT_G = 1.0
    DEFAULT_B = 1.0

    def __init__(self, beatmap: str, scene: Scene):
        self.scene = scene
        config, csv_data = BmPlayer.parse_beatmap(beatmap)

        self.total_time_s = int(config['total_time_s'])
        self.speed_ms = int(config['speed_ms'])
        self.song_file = config['song_file']
        self.hit_sound_file = config['hit_sound']
        self.miss_sound_file = config['miss_sound']

        pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=512)
        self.hit_sound = pygame.mixer.Sound(self.hit_sound_file)
        self.hit_sound.set_volume(self.HIT_SOUND_VOLUME)
        self.miss_sound = pygame.mixer.Sound(self.miss_sound_file)
        self.miss_sound.set_volume(self.MISS_SOUND_VOLUME)
        self.sfx_channel = pygame.mixer.Channel(0)

        self.vfx = VFX(self.VFX_WIDTH, self.VFX_HEIGHT, self.scene)

        self.last_time_ns = 0
        self.started = False
        self.start_time_ns = 0
        self.curr_note = 0
        self.score = 0.0
        self.combo = 0
        self.spawned_notes = []
        self.notes_remove_queue = []

        self.notes_data = []

        index = 0
        for row in csv_data:
            if (index == 0):
                index += 1
                continue
            index += 1
            time_m = int(row[0])
            time_s = int(row[1])
            time_ms = int(row[2])
            pos = int(row[3])

            total_ms = time_m * 60 * 1000 + time_s * 1000 + time_ms
            self.notes_data.append([total_ms, pos])

        print("\n")

        print(F"beatmap loaded.")
        print(f"total time: {self.total_time_s}s")
        print(f"speed: {self.speed_ms}ms")
        print(f"song file: {self.song_file}")

        print("\n")


    def update(self, curr_time_ns, delta_t_ms, input_obj):
        self.vfx.update(delta_t_ms)
        if (not self.started):
            return

        elapsed_ms = int((curr_time_ns - self.start_time_ns) / 1000000)

        self.capture_input(input_obj)
        self.spawn_notes(elapsed_ms)
        self.update_notes(elapsed_ms)
        self.remove_notes()
        self.check_end_condition()

        self.last_time_ns = curr_time_ns

    def spawn_notes(self, elapsed_ms):
        if (self.curr_note < len(self.notes_data)):
            note = self.notes_data[self.curr_note]
            note_ms = note[0]
            note_pos = note[1]
            note_spawn_time_ms = note_ms - self.speed_ms
            if (note_spawn_time_ms < elapsed_ms):
                # print(f"spawning note on {note_pos} at {elapsed_ms}")
                self.spawn_note(note_pos, note_spawn_time_ms)
                self.curr_note += 1

    def spawn_note(self, note_pos, note_spawn_time_ms):
        texture_file = self.IMG_POOL[random.randint(0, len(self.IMG_POOL) - 1)]
        pos_x = self.lane_to_coords(note_pos)
        if pos_x == None:
            print(f"Invalid note position! ({note_pos})")
            return

        note = Note(x=pos_x,
                    y=self.POSY_START,
                    z=self.POSZ,
                    radius=self.RADIUS,
                    res=self.RESOLUTION,
                    texture=texture_file,
                    r=self.DEFAULT_R,
                    g=self.DEFAULT_G,
                    b=self.DEFAULT_B,
                    spawn_time=note_spawn_time_ms,
                    lane=note_pos)

        self.spawned_notes.append(note)
        self.scene.add(note)

    def lane_to_coords(self, lane):
        pos_x = 0.0
        if (lane == 0):
            pos_x = self.POSX_0
        elif (lane == 1):
            pos_x = self.POSX_1
        elif (lane == 2):
            pos_x = self.POSX_2
        elif (lane == 3):
            pos_x = self.POSX_3
        else:
            print(f"Invalid note position! ({lane})")
            return None

        return pos_x



    def update_notes(self, elapsed_ms):
        for nnote in self.spawned_notes:
            note: Note = nnote
            elapsed_since_spawn_ms = elapsed_ms - note.spawn_time
            target_y_ratio = elapsed_since_spawn_ms / self.speed_ms
            start_y = self.POSY_START
            end_y = self.POSY_PERFECT
            total_travel = abs(end_y - start_y)
            target_y = start_y - total_travel * target_y_ratio
            if (target_y_ratio > 1.0 and not note.has_reached_perfect_line):
                # print(f"note reached end at {elapsed_ms}")
                note.has_reached_perfect_line = True
            if note.is_below_range(self.POSY_PERFECT, self.OK_RANGE):
                self.miss(note)
            if (target_y_ratio > 1.3):
                self.remove_note(note)
            note.set_position([note.local_position[0], target_y, note.local_position[2]]);

    def remove_note(self, note: Note):
        self.notes_remove_queue.append(note)

    def remove_notes(self):
        for nnote in self.notes_remove_queue:
            note: Note = nnote
            self.spawned_notes.remove(note)
            self.scene.remove(note)
            # print("despawning note")
        self.notes_remove_queue = []

    def check_end_condition(self):
        if (self.curr_note >= len(self.notes_data) and len(self.spawned_notes) == 0):
            print("beatmap has reached the end")
            self.started = False
            self.stop_song()
            # self.vfx.remove_all()

    def capture_input(self, input_obj):
        input_obj = input_obj
        is_pressing_key = False
        key_0 = False
        key_1 = False
        key_2 = False
        key_3 = False
        if (input_obj.is_key_down(self.KEY_POS_0)):
            key_0 = True
            is_pressing_key = True
        if (input_obj.is_key_down(self.KEY_POS_1)):
            key_1 = True
            is_pressing_key = True
        if (input_obj.is_key_down(self.KEY_POS_2)):
            key_2 = True
            is_pressing_key = True
        if (input_obj.is_key_down(self.KEY_POS_3)):
            key_3 = True
            is_pressing_key = True

        if (not is_pressing_key):
            return

        for nnote in self.spawned_notes:
            note: Note = nnote
            has_corresponding_key_pressed = False
            if note.lane == 0 and key_0:
                has_corresponding_key_pressed = True
            elif note.lane == 1 and key_1:
                has_corresponding_key_pressed = True
            elif note.lane == 2 and key_2:
                has_corresponding_key_pressed = True
            elif note.lane == 3 and key_3:
                has_corresponding_key_pressed = True

            if not has_corresponding_key_pressed:
                continue

            if note.is_within_range(self.POSY_PERFECT, self.PERFECT_RANGE):
                self.remove_note(note)
                self.score += self.calc_score(self.SCORE_PERFECT, self.combo)
                self.combo += 1
                self.play_hit_sound()
                self.vfx.create_perfect_vfx(self.lane_to_coords(note.lane), self.POSY_PERFECT + self.vfx.height / 2)
            elif note.is_within_range(self.POSY_PERFECT, self.GOOD_RANGE):
                self.remove_note(note)
                self.score += self.calc_score(self.SCORE_GOOD, self.combo)
                self.combo += 1
                self.play_hit_sound()
                self.vfx.create_good_vfx(self.lane_to_coords(note.lane), self.POSY_PERFECT + self.vfx.height / 2)
            elif note.is_within_range(self.POSY_PERFECT, self.OK_RANGE):
                self.remove_note(note)
                self.score += self.calc_score(self.SCORE_OK, self.combo)
                self.combo += 1
                self.play_hit_sound()
                self.vfx.create_ok_vfx(self.lane_to_coords(note.lane), self.POSY_PERFECT + self.vfx.height / 2)

    def calc_score(self, hit_score, combo):
        return hit_score + hit_score * combo * self.COMBO_MULTIPLIER
        

    def miss(self, note: Note):
        if note.missed:
            return
        note.missed = True
        # print("miss!")
        self.vfx.create_miss_vfx(self.lane_to_coords(note.lane), self.POSY_PERFECT + self.vfx.height / 2)
        if self.combo > self.MISS_SOUND_COMBO_THRESHOLD:
            self.play_miss_sound()
        self.combo = 0

    def play_hit_sound(self):
        self.sfx_channel.play(self.hit_sound)

    def play_miss_sound(self):
        self.sfx_channel.play(self.miss_sound)

    def start(self, start_time_ns):
        self.start_time_ns = start_time_ns
        self.started = True
        self.last_time_ns = start_time_ns

        self.curr_note = 0
        self.score = 0.0
        self.combo = 0
        self.spawned_notes = []
        self.notes_remove_queue = []
        self.start_song()

    def start_song(self):
        pygame.mixer.music.load(self.song_file)
        pygame.mixer.music.set_volume(self.SONG_VOLUME)
        pygame.mixer.music.play()

    def stop_song(self):
        pygame.mixer.music.stop()

    @staticmethod
    def parse_beatmap(file_path: str):
        config = {}
        csv_lines = []

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if ':' in line: # key-value pair
                    key, value = line.split(':', 1)
                    config[key.strip()] = value.strip().strip('"')
                else:
                    csv_lines.append(line)
                    break
            csv_lines.extend(line.strip() for line in file.readlines())

        csv_data = list(csv.reader(StringIO('\n'.join(csv_lines))))

        return config, csv_data

