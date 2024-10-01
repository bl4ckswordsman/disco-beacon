import { writable, type Writable } from "svelte/store";

type ToastType = "info" | "success" | "error";

interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  const store: Writable<Toast | null> = writable<Toast | null>(null);

  // Wrapping the store's set function
  function setToast(toast: Toast | null): void {
    store.set(toast);
  }

  function subscribeToStore(run: (value: Toast | null) => void) {
    return store.subscribe(run);
  }

  function show(message: string, type: ToastType): void {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null); // Clear the toast after 3 seconds
    }, 3000);
  }

  return {
    subscribe: subscribeToStore,
    show,
  };
}

export const toast = createToastStore();
