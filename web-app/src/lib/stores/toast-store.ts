import { writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  const { subscribe, set } = writable<Toast | null>(null);

  return {
    subscribe,
    show: (message: string, type: ToastType) => {
      set({ message, type });
      setTimeout(() => set(null), 3000);
    },
    hide: () => set(null),
  };
}

export const toast = createToastStore();
