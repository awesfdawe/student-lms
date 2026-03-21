<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[60rem] mx-auto min-h-[calc(100vh-5.625rem)]"
    >
      <h1
        class="font-geologica font-bold text-[2.5rem] md:text-[3.5rem] text-black mb-[2rem] animate-fade-up"
      >
        Публичная оферта
      </h1>
      <div
        class="prose prose-lg prose-blue max-w-none font-roboto text-black/80 animate-fade-up"
        style="animation-delay: 0.1s"
      >
        <p class="mb-4"><strong>1. Предмет договора</strong></p>
        <p class="mb-4">
          Настоящий документ является публичной офертой ООО "СКИЛЛФОРДЖ" в соответствии со ст. 437
          Гражданского кодекса РФ. Оферта определяет условия предоставления платного доступа к
          образовательным материалам (курсам, программам ДПО) посредством Платформы.
        </p>

        <p class="mb-4"><strong>2. Условия оказания услуг и доступ</strong></p>
        <p class="mb-4">
          Доступ к образовательным материалам предоставляется Пользователю после прохождения
          процедуры регистрации и 100% предоплаты стоимости выбранного курса (если не указано иное,
          например, при покупке в рассрочку через банки-партнеры).
        </p>

        <p class="mb-4"><strong>3. Возврат денежных средств</strong></p>
        <p class="mb-4">
          Возврат средств за информационно-консультационные услуги осуществляется в соответствии с
          Законом РФ "О защите прав потребителей". Пользователь вправе отказаться от исполнения
          договора в любое время при условии оплаты Исполнителю фактически понесенных им расходов.
        </p>

        <p class="mb-4"><strong>4. Ответственность сторон</strong></p>
        <p class="mb-4">
          Стороны несут ответственность за неисполнение или ненадлежащее исполнение своих
          обязательств в соответствии с законодательством Российской Федерации.
        </p>
      </div>
      <router-link to="/" class="btn-cta mt-[3rem] inline-block">Вернуться на главную</router-link>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
</script>
