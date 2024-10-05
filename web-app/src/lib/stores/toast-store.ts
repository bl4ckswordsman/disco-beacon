import { writable, type Writable } from "svelte/store";

export type ToastType = "info" | "success" | "error";

export interface Toast {
  message: string;
  type: ToastType;
}

function createToastStore() {
  const { subscribe, set }: Writable<Toast | null> = writable<Toast | null>(
    null,
  );

  function setToast(value: Toast | null): void {
    set(value);
  }

  return {
    subscribe,
    show: (message: string, type: ToastType): void => {
      setToast({ message, type });
      setTimeout(() => setToast(null), 3000);
    },
    hide: (): void => {
      setToast(null);
    },
  };
}

export const toast = createToastStore();
