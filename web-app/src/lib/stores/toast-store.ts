import { writable, type Writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  const { subscribe, set }: Writable<Toast | null> = writable<Toast | null>(
    null,
  );

  return {
    subscribe,
    show: (message: string, type: ToastType): void => {
      set({ message, type });
      setTimeout(() => set(null), 3000);
    },
    hide: (): void => {
      set(null);
    },
  };
}

export const toast = createToastStore();
