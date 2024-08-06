# 数据暂存区
UserFaceResArray = []


# 用户暂存区内存储对象
class UserFaceRes:
    def __init__(self):
        # 存储用户名，用于标识
        self.username = ""

        # 存储人脸识别得出的数据
        # age, emoji, gender, beauty, glaPoss, glaType, dateTime, dataurl
        self.faceData = []

        # 存储分数，便于比较（faceData中包含此条数据）
        self.score = 0
