from logging import Filter


class KafkaFilter(Filter):
    def filter(self, record):
        return super().filter(record)


class MineLogFilter(Filter):
    def filter(self, record):
        return super().filter(record)
