import array
import pyautogui
import time
import operator
import wx
import numpy
import random
import queue
from multiprocessing.dummy import Pool as ThreadPool

BACKGROUND = (4, 6, 6)
GREEN = ((136, 203, 35), 9000, 12000)
BLUE = ((18, 117, 163), 9000, 12000)
FLAME = ((255, 150, 0), 20, 30)
BOX = ((43, 43, 43), 10, 16)
TEXT = ((42, 42, 42), 8, 250)

TEXTS = {
    'Y aqui': ((235, 238), (35200, 36000)),
    'Mira': ((33, 36), (14000, 15850)),
    'Ella': ((25, 28), (10200, 11500)),
    'es': ((16, 19), (2000, 2800)),
    'mi': ((17, 20), (3000, 3690)),
    'abuela': ((45, 48), (27000, 28500)),
}

PAIRS = {
    'el_abuelo_de_carmen': ((135, 138), (105000, 110000), (12000, 30000)),
    'carmens_grandfather': ((143, 146), (120000, 125000), (10000, 40000)),
    'que_inteligente': ((98, 101), (86000, 90000), (10000, 35000)),
    'how_intelligent': ((97, 100), (83000, 85000), (10000, 15000)),
    'su_abuelo': ((64, 67), (45800, 47200), (200, 1000)),
    'her_grandfather': ((105, 108), (88000, 92000), (-5000, -3500)),
    'interesante': ((75, 78), (59500, 61500), (5000, 6000)),
    'interesting': ((71, 74), (55700, 57300), (10000, 17000)),
    'no_habla': ((58, 61), (43600, 45000), (9000, 12500)),
    'he_doesnt_talk': ((96, 99), (74000, 76000), (5000, 8000)),
    'abuelo': ((45, 48), (34000, 35500), (9000, 15000)),
    'grandfather': ((78, 81), (68000, 70000), (600, 1600)),
    'familia': ((45, 48), (32300, 33500), (-4000, 4000)),
    'family': ((40, 43), (28000, 29000), (-2000, -1000)),
    'carros': ((43, 46), (25300, 26300), (3500, 5500)),
    'cars': ((29, 32), (13600, 14400), (400, 1000)),
    'bonita': ((41, 44), (27500, 28800), (-6000, -2000)),
    'pretty': ((39, 42), (26200, 27100), (-4000, -3000)),
    'tengo': ((39, 42), (27500, 29200), (1800, 10000)),
    'i_have': ((39, 42), (22000, 23000), (2800, 4000)),
    'museo': ((44, 47), (28500, 30500), (3500, 6000)),
    'museum': ((57, 60), (39000, 41000), (3000, 6000)),
    'ella': ((25, 28), (13400, 14000), (2200, 5000)),
    'she': ((23, 26), (9500, 10500), (200, 800)),
    'guau': ((34, 47), (20000, 20700), (3200, 4500)),
    'wow': ((30, 33), (16300, 17000), (-400, 0)),
    'solo': ((29, 32), (16500, 18500), (3500, 5500)),
    'just': ((24, 27), (10600, 12100), (-2500, 1000)),
    'foto': ((25, 28), (12300, 13200), (-400, -300)),
    'picture': ((46, 49), (29800, 31200), (6000, 7500)),
    'hay': ((25, 28), (12600, 13200), (1600, 2000)),
    'there_are': ((60, 63), (41000, 42000), (4000, 6000)),
    'muy': ((28, 31), (14300, 15000), (1300, 2000)),
    'very': ((29, 32), (14500, 15100), (-100, 300)),
    'del': ((20, 23), (9500, 10500), (100, 900)),
    'from_the': ((56, 59), (37000, 39000), (-6000, -3000)),
    'es': ((15, 18), (2200, 2800), (-200, 200)),
    'it_is': ((23, 26), (9250, 9400), (100, 400)),
    'un': ((17, 20), (3600, 4100), (-200, 200)),
    'a': ((8, 11), (0, 200), (-300, 300)),
    'si': ((14, 17), (800, 1050), (-300, 300)),
    'yes': ((23, 26), (9800, 10550), (-1000, -300)),
}


PAIRSV = {
    'abuela': (44, [8426, 12460, 11128, 10786], [135, 927, 943, 2311, 6348, 4052, 4276, 6331, 4419, 5379, 7221, 458, 0, 0, 0]),
    'abuelo': (46, [10244, 12835, 11527, 11814], [205, 1489, 1640, 2822, 6111, 5155, 5115, 6055, 5174, 5703, 6599, 352, 0, 0, 0]),
    'and_here': (58, [12355, 12553, 16061, 12700], [124, 941, 956, 3065, 9176, 6231, 5895, 7668, 5264, 6494, 7485, 370, 0, 0, 0]),
    'and': (22, [5313, 5673, 4315, 5026], [0, 0, 0, 934, 3641, 2342, 2023, 2802, 2368, 2726, 3315, 176, 0, 0, 0]),
    'carmens_grandfather': (144, [32338, 28544, 37604, 36727], [575, 3674, 3398, 7796, 23111, 14191, 13682, 17318, 13454, 16189, 18427, 1261, 1202, 935, 0]),
    'carros': (42, [8378, 9246, 8496, 9888], [0, 0, 0, 1818, 7385, 3941, 3604, 4824, 3560, 4618, 5875, 383, 0, 0, 0]),
    'cars': (28, [4913, 5809, 7128, 5637], [0, 0, 0, 1226, 4647, 2509, 2303, 3247, 2052, 3104, 4108, 291, 0, 0, 0]),
    'de': (16, [2877, 5643, 4022, 4550], [61, 491, 508, 1077, 2627, 1937, 1851, 2347, 1401, 2065, 2549, 178, 0, 0, 0]),
    'del': (18, [4181, 5354, 5606, 3491], [72, 563, 577, 1154, 2731, 2234, 2100, 2573, 1528, 2308, 2616, 176, 0, 0, 0]),
    'el_abuelo_de_carmen': (134, [31871, 29602, 30973, 30103], [907, 4881, 3445, 6692, 17907, 13813, 13117, 15567, 11783, 14951, 18577, 909, 0, 0, 0]),
    'el': (12, [897, 3770, 3183, 4454], [72, 440, 447, 759, 1628, 1453, 1490, 1997, 894, 1466, 1561, 97, 0, 0, 0]),
    'ella': (24, [6583, 6235, 6818, 5880], [472, 2673, 1452, 1787, 2604, 2732, 2347, 2576, 2136, 2478, 4162, 97, 0, 0, 0]),
    'esta': (26, [6981, 5071, 7728, 5852], [196, 677, 782, 1509, 4390, 2109, 2387, 4087, 1971, 3037, 4187, 300, 0, 0, 0]),
    'familia': (44, [9948, 11143, 12171, 10803], [298, 2413, 1318, 2421, 7391, 4381, 4159, 5703, 4838, 5022, 5927, 194, 0, 0, 0]),
    'family': (40, [8968, 9495, 10505, 11403], [228, 1823, 1161, 2090, 6238, 4225, 4039, 4892, 4546, 4533, 4941, 531, 651, 473, 0]),
    'foto': (24, [5456, 6578, 6587, 5494], [88, 1053, 954, 1710, 4320, 2673, 2346, 2348, 2370, 2839, 3238, 176, 0, 0, 0]),
    'fotos': (32, [8006, 8677, 7443, 7904], [88, 1047, 957, 2026, 5633, 3484, 3398, 3777, 2990, 3805, 4543, 282, 0, 0, 0]),
    'from_the': (56, [10907, 14399, 9316, 15159], [151, 1502, 1343, 3277, 9575, 5832, 5381, 5857, 5065, 5593, 6020, 185, 0, 0, 0]),
    'grandfather': (78, [19269, 20451, 21126, 17999], [212, 1925, 1893, 4755, 13704, 7960, 7873, 9852, 7968, 9102, 10650, 813, 1203, 935, 0]),
    'grandmother': (86, [21984, 21483, 21359, 21033], [124, 1172, 1440, 4704, 14887, 10237, 9275, 10465, 9061, 10360, 11148, 810, 1221, 955, 0]),
    'hay': (24, [4930, 5964, 6703, 6201], [126, 925, 943, 1348, 2633, 2857, 2585, 2889, 2527, 2505, 2802, 526, 655, 477, 0]),
    'he_doesnt_talk': (96, [19295, 24579, 18354, 27011], [311, 2789, 3268, 5758, 13876, 9650, 9659, 11944, 8614, 10539, 12267, 564, 0, 0, 0]),
    'how_interesting': (102, [24483, 20477, 25279, 27678], [203, 2126, 1785, 4666, 16124, 11728, 11467, 12904, 10055, 11681, 12360, 713, 1158, 947, 0]),
    'i_have': (38, [5080, 9577, 10142, 8800], [124, 937, 956, 1989, 5151, 3644, 3704, 4948, 3748, 3920, 4284, 194, 0, 0, 0]),
    'interesante': (74, [17281, 17427, 16756, 19413], [72, 1024, 1170, 3734, 12558, 7636, 8049, 10655, 6676, 8456, 10353, 494, 0, 0, 0]),
    'interesting': (70, [16906, 15965, 16944, 20240], [142, 1561, 1298, 3423, 11959, 7811, 7921, 9184, 6514, 8281, 9345, 553, 1108, 955, 0]),
    'is': (10, [1061, 3334, 2171, 2098], [70, 577, 165, 332, 1298, 955, 1191, 1192, 508, 929, 1350, 97, 0, 0, 0]),
    'just': (24, [5456, 6833, 4554, 7076], [72, 728, 677, 1042, 3336, 2286, 2456, 2950, 2281, 2882, 3495, 642, 623, 449, 0]),
    'looks_at': (50, [12565, 13724, 8825, 12652], [135, 1129, 1391, 2739, 7048, 4960, 5068, 6545, 5320, 6027, 7023, 381, 0, 0, 0]),
    'mi': (16, [2281, 3547, 2990, 3812], [9, 162, 9, 593, 2623, 1835, 1521, 1492, 1492, 1492, 1402, 0, 0, 0, 0]),
    'mira': (30, [5828, 5741, 8435, 6070], [70, 564, 173, 1284, 5388, 3052, 2677, 3437, 2975, 3033, 3324, 97, 0, 0, 0]),
    'mujer': (38, [8192, 7287, 12266, 8405], [72, 530, 180, 1289, 5888, 4559, 4271, 4736, 3707, 4384, 4798, 632, 644, 460, 0]),
    'museo': (44, [8638, 9956, 10534, 11354], [0, 0, 0, 1643, 7043, 4986, 4881, 5834, 4084, 5397, 6233, 381, 0, 0, 0]),
    'museum': (56, [11525, 13767, 11936, 14065], [0, 0, 0, 2055, 9217, 6474, 6165, 7069, 5433, 6783, 7720, 377, 0, 0, 0]),
    'muy': (28, [5828, 5741, 7137, 7134], [0, 0, 0, 816, 4073, 3464, 3171, 3140, 3143, 3174, 3213, 522, 651, 473, 0]),
    'my': (18, [3956, 3989, 3624, 5131], [0, 0, 0, 656, 2943, 2164, 1891, 1911, 1974, 1863, 1737, 429, 655, 477, 0]),
    'no_habla': (56, [15940, 11471, 15045, 14260], [331, 2413, 2560, 4221, 8308, 5595, 5593, 7172, 6170, 6375, 7615, 363, 0, 0, 0]),
    'no_hay': (44, [12052, 7582, 10070, 12485], [196, 1483, 1616, 2724, 5782, 4431, 4440, 5260, 4747, 4777, 4984, 643, 635, 471, 0]),
    'of': (12, [700, 3433, 3469, 2689], [0, 194, 244, 584, 1668, 1274, 1172, 1187, 1175, 1339, 1366, 88, 0, 0, 0]),
    'one': (22, [4728, 5153, 5158, 5133], [0, 0, 0, 895, 3508, 2443, 2486, 2964, 2351, 2519, 2821, 185, 0, 0, 0]),
    'pasado': (46, [11510, 11324, 11178, 11997], [63, 438, 447, 2313, 7432, 4233, 4305, 6316, 4842, 5880, 7830, 1046, 496, 368, 0]),
    'past': (26, [8535, 4945, 7280, 5790], [0, 130, 224, 1248, 4403, 2389, 2501, 3701, 2659, 3363, 4288, 780, 496, 368, 0]),
    'picture': (44, [13132, 10202, 9125, 10538], [70, 813, 680, 1982, 7334, 5045, 4360, 4879, 4223, 5515, 6481, 801, 447, 367, 0]),
    'pictures': (52, [13344, 11770, 10928, 12935], [72, 752, 629, 2254, 8343, 5684, 5435, 6049, 4284, 6042, 7712, 905, 447, 369, 0]),
    'que_interesante': (102, [28434, 21244, 22665, 25672], [641, 2857, 2702, 5085, 15279, 10203, 10746, 13921, 9485, 11801, 14334, 961, 0, 0, 0]),
    'she': (22, [5816, 6152, 4234, 6280], [61, 503, 508, 1388, 3863, 2289, 2462, 3431, 1922, 2592, 3260, 203, 0, 0, 0]),
    'solo': (28, [7464, 6502, 8115, 6857], [438, 1873, 1290, 1543, 3426, 3626, 3095, 2538, 2554, 3889, 4384, 282, 0, 0, 0]),
    'tengo': (38, [9688, 8468, 11371, 10177], [382, 1988, 496, 1750, 5734, 4522, 4187, 4555, 3593, 4746, 4926, 688, 1202, 935, 0]),
    'the': (20, [5195, 5338, 3930, 6108], [63, 691, 944, 1598, 3505, 2205, 2147, 2635, 1893, 2179, 2614, 97, 0, 0, 0]),
    'there_are': (58, [15868, 12693, 11181, 12898], [63, 753, 944, 3142, 9696, 5590, 5872, 8039, 4667, 5990, 7496, 388, 0, 0, 0]),
    'there_arent': (74, [20250, 14555, 15943, 15273], [115, 1270, 1618, 4027, 11664, 7647, 7362, 9647, 5914, 7747, 8622, 388, 0, 0, 0]),
    'una': (24, [4065, 6690, 3923, 7372], [0, 0, 0, 783, 3595, 2415, 2395, 3193, 2788, 3063, 3633, 185, 0, 0, 0]),
    'very': (26, [5925, 6108, 5617, 5865], [0, 0, 0, 787, 3865, 2873, 3024, 3548, 2443, 2751, 2596, 544, 622, 462, 0]),
    'woman': (46, [10548, 11317, 10128, 10354], [0, 0, 0, 1730, 7543, 5537, 5173, 5968, 5370, 5395, 5446, 185, 0, 0, 0]),
    'y_aqui': (38, [7416, 7588, 9647, 8670], [133, 1071, 1144, 1831, 4704, 3500, 3162, 3878, 3497, 3973, 4893, 712, 448, 375, 0]),
    'y': (8, [0, 1291, 2566, 2503], [72, 553, 738, 844, 990, 836, 563, 447, 447, 447, 423, 0, 0, 0, 0]),
}


TRANSLATIONS = {
    'abuela': 'grandmother',
    'abuelo': 'grandfather',
    'alla': 'she',
    'bonita': 'pretty',
    'carros': 'cars',
    'de': 'of',
    'del': 'from_the',
    'el_abuelo_de_carmen': 'carmens_grandfather',
    'el': 'the',
    'es': 'it_is',
    'famila': 'family',
    'familia': 'family',
    'foto': 'picture',
    'fotos': 'pictures',
    'guau': 'wow',
    'hay': 'there_are',
    'interesante': 'interesting',
    'is': 'esta',
    'looks_at': 'mira',
    'mi': 'my',
    'mujer': 'woman',
    'museo': 'museum',
    'muy': 'very',
    'no_habla': 'he_doesnt_talk',
    'no_hay': 'there_arent',
    'pasado': 'past',
    'que_inteligente': 'how_intelligent',
    'que_interesante': 'how_interesting',
    'she': 'ella',
    'si': 'yes',
    'solo': 'just',
    'su_abuelo': 'her_grandfather',
    'tengo': 'i_have',
    'un': 'a',
    'una': 'one',
    'y_aqui': 'and_here',
    'y': 'and',
}

BOXES = {
    'Yes': (66000, 70000),
    'Only one': (100200, 118700),
    'Grandmother': (152000, 173000),
}

FIRST_SKIP = 2
TEXT_HEIGHT = 30
PAIR_HEIGHT = 35
PAIR_INSET = 10
TEXT_INSET = 6
BLOB_MIN_COUNT = 2000
LESSON_WIDTH = 285
LESSON_HEIGHT = 435
LESSON_BUTTON_INSET = 30
LESSONS = [
    (0, 85),
    (305, 85),
    (610, 85),
    (915, 85),
    (1220, 85),
    (1525, 85),
    (1830, 85),
    (2135, 85),
    (2440, 85),
    (0, 609),
    (305, 609),
    (610, 609),
    (915, 609),
    (1220, 609),
    (1525, 609),
    (1830, 609),
    (2135, 609),
    (2440, 609),
    (0, 1133),
    (305, 1133),
    (610, 1133),
    (915, 1133),
    (1220, 1133),
    (1525, 1133),
    (1830, 1133),
    (2135, 1133),
    (2440, 1133),
]


class Screen():
    def __init__(self, lesson):
        if not wx.GetApp():
            self.app = wx.App(redirect=False)
        screen = wx.ScreenDC()
        self.data = array.array('B', [0] * LESSON_WIDTH * LESSON_HEIGHT * 3)
        bitmap = wx.Bitmap(LESSON_WIDTH, LESSON_HEIGHT)
        mem = wx.MemoryDC(bitmap)
        mem.Blit(0, 0, LESSON_WIDTH, LESSON_HEIGHT, screen, lesson[0], lesson[1])
        del mem
        bitmap.CopyToBuffer(self.data)

    def pixel(self, x, y):
        pos = (y*LESSON_WIDTH+x)*3
        return tuple(self.data[pos: pos+3])


class Action():
    CLICK = 1
    PROCEED = 2
    RESTART = 3

    def __init__(self, lesson, action, params = None):
        self.lesson = lesson
        self.action = action
        self.params = params

    def click(lesson, x, y):
        return Action(lesson, Action.CLICK, (x, y))

    def proceed(lesson):
        return Action(lesson, Action.PROCEED)

    def restart(lesson):
        return Action(lesson, Action.RESTART)

    def run(self):
        if self.action == Action.CLICK:
            pyautogui.moveTo(self.params[0] + self.lesson[0], self.params[1] + self.lesson[1], duration=0)
            pyautogui.click()
        elif self.action == Action.PROCEED:
            pyautogui.moveTo(self.lesson[0]+2*LESSON_WIDTH//6, self.lesson[1] +
                            LESSON_HEIGHT-LESSON_BUTTON_INSET, duration=0)
            pyautogui.click()
        elif self.action == Action.RESTART:
            pyautogui.moveTo(self.lesson[0]+10, self.lesson[1] + LESSON_HEIGHT//2, duration=0)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'f')
            pyautogui.write('In the Museum')
            pyautogui.press('esc')
            pyautogui.press('enter')


class Blob():
    def __init__(self, lesson, color, clz, first, skip):
        self.lesson = lesson
        self.color = color
        self.clz = clz
        self.first = first
        self.last = first
        self.count = skip

    def found(self, found, skip):
        self.last = found
        self.count += skip

    def click(self):
        x = (self.last[0]+self.first[0])//2
        y = (self.last[1]+self.first[1])//2
        return Action.click(self.lesson, x, y)

    def text(self, screen, texts=TEXTS):
        total = 0
        total_lin = 0
        first_r = -1
        for y in range(self.first[1]-TEXT_HEIGHT+TEXT_INSET, self.first[1]-TEXT_INSET):
            for x in range(self.first[0]+TEXT_INSET, self.last[0]-TEXT_INSET):
                red = screen.pixel(x, y)[0]-BACKGROUND[0]
                if red > 100 and first_r < 0:
                    first_r = x
                total += red
                if red > 100:
                    total_lin += ((x-first_r)*(self.first[0]+self.last[0])/2)/self.count
        # if texts == PAIRS:
            # print(self.count, total, total_lin)
            # self.show()
        # print(self.count, total, total_lin)
        results = []
        for text in texts.items():
            if (self.count >= text[1][0][0] and
                self.count < text[1][0][1] and
                total >= text[1][1][0] and
                    total < text[1][1][1]):
                results.append(text[0])
        if len(results) > 1:
            new_results = []
            # print('deduping ', results)
            for text in results:
                if (total_lin >= texts[text][2][0] and
                        total_lin < texts[text][2][1]):
                    new_results.append(text)
            results = new_results
        # elif len(results) == 1:
        #     if len(texts[results[0]]) > 2:
        #         if total_lin < texts[results[0]][2][0]:
        #             print('for', results[0], total_lin, 'is too little')
        #             assert False
        #         if total_lin >= texts[results[0]][2][1]:
        #             print('for', results[0], total_lin, 'is too much')
        #             assert False
        assert len(results) < 2
        return ' | '.join(results)

    def pair(self, screen):
        vy = []
        vx = [0] * 4
        dx = self.last[0] - self.first[0]
        for y in range(self.first[1]-PAIR_HEIGHT+PAIR_INSET, self.first[1]-PAIR_INSET):
            vty = 0
            for x in range(self.first[0], self.last[0]):
                vxi = (x-self.first[0])*4//(self.last[0]-self.first[0])
                red = screen.pixel(x, y)[0]-BACKGROUND[0]
                # if red > 100:
                vty += red
                vx[vxi] += red
            vy.append(vty)
        # print(v)
        max_corr = 0
        best = None
        for text in PAIRSV:
            ratio = float(dx+PAIR_INSET) / float(PAIRSV[text][0]+PAIR_INSET)
            ratio = min(ratio, 1.0/ratio)
            ratio = 1 - (1-ratio) ** 2
            # corr = numpy.corrcoef(vy, PAIRSV[text][2])[0][1] * numpy.corrcoef(vx, PAIRSV[text][1])[0][1] * ratio
            corr = numpy.corrcoef(vy, PAIRSV[text][2])[0][1] * ratio
            if corr > max_corr:
                max_corr = corr
                best = text
        # if max_corr < 0.99:
        #     best = best + '(?)'
        # print('>>>              ', best)
        # print('('+str(dx)+','+str(vx)+','+str(vy)+'),')
        # print(max_corr)
        # PAIRSV[best] = (dx, vx, vy)
        return best

    def box(self, screen):
        total = 0
        for y in range(self.first[1]-TEXT_INSET-16, self.last[1]+TEXT_INSET):
            for x in range(self.last[0]+TEXT_INSET, LESSON_WIDTH-TEXT_INSET):
                total += screen.pixel(x, y)[0]-BACKGROUND[0]
        # print(self.count, total)
        for box in BOXES.items():
            if (total >= box[1][0] and
                    total < box[1][1]):
                return box[0]


def blobs(skip, lesson, screen, classes, find_text):
    colors = set()
    allowed_sizes = {}
    color_to_clz = {}
    for clz in classes:
        color = clz[0]
        color_to_clz[color] = clz
        colors.add(color)
        if color not in allowed_sizes:
            allowed_sizes[color] = []
        allowed_sizes[color].append((clz[1], clz[2]))
    w, h = (LESSON_WIDTH, LESSON_HEIGHT)
    mask = [[-1] * h] * w
    cur = -1
    blobs = {}
    color_hist = {}
    for y in range(1, h-1):
        for x in range(1, w-1, skip):
            c = screen.pixel(x, y)
            if (c != screen.pixel(x-2, y-1) or
                    c != screen.pixel(x-2, y) or
                    c != screen.pixel(x-2, y+1) or
                    c != screen.pixel(x, y-1) or
                    c != screen.pixel(x, y+1) or
                    c != screen.pixel(x+2, y-1) or
                    c != screen.pixel(x+2, y) or
                    c != screen.pixel(x+2, y+1)):
                continue
            if c not in color_hist:
                color_hist[c] = 1
            else:
                color_hist[c] += 1
            if c in colors:
                if mask[x-1][y] >= 0:
                    mask[x][y] = mask[x-1][y]
                    blobs[mask[x][y]].found((x, y), skip)
                elif mask[x][y-1] >= 0:
                    mask[x][y] = mask[x][y-1]
                    blobs[mask[x][y]].found((x, y), skip)
                else:
                    cur += 1
                    blobs[cur] = Blob(lesson, c, color_to_clz[c], (x, y), skip)
                    mask[x][y] = cur
            else:
                if find_text:
                    mask[x][y] = -1
    # print('Before:')
    # for blob in blobs.values():
    #     print(blob.color, blob.first, blob.last, blob.count)
    results = []
    for blob in blobs.values():
        for allowed_size in allowed_sizes[blob.color]:
            if blob.count >= allowed_size[0] and blob.count < allowed_size[1]:
                results.append(blob)
                continue
    # print('After:')
    # for blob in results:
    #     print(blob.color, blob.first, blob.last, blob.count)
    return results


# screen = Screen()
# print(screen.pixel(10, 200))
# blobs(screen, [BACKGROUND])

def act(skip, lesson, screen):
    # pyautogui.moveTo(lesson[0]+LESSON_WIDTH//2-10, lesson[1]+20, duration=0)
    # print(screen.pixel(lesson[0]+LESSON_WIDTH//2-10, lesson[1]+20))
    # return
    buttons = blobs(skip, lesson, screen, [GREEN, BLUE], False)
    if len(buttons) == 1:
        return [buttons[0].click()]
    else:
        boxes = blobs(skip, lesson, screen, [BOX], False)
        if boxes and all([x.clz == BOX for x in boxes]):
            boxes = {x.box(screen): x for x in boxes}
            for box in boxes:
                if box in (BOXES.keys()):
                    return [boxes[box].click(), Action.proceed(lesson)]
        else:
            found = blobs(skip, lesson, screen, [TEXT], True)
            random.shuffle(found)
            texts = {x.text(screen): x for x in found}
            # print(texts.keys())
            # return
            if texts.keys() == {'Y aqui', ''}:
                return [texts['Y aqui'].click(), Action.proceed(lesson)]
            elif texts.keys() == {'Mira', ''}:
                return [texts['Mira'].click(), Action.proceed(lesson), Action.proceed(lesson)]
            elif texts.keys() == {'Ella', 'es', 'mi', 'abuela'}:
                return [texts['Ella'].click(),
                        texts['es'].click(),
                        texts['mi'].click(),
                        texts['abuela'].click(),
                        Action.proceed(lesson),
                        Action.proceed(lesson)]
            else:
                pairs = {x.pair(screen): x for x in found}
                if pairs:
                    pwise = [(pairs[x], pairs[TRANSLATIONS[x]])
                             for x in TRANSLATIONS if x in pairs and TRANSLATIONS[x] in pairs]
                    actions = []
                    for p in pwise:
                      actions += [p[0].click(), p[1].click()]
                    if len(pwise) != 5:
                        for f in found:
                          actions.append(f.click())
                    actions.append(Action.proceed(lesson))
                    return actions
    if skip > 1:
        return act(skip//2, lesson, screen)
    else:
        flames = blobs(skip, lesson, screen, [FLAME], False)
        if not flames:
            return [Action.proceed(lesson)]
            # pyautogui.scroll(-10)
        if len(flames) == 1:
            return [Action.restart(lesson)]


p1 = set(PAIRSV.keys())
p2 = set(TRANSLATIONS.keys())
p2 = p2.union(TRANSLATIONS.values())
diff = p1.difference(p2)
if diff:
    print(diff)
    assert False


# def lesson_thread(lesson):
#   while True:
#     print('I am', lesson)
#   time.sleep(1)
#   pass

# threads = [threading.Thread(target=lesson_thread, args=(x)) for x in LESSONS]
# print(threads)
# for thread in threads:
#   thread.start()

# for thread in threads:
#   thread.join()

POOL_SIZE = 8
DEBUG = 0


pool = ThreadPool(POOL_SIZE)
task_queue = queue.Queue()
action_queue = queue.Queue()


def should_quit():
    mx, my = pyautogui.position()
    return mx > LESSONS[-1][0] + LESSON_WIDTH


def lesson_func(index):
  action_taken = False
  # while not should_quit() or not action_taken:
  while True:
      try:
        if DEBUG:
            print(index, 'waiting')
        lesson = task_queue.get()
        if DEBUG:
            print(index, 'running', lesson)
        actions = act(FIRST_SKIP, lesson, Screen(lesson))
        if DEBUG:
            print(index, 'done')
        action_queue.put((lesson, actions))
        if DEBUG:
            print(index, 'sent')
        task_queue.task_done()
        action_taken = True
      except queue.Empty:
        pass
  if DEBUG:
      print(index, 'chilling')

pool.map_async(lesson_func, range(POOL_SIZE))

action_taken = False
for lesson in LESSONS:
  task_queue.put(lesson)
while not should_quit() or not action_taken:
    # for lesson in LESSONS:
    #     # mxb, myb = pyautogui.position()
    #     # # time.sleep(0.1)
    #     # mx, my = pyautogui.position()
    #     # if mx != mxb or my != myb:
    #     #     break
    #     # show_lesson(lesson)
    #     actions = act(FIRST_SKIP, lesson, screen)
    #     for action in actions:
    #         action.run()
    #     mx, my = pyautogui.position()
    #     if mx > LESSONS[-1][0] + LESSON_WIDTH:
    #         break
    # time.sleep(1)

    print('\r    Queued prompts: ', task_queue.qsize(), '      Queued actions: ', action_queue.qsize(), '              ', end='')
    try:
        task = action_queue.get_nowait()
        (lesson, actions) = task
        for action in actions:
            action_taken = True
            # print('Running', action.action, action.params)
            action.run()
        task_queue.put(lesson)
        action_queue.task_done()
    except queue.Empty:
        pass


pool.join()
