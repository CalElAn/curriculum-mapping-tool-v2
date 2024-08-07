import { ref } from 'vue';
import { useForm, usePage } from '@inertiajs/vue3';
import { toast, deleteConfirmationDialog } from '@/Components/swal.js';

export const emittedEvents = ['cancelAdd', 'stored', 'destroyed'] as const;

export function useSubformHelpers(
  subformData: object,
  useFormData: object,
  emitFunction: (event: (typeof emittedEvents)[number], ...args: any[]) => void,
  storeRoute: string,
  updateRouteName: string,
  destroyRouteName: string,
) {
  const uid = ref(subformData.uid);

  const form: object & InertiaFormProps<object> = useForm(useFormData);

  const adding = ref(subformData.adding ?? false);
  const editing = ref(false);

  function store(): void {
    form.post(storeRoute, {
      preserveScroll: true,
      onSuccess: () => {
        adding.value = false;
        console.log(usePage().props.session);
        uid.value = usePage().props.session.data.uid;
        emitFunction('stored');
        toast.fire({ title: `Added!` });
      },
    });
  }

  function update(): void {
    form.post(
      reverseUrl(updateRouteName, uid.value),
      {
        preserveScroll: true,
        onSuccess: () => {
          toast.fire({ title: `Saved!` });
        },
      },
    );
  }

  function destroy(): void {
    deleteConfirmationDialog(() =>
      form.post(reverseUrl(destroyRouteName, uid.value), {
        preserveScroll: true,
        onSuccess: () => {
          emitFunction('destroyed');
          toast.fire({ title: `Deleted!` });
        },
      }),
    );
  }

  return { form, adding, editing, store, update, destroy, uid };
}
