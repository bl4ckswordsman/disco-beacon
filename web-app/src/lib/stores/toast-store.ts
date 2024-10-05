import { writable, type Writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  const { subscribe, set } = writable<Toast | null>(
    null,
  ) as Writable<Toast | null>;

  function show(message: string, type: ToastType): void {
    set({ message, type });
    setTimeout(() => set(null), 3000);
  }
  return {
    subscribe,
    show,
  };
}

export const toast = createToastStore();
