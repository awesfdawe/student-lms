import { ref, onMounted, onUnmounted, type Ref } from 'vue'

export function useIntersectionAnimation(
  targetRef: Ref<HTMLElement | null>,
  threshold: number = 0.1,
) {
  const isVisible = ref(false)
  let observer: IntersectionObserver | null = null

  onMounted(() => {
    observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0]
        if (entry?.isIntersecting && !isVisible.value) {
          isVisible.value = true
          if (targetRef.value) {
            observer?.unobserve(targetRef.value)
          }
        }
      },
      { threshold },
    )

    if (targetRef.value) {
      observer.observe(targetRef.value)
    }
  })

  onUnmounted(() => {
    if (observer) observer.disconnect()
  })

  return { isVisible }
}
