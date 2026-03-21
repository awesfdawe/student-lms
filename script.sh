#!/bin/bash

echo "Начинаем рефакторинг проекта Student LMS..."

# --- 1. Создание необходимых директорий ---
mkdir -p backend/app/api/routers
mkdir -p backend/app/crud
mkdir -p frontend/src/api
mkdir -p frontend/src/composables
mkdir -p frontend/src/data

touch backend/app/api/__init__.py
touch backend/app/api/routers/__init__.py
touch backend/app/crud/__init__.py

# --- 2. БЭКЕНД: Конфигурация, Безопасность и БД ---

cat << 'EOF' > backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student LMS API"
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "student_lms"
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str = "super_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DIRECTUS_URL: str = ""
    DIRECTUS_API_KEY: str = ""

    @property
    def sqlalchemy_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True, 
        extra='ignore'
    )

settings = Settings()
EOF

cat << 'EOF' > backend/app/core/security.py
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
EOF

cat << 'EOF' > backend/app/crud/crud_user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
EOF

cat << 'EOF' > backend/app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db():
    async with SessionLocal() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
EOF

cat << 'EOF' > backend/app/api/routers/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserRead, UserCreate
from app.api.deps import get_db

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db=db, user_in=user_in)

@router.post("/login")
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
EOF

cat << 'EOF' > backend/app/api/routers/users.py
from fastapi import APIRouter, Depends
from app.schemas.user import UserRead
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
EOF

cat << 'EOF' > backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import auth, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
EOF


# --- 3. ФРОНТЕНД: Стили, Логика, Компоненты ---

cat << 'EOF' > frontend/src/assets/style.css
@import 'tailwindcss';
@import '@fortawesome/fontawesome-free/css/all.css';
@import url('https://fonts.googleapis.com/css2?family=Geologica:wght@400;700;800&family=Roboto:wght@400;700&display=swap');

@theme {
  --font-geologica: 'Geologica', sans-serif;
  --font-roboto: 'Roboto', sans-serif;
  --font-icons: 'Font Awesome 6 Free', sans-serif;
  --font-logo: 'Font Awesome 6 Free', sans-serif;

  --color-accent: #f9a9a9;
  --color-accent-dark: #e08383;

  --spacing-container-px: 5.625rem;
  --spacing-header-py: 2.125rem;
  --width-container: 80rem;
  --width-cta: 11.1875rem;
  --height-cta: 3.5625rem;
  --height-header: 5.625rem;
}

@layer base {
  html {
    scroll-padding-top: var(--height-header);
    scroll-behavior: smooth;
  }
  body {
    font-family: var(--font-geologica);
    @apply text-black bg-white antialiased overflow-x-hidden;
  }
}

@layer components {
  .btn-cta {
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-geologica);
    font-weight: 700;
    color: white;
    border-radius: 3.3125rem;
    transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    font-size: 0.9375rem;
    width: var(--width-cta);
    height: var(--height-cta);
    background: var(--color-accent);
    line-height: 1;
    box-shadow: inset 0 0 1.5125rem 0.1875rem rgba(255, 255, 255, 0.25);
    text-shadow: 0.125rem 0.4375rem 0.7rem rgba(210, 77, 134, 0.28);
    padding-bottom: 0.125rem;
    text-decoration: none;
  }
  .btn-cta:hover {
    transform: translateY(-0.25rem);
    box-shadow: inset 0 0 1.5125rem 0.1875rem rgba(255, 255, 255, 0.4), 0 0.625rem 1.25rem rgba(249, 169, 169, 0.3);
  }
  .btn-cta:active {
    transform: scale(0.9);
    opacity: 0.85;
  }
  .hero-start {
    font-weight: 400;
    text-decoration-line: none;
    width: 16.5625rem;
    height: 6.5rem;
    font-size: 4rem;
    background: linear-gradient(180deg, #e5baba 0%, #e08383 100%);
    padding-bottom: 0.375rem;
  }
  .quiz-container {
    @apply w-full lg:w-[25rem] shrink-0 bg-gradient-to-b from-[#e5baba99] to-[#e08383db] shadow-[8px_55px_160px_-27px_rgba(223,123,232,0.71)] rounded-[2rem] p-[1.5rem] md:p-[2rem] flex flex-col gap-[2rem];
  }
  .quiz-question-box {
    @apply bg-[#2D3149]/38 rounded-[3rem] p-[1.5rem] md:p-[2rem] relative min-h-[9.3125rem] flex items-center;
  }
  .quiz-btn {
    @apply w-full bg-white transition-all h-[4.5rem] md:h-[5.75rem] rounded-[4.8rem] font-roboto text-[1rem] md:text-[1.25rem] text-[#3F3F3F] px-4 shadow-sm cursor-pointer hover:shadow-[inset_0_0_1.5125rem_0.1875rem_rgba(249,169,169,0.2),0_10px_20px_rgba(249,169,169,0.2)] hover:-translate-y-1 active:scale-95;
  }
  .text-h2 {
    @apply font-geologica font-bold text-[2.5rem] md:text-[3rem] leading-[1.2] text-black;
  }
  .text-body {
    @apply font-roboto font-normal text-[1rem] md:text-[1.25rem] leading-[1.4] text-black tracking-[0.03em];
  }
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(3rem); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-up {
  animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@media (prefers-reduced-motion: reduce) {
  .animate-fade-up { animation: none; opacity: 1; transform: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
.hero-wrapper {
  position: relative;
  z-index: 1;
}
.hero-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 87.5rem;
  height: 56.25rem;
  background-image: url('@/assets/svg/background-hero-block.svg');
  background-repeat: no-repeat;
  background-position: center top;
  background-size: cover;
  pointer-events: none;
  z-index: -1;
}
@media (min-width: 100rem) {
  .hero-wrapper::before { max-width: 112.5rem; }
}
EOF

cat << 'EOF' > frontend/src/api/index.ts
export const API_BASE_URL = 'http://localhost:8000/api/v1';

export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};
EOF

cat << 'EOF' > frontend/src/composables/useIntersectionAnimation.ts
import { ref, onMounted, onUnmounted, type Ref } from 'vue'

export function useIntersectionAnimation(targetRef: Ref<HTMLElement | null>, threshold: number = 0.1) {
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
      { threshold }
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
EOF

cat << 'EOF' > frontend/src/data/quiz.ts
export const quizData = [
  {
    title: 'Есть ли у тебя опыт с этой профессией?',
    answers: [
      { id: 1, text: 'Да, просто хочу подтянуть знания', experienceScore: 10 },
      { id: 2, text: 'Да, но совсем немного', experienceScore: 5 },
      { id: 3, text: 'Нет, буду учиться с нуля', experienceScore: 0 },
    ],
  },
  {
    title: 'Какую сферу обучения ты рассматриваешь?',
    answers: [
      { id: 4, text: 'Программирование и код', experienceScore: 0 },
      { id: 5, text: 'UX/UI и веб-дизайн', experienceScore: 0 },
      { id: 6, text: '3D-графика и моделирование', experienceScore: 0 },
    ],
  },
  {
    title: 'Как ты оцениваешь свою техническую грамотность?',
    answers: [
      { id: 7, text: 'Уверенно пишу код / работаю в редакторах', experienceScore: 10 },
      { id: 8, text: 'Разбираюсь в ПК на уровне продвинутого пользователя', experienceScore: 5 },
      { id: 9, text: 'Только начинаю осваивать', experienceScore: 0 },
    ],
  },
  {
    title: 'Какой темп обучения тебе подходит?',
    answers: [
      { id: 10, text: 'Интенсивный (3-4 часа в день)', experienceScore: 0 },
      { id: 11, text: 'Стандартный (1-2 часа в день)', experienceScore: 0 },
      { id: 12, text: 'Размеренный (выходные дни)', experienceScore: 0 },
    ],
  },
  {
    title: 'Какова твоя главная цель обучения?',
    answers: [
      { id: 13, text: 'Быстро найти первую работу', experienceScore: 5 },
      { id: 14, text: 'Сменить профессию / сферу', experienceScore: 5 },
      { id: 15, text: 'Реализовать свой пет-проект', experienceScore: 10 },
    ],
  },
]
EOF

cat << 'EOF' > frontend/src/composables/useQuiz.ts
import { ref, computed } from 'vue'
import { quizData } from '../data/quiz'

export function useQuiz() {
  const currentQuestionIndex = ref(0)
  const experienceScore = ref(0)
  const isFinished = ref(false)
  const totalQuestions = quizData.length

  const currentQuestion = computed(() => {
    return quizData[currentQuestionIndex.value] || null
  })

  const resultText = computed(() => {
    if (experienceScore.value >= 25) {
      return 'Вам подходит продвинутый трек. Мы подготовим сложную, ускоренную программу, фокусируясь на создании глубокого пет-проекта для вашего портфолио.'
    } else if (experienceScore.value >= 10) {
      return 'Вам подходит базовый трек. Программа начнется с углубленного повторения основ и быстро перейдет к практическим задачам и командной работе.'
    } else {
      return "Вам подходит трек 'С нуля'. Мы выстроим последовательную, пошаговую программу от самых азов, с упором на наставничество и помощь на каждом этапе."
    }
  })

  function handleAnswer(scoreToAdd: number) {
    experienceScore.value += scoreToAdd
    if (currentQuestionIndex.value < totalQuestions - 1) {
      currentQuestionIndex.value++
    } else {
      isFinished.value = true
    }
  }

  function resetQuiz() {
    currentQuestionIndex.value = 0
    experienceScore.value = 0
    isFinished.value = false
  }

  return {
    currentQuestionIndex,
    experienceScore,
    isFinished,
    totalQuestions,
    currentQuestion,
    resultText,
    handleAnswer,
    resetQuiz
  }
}
EOF

cat << 'EOF' > frontend/src/components/quiz/QuizQuestionCard.vue
<template>
  <div class="flex flex-col gap-[2rem]">
    <div class="quiz-question-box">
      <h3 class="font-geologica text-white text-[1.25rem] md:text-[1.5rem] leading-[1.4] md:leading-[1.875rem] pr-[1.5rem] md:pr-[2rem]">
        {{ question.title }}
      </h3>
      <span class="absolute bottom-[1.5rem] right-[2rem] text-white font-black text-[1rem]">
        {{ currentIndex + 1 }}/{{ total }}
      </span>
    </div>
    <div class="flex flex-col gap-[1rem]">
      <button
        v-for="answer in question.answers"
        :key="answer.id"
        @click="$emit('answer', answer.experienceScore)"
        class="quiz-btn"
      >
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  question: { title: string, answers: { id: number, text: string, experienceScore: number }[] }
  currentIndex: number
  total: number
}>()

defineEmits<{
  (e: 'answer', score: number): void
}>()
</script>
EOF

cat << 'EOF' > frontend/src/components/quiz/QuizResultCard.vue
<template>
  <div class="flex flex-col gap-[2rem] p-2">
    <div class="bg-[#2D3149]/38 rounded-[3rem] p-[2rem] min-h-[9.3125rem] flex flex-col items-center justify-center gap-2 text-center">
      <h3 class="font-geologica text-white text-[1.5rem] md:text-[1.75rem] font-bold">Ваш план готов!</h3>
      <p class="font-geologica text-white text-[1rem]">Основан на вашем опыте</p>
    </div>
    <div class="bg-white/70 backdrop-blur-sm rounded-[2rem] p-6 text-left shadow-inner">
      <p class="font-roboto text-[1.125rem] leading-[1.6] text-black">
        {{ resultText }}
      </p>
    </div>
    <div class="flex flex-col gap-[1rem] mt-2">
      <button class="btn-cta w-full">Получить полную программу</button>
      <button
        @click="$emit('reset')"
        class="w-full h-[3.5rem] flex items-center justify-center font-geologica font-bold text-[0.9375rem] text-white/80 hover:text-white transition-colors cursor-pointer"
      >
        Пройти заново
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ resultText: string }>()
defineEmits<{ (e: 'reset'): void }>()
</script>
EOF

cat << 'EOF' > frontend/src/components/quiz/QuizSection.vue
<template>
  <section id="test" class="relative z-10 pt-[5rem] md:pt-[10rem] pb-[5rem] md:pb-[10rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto overflow-hidden">
    <div
      ref="sectionRef"
      class="flex flex-col-reverse lg:flex-row items-center justify-between gap-[3rem] lg:gap-[5rem] transition-all duration-1000 transform"
      :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-[3rem]'"
    >
      <div class="quiz-container">
        <transition name="fade-quiz" mode="out-in">
          <QuizQuestionCard
            v-if="!isFinished && currentQuestion"
            :key="currentQuestionIndex"
            :question="currentQuestion"
            :current-index="currentQuestionIndex"
            :total="totalQuestions"
            @answer="handleAnswer"
          />
          <QuizResultCard
            v-else-if="isFinished"
            :key="'result'"
            :result-text="resultText"
            @reset="resetQuiz"
          />
        </transition>
      </div>

      <div class="w-full lg:w-1/2 flex flex-col gap-[1.5rem] text-left lg:text-right">
        <h2 class="text-h2">Ответь на несколько вопросов</h2>
        <p class="text-body lg:ml-auto max-w-[34.375rem]">
          Это необходимо для проверки твоих знаний и подбора
          <span class="text-accent-dark">индивидуального</span> плана обучения
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionAnimation } from '../../composables/useIntersectionAnimation'
import { useQuiz } from '../../composables/useQuiz'
import QuizQuestionCard from './QuizQuestionCard.vue'
import QuizResultCard from './QuizResultCard.vue'

const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionAnimation(sectionRef)

const {
  currentQuestionIndex,
  isFinished,
  totalQuestions,
  currentQuestion,
  resultText,
  handleAnswer,
  resetQuiz
} = useQuiz()
</script>

<style scoped>
.fade-quiz-enter-active,
.fade-quiz-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.fade-quiz-enter-from {
  opacity: 0;
  transform: translateX(1.25rem);
}
.fade-quiz-leave-to {
  opacity: 0;
  transform: translateX(-1.25rem);
}
</style>
EOF

echo "Рефакторинг успешно завершен!"
