import { writable, type Writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  // Writable store with proper type inference
  const store: Writable<Toast | null> = writable<Toast | null>(null);

  function show(message: string, type: ToastType): void {
    store.set({ message, type });
    setTimeout(() => {
      store.set(null); // Clear the toast after 3 seconds
    }, 3000);
  }

  return {
    subscribe: store.subscribe,
    show,
  };
}

export const toast = createToastStore();
