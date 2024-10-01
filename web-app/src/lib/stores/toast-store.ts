import { writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  const store = writable<Toast | null>(null);

  function show(message: string, type: ToastType): void {
    store.set({ message, type });
    setTimeout(() => store.set(null), 3000);
  }

  function hide(): void {
    store.set(null);
  }

  return {
    subscribe: store.subscribe,
    show,
    hide,
  };
}

export const toast = createToastStore();
