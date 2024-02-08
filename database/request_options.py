from typing import Optional, Literal


class RequestOptions:
    def __init__(
            self,
            where_to_look: str = '',
            what_to_look_for: str = '',
            requester: str = '',
            where_clause: Optional[dict] = None,
            operation_type: Literal['read', 'write', 'update'] = 'read',
            get_all_results: bool = True
    ):
        self.where_to_look: str = where_to_look
        self.what_to_look_for: str = what_to_look_for
        self.requester: str = requester
        self.where_clause: Optional[dict] = where_clause
        self.operation_type: Literal['read', 'write', 'update'] = operation_type
        self.get_all_results: bool = get_all_results
