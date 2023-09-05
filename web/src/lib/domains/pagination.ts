export interface Pagination<T> {
  total: number;
  offset: number;
  limit: number;
  data: T[];
}

export function hasMore(pagination: Pagination<any>) {
  return pagination.total > pagination.offset + pagination.limit;
}
