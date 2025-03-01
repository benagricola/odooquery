from typing import List
from datetime import datetime
from .types import Message
from .utils.text_processing import _strip_html

def fetch_messages(self, domain: List, order: str) -> List[Message]:
    """Base function to fetch messages matching given criteria."""
    fields = ['subject', 'body', 'date', 'email_from', 'author_id', 'message_type',
              'subtype_id', 'partner_ids', 'model', 'res_id']

    records = self.auto_paginated_search_read('mail.message', domain, fields, order)

    return [{
        'id': msg['id'],
        'subject': msg['subject'],
        'body': _strip_html(msg['body']),
        'date': msg['date'],
        'email_from': msg['email_from'],
        'author_id': msg['author_id'][0] if isinstance(msg['author_id'], (list, tuple)) else msg['author_id'],
        'message_type': msg['message_type'],
        'subtype_id': msg['subtype_id'][0] if isinstance(msg['subtype_id'], (list, tuple)) else msg['subtype_id'],
        'partner_ids': msg['partner_ids'],
        'model': msg['model'],
        'res_id': msg['res_id']
    } for msg in records]

def fetch_messages_by_date_range(self, start_timestamp: int, end_timestamp: int, order: str) -> List[Message]:
    """Fetch messages within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    end_date = datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return self.fetch_messages([
        ('date', '>=', start_date),
        ('date', '<=', end_date)
    ], order)

def fetch_messages_by_model(self, model: str, res_ids: List[int], order: str) -> List[Message]:
    """Fetch messages related to specific model records."""
    return self.fetch_messages([
        ('model', '=', model),
        ('res_id', 'in', res_ids)
    ], order)

def fetch_messages_by_author(self, author_ids: List[int], order: str) -> List[Message]:
    """Fetch messages from specific authors."""
    return self.fetch_messages([
        ('author_id', 'in', author_ids)
    ], order)