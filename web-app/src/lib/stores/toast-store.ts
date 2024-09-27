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
    show: (message: string, type: ToastType): void => {
      try {
        set({ message, type } as Toast);
        setTimeout(() => {
          try {
            set(null);
          } catch (error) {
            console.error("Error hiding toast:", error);
          }
        }, 3000);
      } catch (error) {
        console.error("Error showing toast:", error);
      }
    },
    hide: (): void => {
      try {
        set(null);
      } catch (error) {
        console.error("Error hiding toast:", error);
      }
    },
  };
}

export const toast = createToastStore();
