import type { ContextMenuContext } from '$lib/components/context_menu.svelte';
import { getContext } from 'svelte';

export const useContextMenu = (): ContextMenuContext => {
  return getContext('contextmenu');
}