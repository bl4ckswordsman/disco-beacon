import { writable, type Writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  const toastStore: Writable<Toast | null> = writable<Toast | null>(null);

  return {
    subscribe: toastStore.subscribe,
    show: (message: string, type: ToastType): void => {
      toastStore.set({ message, type });
      setTimeout(() => toastStore.set(null), 3000);
    },
    hide: (): void => {
      toastStore.set(null);
    },
  };
}

export const toast = createToastStore();
