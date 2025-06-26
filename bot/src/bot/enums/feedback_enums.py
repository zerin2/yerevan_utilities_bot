from enum import Enum


class FeedbackType(str, Enum):
    REVIEW = 'review'
    ERROR = 'error'


class FeedbackStatus(str, Enum):
    NEW = 'new'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
