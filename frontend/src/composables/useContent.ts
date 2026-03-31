import { ref } from 'vue';
import { directus, readItems } from '@/api/directus';

const globals = ref<Record<string, any>>({});
const landingPage = ref<Record<string, any>>({});
const uiDict = ref<Record<string, string>>({});
const isLoaded = ref(false);

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
  validation_required: 'Это поле обязательно для заполнения',
  validation_invalid_email: 'Пожалуйста, введите корректный email',
  error_server_down: 'Упс! Сервер временно недоступен.',
  error_auth_failed: 'Неверный email или пароль',
  system_loading: 'Загрузка...',
};

export function useContent() {
  const fetchContent = async () => {
    if (isLoaded.value) return;
    try {
      const [g, l, u] = await Promise.all([
        directus.request(readItems('globals')),
        directus.request(readItems('landing_page')),
        directus.request(readItems('ui_dictionary', { limit: -1 }))
      ]);
      
      globals.value = g || {};
      landingPage.value = l || {};
      
      const dict: Record<string, string> = { ...fallbackDict };
      if (u) {
        u.forEach((item: any) => {
          if (item.key && item.value) dict[item.key] = item.value;
        });
      }
      uiDict.value = dict;
      isLoaded.value = true;
    } catch (error) {
      console.error(error);
      uiDict.value = fallbackDict;
      isLoaded.value = true;
    }
  };

  const t = (key: string) => uiDict.value[key] || key;

  return { fetchContent, isLoaded, globals, landingPage, t };
}
