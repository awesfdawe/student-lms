import { computed } from 'vue';
import { useContentStore } from '@/stores/content';

export function useContent() {
  const store = useContentStore();

  return {
    fetchContent: () => store.fetchContent(),
    fetchPage: (slug: string) => store.fetchPage(slug),
    fetchCourse: (slug: string) => store.fetchCourse(slug),
    fetchCourses: () => store.fetchCourses(),
    isLoaded: computed(() => store.isLoaded),
    globals: computed(() => store.globals),
    landingPage: computed(() => store.landingPage),
    courseList: computed(() => store.courseList || []),
    t: (key: string) => store.t(key),
    store
  };
}
