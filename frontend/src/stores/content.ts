import { defineStore } from 'pinia';
import { API_BASE_URL } from '@/api/index';

const fallbackDict: Record<string, string> = {
  global_btn_back: 'Назад',
  global_btn_home: 'На главную',
  header_nav_faq: 'Частые вопросы',
  header_nav_free: 'Бесплатные курсы',
  header_nav_about: 'О нас',
  header_nav_contacts: 'Контакты',
  header_cta_login: 'Войти',
  header_cta_register: 'Регистрация',
  footer_cta_button: 'Свяжись с нами',
  footer_bottom_privacy: 'Политика конфиденциальности',
  footer_bottom_terms: 'Публичная оферта',
  hero_cta_text: 'Подобрать профессию',
  course_btn_enroll: 'Записаться на курс',
  course_label_duration: 'Длительность:',
  course_label_feature: 'Формат:',
  course_not_found_title: 'Курс не найден',
  course_not_found_desc: 'Возможно, ссылка устарела или курс был удален.',
  validation_required: 'Это поле обязательно для заполнения',
  validation_invalid_email: 'Пожалуйста, введите корректный email',
  error_server_down: 'Упс! Сервер временно недоступен.',
  error_auth_failed: 'Неверный email или пароль',
  system_loading: 'Загрузка...'
};

export const useContentStore = defineStore('content', {
  state: () => ({
    globals: {} as Record<string, any>,
    landingPage: {} as Record<string, any>,
    uiDict: { ...fallbackDict } as Record<string, string>,
    pages: {} as Record<string, any>,
    courses: {} as Record<string, any>,
    courseList: [] as any[],
    isLoaded: false,
    _fetchPromise: null as Promise<void> | null
  }),
  actions: {
    fetchContent() {
      if (this.isLoaded) return Promise.resolve();
      if (this._fetchPromise) return this._fetchPromise;
      
      this._fetchPromise = Promise.all([
        fetch(`${API_BASE_URL}/cms/globals`),
        fetch(`${API_BASE_URL}/cms/landing_page`),
        fetch(`${API_BASE_URL}/cms/ui_dictionary`)
      ]).then(async ([gRes, lRes, uRes]) => {
        this.globals = gRes.ok ? await gRes.json() : {};
        this.landingPage = lRes.ok ? await lRes.json() : {};
        
        const dict: Record<string, string> = { ...fallbackDict };
        if (uRes.ok) {
          const u = await uRes.json();
          if (Array.isArray(u)) {
            u.forEach((item: any) => {
              if (item.key && item.value) dict[item.key] = item.value;
            });
          }
        }
        this.uiDict = dict;
        this.isLoaded = true;
      }).catch(() => {
        this.uiDict = { ...fallbackDict };
        this.isLoaded = true;
      });
      
      return this._fetchPromise;
    },
    async fetchPage(slug: string) {
      if (this.pages[slug]) return this.pages[slug];
      try {
        let res = await fetch(`${API_BASE_URL}/cms/pages/${slug}`);
        if (!res.ok) {
          res = await fetch(`${API_BASE_URL}/cms/${slug}`);
        }
        if (res.ok) {
          const data = await res.json();
          this.pages[slug] = data;
          return data;
        }
      } catch (e) {}
      return null;
    },
    async fetchCourse(slug: string) {
      if (this.courses[slug]) return this.courses[slug];
      try {
        const res = await fetch(`${API_BASE_URL}/cms/courses/${slug}`);
        if (res.ok) {
          const data = await res.json();
          this.courses[slug] = data;
          return data;
        }
      } catch (e) {}
      return null;
    },
    async fetchCourses() {
      if (this.courseList && this.courseList.length > 0) return this.courseList;
      try {
        const res = await fetch(`${API_BASE_URL}/cms/courses`);
        if (res.ok) {
          const data = await res.json();
          this.courseList = Array.isArray(data) ? data : [];
          return this.courseList;
        }
      } catch (e) {}
      this.courseList = [];
      return [];
    }
  },
  getters: {
    t: (state) => (key: string) => state.uiDict[key] || key
  }
});
