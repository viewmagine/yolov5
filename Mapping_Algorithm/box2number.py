

class Inference_result(object):
    def __init__(self, needle_ratio=None, gauge_ratio = None):
        """
        @param needle_ratio: (float) ratio of points from needle.
             ---  <-  needle_ratio = 0
            |   | <-  needle_ratio = 0.33                  <-bBox of needle ratio
            |   | <-  needle_ratio = 0.66
             ---  <-  needle_ratio = 1
        @param gauge_ratio: (list of float)
             -------  <-  gauge_ratio = 0
            |   120   | <-  gauge_ratio = 0.33                  <-bBox of needle ratio
            |   240   | <-  gauge_ratio = 0.66
             -------  <-  gauge_ratio = 1
             -> gauge_ratio = [ 0, 0.33, 0.66, 1]  \\ gauge_label = [-999, 120, 240, 999]
             You may define inf. and -inf. as you want. i.e) -999, 999
        """
        if needle_ratio is None:
            needle_ratio = 10/30
        if gauge_ratio is None:
            gauge_ratio = [0/450, 140/450, 170/450, 210/450, 260/450, 300/450, 1]
        self.gauge_label = [999, 240, 200, 200, 100, 50, 0, -100]
        self.needle_ratio = needle_ratio
        self.gauge_ratio = gauge_ratio


    def needle_point_pixel(self, position):
        """
        @param position: BBox of needle position
        @return: position of relative points(needle 내 상대적 눈금) from needle
        """
        Nx1, Ny1, Nx2, Ny2 = position
        # print("Needle Point", Nx1, Ny1, Nx2, Ny2)
        return (1 - self.needle_ratio) * Ny1 + self.needle_ratio * Ny2

    def map_needle_to_gauge(self, needle_relative_poses):
        """
        @param needle_relative_poses: position of needle compare to gauge. if needle is on top, it is 0
        @return: answer what we want(눈금)
        """
        # print(needle_relative_poses)
        # for needle_relative_pos in needle_relative_poses:
        #     # for i in range(len(self.gauge_ratio)-1):
        #     #     if needle_relative_pos > self.gauge_ratio[i]:
        #     #         if needle_relative_pos < self.gauge_ratio[i+1]:
        #     #             print(needle_relative_pos, self.gauge_ratio[i], self.gauge_ratio[i+1])
        #     return -240*324/87*needle_relative_pos+617
        #                 # return self.gauge_label[i:i+2]
        print(needle_relative_poses)
        for needle_relative_pos in needle_relative_poses:
            print(needle_relative_pos)
            if needle_relative_pos <= 73 / 240:
                return "more than 360"
            elif needle_relative_pos <= 85 / 240:
                return -(240 * 60) / (85 - 73) * (needle_relative_pos - 85 / 240) + 300
            elif needle_relative_pos <= 96.5 / 240:
                return -(240 * 50) / (96.5 - 85) * (needle_relative_pos - 96.5 / 240) + 250
            elif needle_relative_pos <= 108 / 240:
                return -(240 * 50) / (108 - 96.5) * (needle_relative_pos - 108 / 240) + 200
            elif needle_relative_pos <= 121.5 / 240:
                return -(240 * 50) / (121.5 - 108) * (needle_relative_pos - 121.5 / 240) + 150
            elif needle_relative_pos <= 135 / 240:
                return -(240 * 50) / (135 - 121.5) * (needle_relative_pos - 135 / 240) + 100
            elif needle_relative_pos <= 150 / 240:
                return -(240 * 50) / (150 - 135) * (needle_relative_pos - 150 / 240) + 50
            elif needle_relative_pos <= 160 / 240:
                return -(240 * 3) / (153 - 150) * (needle_relative_pos - 153 / 240) + 36

            # return -1008*needle_relative_pos+658.2
            # return self.gauge_label[i:i+2]
        return "error"

    def result(self, positions):
        needle_points = []
        gauge_height = []
        needle_pos_ratio = []
        for pos in positions:
            if pos[4] == 0:
                start,height = pos[1], pos[3]-pos[1]
                gauge_height.append((start,height))
            if pos[4] == 1:
                pixel_result = self.needle_point_pixel(pos[0:4])
                needle_points.append(pixel_result)

        a_zip= list(zip(gauge_height, needle_points))
        for data in a_zip:
            gauge_sh, needle_p = data[0], data[1]
            gauge_s, gauge_h = gauge_sh[0], gauge_sh[1]
            needle_pos_ratio.append((needle_p-gauge_s)/gauge_h)

        return self.map_needle_to_gauge(needle_pos_ratio)

if __name__ == "__main__":
    # boxN: [[gauge0_xywh(tuple), gauge1_xyxy, ...], [needle0_xywh, needle1_xywh, ...]]
    # boxN: [[gauge0_xywh(tuple), gauge1_xywh, ...], [needle0_xywh, needle1_xywh, ...]]
    position = [[126.19498443603516, 39.42572021484375, 477.67144775390625, 1080.0, 0.0],
                [250, 650, 330, 778, 1],
                [840.2291259765625, 31.248046875, 1086.451904296875, 1080.0, 0.0],
                [925, 591, 1005, 765, 1],
                [1453.159423828125, 46.44621276855469, 1780.2269287109375, 1080.0, 0.0],
                [1573, 604, 1663, 769, 1]
                ]

    image = "108.jpg"

    inference = Inference_result(None, None)
    print(inference.result(position))