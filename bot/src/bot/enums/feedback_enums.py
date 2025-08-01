from enum import StrEnum


class FeedbackType(StrEnum):
    REVIEW = 'review'
    ERROR = 'error'


class FeedbackStatus(StrEnum):
    NEW = 'new'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
