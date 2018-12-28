import re
from random import choice

import redis

from app.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY_FOR_PROXY_COOKIES, MAX_SCORE, MIN_SCORE, INITIAL_SCORE


class RedisClient(object):
    def __init__(self, redis_key=REDIS_KEY_FOR_PROXY_COOKIES):
        """
        初始化
        :param redis_key: 存储的key名称
        """
        self.redis_key = redis_key
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    def add(self, value, score=INITIAL_SCORE):
        """
        添加值，设置分数为最高
        :param value: 值
        :param score: 分数
        :return: 添加结果
        """
        if not re.match('[\s\S]+', value):
            print('值不符合规范', value, '丢弃')
            return False
        if not self.db.zscore(self.redis_key, value):
            return self.db.zadd(self.redis_key, score, value)

    def random(self):
        """
        随机获取有效值，首先尝试获取最高分数的值，如果不存在，按照排名获取，否则异常
        :return: 随机值
        """
        result = self.db.zrangebyscore(self.redis_key, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(self.redis_key, 0, 10)
            if len(result):
                return choice(result)
            else:
                return None

    def decrease(self, value):
        """
        值值减一分，小于最小值则删除
        :param value: 值
        :return: 修改后的值分数
        """
        score = self.db.zscore(self.redis_key, value)
        if score and score > MIN_SCORE:
            # print('值', value, '当前分数', score, '减1')
            return self.db.zincrby(self.redis_key, -1, value)
        else:
            pass
            # print('值', value, '当前分数', score, '移除')
            # return self.db.zrem(self.redis_key, value)

    def exists(self, value):
        """
        判断是否存在
        :param value: 值
        :return: 是否存在
        """
        return self.db.zscore(self.redis_key, value) is not None

    def max(self, value):
        """
        将值设置为MAX_SCORE
        :param value: 值
        :return: 设置结果
        """
        print('值', value, '可用，设置为', MAX_SCORE)
        return self.db.zadd(self.redis_key, MAX_SCORE, value)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(self.redis_key)

    def all(self):
        """
        获取全部值
        :return: 全部值列表
        """
        return self.db.zrangebyscore(self.redis_key, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 值列表
        """
        return self.db.zrevrange(self.redis_key, start, stop - 1)
