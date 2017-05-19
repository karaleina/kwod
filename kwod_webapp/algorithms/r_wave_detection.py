class Algorithm(object):
    def name(self):
        raise NotImplementedError()
    def detect_r_waves(self, channel):
        raise NotImplementedError()


class Algorithm1(object):
    def name(self):
        return "Algorithm 1"

    def detect_r_waves(self, channel):
        return [1005, 2005]


class Algorithm2(object):
    def name(self):
        return "Algorithm 2"

    def detect_r_waves(self, channel):
        return [100, 600, 900, 3000]


algorithms = [Algorithm1(), Algorithm2()]
