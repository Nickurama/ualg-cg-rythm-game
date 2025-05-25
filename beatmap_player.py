import random
import csv
from io import StringIO
import math
from note import Note
from core_ext.scene import Scene

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

    PERFECT_RANGE = 0.05
    GOOD_RANGE = 0.15
    OK_RANGE = 0.30

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

        self.last_time_ns = 0
        self.started = False
        self.start_time_ns = 0
        self.curr_note = 0
        self.score = 0.0
        self.combo = 0
        self.spawned_notes = []
        self.notes_remove_queue = []

        print("\n")

        print(f"total time: {self.total_time_s}s")
        print(f"speed: {self.speed_ms}ms")
        print(f"song file: {self.song_file}")

        print("\n")

        self.notes_data = []

        print(csv_data)
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

    def update(self, curr_time_ns, input_obj):
        if (not self.started):
            return

        elapsed_ms = int((curr_time_ns - self.start_time_ns) / 1000000)
        delta_t_ms = int((curr_time_ns - self.last_time_ns) / 1000000)
        curr_fps = 0
        if (delta_t_ms != 0):
            curr_fps = int(1000 / delta_t_ms)

        print(curr_fps)
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
                print(f"Spawning note on {note_pos} at {elapsed_ms}")
                self.spawn_note(note_pos, note_spawn_time_ms)
                self.curr_note += 1

    def spawn_note(self, note_pos, note_spawn_time_ms):
        texture_file = self.IMG_POOL[random.randint(0, len(self.IMG_POOL) - 1)]
        pos_x = 0
        if (note_pos == 0):
            pos_x = self.POSX_0
        elif (note_pos == 1):
            pos_x = self.POSX_1
        elif (note_pos == 2):
            pos_x = self.POSX_2
        elif (note_pos == 3):
            pos_x = self.POSX_3
        else:
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
                print(f"note reached end at {elapsed_ms}")
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
            print("despawning note")
        self.notes_remove_queue = []

    def check_end_condition(self):
        if (self.curr_note >= len(self.notes_data) and len(self.spawned_notes) == 0):
            print("beatmap has reached the end")
            self.started = False

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
                self.combo += 1
                self.score += self.SCORE_PERFECT * self.combo * self.COMBO_MULTIPLIER
                self.remove_note(note)
                print(f"combo: {self.combo}")
                print(f"score: {self.score}")
            elif note.is_within_range(self.POSY_PERFECT, self.GOOD_RANGE):
                self.combo += 1
                self.score += self.SCORE_GOOD * self.combo * self.COMBO_MULTIPLIER
                self.remove_note(note)
                print(f"combo: {self.combo}")
                print(f"score: {self.score}")
            elif note.is_within_range(self.POSY_PERFECT, self.OK_RANGE):
                self.remove_note(note)
                self.combo += 1
                self.score += self.SCORE_OK * self.combo * self.COMBO_MULTIPLIER
                print(f"combo: {self.combo}")
                print(f"score: {self.score}")
            # else:
            #     self.miss(note)
        

    def miss(self, note):
        if note.missed:
            return
        note.missed = True
        print("miss!")
        self.combo = 0

    def start(self, start_time_ns):
        self.start_time_ns = start_time_ns
        self.started = True
        self.last_time_ns = start_time_ns


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

