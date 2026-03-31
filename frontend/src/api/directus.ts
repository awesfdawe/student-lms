import { createDirectus, rest, readItems, readItem } from '@directus/sdk';

export const directus = createDirectus('http://localhost:8055').with(rest());
export { readItems, readItem };
