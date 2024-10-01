import { writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  // Initialize the store with a correctly typed default value
  const { subscribe, set } = writable<Toast | null>(null);

  function show(message: string, type: ToastType): void {
    // Set the toast and reset it after a timeout
    set({ message, type });
    setTimeout(() => {
      set(null); // Clear the toast after 3 seconds
    }, 3000);
  }

  return {
    subscribe,
    show,
  };
}

export const toast = createToastStore();
