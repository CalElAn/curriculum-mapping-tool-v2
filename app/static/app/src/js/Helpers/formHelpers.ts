import { ref, toValue } from 'vue';
import type { Ref } from 'vue';
import remove from 'lodash/remove';

export function useFormHelpers(
  initialSubformItems: Array,
  newSubformItem: Object,
) {
  const subformItems: Ref<Array<Record<number, unknown>>> =
    ref(initialSubformItems);
  const shouldAllowAdd: Ref<Boolean> = ref(true);

  function add(): void {
    subformItems.value.unshift({
      ...toValue(newSubformItem),
      adding: true,
    });

    shouldAllowAdd.value = false;
  }

  function onCancelAdd(): void {
    subformItems.value.shift();
    shouldAllowAdd.value = true;
  }

  function onDestroyed(index: Number): void {
    remove(subformItems.value, (item, itemIndex) => itemIndex === index);
  }

  return { subformItems, shouldAllowAdd, add, onCancelAdd, onDestroyed };
}

export function handleViewing(
  shouldView: Boolean,
  subformItems: Ref<Array<Record<number, unknown>>>,
  showLoadingSpinner: Boolean,
  route: string,
): void {
  if (!shouldView) {
    subformItems.value = [];
    return;
  }

  showLoadingSpinner.value = true;

  axios.get(route).then((response) => {
    subformItems.value = response.data;
    showLoadingSpinner.value = false;
  });
}
