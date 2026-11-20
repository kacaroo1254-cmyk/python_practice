class Box:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class LabelBox(Box):
    def __init__(self, x1, y1, x2, y2, label):
        super().__init__(x1, y1, x2, y2)
        self.label = label

    def to_dict(self):
        return {"x1" : self.x1, "label" : self.label}

b3 = LabelBox(0,400,200,600,"car")
b4 = LabelBox(0,400,200,600,"person")

records = []

records.append(b3.to_dict)
records.append(b4.to_dict)




