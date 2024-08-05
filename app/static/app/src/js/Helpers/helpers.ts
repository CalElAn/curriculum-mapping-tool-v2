import { router } from '@inertiajs/vue3';
import type { Ref } from 'vue';

export function autoGrow(event): void {
  event.target.style.height = '';
  event.target.style.height = event.target.scrollHeight + 'px';
}

export function getFilteredItems(
  route: string,
  filterValue: string,
  subformItems: Ref<Array<Record<number, unknown>>>,
  dataProp: String,
): void {
  router.get(
    route,
    { filter: filterValue },
    {
      preserveState: true,
      replace: true,
      onSuccess: (page) => {
        subformItems.value = page.props[dataProp];
      },
    },
  );
}
